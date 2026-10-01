---
id: UNITTEST-038
type: unittest
title: 'UNITTEST-038: Unit tests for doc-only skill conversion (no scripts, pal-found-* invocations,
  install-requirement)'
status: Closed
created: 2026-10-01
updated: 2026-10-01
priority: High
assignee: python-developer
reporter: tech-lead
estimated_hours: 6
time_spent_hours: 6
---

# UNITTEST-038: UNITTEST-038: Unit tests for doc-only skill conversion (no scripts, pal-found-* invocations, install-requirement)

## Description

Unit tests for DEV-038.

Cover: (1) each of the 16 skill folders has a SKILL.md and no scripts/ dir and no .py file; (2) every command example in each SKILL.md invokes a pal-found-* command (no 'python ..._cli.py' / 'pal_found_*_cli.py'); (3) install-requirement block present (pal_found_cli dependency + conda/pip/uv lines) in each converted skill; (4) 18-entry pal-found-* surface untouched. On pal_found_cli_skills tests/ per repo harness.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
