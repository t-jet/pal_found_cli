---
id: DEVOPS-010
type: devops
title: Package and verify Foundry Audit entry points
status: Closed
created: 2026-08-01
updated: 2026-08-01
priority: High
assignee: devops-engineer
reporter: devops-engineer
estimated_hours: 2
time_spent_hours: 0.2
---

# DEVOPS-010: Package and verify Foundry Audit entry points

## Description

Validate additive packaging and deployment readiness.

## Acceptance Criteria

- Wheel and editable installs expose `foundry-audit`.
- Packaged console and Claude launcher help return exit code 0.
- `pyproject.toml` `project.scripts` maps `foundry-audit` to `foundry_cli.audit.scripts.foundry_audit_cli:console_main`.
- Existing entry points remain available.
- CI gates pass on Python 3.11 and 3.12.
- No new infrastructure, secrets, dependencies, or environment variables are introduced.
- DEVOPS-010 begins only after successful TESTEXEC-010.
- Operational rollback identifies the previous known-good package version or artifact, reinstalls that artifact, restores the prior release bundle without the Audit launcher, and smoke-tests retained console commands; deleting source files alone is not rollback.

## Related Documentation

- `.ept/docs/deliverables/architecture/DESIGN-010-audit-cli.md`
- `DEV-STORY-010`
- `TESTEXEC-010`

## Notes

Packaging-verification estimate: 2 hours. Work begins after successful TESTEXEC-010.
