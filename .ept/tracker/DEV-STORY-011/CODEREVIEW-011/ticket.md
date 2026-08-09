---
id: CODEREVIEW-011
type: codereview
title: Review Foundry AIP Agents CLI implementation
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: tech-lead
reporter: workflow-mgr
estimated_hours: 5
time_spent_hours: 5
---

# CODEREVIEW-011: Review Foundry AIP Agents CLI implementation

## Description

## Description
Review the Foundry AIP Agents implementation for contract correctness, SDK behavior, concurrency, security, and package compatibility. Reviewer must differ from the implementer.

## Acceptance Criteria
- Review covers nested SDK routing, retries, races, session locking, secret handling, ACL precedence, purge classification, attribution exclusion, B3 propagation, output, and package behavior.
- Findings cite concrete files and lines.
- Reviewer is not the DEV implementer.
- All findings are resolved or tracked before approval.
- Ruff, mypy, tests, security checks, and package gates pass before closure.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
