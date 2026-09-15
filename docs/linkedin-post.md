# LinkedIn Post - P01 AI Job Platform

I finished a production-oriented Kubernetes deployment demo for an AI Job Platform.

This was not just about building a small FastAPI app.

The real goal was to practice the full DevOps lifecycle around a service:
building it, testing it, packaging it, deploying it, troubleshooting it, and
capturing evidence that it actually works.

The application evaluates how well a candidate matches a job based on required
skills, then returns an explainable score with matched and missing skills.

For the platform side, I deployed the app to Amazon EKS using Helm, pushed the
container image to Amazon ECR, used PostgreSQL for persistence, and added an
explicit Alembic migration lifecycle through a Helm pre-upgrade Job.

Some of the work I validated:

- FastAPI application with a lightweight demo GUI
- PostgreSQL-backed persistence
- Docker image build and runtime checks
- Amazon ECR image delivery
- Helm deployment to Amazon EKS
- Alembic migrations through a Kubernetes Job
- Liveness and readiness health checks
- Non-root container security settings
- Trivy and Gitleaks CI security gates
- Runtime evidence from Pods, Services, Jobs, logs, and health endpoints

The most valuable part was the troubleshooting.

I hit a Helm pre-upgrade hook timeout, traced it to an invalid ECR image
reference, fixed the image delivery path, and added guardrails so empty or
placeholder image values fail early.

I also fixed a Trivy Kubernetes finding by hardening the PostgreSQL demo
manifest with a read-only root filesystem and explicit writable paths.

Final demo result:

- Helm release deployed successfully
- Migration Job completed in 9 seconds
- Application Pod running with 0 restarts
- PostgreSQL Pod running with 0 restarts
- `/health/live` returned HTTP 200
- `/health/ready` returned HTTP 200
- GUI returned an explainable matching result

Tech stack:

AWS EKS, Amazon ECR, Kubernetes, Helm, FastAPI, PostgreSQL, Alembic, Docker,
Python, Terraform, GitHub Actions.

I am using this project as part of my DevOps/SRE portfolio to show practical
cloud deployment, CI security, Kubernetes operations, and production-style
troubleshooting.

Important note: I describe this as production-oriented, not fully
production-ready. A real production version would still need managed database
operations, TLS ingress, observability, alerts, autoscaling, backup automation,
and stronger release controls.
