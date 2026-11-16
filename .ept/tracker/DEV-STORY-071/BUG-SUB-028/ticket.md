---
id: BUG-SUB-028
type: bug_subtask
title: Admin get_batch examples accept empty results for requested IDs
status: Closed
created: 2026-10-16
updated: 2026-10-28
priority: High
resolution: Done
assignee: python-developer
reporter: qa-engineer
time_spent_hours: 0
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

- [x] Group and User batch examples return requested IDs with matching map keys and object IDs.
- [x] Regression guards reject empty maps, wrong keys and mismatched object IDs.
- [x] Independent source review, dedicated unit suite and formal cases F071-04/F071-19 pass.

## Related Documentation

- `.ept/docs/document_index.md`, FEATURE-015 REST handoff and approved design.
- `pal_found_cli_skills/tests/test_offline_rest_071.py`, committed0623f5a.
- `.ept/tmp/feature015_rest071_recovered_formal_qa_20261028.json`, exact independent execution proof.
- `.ept/tmp/feature015_rest071_code_review_20261027.json`, independent unit/source review.

## Notes

Historical defect and prior pending statements are retained above. Current offline regression and formal execution passed; no live tenant verification or integrated release acceptance is claimed.
