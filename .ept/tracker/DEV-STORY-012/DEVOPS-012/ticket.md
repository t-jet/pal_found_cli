---
id: DEVOPS-012
type: devops
title: Package and verify Foundry Language Models entry points
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: devops-engineer
reporter: devops-engineer
estimated_hours: 2
time_spent_hours: 2
---

# DEVOPS-012: Package and verify Foundry Language Models entry points

## Description

Package and verify the Language Models console entry, Claude launcher, policy, and supported-version release gates.

## Acceptance Criteria

- Build clean wheel and editable installations and verify all console entries, launcher help, imports, and packaged policy from an empty working directory.
- Verify Python 3.11/3.12 tests, coverage, Ruff, mypy, Bandit, dependency/security checks, and exact ACL policy behavior.
- Record artifact hashes, reproducible commands, clean-candidate scope, rollback procedure, and restoration evidence; do not publish or change cloud state.

## Related Documentation

- DEV-STORY-012
- TESTEXEC-012

## Notes

Blocked until QA closes.
