---
id: QUESTION-021
type: question
title: 'QUESTION: TESTCASE-003 D-7 OSError errno 11/115 rate-limit heuristic likely dead
  code'
status: New
addressed_to: architect
created: 2026-07-04
updated: 2026-07-04
priority: Medium
reporter: qa-engineer
---

# QUESTION-021: QUESTION: TESTCASE-003 D-7 OSError errno 11/115 rate-limit heuristic likely dead code

## Description

L444 maps errno in (11,115) to exit 7. SDK HTTP 429 raises ApiError not OSError, so this branch is unreachable; real 429 falls through to exit 6. See TESTCASE-003-test-cases.md D-7.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
