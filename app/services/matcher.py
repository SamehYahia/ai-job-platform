from app.schemas.match import MatchRequest, MatchResponse


def calculate_match(request: MatchRequest) -> MatchResponse:
    required_skills = set(request.job.required_skills)
    candidate_skills = set(request.candidate.skills)

    matched_skills = sorted(required_skills & candidate_skills)
    missing_skills = sorted(required_skills - candidate_skills)

    score = round((len(matched_skills) / len(required_skills)) * 100, 2)

    return MatchResponse(
        score_percent=score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        explanation=(f"Matched {len(matched_skills)} of {len(required_skills)} required skills."),
    )
