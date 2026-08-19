from fastapi import FastAPI

app = FastAPI(
    title="AI Job Platform",
    version="0.1.0",
    description="A minimal workload for the P01 DevOps portfolio project.",
)


@app.get("/health/live", tags=["Health"])
async def liveness() -> dict[str, str]:
    """Confirm that the API process is running."""
    return {"status": "ok"}
