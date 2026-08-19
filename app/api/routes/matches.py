from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.matches import save_match_evaluation
from app.schemas.match import MatchRequest, MatchResponse
from app.services.matcher import calculate_match

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.post("/evaluate", response_model=MatchResponse)
async def evaluate_match(
    payload: MatchRequest,
    db: Session = Depends(get_db),
) -> MatchResponse:
    """Evaluate a candidate and persist the result for auditing."""
    result = calculate_match(payload)
    save_match_evaluation(db, payload, result)
    return result
