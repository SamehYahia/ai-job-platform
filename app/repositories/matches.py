from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Candidate, Job, MatchResult
from app.schemas.match import MatchRequest, MatchResponse


def save_match_evaluation(
    db: Session,
    request: MatchRequest,
    result: MatchResponse,
) -> MatchResult:
    """Persist a match evaluation and return its database record."""
    candidate = db.scalar(
        select(Candidate).where(Candidate.profile_id == request.candidate.profile_id)
    )

    # Reuse the candidate to prevent duplicate profile IDs.
    if candidate is None:
        candidate = Candidate(
            profile_id=request.candidate.profile_id,
            skills=request.candidate.skills,
        )
        db.add(candidate)
    else:
        candidate.skills = request.candidate.skills

    job = Job(
        title=request.job.title,
        required_skills=request.job.required_skills,
    )
    db.add(job)
    db.flush()

    match_result = MatchResult(
        job_id=job.id,
        candidate_id=candidate.id,
        score_percent=result.score_percent,
        matched_skills=result.matched_skills,
        missing_skills=result.missing_skills,
        explanation=result.explanation,
    )
    db.add(match_result)
    db.commit()
    db.refresh(match_result)

    return match_result
