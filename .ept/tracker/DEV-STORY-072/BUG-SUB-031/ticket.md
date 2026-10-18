---
id: BUG-SUB-031
type: bug_subtask
title: Classification parser example loses requested string outcome
status: Closed
created: 2026-10-16
updated: 2026-10-18
priority: High
assignee: python-developer
reporter: qa-engineer
time_spent_hours: 0.25
---

# BUG-SUB-031: Classification parser example loses requested string outcome

## Description

# Defect
Affected version: FEATURE-015 candidate 408ad8c0a737683a99824f9ab978ede56f8bff48; SDK 1.101.0. Severity: High.
Reproduce: from pal-found-dev run python -B examples/rest/072/v2/admin/Marking/parse_classifications.py with prepared SDK. The fixture passes. It submits classification_strings containing synthetic-value, then asserts SUCCESS parsed: {} and errors: {}.
Expected: every submitted string is checked in parsed or errors; invalid strings produce human-readable errors per frozen SDK method documentation. Test at least one valid and one invalid string, assert both result paths.
Actual: requested string appears in neither map, yet fixture passes. A reader following this example can silently lose classification parse failures.
Test reference: TESTEXEC-075 Open; independent preflight evidence maintainer/rest-qa-072.json. No live enrollment test.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
