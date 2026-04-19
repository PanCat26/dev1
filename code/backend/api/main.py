from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.routers import conversations, repositories

app = FastAPI(title="dev1's backend")

app.include_router(repositories.router)
app.include_router(conversations.router)


@app.exception_handler(ValueError)
async def value_error_handler(_request: Request, exc: ValueError):
    # Manager functions use ValueError for invalid input and missing entities.
    # Map those to HTTP 400 here to keep endpoint code clean.
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/health")
def health():
    return {"status": "ok"}
