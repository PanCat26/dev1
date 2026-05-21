# Backend evaluation metrics

Small harness under `evaluation/` plus `scripts/run_evaluation.py`. It scores **real** retrieval (Qdrant + embeddings + rerank) and optionally **answer quality** (orchestration + DeepEval judges).

## What gets measured

| Area | Metrics | Data |
|------|---------|------|
| **Retrieval** | Top-1 accuracy, Recall@3, Recall@5 | Questions auto-built from Python AST over each repo **`snapshot_path`** |
| **Answers** | DeepEval `AnswerRelevancyMetric`, `FaithfulnessMetric` | Manual **`questions`** in the repos JSON (+ streamed `answer_query`; faithfulness uses replayed retrieval context) |

Retrieval ranking uses `retrieve_ranked_chunks` (same pipeline as production retrieval before evidence-role truncation).

## Prerequisites

- Shell **cwd**: `code/backend` (same as other scripts).
- Virtualenv + deps: `pip install -r requirements.txt`.
- **Retrieval eval**: Qdrant up; vectors indexed for each entry’s **`repo_id`** (and **`commit_sha`** if chunks were stored with it); **`snapshot_path`** must exist on disk for AST question generation.
- **Answer eval**: `llama-server` (or compatible API) reachable via **`LLAMA_SERVER_URL`** / **`LLAMA_MODEL`** in `.env`.
- **DeepEval judges**:
  - Recommended: **`OPENROUTER_API_KEY`** with **`deepeval.models.OpenRouterModel`** (**`OPENROUTER_JUDGE_MODEL`**, default **`deepseek/deepseek-v4-flash:free`**; **`OPENROUTER_BASE_URL`**, default `https://openrouter.ai/api/v1`). **`OPENROUTER_JUDGE_REASONING`** defaults to **`1`** and passes **`extra_body: { reasoning: { enabled: true } }`** (OpenRouter + Python `OpenAI` client); use **`0`** to turn that off.
  - If **`OPENROUTER_API_KEY`** is unset, DeepEval uses its built-in **OpenAI-compatible** defaults (**`OPENAI_API_KEY`**, optional **`OPENAI_BASE_URL`**).
  - Use **`--skip-deepeval`** to omit judge HTTP calls while still streaming answers into the report.

Tip: set **`RLHF_PROBABILITY=0`** in `.env` for cleaner answer transcripts while benchmarking.

### Console noise and common failures

| What you see | Meaning / what to do |
|--------------|----------------------|
| **HF Hub unauthenticated** | Optional: set **`HF_TOKEN`** so embedding model downloads hit higher rate limits. |
| **Qdrant client vs server version** | Align **client** (`qdrant-client` in `requirements.txt`) with your **server** major/minor, or ignore if everything still works (see Qdrant docs for `check_compatibility=False`). |
| **`Structured outputs not supported … Falling back`** | Faithfulness/Relevancy first ask OpenRouter for **JSON-schema** completions; many models refuse or error, then DeepEval retries with plain text + parsing. Harmless noise unless the following call also fails. |
| **HTTP `429` on `:free` models** | Shared **free-route** quotas on OpenRouter/upstream (**“temporarily rate-limited upstream”**). Retry later; set **`OPENROUTER_JUDGE_MODEL`** to a **paid** slug your key can use (see [OpenRouter models](https://openrouter.ai/models)); or add **provider/BYOK** keys under OpenRouter **[Integrations](https://openrouter.ai/settings/integrations)** so limits accrue to you. **`OPENROUTER_JUDGE_REASONING=0`** slightly reduces judge payload but does not fix a saturated free pool. |

## Config file

Use a JSON **array** of objects. Required per entry: **`repo_id`**, **`snapshot_path`**. Strongly recommended: **`commit_sha`** if indexing filtered by commit.

Optional: **`name`**, **`questions`** (strings for manual / DeepEval path).

Paths under **`snapshot_path`** can be absolute or relative to `code/backend`.

Example template: `evaluation/eval_repos.example.json`. Copy to e.g. `evaluation/my_eval.json` so local paths don’t overwrite the template.

Optional **`--questions-file`**: another JSON array with the same shape; overrides **`questions`** per **`repo_id`** (every `repo_id` must still appear in `--repos-file`).

## Commands

Help:

```bash
python scripts/run_evaluation.py --help
```

**Retrieval only** (no LLM answers; fastest sanity check):

```bash
python scripts/run_evaluation.py --repos-file evaluation/my_eval.json --retrieval-only --output-dir reports/evaluation
```

**Full run** (retrieval + manual questions + DeepEval, if configured):

```bash
python scripts/run_evaluation.py --repos-file evaluation/my_eval.json --output-dir reports/evaluation
```

**Answers only** (skip AST retrieval metrics):

```bash
python scripts/run_evaluation.py --repos-file evaluation/my_eval.json --answers-only --output-dir reports/evaluation
```

**Skip DeepEval** (still runs `answer_query`; no judge API):

```bash
python scripts/run_evaluation.py --repos-file evaluation/my_eval.json --skip-deepeval --output-dir reports/evaluation
```

Useful flags:

| Flag | Default | Role |
|------|---------|------|
| `--max-questions-per-repo` | 120 | Cap AST-generated retrieval questions |
| `--num-candidates` | 48 | How many vectors to pull before rerank |
| `--output-dir` | `reports/evaluation` | Report folder |

## Reports

Each run writes timestamped **`evaluation_report_<UTC>.json`** and **`.md`**, plus **`evaluation_report_latest.json`** / **`.md`** in `--output-dir`.

Read **Markdown** for humans; **JSON** for tooling. Sections cover aggregate retrieval stats, per-question retrieval debug, manual QA rows, DeepEval scores when run, and warnings/errors.

## Offline checks (no Qdrant)

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Troubleshooting

| Symptom | Likely cause |
|---------|----------------|
| `FileNotFoundError` on repos JSON | Wrong **`--repos-file`** path; file missing under `evaluation/`. |
| All retrieval zeros | Wrong **`repo_id`** / **`commit_sha`**, snapshot empty, or index empty. |
| DeepEval errors | Missing judge credentials or blocked API; try **`--skip-deepeval`**. |
| Empty manual QA section | No **`questions`** in JSON or **`--retrieval-only`**. |

More backend-wide setup (Docker Postgres/Qdrant, llama-server): see `../README.md`.
