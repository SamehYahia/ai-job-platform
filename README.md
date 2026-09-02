# P01 - AI Job Platform

[![CI Quality Gates](https://github.com/SamehYahia/ai-job-platform/actions/workflows/quality.yml/badge.svg)](https://github.com/SamehYahia/ai-job-platform/actions/workflows/quality.yml)

> **Status:** Phase 3 completed - Terraform and AWS foundation is next  
> **Current state:** Containerized FastAPI backend with PostgreSQL, CI quality gates, and security scanning  
> **Project type:** DevOps-first portfolio project  
> **Production readiness:** Not production-ready

## Overview

AI Job Platform is a DevOps-focused portfolio project built around a small but
realistic job-matching API.

The application provides a workload for practicing and demonstrating:

- Application containerization
- CI/CD engineering
- DevSecOps controls
- Infrastructure as Code
- AWS infrastructure
- Kubernetes operations
- GitOps
- Observability
- Reliability engineering
- Disaster recovery

The application functionality remains intentionally focused so the project can
demonstrate how a service is built, tested, secured, deployed, and operated
through a production-oriented DevOps lifecycle.

## Current Capabilities

The backend currently supports:

- Synthetic job and candidate profiles.
- Deterministic and explainable job matching.
- Skill normalization before comparison and persistence.
- PostgreSQL persistence using SQLAlchemy.
- Database schema management with Alembic.
- Candidate profile reuse without duplicate profile IDs.
- Liveness and database readiness endpoints.
- Unit and PostgreSQL integration testing.
- Docker-based local runtime.
- Automated CI validation with GitHub Actions.
- Secret scanning with Gitleaks.
- Vulnerability and configuration scanning with Trivy.
- Protected `main` branch with required CI checks.

Only synthetic data is used.

Real resumes, personal information, and automated job applications are outside
the current project scope.

## Current Architecture

```mermaid
flowchart TB
    CLIENT["API Client"] --> API["FastAPI"]

    API --> MATCHER["Matching Service"]
    API --> REPOSITORY["Repository Layer"]

    REPOSITORY --> ORM["SQLAlchemy ORM"]
    ORM --> DATABASE[("PostgreSQL")]

    ALEMBIC["Alembic"] --> DATABASE

    COMPOSE["Docker Compose"] --> API
    COMPOSE --> DATABASE

    DEVELOPER["Developer"] --> PR["Pull Request"]
    PR --> CI["GitHub Actions"]

    CI --> QUALITY["Python Quality"]
    CI --> INTEGRATION["PostgreSQL Integration"]
    CI --> DOCKER["Docker Image Validation"]
    CI --> TRIVY["Trivy Security Scanning"]
    CI --> GITLEAKS["Gitleaks Secret Scanning"]
```

The application currently runs locally through Docker Compose.

PostgreSQL is the runtime database, while isolated automated tests may use
SQLite where an external database is not required.

AWS and Kubernetes infrastructure will be introduced in the next delivery
stages.

## Technology Stack

| Area | Technology | Status |
| --- | --- | --- |
| API | FastAPI | Implemented |
| Validation | Pydantic | Implemented |
| Matching | Deterministic Python service | Implemented |
| Persistence | SQLAlchemy 2 | Implemented |
| Migrations | Alembic | Implemented |
| Runtime database | PostgreSQL with Psycopg | Implemented |
| Testing | Pytest | Implemented |
| Code quality | Ruff | Implemented |
| Containers | Docker | Implemented |
| Local orchestration | Docker Compose | Implemented |
| CI | GitHub Actions | Implemented |
| Secret scanning | Gitleaks | Implemented |
| Vulnerability scanning | Trivy | Implemented |
| Branch protection | GitHub Rulesets | Implemented |
| Infrastructure as Code | Terraform | Next |
| Cloud platform | AWS | Next |
| Container registry | Amazon ECR | Planned |
| Kubernetes | Local Kubernetes and Amazon EKS | Planned |
| Packaging | Helm | Planned |
| GitOps | Argo CD | Planned |
| Observability | Prometheus and Grafana | Planned |
| Reliability | SRE and failure testing | Planned |
| Disaster recovery | Backup and restore validation | Planned |

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

## Local Development with Docker

Docker Compose is the primary local runtime environment.

### 1. Configure local environment variables

```bash
export POSTGRES_DB=ai_job_platform
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=local-development-only
```

These credentials are intended only for local development.

Do not reuse them for production or cloud environments.

### 2. Validate the Compose configuration

```bash
docker compose config --quiet
```

### 3. Build and start the stack

```bash
docker compose up --build --detach --wait
```

### 4. Verify application health

```bash
curl --fail http://127.0.0.1:8000/health/live
```

```bash
curl --fail http://127.0.0.1:8000/health/ready
```

The interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### 5. Stop the environment

```bash
docker compose down
```

To also remove the local PostgreSQL volume:

```bash
docker compose down --volumes
```

## Local Python Development

A Python virtual environment can also be used for application development and
testing.

### Create the environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Install development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install --requirement requirements-dev.txt
```

## Database Migrations

Alembic manages database schema changes.

Apply all migrations with:

```bash
python -m alembic upgrade head
```

The PostgreSQL connection format is:

```text
postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE
```

## Quality Checks

The same core checks used during development are enforced through CI.

### Dependency compatibility

```bash
python -m pip check
```

### Ruff linting

```bash
ruff check .
```

### Ruff formatting

```bash
ruff format --check .
```

### Fast test suite

```bash
python -m pytest -m "not integration"
```

PostgreSQL integration tests are executed separately in CI against a disposable
PostgreSQL service.

## CI and Security Gates

Pull requests targeting `main` are validated through GitHub Actions before they
can be merged.

Required checks currently include:

- `Python Quality`
- `PostgreSQL Integration`
- `Docker Image`
- `Trivy Filesystem`
- `Secret Scan`

### Python Quality

Validates:

- Dependency compatibility
- Ruff linting
- Ruff formatting
- Fast automated tests

### PostgreSQL Integration

Validates the real PostgreSQL integration path by:

- Starting a disposable PostgreSQL service.
- Applying Alembic migrations.
- Running PostgreSQL-specific integration tests.

### Docker Image

Validates the containerized runtime by:

- Validating Docker Compose configuration.
- Building the application image.
- Scanning the final image with Trivy.
- Starting the application stack.
- Checking liveness and readiness endpoints.
- Verifying non-root execution.
- Cleaning disposable resources after validation.

### Gitleaks

Gitleaks scans the repository and Git history for committed secrets.

Real credentials must never be introduced merely to test secret detection.

A genuine leaked credential must be revoked or rotated and investigated rather
than bypassing the security gate.

### Trivy Filesystem Scan

Trivy scans the repository for:

- Vulnerable application dependencies.
- Dockerfile and configuration misconfigurations.

HIGH and CRITICAL findings are treated as blocking security findings according
to the configured policy.

### Trivy Container Image Scan

The final runtime image is scanned for:

- Operating system vulnerabilities.
- Application dependency vulnerabilities.
- Embedded secrets.

Fixable HIGH and CRITICAL image vulnerabilities block CI.

Unfixed upstream base-image findings are monitored instead of being hidden by a
blanket repository-wide ignore policy.

## Container Security Controls

The application container currently uses several defensive controls:

- Multi-stage Docker build.
- Dedicated non-root runtime user.
- Read-only application root filesystem through Docker Compose.
- `no-new-privileges`.
- Explicit health checks.
- Local-only application port binding.
- Runtime validation through CI.
- Trivy image scanning before container runtime validation.

## Main Branch Protection

The `main` branch is protected through a GitHub repository ruleset.

Current controls include:

- Pull requests required before merging.
- Required CI status checks.
- Branch must be up to date before merging.
- Force pushes blocked.
- Branch deletion blocked.
- No bypass actors configured.
- Merge and squash merge methods allowed.

This prevents code from bypassing the established quality and security gates.

## Security Policy

Security reporting requirements and project security expectations are defined
in:

[`SECURITY.md`](SECURITY.md)

Implementation details for CI security gates, secret scanning, vulnerability
scanning, branch protection, incident response, and rollback procedures are
documented in:

[`docs/security.md`](docs/security.md)

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── quality.yml
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── docs/
│   ├── adr/
│   ├── charter.md
│   └── security.md
├── scripts/
│   └── start.sh
├── tests/
│   ├── conftest.py
│   ├── test_db_connection.py
│   ├── test_health.py
│   └── test_matches.py
├── .dockerignore
├── .gitignore
├── alembic.ini
├── compose.yaml
├── Dockerfile
├── pyproject.toml
├── requirements-dev.txt
├── requirements.txt
├── SECURITY.md
└── README.md
```

## Delivery Roadmap

### Completed

- [x] Phase 0 - Project foundation and governance
- [x] Phase 1 - FastAPI application baseline
- [x] Phase 1 - Deterministic job matching
- [x] Phase 1 - Persistence models and migrations
- [x] Phase 1 - Liveness, readiness, and automated testing
- [x] Phase 2 - Docker containerization
- [x] Phase 2 - Local PostgreSQL runtime
- [x] Phase 2 - Container health and runtime validation
- [x] Phase 3 - GitHub Actions CI quality gates
- [x] Phase 3 - Gitleaks secret scanning
- [x] Phase 3 - Trivy filesystem scanning
- [x] Phase 3 - Trivy container image scanning
- [x] Phase 3 - Protected `main` branch and required checks
- [x] Phase 3 - Security policy and operational security documentation

### Next

- [ ] Phase 4 - Terraform and AWS foundation

### Planned

- [ ] Phase 5 - Local Kubernetes baseline
- [ ] Phase 6 - Helm packaging and local GitOps
- [ ] Phase 7 - Temporary Amazon EKS environment
- [ ] Phase 8 - Observability and SRE controls
- [ ] Phase 9 - Reliability and disaster recovery
- [ ] Phase 10 - Portfolio evidence and interview documentation

A phase is considered complete only after its implementation, validation, and
required evidence have been reviewed.

## Planned Cloud Delivery Flow

```mermaid
flowchart TB
    DEV["Developer"] --> PR["Protected GitHub Pull Request"]
    PR --> CI["CI Quality and Security Gates"]

    CI --> IMAGE["Validated Container Image"]

    IMAGE --> ECR["Amazon ECR"]

    CI --> GITOPS["GitOps Update"]
    GITOPS --> ARGO["Argo CD"]
    ARGO --> EKS["Amazon EKS"]
```

The AWS implementation is planned to use short-lived authentication through
GitHub Actions OpenID Connect rather than long-lived AWS access keys.

## Phase 4 Direction

The next workstream introduces the AWS and Terraform infrastructure foundation.

Planned areas include:

- Terraform project structure.
- Remote Terraform state.
- State locking and recovery considerations.
- AWS authentication.
- GitHub Actions OpenID Connect.
- Least-privilege IAM.
- Amazon ECR.
- Network foundation.
- Cost controls.
- Resource teardown procedures.
- Preparation for Amazon EKS.

Cloud infrastructure will not be considered complete until its deployment and
destruction paths have both been validated.

## Security and Cost Boundaries

- Secrets must not be committed to Git, container images, logs, or Terraform.
- Real candidate or personal data must not be used.
- AWS authentication will use short-lived credentials.
- IAM policies should follow least privilege.
- Security findings must not be silently ignored.
- Cloud resources require an estimated cost before deployment.
- Temporary infrastructure must have a documented teardown procedure.
- Terraform state must not contain unmanaged sensitive information.
- Backups are not considered successful until restoration has been tested.

## Engineering Principles

The project follows these principles as it evolves:

- Infrastructure as Code
- Automation First
- Security by Default
- Least Privilege
- Immutable and reproducible delivery
- Observability by Default
- Failure-aware architecture
- Documented rollback
- Cost Awareness
- No portfolio claim without implementation evidence

## Documentation

Architecture decisions and project boundaries are stored under `docs/`.

Security implementation details are documented in:

```text
docs/security.md
```

Architecture Decision Records are stored under:

```text
docs/adr/
```

Documentation is updated as implementation progresses and should not claim
unfinished infrastructure or operational controls as completed.

## License

This project is licensed under the [MIT License](LICENSE).