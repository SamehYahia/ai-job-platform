# ADR-0001: Repository Strategy

- Status: Proposed
- Date: 2026-08-18
- Project: P01 — AI Job Platform
- Decision owners: Sameh Yahia

## Context

P01 will contain application code, automated tests, container configuration,
CI workflows, infrastructure code, Kubernetes packaging, operational
documentation, and validation evidence.

The project will later use Argo CD for GitOps-based deployment.

A repository strategy is required to keep application development simple during
the early phases while separating build concerns from deployed environment state
when continuous deployment is introduced.

The strategy must:

- Keep the initial development workflow understandable.
- Avoid creating empty repositories before they provide operational value.
- Allow application and infrastructure changes to be reviewed.
- Prevent CI from directly modifying a Kubernetes cluster.
- Preserve Git as the source of truth for deployed configuration.
- Support independent application delivery and GitOps reconciliation.

## Decision

P01 will use two repositories introduced progressively.

### 1. Source and Platform Repository

The existing repository will remain:

```text
ai-job-platform