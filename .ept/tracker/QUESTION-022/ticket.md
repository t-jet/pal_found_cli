---
id: QUESTION-022
type: question
title: 'QUESTION: TESTCASE-003 D-8 AccessControlError envelope schema bypasses ErrorSerializer'
status: Closed
addressed_to: architect
created: 2026-07-04
updated: 2026-07-05
priority: Critical
assignee: architect
reporter: qa-engineer
---

# QUESTION-022: QUESTION: TESTCASE-003 D-8 AccessControlError envelope schema bypasses ErrorSerializer

## Description

Datasets CLI catches AccessControlError directly (L389, L423) and returns EXIT_ACCESS_CONTROL without going through ErrorSerializer.serialize (cf BUG-SUB-004). Verify stdout envelope still contains ADR-001 fields. See TESTCASE-003-test-cases.md D-8.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
