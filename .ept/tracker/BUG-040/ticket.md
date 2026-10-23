---
id: BUG-040
type: bug
title: Retry MAX_ATTEMPTS=4 executes five calls instead of four total
status: Closed
affected_version: 0963e6e006f82ad1997be0e22c6b750ed0bbce3b
created: 2026-10-20
updated: 2026-10-21
priority: High
resolution: Done
assignee: python-developer
reporter: project-manager
component: shared-cli
---

# BUG-040: Retry MAX_ATTEMPTS=4 executes five calls instead of four total

## Description

## Observed defect
Pinned tool 0963e6e006f82ad1997be0e22c6b750ed0bbce3b, Windows PowerShell, local source inspection. No live Foundry call.

## Requirements and evidence
- SRS-001:422 says Maximum retry attempts
- SRS-001 OI-3:532 says4 attempts
- DEV-STORY-008 AC-5:72 explicitly says default4 total
- retry.py:314-318 stores env MAX_ATTEMPTS as max_retries
- retry.py:440 range(max_retries+1) permits5 attempts by default

## Reproduce / expected versus actual
Record clarification question to Architect with BA/Tech Lead input; select one canonical total-attempt contract, define zero/negative/invalid behavior and retryable failures, then assign implementation/document/test correction. Existing explicit4-total AC makes five calls a likely defect, but no unilateral requirement rewrite.

## Existing coverage
DEV-STORY-002 wording mixes retries/attempts; DEV-STORY-008 explicitly specifies total. No dedicated current retry-count decision found.

## Acceptance criteria
- Correct behavior against cited approved requirements; preserve explicit CLI choices and existing safe behavior.
- Independent regression proves failing baseline and corrected candidate, including adverse inputs and exact stdout/stderr/exit behavior where relevant.
- Review affected namespace callers and update skill guidance only after corrected behavior is pinned.
- Record implementation, code review and independent QA evidence before closure.

## Ownership and acceptance dependency
Shared tool defect predates FEATURE-015 document corrections. Relates to archived FEATURE-012 scope; do not edit or reopen archived requirements. Blocks DEV-STORY-070 acceptance of affected shared CLI guidance under BA-DES-015 BD-015-09/11/12 until resolved and retested. Original approved requirement is not waived.

## Review artifact
.ept/tmp/feature015_cli_spec_scope_triage.json (source hashes and bounded review scope). Requirements and source locators above remain readable if temporary review artifact is removed.

DEV-STORY-008 explicitly specifies four total attempts. Preserve that accepted AC while Architect reconciles ambiguous SRS retry wording. Do not silently redefine MAX_ATTEMPTS.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
