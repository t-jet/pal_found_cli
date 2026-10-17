---
id: BUG-SUB-028
type: bug_subtask
title: Admin get_batch examples accept empty results for requested IDs
status: Open
created: 2026-10-16
updated: 2026-10-16
priority: Medium
assignee: python-developer
reporter: qa-engineer
---

# BUG-SUB-028: Admin get_batch examples accept empty results for requested IDs

## Description

# Defect
Affected version: FEATURE-015 candidate f30c97242c8fef553b72984bdaf02b3fe52d34db; SDK 1.101.0.
Severity: Medium.
Reproduce: run python -B examples/rest/071/v2/admin/Group/get_batch.py and User/get_batch.py from pal-found-dev with prepared SDK. Both network-denied fixtures pass. Inspect both files: each requests one UUID, sets SUCCESS to data: {}, and compares decoded output only with that empty object.
Expected: examples check returned map key and identity against requested GroupId/UserId, per DEV-STORY-071 guides and acceptance.
Actual: empty result maps pass; neither example exercises result matching or missing requested entries. Frozen SDK models GetGroupsBatchResponse and GetUsersBatchResponse type data as maps keyed by respective IDs.
Test reference: TESTEXEC-074 remains Open; independent preflight review recorded in maintainer/rest-qa-071.json. No live enrollment test.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
