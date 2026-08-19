# P01 - AI Job Platform

> **Status:** Phase 1 completed - Containerization is next  
> **Current state:** Backend MVP implemented and tested  
> **Project type:** DevOps-first portfolio project  
> **Production readiness:** Not production-ready

## Overview

AI Job Platform is a DevOps portfolio project built around a small but realistic
job-matching API.

The application provides a workload for practicing containerization, CI/CD,
DevSecOps, infrastructure automation, Kubernetes operations, observability,
reliability, and disaster recovery.

Application functionality remains intentionally focused so the project can
demonstrate how a service is built, tested, secured, deployed, and operated.

## Implemented Workload

The current backend can:

- Accept synthetic job and candidate profiles through a REST API.
- Normalize skill names to produce consistent comparisons.
- Calculate deterministic and explainable match results.
- Store jobs, candidates, and match results through SQLAlchemy.
- Manage database schema changes with Alembic.
- Reuse candidate profiles without creating duplicate profile IDs.
- Expose liveness and database readiness endpoints.
- Validate behavior using unit and integration tests.

Only synthetic data is used. Real resumes, personal information, and automatic
job applications are outside the current scope.

## Current Architecture

```mermaid
flowchart TB
    CLIENT["API Client"] --> API["FastAPI"]
    API --> MATCHER["Matching Service"]
    API --> REPOSITORY["Repository Layer"]
    REPOSITORY --> ORM["SQLAlchemy ORM"]
    ORM --> DATABASE[("PostgreSQL")]
    ALEMBIC["Alembic"] --> DATABASE
```

SQLite is used for isolated automated tests. PostgreSQL is the target runtime
database and will be validated through Docker Compose in Phase 2.

## Technology Stack

| Area | Technology | Status |
| --- | --- | --- |
| API | FastAPI | Implemented |
| Validation | Pydantic | Implemented |
| Matching | Deterministic Python service | Implemented |
| Persistence | SQLAlchemy 2 | Implemented |
| Migrations | Alembic | Implemented |
| Runtime database | PostgreSQL with Psycopg | Integration next |
| Test database | In-memory SQLite | Implemented |
| Testing | Pytest and FastAPI TestClient | Implemented |
| Code quality | Ruff | Implemented |
| Containers | Docker and Docker Compose | Next |
| CI/CD | GitHub Actions | Planned |
| Security | Gitleaks and Trivy | Planned |
| Infrastructure | Terraform and AWS | Planned |
| Kubernetes | Local Kubernetes and Amazon EKS | Planned |
| Packaging | Helm | Planned |
| GitOps | Argo CD | Planned |
| Observability | Prometheus and Grafana | Planned |

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health/live` | Confirms that the API process is running |
| `GET` | `/health/ready` | Confirms that the database accepts queries |
| `POST` | `/api/v1/matches/evaluate` | Evaluates and persists a match |
| `GET` | `/docs` | Opens the interactive OpenAPI documentation |

## Match Request Example

```bash
curl -X POST http://127.0.0.1:8000/api/v1/matches/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "job": {
      "title": "Junior DevOps Engineer",
      "required_skills": ["AWS", "Docker", "Kubernetes"]
    },
    "candidate": {
      "profile_id": "candidate-001",
      "skills": ["AWS", "Docker"]
    }
  }'
```

The response includes:

- `score_percent`
- `matched_skills`
- `missing_skills`
- `explanation`

Skills are normalized before comparison and persistence, so values such as
`AWS`, `aws`, and ` AWS ` are treated consistently.

## Local Development

### 1. Create the environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

### 2. Configure a local database

Use persistent SQLite before Docker Compose is added:

```bash
export DATABASE_URL="sqlite+pysqlite:///./ai_job_platform.db"
```

The PostgreSQL URL format used by the containerized environment will be:

```text
postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE
```

### 3. Apply migrations

```bash
python -m alembic upgrade head
```

### 4. Start the API

```bash
python -m uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`, with interactive documentation
at `http://127.0.0.1:8000/docs`.

## Quality Checks

```bash
# Check installed dependency compatibility.
python -m pip check

# Run linting and formatting validation.
python -m ruff check app tests alembic
python -m ruff format --check app tests alembic

# Run the complete test suite.
python -m pytest -W error::DeprecationWarning
```

The current test suite contains six tests covering health endpoints,
deterministic matching, skill normalization, database models, and persistence.

## Repository Structure

```text
.
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── api/routes/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── docs/
│   ├── adr/
│   └── charter.md
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_matches.py
│   └── test_persistence.py
├── alembic.ini
├── pyproject.toml
├── requirements-dev.txt
├── requirements.txt
├── SECURITY.md
└── README.md
```

## Delivery Roadmap

- [x] Phase 0 - Project foundation and governance
- [x] Phase 1 - FastAPI application baseline
- [x] Phase 1 - Deterministic job matching
- [x] Phase 1 - Persistence models and migrations
- [x] Phase 1 - Liveness, readiness, and integration tests
- [ ] Phase 2 - Docker and local PostgreSQL operations
- [ ] Phase 3 - GitHub Actions and security controls
- [ ] Phase 4 - Terraform and AWS foundation
- [ ] Phase 5 - Local Kubernetes baseline
- [ ] Phase 6 - Helm packaging and local GitOps
- [ ] Phase 7 - Temporary Amazon EKS environment
- [ ] Phase 8 - Observability and SRE controls
- [ ] Phase 9 - Reliability and disaster recovery
- [ ] Phase 10 - Portfolio evidence and interview documentation

A phase is complete only after its acceptance criteria and validation evidence
have been reviewed.

## Planned Delivery Flow

```mermaid
flowchart TB
    DEV["Developer"] --> PR["Protected GitHub PR"]
    PR --> CI["Tests and security gates"]
    CI --> IMAGE["Immutable image"]
    IMAGE --> ECR["Amazon ECR"]
    CI --> GITOPS["GitOps update PR"]
    GITOPS --> ARGO["Argo CD"]
    ARGO --> EKS["Amazon EKS"]
```

GitHub Actions will authenticate to AWS through OpenID Connect instead of
long-lived AWS access keys.

## Security and Cost Boundaries

- Secrets must not be committed to Git, container images, logs, or Terraform.
- Real candidate data and automatic job applications are not currently used.
- AWS access will use short-lived identities and least-privileged IAM policies.
- Security findings will not be silently ignored.
- Cloud resources require a cost estimate and documented teardown procedure.
- Backups are not considered successful until restoration is tested.

## Documentation

Architecture decisions and project boundaries are recorded under `docs/`.
Operational runbooks, validation evidence, incident exercises, and recovery
procedures will be added as their related phases are implemented.

Documentation will not claim unfinished work as completed.

## License

This project is licensed under the [MIT License](LICENSE).