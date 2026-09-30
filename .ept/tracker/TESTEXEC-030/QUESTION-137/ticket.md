---
id: QUESTION-137
type: question
title: 'Reconcile TESTCASE-030 wording: idempotency scope and empty-sentinel detection'
status: Closed
addressed_to: tech-lead
created: 2026-09-28
updated: 2026-09-28
priority: High
assignee: qa-engineer
reporter: qa-engineer
---

# QUESTION-137: Reconcile TESTCASE-030 wording: idempotency scope and empty-sentinel detection

## Description

TESTEXEC-030 executed GCD-TC-001..017 against the live canonical skills repo and the documented README commands. Two TESTCASE-030 case premises are broader than the implemented/documented contract, verified against the skills repo executable tests:

1. GCD-TC-007 expected output: rerun removes extra non-canonical pal-found* folders (exactly canonical 19, no stale leftovers). The documented PowerShell command replaces only the 19 validated target skill folders; it preserves non-canonical user folders (repo test test_published_powershell_copy_is_complete_and_safe_to_rerun asserts unrelated/custom-skill preserved). The documented guarantee (clear stale content under canonical names) PASSED.

2. GCD-TC-009 premise includes empty sentinel. The documented command validates sentinels by existence only (Test-Path -PathType Leaf); missing sentinel is caught atomically, an empty sentinel is not. Repo test test_published_powershell_copy_rejects_missing_sentinel_atomically covers only missing.

Request: reconcile TESTCASE-030 wording (scope GCD-TC-007 idempotency to canonical-named content; narrow GCD-TC-009 to missing sentinel, or amend the documented command to validate non-empty sentinels). TESTEXEC-030 remains PASS for the documented contract; no BUG-SUB opened.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
