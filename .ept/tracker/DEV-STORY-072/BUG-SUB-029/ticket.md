---
id: BUG-SUB-029
type: bug_subtask
title: CBAC examples omit marking IDs while asserting marking-specific results
status: Closed
created: 2026-10-16
updated: 2026-10-18
priority: High
assignee: python-developer
reporter: qa-engineer
time_spent_hours: 0.02
---

# BUG-SUB-029: CBAC examples omit marking IDs while asserting marking-specific results

## Description

# Defect
Affected version: FEATURE-015 candidate 408ad8c0a737683a99824f9ab978ede56f8bff48; SDK 1.101.0. Severity: High.
Reproduce: from pal-found-dev run python -B examples/rest/072/v2/admin/CbacBanner/get.py and CbacMarkingRestrictions/get.py with prepared SDK. Both pass offline. Inspect invoke: each calls get(request_timeout=30) without marking_ids; responses assert marking-specific classifications/restrictions.
Expected: examples provide resolved/proposed marking IDs and check returned classification/restrictions for that set, as both resource guides require.
Actual: both requests omit markingIds query; synthetic responses report specific marking values anyway. SDK methods accept marking_ids but source describes output for the given set.
Test reference: TESTEXEC-075 Open; independent preflight evidence maintainer/rest-qa-072.json. No live enrollment test.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
