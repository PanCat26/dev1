# Model Training and Serving

This folder contains the model fine-tuning and export pipeline:

- `config.py` - model, dataset, and training configuration
- `data.py` - streaming dataset loader for OpenCodeInstruct
- `train_sft.py` - QLoRA supervised fine-tuning script
- `merge_adapter.py` - script to merge the LoRA adapter into the base model
- `requirements.txt` - Python dependencies

If you want to skip the adapter training, merging, and quantization phases, only follow the steps in sections [1](#1-create-the-python-environment), [6.1](#61-get-llamacpp), [6.2](#62-build-llamacpp), and [8](#8-run-the-quantized-model-locally-with-llamacpp).

## 1. Create the Python environment

### Windows (PowerShell)

```powershell
cd code\model
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Linux / macOS

```bash
cd code/model
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Environment variables

This project loads environment variables from a `.env` file through `python-dotenv`.

Create a `.env` file in `code/model`:

```env
ADAPTER_REPO=<local-or-remote-adapter>
```

Notes:
- `ADAPTER_REPO` is only used in `merge_adapter.py`.
- `ADAPTER_REPO` can point to a local adapter (obtained after section [3](#3-training)) or a remote one (obtained after section [4](#4-upload-the-adapter-to-hugging-face-optional)).
- If you want to skip training, a pretrained adapter is available here:
  - `https://huggingface.co/catalin-pangaleanu/qwen25coder-7b-lora-adapter`

## 3. Training

The training script fine-tunes `Qwen/Qwen2.5-Coder-7B-Instruct` with QLoRA on `nvidia/OpenCodeInstruct`.

Run:

### Windows

```powershell
cd code\model
.\.venv\Scripts\Activate.ps1
python train_sft.py
```

### Linux / macOS

```bash
cd code/model
source .venv/bin/activate
python train_sft.py
```

The adapter is saved locally to:

```text
outputs/sft/final_adapter
```

## 4. Upload the adapter to Hugging Face (optional)

Authenticate first:

```bash
hf auth login
```

Create the repo if needed:

```bash
hf repo create <namespace>/<repository> --type model
```

Upload the saved adapter folder:

```bash
hf upload <namespace>/<repository> ./outputs/sft/final_adapter
```

## 5. Merge the base model with the adapter

`merge_adapter.py` loads the adapter from `ADAPTER_REPO`. This can point to the local `./outputs/sft/final_adapter` or a remote repo such as `https://huggingface.co/catalin-pangaleanu/qwen25coder-7b-lora-adapter`

The merged model is placed in:

```text
outputs/merged
```

Run:

### Windows

```powershell
cd code\model
.\.venv\Scripts\Activate.ps1
python merge_adapter.py
```

### Linux / macOS

```bash
cd code/model
source .venv/bin/activate
python merge_adapter.py
```

Important: make sure you have enough free disk space before running this step, as the merged model is much larger than the adapter.

## DPO preference fine-tuning (optional)

You can further fine-tune the SFT-merged model with Direct Preference Optimization (DPO) using pairwise feedback collected from the backend's `rlhf_feedback` table. This produces a separate `dpo_adapter` that sits on top of the SFT-merged base.

Prerequisites:

- The SFT-merged model must already exist at `outputs/merged` (see section [5](#5-merge-the-base-model-with-the-adapter)).
- The backend Postgres database must be running with collected feedback rows in `rlhf_feedback`.

### A. Export preference data from Postgres

This step runs from the backend folder (not `code/model`), since it depends on the backend's database session.

#### Windows

```powershell
cd code\backend
.\.venv\Scripts\Activate.ps1
python scripts/export_preferences.py
```

#### Linux / macOS

```bash
cd code/backend
source .venv/bin/activate
python scripts/export_preferences.py
```

By default this writes `code/backend/storage/preferences/dpo_<UTC-timestamp>.jsonl`. Override with `--out <path>` or cap with `--limit N`.

The exporter skips rows with NULL or identical responses, and rows where either response is shorter than 10 characters.

### B. Set DPO environment variables

Add to `code/model/.env`:

```env
DPO_DATASET_PATH=<absolute-or-relative-path-to-the-exported-jsonl>
```

Optional overrides:

- `SFT_MERGED_MODEL_PATH` - defaults to `outputs/merged` (the section [5](#5-merge-the-base-model-with-the-adapter) output). Override only if the merged base lives elsewhere.
- `DPO_ADAPTER_REPO` - used by `merge_dpo_adapter.py` in step D.

### C. Train

#### Windows

```powershell
cd code\model
.\.venv\Scripts\Activate.ps1
python train_dpo.py
```

#### Linux / macOS

```bash
cd code/model
source .venv/bin/activate
python train_dpo.py
```

The DPO adapter is saved locally to:

```text
outputs/dpo/final_adapter
```

### D. Merge the DPO adapter (optional, for serving)

To produce a single deployable model that bakes in both SFT and DPO, merge the DPO adapter into the SFT-merged base. Set `DPO_ADAPTER_REPO` in `code/model/.env` (local path or Hugging Face repo id), then:

#### Windows

```powershell
python merge_dpo_adapter.py
```

#### Linux / macOS

```bash
python merge_dpo_adapter.py
```

The fully-merged model is placed in:

```text
outputs/merged_dpo
```

From here you can resume the standard pipeline at section [6.3](#63-convert-the-merged-model-to-gguf), pointing the GGUF converter at `outputs/merged_dpo` instead of `outputs/merged`.

## 6. Convert to GGUF and quantize

### 6.1 Get `llama.cpp`

In a folder on your machine:

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
```

### 6.2 Build `llama.cpp`

#### Linux / macOS

Generic:
```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
```

CUDA:
```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=ON
cmake --build build -j
```

Vulkan (after downloading Vulkan SDK):
```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_VULKAN=ON
cmake --build build -j
```

Note: on macOS, Metal is enabled by default in the generic build.

#### Windows

Generic:
```bash
cmake -B build
cmake --build build --config Release
```

CUDA:
```bash
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release
```

Vulkan (after downloading Vulkan SDK):
```bash
cmake -B build -DGGML_VULKAN=ON
cmake --build build --config Release
```

### 6.3 Convert the merged model to GGUF

From inside `llama.cpp`:

#### Linux / macOS

```bash
python convert_hf_to_gguf.py <merged-model-path> --outfile <your-chosen-path>/model-f16.gguf --outtype f16
```

#### Windows

```powershell
python convert_hf_to_gguf.py <merged-model-path> --outfile <your-chosen-path>\model-f16.gguf --outtype f16
```

### 6.4 Quantize the GGUF model

Use `Q4_K_M` as a practical default. From inside `llama.cpp`:

#### Linux / macOS

```bash
./build/bin/llama-quantize <your-chosen-path>/model-f16.gguf <your-chosen-path>/model-q4_k_m.gguf Q4_K_M
```

#### Windows

```powershell
.\build\bin\Release\llama-quantize.exe <your-chosen-path>\model-f16.gguf <your-chosen-path>\model-q4_k_m.gguf Q4_K_M
```

## 7. Upload the GGUF file to Hugging Face (optional)

Authenticate first:

```bash
hf auth login
```

Create a repo if needed:

```bash
hf repo create <namespace>/<repository> --type model
```

Upload the GGUF file:

```bash
hf upload <namespace>/<repository> <your-chosen-path>/model-q4_k_m.gguf
```

## 8. Run the quantized model locally with `llama.cpp`

You can either:
- run it in the terminal with `llama-cli`
- run a local server with `llama-server`

If you skipped over the previous steps, you can download a ready-to-use quantized model from: `https://huggingface.co/catalin-pangaleanu/qwen25coder-7b-quantized-gguf`:

```bash
hf download catalin-pangaleanu/qwen25coder-7b-quantized-gguf --local-dir <your-chosen-path>
```

### 8.1 See available devices

If you want GPU offload:

#### Linux / macOS

```bash
./build/bin/llama-cli --list-devices
```

#### Windows

```powershell
.\build\bin\Release\llama-cli.exe --list-devices
```

This shows devices such as `CUDA0`, `Vulkan0`, `Vulkan1`, etc.

### 8.2 Run in CLI mode

From `llama.cpp` folder:

#### Linux / macOS

```bash
./build/bin/llama-cli -m <path-to-gguf-file> -c 4096 -cnv
```

#### Windows

```powershell
.\build\bin\Release\llama-cli.exe -m <path-to-gguf-file> -c 4096 -cnv
```

### 8.3 Offload to GPU

To offload layers to a specific device, add:

- `--device Vulkan0`, `--device Vulkan1` etc. to select
- `-ngl all` to try to offload all layers

Example:

#### Linux / macOS

```bash
./build/bin/llama-cli -m <path-to-gguf-file> --device Vulkan0 -ngl all -c 4096 -cnv
```

#### Windows

```powershell
.\build\bin\Release\llama-cli.exe -m <path-to-gguf-file> --device Vulkan0 -ngl all -c 4096 -cnv
```

If this uses too much VRAM, lower `-ngl`, for example `-ngl 30`.

### 8.4 Run as a local server

#### Linux / macOS

```bash
./build/bin/llama-server -m <path-to-gguf-file> --port 8080 -c 4096
```

#### Windows

```powershell
.\build\bin\Release\llama-server.exe -m <path-to-gguf-file> --port 8080 -c 4096
```

With GPU offload:

#### Linux / macOS

```bash
./build/bin/llama-server -m <path-to-gguf-file> --device Vulkan0 -ngl all --port 8080 -c 4096
```

#### Windows

```powershell
.\build\bin\Release\llama-server.exe -m <path-to-gguf-file> --device Vulkan1 -ngl all --port 8080 -c 4096
```

Then open:

```text
http://localhost:8080
```
