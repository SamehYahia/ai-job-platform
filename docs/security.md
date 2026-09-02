# Security Controls

## CI Quality and Security Gates

Every pull request targeting `main` must pass the following GitHub Actions checks:

- Python Quality
- PostgreSQL Integration
- Docker Image
- Trivy Filesystem
- Secret Scan

## Secret Scanning

Gitleaks scans the repository for committed secrets.

Real credentials must never be bypassed or added to an allowlist simply to make CI pass.

If a real credential is exposed:

1. Revoke or rotate the credential.
2. Investigate the exposure.
3. Remove the secret from the source.
4. Rewrite Git history when required.
5. Run Gitleaks again.
6. Never disable the security gate to permit merging.

## Vulnerability Scanning

Trivy performs two complementary scans.

### Filesystem Scan

Checks:

- Python dependencies
- Dockerfile and configuration misconfigurations

HIGH and CRITICAL findings block the pipeline.

### Container Image Scan

Checks the final runtime image for:

- OS package vulnerabilities
- Application dependency vulnerabilities
- Embedded secrets

Fixable HIGH and CRITICAL vulnerabilities block CI.

Unfixed upstream base-image vulnerabilities are monitored rather than blindly suppressed with a repository-wide ignore file.

## Container Security

The application container:

- runs as a non-root user
- uses a read-only root filesystem
- enables `no-new-privileges`
- uses a multi-stage Docker build
- is validated through runtime health checks

## Main Branch Protection

The `main` branch is protected with a GitHub repository ruleset.

Controls include:

- pull requests required
- required CI status checks
- branches must be up to date before merging
- force pushes blocked
- branch deletion blocked
- no bypass actors configured

## Rollback Policy

A defective application or CI change should be reverted through a reviewed pull request.

A genuine security finding must not be bypassed by disabling the relevant security control.

Security issues should be remediated before merging whenever a remediation is available.
