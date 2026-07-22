---
id: QUESTION-023
type: question
title: 'QUESTION: TESTCASE-003 D-9 No asyncio.wait_for() timeout wrapper; relies on SDK honoring
  request_timeout'
status: Closed
addressed_to: architect
created: 2026-07-04
updated: 2026-07-05
priority: Critical
assignee: architect
reporter: qa-engineer
---

# QUESTION-023: QUESTION: TESTCASE-003 D-9 No asyncio.wait_for() timeout wrapper; relies on SDK honoring request_timeout

## Description

CLI forwards request_timeout= kwarg but does not wrap await in asyncio.wait_for (same gap as BUG-SUB-001). If SDK ignores kwarg, calls hang. See TESTCASE-003-test-cases.md D-9.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
