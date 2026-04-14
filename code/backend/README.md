# Backend Setup

## Prerequisites

- Python 3.12
- Git
- Docker (for Qdrant)

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
```

All variables have sensible defaults, so `.env` is optional for local development.

## Start Qdrant (Docker)

```bash
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

Qdrant dashboard will be available at http://localhost:6333/dashboard.

## Create the Qdrant collection

With the virtual environment activated and Qdrant running:

```bash
python scripts/create_qdrant_collection.py
```

This creates the collection configured in your `.env` (or uses defaults).
