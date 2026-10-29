---
id: BUG-039
type: bug
title: RetryHandler outer timeout bypasses approved range and CLI override
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

# BUG-039: RetryHandler outer timeout bypasses approved range and CLI override

## Description

## Observed defect
Pinned tool 0963e6e006f82ad1997be0e22c6b750ed0bbce3b, Windows PowerShell, local source inspection. No live Foundry call.

## Requirements and evidence
- SRS-001 FR-ASYNC-3:221
- Accepted ADR-002 default30,min1,max3600
- TESTCASE-003:62 names --timeout precedence over cfg.timeout_s
- filesystem CLI:598 resolves --timeout or cfg.timeout_s for SDK request_timeout
- filesystem CLI:599 constructs RetryHandler() without resolved timeout
- retry.py:345-347 directly float-parses env, no clamp
- retry.py:402-404 applies asyncio.wait_for
- config_loader.py:280-289 clamps SDK timeout to1..3600

## Reproduce / expected versus actual
Register range/integration defect with env5000, invalid input and finite override cases. Ask Architect/Tech Lead whether --timeout overrides both layers, per existing TESTCASE-003 intent; test slow SDK call with lower env and higher CLI timeout. Do not claim FR-ASYNC-3 wholly absent.

## Existing coverage
Closed BUG-SUB-001 and QUESTION-023 concern absent wait_for; wrapper now exists, so do not reopen as missing wrapper. New problem is inconsistent timeout values/range.

## Acceptance criteria
- Correct behavior against cited approved requirements; preserve explicit CLI choices and existing safe behavior.
- Independent regression proves failing baseline and corrected candidate, including adverse inputs and exact stdout/stderr/exit behavior where relevant.
- Review affected namespace callers and update skill guidance only after corrected behavior is pinned.
- Record implementation, code review and independent QA evidence before closure.

## Ownership and acceptance dependency
Shared tool defect predates FEATURE-015 document corrections. Relates to archived FEATURE-012 scope; do not edit or reopen archived requirements. Blocks DEV-STORY-070 acceptance of affected shared CLI guidance under BA-DES-015 BD-015-09/11/12 until resolved and retested. Original approved requirement is not waived.

## Review artifact
.ept/tmp/feature015_cli_spec_scope_triage.json (source hashes and bounded review scope). Requirements and source locators above remain readable if temporary review artifact is removed.

The outer wait_for wrapper exists. This is not recurrence of missing-wrapper BUG-SUB-001. Unclamped env timeout is confirmed; intended --timeout precedence requires Architect clarification.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
