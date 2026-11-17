---
id: BUG-SUB-027
type: bug_subtask
title: Admin membership expiration example sends empty replacement
status: Closed
created: 2026-10-16
updated: 2026-10-28
priority: High
resolution: Done
assignee: python-developer
reporter: qa-engineer
time_spent_hours: 0
---

# BUG-SUB-027: Admin membership expiration example sends empty replacement

## Description

# Defect
Affected version: FEATURE-015 candidate f30c97242c8fef553b72984bdaf02b3fe52d34db; SDK 1.101.0.
Severity: High.
Reproduce: inspect pal-found-dev/examples/rest/071/v2/admin/GroupMembershipExpirationPolicy/replace.py and run python -B examples/rest/071/v2/admin/GroupMembershipExpirationPolicy/replace.py from pal-found-dev with prepared SDK; network-denied fixture passes. EXPECTED_BODY is {}, invoke passes no maximum_duration or maximum_value, SUCCESS is {}.
Expected: meaningful policy replacement example sends an intended maximum_duration or maximum_value and checks returned value, per DEV-STORY-071 acceptance and local guide.
Actual: empty request and empty response fixture pass, demonstrating no expiration setting; a reader copying the pattern could replace existing policy without preserving an intended rule. Frozen SDK source group_membership_expiration_policy.py makes both fields optional.
Test reference: TESTEXEC-074 remains Open; independent preflight review recorded in maintainer/rest-qa-071.json. No live enrollment test.

## Acceptance Criteria

- [x] Replace policy with an explicit intended maximumDuration and verify the returned duration.
- [x] Mutation guards reject an empty or mismatched policy example.
- [x] Independent source review, dedicated unit suite and formal case F071-14 pass.

## Related Documentation

- `.ept/docs/document_index.md`, FEATURE-015 REST handoff and approved design.
- `pal_found_cli_skills/tests/test_offline_rest_071.py`, committed0623f5a.
- `.ept/tmp/feature015_rest071_recovered_formal_qa_20261028.json`, exact independent execution proof.
- `.ept/tmp/feature015_rest071_code_review_20261027.json`, independent unit/source review.

## Notes

Historical defect and prior pending statements are retained above. Current offline regression and formal execution passed; no live tenant verification or integrated release acceptance is claimed.
