---
id: QUESTION-016
type: question
title: 'QUESTION: TESTCASE-003 D-2 Invalid JSON args return exit 6 (ServerError) not exit
  1 (UserInputError)'
status: New
addressed_to: architect
created: 2026-07-04
updated: 2026-07-04
priority: High
reporter: qa-engineer
---

# QUESTION-016: QUESTION: TESTCASE-003 D-2 Invalid JSON args return exit 6 (ServerError) not exit 1 (UserInputError)

## Description

json.loads on --dataset-r/--schema/--backing-datasets/--primary-key raises ValueError that propagates to the generic except Exception (L447) returning exit 6. ADR-001 expects user-input validation -> exit 1. See TESTCASE-003-test-cases.md D-2.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
