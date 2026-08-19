from fastapi import FastAPI

from app.api.routes.matches import router as matches_router

app = FastAPI(
    title="AI Job Platform",
    version="0.1.0",
    description="A minimal workload for the P01 DevOps portfolio project.",
)

app.include_router(matches_router, prefix="/api/v1")


@app.get("/health/live", tags=["Health"])
async def liveness() -> dict[str, str]:
    """Confirm that the API process is running."""
    return {"status": "ok"}
