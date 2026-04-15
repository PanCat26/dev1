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
```

All variables have defaults, so `.env` is optional for local development.

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

After making any changes to the SQLAlchemy models located in `database/models/`, generate a new migration script using the autogeneration feature:
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
python scripts/run_repository_demo.py <source_path> <repo_name> [commit_sha]
```

Example analyzing the backend directory:

```bash
python scripts/run_repository_demo.py . my-repo abc1234
```

This will:
1. Copy the current folder to `storage/snapshots/<repo_name>_<uuid>`
2. Skip redundant files and directories (`.git`, `__pycache__`, etc.)
3. Add a row to the Postgres `repositories` table.
4. Run background chunking and index it to Qdrant.
5. Watch the Postgres database until the `status` flips to `ready`.
