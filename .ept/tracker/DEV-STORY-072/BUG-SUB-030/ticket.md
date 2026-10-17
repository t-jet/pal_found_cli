---
id: BUG-SUB-030
type: bug_subtask
title: Admin marking and role batch examples accept empty results
status: Open
created: 2026-10-16
updated: 2026-10-16
priority: Medium
assignee: python-developer
reporter: qa-engineer
---

# BUG-SUB-030: Admin marking and role batch examples accept empty results

## Description

# Defect
Affected version: FEATURE-015 candidate 408ad8c0a737683a99824f9ab978ede56f8bff48; SDK 1.101.0. Severity: Medium.
Reproduce: from pal-found-dev run python -B examples/rest/072/v2/admin/Marking/get_batch.py and Role/get_batch.py with prepared SDK. Both pass offline. Each requests one ID, sets SUCCESS to data: {}, and checks only equality to that empty map.
Expected: decoded data map contains requested ID and matching Marking/Role definition, or explicitly checks and explains missing requested result, per guides.
Actual: empty maps pass, so request-result identity matching is untested. Frozen SDK GetMarkingsBatchResponse and GetRolesBatchResponse data fields are keyed by requested IDs.
Test reference: TESTEXEC-075 Open; independent preflight evidence maintainer/rest-qa-072.json. No live enrollment test.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
