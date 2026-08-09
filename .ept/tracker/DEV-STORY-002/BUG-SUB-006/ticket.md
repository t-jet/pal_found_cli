---
id: BUG-SUB-006
type: bug_subtask
title: Resolve Foundry SDK dependency and import validation blockers
status: Closed
created: 2026-07-26
updated: 2026-07-26
priority: Critical
assignee: developer
reporter: manager
component: dependencies
labels: deployment-validation
time_spent_hours: 1
---

# BUG-SUB-006: Resolve Foundry SDK dependency and import validation blockers

## Description

Deployment validation evidence from DEVOPS-002 comment 20260726-164503-manager:
- Dependency install cannot resolve foundry-platform-python>=2.0.0.
- mypy reports missing foundry_sdk imports in auth_provider.py and async_client_factory.py.
Expected: dependency spec resolves in supported environments and mypy can analyze SDK imports or documented stubs consistently.
Actual: install/type-check validation blocks deployment.
Scope: fix package dependency constraints/import strategy/type hints without weakening validation.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
