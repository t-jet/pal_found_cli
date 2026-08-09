---
id: DEV-010
type: development
title: Implement Foundry Audit CLI and skill
status: Closed
created: 2026-08-01
updated: 2026-08-01
priority: High
assignee: python-developer
reporter: python-developer
estimated_hours: 10
time_spent_hours: 0.77
---

# DEV-010: Implement Foundry Audit CLI and skill

## Description

Add the Audit package, two-operation CLI, raw-page adapter, streamed bounded download, Claude skill launcher, and console entry point.

## Acceptance Criteria

- Both routes and inputs match the DESIGN-010 operation catalog.
- ACL runs before client creation.
- The invocation scope encloses client construction and all retries.
- Audit content is never eagerly read.
- Lint and type checks pass.

## Related Documentation

- `.ept/docs/deliverables/architecture/DESIGN-010-audit-cli.md`
- `DEV-STORY-010`

## Notes

Implementation estimate: 10 hours. Related review: CODEREVIEW-010.
