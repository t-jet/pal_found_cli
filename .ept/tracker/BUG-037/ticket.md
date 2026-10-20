---
id: BUG-037
type: bug
title: OutputFormatter custom table violates approved TOON library contract
status: In Progress
affected_version: 0963e6e006f82ad1997be0e22c6b750ed0bbce3b
created: 2026-10-20
updated: 2026-10-20
priority: High
assignee: python-developer
reporter: project-manager
component: shared-cli
---

# BUG-037: OutputFormatter custom table violates approved TOON library contract

## Description

## Observed defect
Pinned tool 0963e6e006f82ad1997be0e22c6b750ed0bbce3b, Windows PowerShell, local source inspection. No live Foundry call.

## Requirements and evidence
- SRS-001:142,C-2:516
- ADR-004 Consequences
- Closed QUESTION-012 architect comment 20260704-232742:9,27-36; requester confirms 20260705-001202
- output_formatter.py:130-179 implements aligned table itself
- pyproject.toml:26-30 dependencies omit toon-python

## Reproduce / expected versus actual
Create linked implementation defect or reopen owning development workflow under PM rules, referencing QUESTION-012 rather than asking same design question again. Tech Lead verifies current compatible library API/source and DevOps distribution constraints before code change. No silent substitution or waiver.

## Existing coverage
Closed QUESTION-012 already chose library adoption and rejected custom renderer and deferral. Closed question is decision evidence, not proof implementation conforms.

## Acceptance criteria
- Correct behavior against cited approved requirements; preserve explicit CLI choices and existing safe behavior.
- Independent regression proves failing baseline and corrected candidate, including adverse inputs and exact stdout/stderr/exit behavior where relevant.
- Review affected namespace callers and update skill guidance only after corrected behavior is pinned.
- Record implementation, code review and independent QA evidence before closure.

## Ownership and acceptance dependency
Shared tool defect predates FEATURE-015 document corrections. Relates to archived FEATURE-012 scope; do not edit or reopen archived requirements. Blocks DEV-STORY-070 acceptance of affected shared CLI guidance under BA-DES-015 BD-015-09/11/12 until resolved and retested. Original approved requirement is not waived.

## Review artifact
.ept/tmp/feature015_cli_spec_scope_triage.json (source hashes and bounded review scope). Requirements and source locators above remain readable if temporary review artifact is removed.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
