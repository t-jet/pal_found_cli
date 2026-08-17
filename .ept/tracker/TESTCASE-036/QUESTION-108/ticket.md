---
id: QUESTION-108
type: question
title: Confirm rename QA acceptance with dirty tracker files
status: Closed
addressed_to: architect
created: 2026-08-13
updated: 2026-08-13
priority: Medium
reporter: qa-engineer
time_spent_hours: 1
---

# QUESTION-108: Confirm rename QA acceptance with dirty tracker files

## Description

QA needs an explicit architecture decision for TESTCASE-036. The 16 .claude legacy launcher probes are outside the confirmed canonical .agents migration scope. Product/source scoped diff check passes, while full git diff --check fails only on pre-existing dirty tracker ticket files that were not changed. Please confirm canonical-only acceptance and that unrelated tracker-file dirt does not block the TESTCASE DoD. Prior parent status: Open.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
