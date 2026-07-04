---
id: QUESTION-011
type: question
title: 'QUESTION: TC2.R2 ErrorSerializer envelope schema — missing attempt/operation/details
  (AC conflict)'
status: New
addressed_to: architect
created: 2026-07-04
updated: 2026-07-04
priority: Critical
reporter: qa-engineer
---

# QUESTION-011: QUESTION: TC2.R2 ErrorSerializer envelope schema — missing attempt/operation/details (AC conflict)

## Description

AC for DEV-STORY-002 ErrorSerializer specifies envelope schema with attempt/operation/details fields but implementation omits these. Source: TESTCASE-001 comment 20260704-224649-qa-engineer. Need decision: (a) add the missing fields to implementation, (b) update AC to drop them, or (c) define a v2 envelope schema with migration path. Affects error CLI output contract for downstream consumers.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
