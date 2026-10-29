---
id: BUG-036
type: bug
title: Namespace parser masks environment default output format
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

# BUG-036: Namespace parser masks environment default output format

## Description

## Observed defect
Pinned tool 0963e6e006f82ad1997be0e22c6b750ed0bbce3b, Windows PowerShell, local source inspection. No live Foundry call.

## Requirements and evidence
- SRS-001 FR-OUT-6:189
- DEV-STORY-006 AC-FS-INFRA-OUTPUT:58
- DEV-STORY-002:95
- filesystem CLI:360 sets --format default auto
- filesystem CLI:627 passes nonempty auto to OutputFormatter
- output_formatter.py:54-56 consults env only when format_setting falsey

## Reproduce / expected versus actual
Register linked shared-tool defect with omitted --format + env json/toon/auto cases, explicit flags including explicit auto, and representative namespace callers. Preserve FEATURE-012 ownership; link affected FEATURE-015 audit acceptance.

## Existing coverage
DEV-STORY-002 and DEV-STORY-006 acceptance cover behavior; ticket search found no dedicated current bug for parser masking.

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
