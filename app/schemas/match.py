from pydantic import BaseModel, ConfigDict, Field, field_validator


def normalize_skills(skills: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()

    for skill in skills:
        value = " ".join(skill.lower().split())

        if not value:
            raise ValueError("Skills must not be empty")

        if value not in seen:
            normalized.append(value)
            seen.add(value)

    return normalized


class JobInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    required_skills: list[str] = Field(min_length=1, max_length=50)

    @field_validator("required_skills")
    @classmethod
    def normalize_required_skills(cls, skills: list[str]) -> list[str]:
        return normalize_skills(skills)


class CandidateInput(BaseModel):
    profile_id: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"^[A-Za-z0-9_-]+$",
    )
    skills: list[str] = Field(default_factory=list, max_length=100)

    @field_validator("skills")
    @classmethod
    def normalize_candidate_skills(cls, skills: list[str]) -> list[str]:
        return normalize_skills(skills)


class MatchRequest(BaseModel):
    job: JobInput
    candidate: CandidateInput


class MatchResponse(BaseModel):
    score_percent: float = Field(ge=0, le=100)
    matched_skills: list[str]
    missing_skills: list[str]
    explanation: str
