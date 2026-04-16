# setup.ps1

Write-Host "Creating virtual environment..." -ForegroundColor Cyan
py -3.12 -m venv .venv

Write-Host "Installing dependencies..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Setting up .env file..." -ForegroundColor Cyan
if (-Not (Test-Path ".env")) {
    $envContent = @"
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=repo_snapshots
QDRANT_VECTOR_SIZE=384
QDRANT_DISTANCE_METRIC=Cosine
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
DATABASE_URL=postgresql://dev1:dev1@127.0.0.1:5433/dev1db
GITHUB_TOKEN=
"@
    Set-Content -Path ".env" -Value $envContent
    Write-Host "Created default .env file." -ForegroundColor Green
} else {
    Write-Host ".env file already exists. Skipping." -ForegroundColor Yellow
}

Write-Host "Starting Docker containers..." -ForegroundColor Cyan

# Check and start postgres_db
$postgresExists = docker ps -a -q -f name=postgres_db
if ($postgresExists) {
    Write-Host "Starting existing postgres_db container..."
    docker start postgres_db
} else {
    Write-Host "Creating and starting new postgres_db container..."
    docker run -d --name postgres_db -p 5433:5432 -e POSTGRES_USER=dev1 -e POSTGRES_PASSWORD=dev1 -e POSTGRES_DB=dev1db postgres:15
}

# Check and start qdrant
$qdrantExists = docker ps -a -q -f name=qdrant
if ($qdrantExists) {
    Write-Host "Starting existing qdrant container..."
    docker start qdrant
} else {
    Write-Host "Creating and starting new qdrant container..."
    docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant:v1.13.2
}

Write-Host "Waiting 5 seconds for PostgreSQL to accept connections..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

Write-Host "Applying Database Migrations..." -ForegroundColor Cyan
.\.venv\Scripts\alembic.exe upgrade head

Write-Host "Setup finished successfully!" -ForegroundColor Green
