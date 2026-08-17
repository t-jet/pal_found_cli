---
id: DEV-032
type: development
title: 'DEV: canonical skill-tree migration - implementation'
status: Closed
created: 2026-08-13
updated: 2026-08-13
priority: High
assignee: python-developer
reporter: tech_lead
estimated_hours: 24
time_spent_hours: 1.5
---

# DEV-032: DEV: canonical skill-tree migration - implementation

## Description

## Description
Move and rename the 19 skill folders into `.agents/skills`, then update frontmatter, launchers, and internal references.

Acceptance criteria:
- Create one canonical `.agents/skills` tree with `pal-found` and 18 `pal-found-*` folders.
- Preserve skill behavior and keep old content read-only until discovery passes.
- Avoid overwriting content sections owned by DEV-STORY-032, 034, and 035.
- Record changed paths and rollback steps.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
