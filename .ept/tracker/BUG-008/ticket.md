---
id: BUG-008
type: bug
title: Preserve tracker comment author names ending in numeric suffixes
status: Duplicated
affected_version: current-workspace-tracker
created: 2026-10-12
updated: 2026-10-12
priority: High
assignee: project-manager
reporter: project-manager
component: tracker
---

# BUG-008: Preserve tracker comment author names ending in numeric suffixes

## Description

# Defect
The BUG-005 same-second comment fix treats a trailing _NNN in a legitimate author name as a collision suffix. On an isolated fixture, first comment ID 20261006-162954-service_001 is read back with author service. IDs also become ambiguous between service and service_001.

## Expected
Comment get/list preserves exact sanitized author and all same-second writes. Legacy comment IDs and references remain readable.

## Actual
_parse_comment_metadata strips _001 from service_001 on its first comment. Existing tests miss this author identity case.

## Acceptance criteria
- New IDs distinguish author from collision sequence without ambiguity.
- Same-second and concurrent writes preserve content and exact author, including service and service_001.
- Legacy IDs remain readable and updateable.
- Focused and full tracker tests pass; independent QA verifies readback in isolated storage.

Related: BUG-005 (Closed); tracker/comments.py and tests/test_comments.py.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
