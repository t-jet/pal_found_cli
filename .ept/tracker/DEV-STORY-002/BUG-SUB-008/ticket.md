---
id: BUG-SUB-008
type: bug_subtask
title: Fix current pytest failures not covered by BUG-SUB-005
status: Closed
created: 2026-07-26
updated: 2026-07-26
priority: Critical
assignee: developer
reporter: manager
component: tests
labels: deployment-validation
---

# BUG-SUB-008: Fix current pytest failures not covered by BUG-SUB-005

## Description

Deployment validation evidence from DEVOPS-002 comment 20260726-164503-manager: current focused/full pytest failures and errors remain and are not covered by closed BUG-SUB-005.
Expected: focused and full pytest suites pass for DEV-STORY-002 validation, excluding defects already resolved by BUG-SUB-005.
Actual: pytest still reports failures/errors that block deployment.
Scope: identify failing tests, fix product or test defects, document exact cases and verification command output before resolution.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
