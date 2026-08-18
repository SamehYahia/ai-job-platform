# P01 — Project Charter

| Field | Value |
| --- | --- |
| Project ID | `P01` |
| Project name | AI Job Platform |
| Project type | DevOps-first portfolio project |
| Owner | Sameh Yahia |
| Current phase | Phase 0 — Project Foundation |
| Charter status | Proposed |
| Application status | Not Started |
| Production readiness | Not production-ready |

## 1. Business Problem

A realistic software workload needs more than application code before it can be operated safely.

It requires repeatable builds, automated testing, secure artifact creation, controlled deployment, infrastructure automation, monitoring, incident response, backup restoration, and cost management.

This project uses a minimal AI Job Platform workload to demonstrate those engineering capabilities without turning the project into a large application-development exercise.

## 2. Project Purpose

The purpose of P01 is to build verifiable evidence of DevOps, cloud, platform engineering, DevSecOps, Kubernetes, observability, SRE, and disaster-recovery skills.

The application exists primarily as a workload for deploying, securing, operating, scaling, monitoring, troubleshooting, and recovering the platform.

Application development should consume no more than approximately 10–15% of the total project effort.

## 3. Project Objectives

The project will progressively demonstrate:

1. Professional Git and GitHub workflows.
2. Secure and reproducible container builds.
3. Local integration using Docker Compose.
4. Automated pull-request validation using GitHub Actions.
5. DevSecOps and software supply-chain controls.
6. Infrastructure as Code using Terraform.
7. Secure access from GitHub Actions to AWS using OpenID Connect.
8. Kubernetes deployment and operations.
9. Helm-based workload packaging.
10. GitOps deployment and reconciliation using Argo CD.
11. Application and infrastructure observability.
12. SLI, SLO, error-budget, and incident-response practices.
13. Failure testing, rollback, backup restoration, and disaster recovery.
14. AWS cost controls and safe infrastructure teardown.
15. Accurate portfolio and interview evidence based on validated work.

## 4. Business Workload

The minimal application will represent a job-matching platform.

It will:

- Accept synthetic job descriptions through an API.
- Store synthetic jobs and candidate profiles.
- Compare candidate skills with job requirements.
- Return a deterministic and explainable match result.
- Queue background analysis tasks.
- Store task state and results.
- Expose liveness, readiness, and metrics endpoints.
- Emit structured logs with correlation identifiers.

The initial matcher will be deterministic. An external AI or LLM provider is not required for the core implementation.

## 5. Functional Requirements

| ID | Requirement |
| --- | --- |
| `FR-01` | The API must accept a synthetic job description. |
| `FR-02` | The API must create and retrieve synthetic candidate profiles. |
| `FR-03` | Jobs, profiles, tasks, and results must be persisted in PostgreSQL. |
| `FR-04` | The platform must calculate an explainable job-match result. |
| `FR-05` | The API must enqueue background analysis work through Redis. |
| `FR-06` | A background worker must process queued tasks. |
| `FR-07` | The client must be able to retrieve task status and results. |
| `FR-08` | Duplicate task processing must be controlled through idempotency behavior. |
| `FR-09` | The service must expose separate liveness and readiness endpoints. |
| `FR-10` | Readiness must reflect the availability of critical dependencies. |
| `FR-11` | The service must expose Prometheus-compatible metrics. |
| `FR-12` | The API and worker must support graceful termination. |

## 6. Non-Functional Requirements

### 6.1 Security

- Secrets must not be committed to Git.
- Secrets must not be stored inside container images.
- Runtime containers must use non-root execution.
- Container privileges and Linux capabilities must be minimized.
- AWS permissions must follow least privilege.
- GitHub Actions must use short-lived AWS credentials through OIDC.
- Public write operations must not be exposed before an authentication design is approved.
- Security findings must be blocked, fixed, or covered by a documented time-limited exception.

### 6.2 Data Privacy

- Only synthetic job and candidate information is allowed.
- Real resumes, email addresses, phone numbers, and personal identifiers are prohibited.
- Sensitive values must not appear in logs, metrics, traces, screenshots, or public evidence.

### 6.3 Reliability

- Dependency failures must return controlled errors.
- Queue retries must be bounded.
- Worker tasks must define timeout and failure behavior.
- The API and worker must terminate gracefully.
- Deployment rollback must be tested.
- Backup success requires a successful restoration test.

### 6.4 Performance and Scalability

- Resource requests and limits must be based on measurements.
- Replica counts must not be invented without a documented assumption or test.
- The API and worker must be independently scalable.
- Load testing must establish a baseline before latency and throughput objectives are approved.
- Autoscaling thresholds must be connected to measured workload behavior.

### 6.5 Observability

- The API and worker must expose useful metrics.
- Logs must be structured and include correlation identifiers.
- Alerts must be actionable and linked to runbooks.
- Telemetry must not expose secrets or personal information.
- Distributed tracing will be implemented only when it provides a demonstrated troubleshooting benefit.

### 6.6 Maintainability

- Dependencies and infrastructure providers must be version-controlled.
- GitHub Actions must be pinned to immutable commit SHAs.
- Architecture decisions must be recorded using ADRs.
- Operational procedures must be documented and tested.
- Manual infrastructure changes must be avoided or reconciled back into code.

### 6.7 Recovery

- RPO and RTO targets must be declared before backup implementation.
- Database restoration must be tested.
- Kubernetes and infrastructure recovery responsibilities must be documented separately.
- Git, Terraform, GitOps configuration, and database backups must have clearly defined recovery roles.

### 6.8 Cost

- Paid AWS resources require a cost estimate before deployment.
- Continuously billed resources require an approved lifetime and teardown plan.
- Cloud resources must use mandatory project and environment tags.
- Post-teardown checks must confirm that unintended resources are not left running.

## 7. In Scope

- Minimal FastAPI application workload.
- PostgreSQL database.
- Redis queue.
- One background-worker type.
- Minimal automated tests.
- Secure Docker images.
- Docker Compose local integration.
- GitHub Actions CI.
- DevSecOps security gates.
- Terraform-managed AWS infrastructure.
- Amazon ECR and Amazon EKS.
- Helm charts.
- Argo CD and GitOps.
- Metrics, structured logs, selected traces, dashboards, and alerts.
- Load testing and failure testing.
- Rollback and drift-recovery validation.
- Backup restoration and disaster-recovery exercises.
- Architecture, security, cost, operational, and recovery documentation.

## 8. Out of Scope

The initial project excludes:

- Advanced frontend development.
- LinkedIn or job-board scraping.
- Automatic job applications.
- Browser automation.
- Real candidate data.
- LLM training.
- Retrieval-augmented generation.
- Vector databases.
- Complex AI orchestration.
- Multiple application microservices.
- Kafka.
- Service mesh.
- Multi-region active-active deployment.
- Multi-account AWS landing zones.
- A permanently running production environment.

Items may enter a future phase only through a documented requirement and architecture decision.

## 9. Assumptions

- GitHub is the primary source-control and automation platform.
- AWS is the first cloud provider.
- GitHub-hosted runners are sufficient during the initial phases.
- Local Docker and Kubernetes environments are available.
- Cloud environments will be temporary and cost-controlled.
- The repository is public and must never contain secrets or personal data.
- One engineer currently implements and operates the platform.
- Business SLO, RPO, RTO, AWS region, domain, and maximum budget are not yet approved.

## 10. Constraints

- Application work is limited to approximately 10–15% of project effort.
- The application begins as a modular monolith plus one worker.
- No public database is permitted.
- Long-lived AWS access keys are not permitted in GitHub.
- Wildcard administrative IAM permissions are not accepted by default.
- Manual SSH-based deployment is not the standard delivery method.
- Cloud resources must not be provisioned before their cost gate.
- Resource values require measurements or documented provisional assumptions.
- One task should be implemented and reviewed before beginning the next task.

## 11. Repository Strategy

The project will initially use one source and platform repository:

```text
ai-job-platform