# DevOps Engineer Improvement Memory

## Improvement: verify CI pipeline actually enforces security scans

Condition:
- When reviewing or wiring a CI/CD pipeline for new code

Action:
- Do check that security scan steps (bandit, safety, SAST) actually fail the build on HIGH+ severity findings. Don't leave `|| true` on bandit/safety invocations — it silently swallows failures and violates OWASP DevSecOps controls.

## Improvement: distinguish DevOps scope from Developer scope during pipeline verification

Condition:
- When CI pipeline verification reveals lint/type errors in application code

Action:
- Do NOT patch the application code inline. Do flag the issues, transition the DevOps ticket to Blocked (with a Blocks link to the Developer's ticket), and document the specific file:line failures so the Developer can fix them. Do complete and document the DevOps-owned deliverables (workflow file, env templates, packaging config) before transitioning.

## Improvement: confirm bandit flag semantics before committing CI changes

Condition:
- When changing bandit invocation flags in a CI workflow

Action:
- Do verify flag syntax locally before committing (`bandit --help` shows `-l` is severity alias but `--severity-level high` is the explicit form). Don't assume `-ll` means "HIGH only" — it actually means "LOW or higher" (reports everything). Test the command locally and confirm exit codes.
