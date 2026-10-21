---
id: WORK-002
type: workitem
title: Retry PyPI v0.1.4 release after TestPyPI service recovery
status: Closed
created: 2026-10-06
updated: 2026-10-11
priority: High
assignee: devops-engineer
reporter: devops-engineer
estimated_hours: 1
time_spent_hours: 1.0
---

# Retry PyPI v0.1.4 release

## Scope

Retry the failed PyPI job in GitHub Actions run 37427214165 at source commit
86b060271bbff50b4fc8a4d62b09d489099ae6fb and tag v0.1.4. Conda 0.1.4 is already
published and verified. TestPyPI service availability is the only dependency.

## Acceptance criteria and deliverables

- TestPyPI trusted publishing and the existing clean staging install gate succeed.
- Production PyPI pal_found_cli 0.1.4 is available; a fresh pip install and all
  18 launcher help checks pass.
- TASK-004 records the run attempt, source, public URLs, artifact hashes and
  verification commands. If the external service still fails, record the exact
  error and retain the publication blocker.

## Related documentation

- `.ept/docs/deliverables/development/DEV-026-release-verification.md`

Estimated work: one hour. Execution plan is recorded in ticket comments.
