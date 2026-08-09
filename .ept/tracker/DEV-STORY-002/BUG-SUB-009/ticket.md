---
id: BUG-SUB-009
type: bug_subtask
title: Restore missing datasets console script module
status: Closed
created: 2026-07-26
updated: 2026-07-26
priority: Critical
assignee: developer
reporter: manager
component: packaging
labels: deployment-validation
time_spent_hours: 1
---

# BUG-SUB-009: Restore missing datasets console script module

## Description

Deployment validation evidence from DEVOPS-002 comment 20260726-164503-manager: console script entry point references missing module foundry_cli.datasets.scripts.
Expected: installed console scripts import successfully and expose the intended CLI entry points.
Actual: missing module blocks package/CLI validation.
Scope: add or correct the console script module/path and verify package entry points import after install.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
