from fastapi import APIRouter

from app.schemas.match import MatchRequest, MatchResponse
from app.services.matcher import calculate_match

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.post("/evaluate", response_model=MatchResponse)
async def evaluate_match(request: MatchRequest) -> MatchResponse:
    return calculate_match(request)
