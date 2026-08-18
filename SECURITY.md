# Security Policy

## Supported Versions

This project is under active development. Only the latest version of the default
branch is supported.

## Reporting a Vulnerability

Do not report security vulnerabilities through public GitHub issues.

Use GitHub Private Vulnerability Reporting when available and include:

- A description of the vulnerability.
- Steps required to reproduce it.
- The expected and actual behavior.
- The potential security impact.
- A suggested remediation, if known.

Do not include real credentials, personal data, or actively exploitable secrets.

## Security Requirements

- Secrets must not be committed to Git.
- Real candidate or personal data must not be used.
- Dependencies and container images must be scanned.
- Critical and High findings require remediation or a documented exception.
- AWS authentication must use short-lived credentials.
- Suspected credential exposure requires immediate revocation and rotation.