---
id: QUESTION-014
type: question
title: 'QUESTION: TC4.R2 LogSetup log file/rotation — AC vs ADR-005 conflict'
status: New
addressed_to: architect
created: 2026-07-04
updated: 2026-07-04
priority: High
reporter: qa-engineer
---

# QUESTION-014: QUESTION: TC4.R2 LogSetup log file/rotation — AC vs ADR-005 conflict

## Description

AC for DEV-STORY-002 LogSetup mentions log file output and rotation, but ADR-005 specifies NDJSON stdout/stderr only (no file handler). Implementation follows ADR-005 (no file/rotation). Source: TESTCASE-001 comment 20260704-224649-qa-engineer. Need decision: (a) update AC to remove file/rotation requirement and align with ADR-005, (b) update ADR-005 to add file/rotation and add the feature to LogSetup, or (c) split into a separate non-functional requirement story. Affects operational logging contract for Foundry CLI deployments.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
