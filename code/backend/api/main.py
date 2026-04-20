from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.routers import conversations, repositories

app = FastAPI(title="dev1's backend")

app.include_router(repositories.router)
app.include_router(conversations.router)


@app.exception_handler(ValueError)
async def value_error_handler(_request: Request, exc: ValueError):
    detail = str(exc)

    # Manager functions use ValueError for both invalid input and missing entities.
    # Preserve 400 for validation/input errors, but return 404 for missing resources.
    status_code = 404 if "not found" in detail.lower() else 400
    return JSONResponse(status_code=status_code, content={"detail": detail})


@app.get("/health")
def health():
    return {"status": "ok"}
