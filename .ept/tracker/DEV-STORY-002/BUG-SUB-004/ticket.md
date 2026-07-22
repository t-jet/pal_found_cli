---
id: BUG-SUB-004
type: bug_subtask
title: 'BUG-SUB: ErrorSerializer exit code 8 (AccessControlError) unreachable via serialize()
  (TC2.R1)'
status: Closed
created: 2026-07-04
updated: 2026-07-22
priority: Critical
assignee: qa-engineer
reporter: qa-engineer
component: src/foundry_cli/common/error_serializer.py
time_spent_hours: 2.0
---

# BUG-SUB-004: ErrorSerializer exit code 8 unreachable via serialize() (TC2.R1)

## Description

Discovered during TESTCASE-001 scenario TC2.R1. DEV-STORY-002 and ADR-001 require AccessControlError to serialize to exit code 8, but that path is unreachable through `ErrorSerializer.serialize()`. Evidence source: TESTCASE-001 comment `20260704-224649-qa-engineer`. Component: `src/foundry_cli/common/error_serializer.py`.

## Acceptance Criteria

- [ ] `ErrorSerializer.serialize()` can serialize AccessControlError.
- [ ] AccessControlError maps to exit code 8 per ADR-001.
- [ ] Stdout error envelope uses type `AccessControlError` and preserves the expected message/details fields.
- [ ] Regression tests cover direct AccessControlError serialization through `serialize()`.

## Related Documentation

- DEV-STORY-002 ErrorSerializer acceptance criteria
- SRS FR-ERR-1, FR-ERR-2, and FR-ERR-5
- ADR-001 Exit Code Taxonomy
- SAD-001 access control sequence

## Notes

Triage correction only. No code changed in this handoff.
