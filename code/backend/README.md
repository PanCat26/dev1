# Backend Setup

## Prerequisites

- Python 3.12
- Git
- Docker (for Qdrant and PostgreSQL)

## Open the backend folder

### Windows PowerShell

```powershell
cd code\backend
```

### macOS / Linux

```bash
cd code/backend
```

## Create a virtual environment

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
```

### macOS / Linux

```bash
python3.12 -m venv .venv
```

## Activate the virtual environment

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Environment can be deactivated with:

```bash
deactivate
```

## Install dependencies from `requirements.txt`

With environment activated:

```bash
python -m pip install -r requirements.txt
```

## Environment variables

Create a `.env` file in `code/backend/` with the following:

```dotenv
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=repo_snapshots
QDRANT_VECTOR_SIZE=384
QDRANT_DISTANCE_METRIC=Cosine
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
DATABASE_URL=postgresql://dev1:dev1@127.0.0.1:5433/dev1db
GITHUB_TOKEN=<your-github-api-token>
LLAMA_SERVER_URL=http://localhost:8080
```
Most variables have defaults, so `.env` is generally optional for local development. However, `GITHUB_TOKEN` does not have a default value; if it is not provided, you might encounter GitHub API rate limits during repository ingestion.

Override the default for `LLAMA_SERVER_URL` it if your llama-server runs on a different port.

## Start Services (PostgreSQL & Qdrant)

Start PostgreSQL:
```bash
docker run -d --name postgres_db -p 5433:5432 -e POSTGRES_USER=dev1 -e POSTGRES_PASSWORD=dev1 -e POSTGRES_DB=dev1db postgres:15
```

Start Qdrant:
```bash
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant:v1.13.2
```

Qdrant dashboard will be available at http://localhost:6333/dashboard.

## Run Database Migrations (Alembic)

With the virtual environment activated and PostgreSQL running, apply database migrations:
```bash
alembic upgrade head
```

## Generate a New Database Migration (Alembic)

After making any changes to the SQLAlchemy models located in `repository_management/models/`, generate a new migration script using the autogeneration feature:
```bash
alembic revision --autogenerate -m "Your descriptive message here"
```
Then run the `alembic upgrade head` command shown above to apply it.

## Create the Qdrant collection

With the virtual environment activated and Qdrant running:

```bash
python scripts/create_qdrant_collection.py
```

This creates the collection configured in your `.env` (or uses defaults).

## Run the indexing pipeline

Make sure Qdrant is running and the collection is created (see above), then:

```bash
python scripts/run_indexing_demo.py <snapshot_path> [repo_id] [commit_sha]
```

Example indexing the backend itself:

```bash
python scripts/run_indexing_demo.py . my-repo abc1234
```

The script prints a result summary with file count, chunk count, and any errors.
You can verify the data in the Qdrant dashboard at http://localhost:6333/dashboard.

## Run the Repository Manager demo

This script demonstrates the full ingestion pipeline: it creates a new database entry, snapshots the target directory to local storage, and then automatically kicks off the asynchronous indexing pipeline.

```bash
python scripts/run_repository_demo.py <github_url>
```
or
```bash
python scripts/run_repository_demo.py add <github_url>
```

Example analyzing the backend directory:

```bash
python scripts/run_repository_demo.py add https://github.com/antoniunegrea/Task-Management
```

This will:
1. Copy the current folder to `storage/snapshots/<repo_name>_<uuid>`
2. Skip redundant files and directories (`.git`, `__pycache__`, etc.)
3. Add a row to the Postgres `repositories` table.
4. Run background chunking and index it to Qdrant.
5. Watch the Postgres database until the `status` flips to `ready`.

### Delete a repository

Removes the repository's DB row, its indexed chunks from Qdrant (filtered by `repo_id`), and its snapshot directory on disk.

```bash
python scripts/run_repository_demo.py delete <repo_id>
```

The `<repo_id>` is the UUID printed by the `add` command above, and can also be found in the `repositories` table or in any Qdrant chunk's payload.

## Run the API server

With Postgres and Qdrant running and migrations applied:

```bash
uvicorn api.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the Swagger UI listing every endpoint interactively.

## Start the language model server

The backend communicates with a locally running llama-server instance (from llama.cpp) that serves the fine-tuned model. See `code/model/README.md` for full instructions on building llama.cpp and running the model.

Once you have a GGUF model file ready, start the server:

### Linux / macOS

```bash
./build/bin/llama-server -m <path-to-gguf-file> --port 8080 -c <total-context>
```

### Windows

```powershell
.\build\bin\Release\llama-server.exe -m <path-to-gguf-file> --port 8080 -c <total-context>
```

The server exposes an OpenAI-compatible API at `http://localhost:8080`. The backend connects to it automatically using the `LLAMA_SERVER_URL` environment variable.

## Run the language model demo

Make sure llama-server is running, then:

```bash
python scripts/run_language_model_demo.py <prompt>
```

If no prompt is provided, a default one is used. The script streams the model's response token by token to the terminal.
