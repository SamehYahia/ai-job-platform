from fastapi import Depends, FastAPI, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.routes.matches import router as matches_router
from app.db.dependencies import get_db

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


@app.get("/health/ready", tags=["Health"])
def readiness(
    response: Response,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Confirm that the application can communicate with its database."""
    try:
        # A lightweight query verifies that the database accepts connections.
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not_ready"}

    return {"status": "ready"}
