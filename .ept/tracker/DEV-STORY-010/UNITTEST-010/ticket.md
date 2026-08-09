---
id: UNITTEST-010
type: unittest
title: Add Audit CLI unit and integration tests
status: Closed
created: 2026-08-01
updated: 2026-08-01
priority: High
assignee: python-developer
reporter: python-developer
estimated_hours: 7
time_spent_hours: 0.27
---

# UNITTEST-010: Add Audit CLI unit and integration tests

## Description

Add `tests/test_foundry_audit_cli.py` and `tests/test_audit_console_wrapper.py`.

## Acceptance Criteria

- Every DESIGN-010 unit-coverage item has an assertion.
- Real iterator and streaming protocols are consumed.
- The targeted suite passes.
- Repository branch coverage remains at least 80%.

## Related Documentation

- `.ept/docs/deliverables/architecture/DESIGN-010-audit-cli.md`
- `DEV-STORY-010`

## Notes

Unit and integration test estimate: 7 hours.
