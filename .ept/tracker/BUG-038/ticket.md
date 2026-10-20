---
id: BUG-038
type: bug
title: Filesystem argparse errors bypass structured JSON stdout
status: In Progress
affected_version: 0963e6e006f82ad1997be0e22c6b750ed0bbce3b
created: 2026-10-20
updated: 2026-10-20
priority: High
assignee: python-developer
reporter: project-manager
component: shared-cli
---

# BUG-038: Filesystem argparse errors bypass structured JSON stdout

## Description

## Observed defect
Pinned tool 0963e6e006f82ad1997be0e22c6b750ed0bbce3b, Windows PowerShell, local source inspection. No live Foundry call.

## Requirements and evidence
- SRS-001 FR-OUT-4:187
- SRS-001 FR-ERR-1:247
- filesystem CLI:382 creates standard argparse.ArgumentParser
- filesystem CLI:564 parse_args runs before operation error handling at590 onward

## Reproduce / expected versus actual
Register linked shared-parser defect; independently exercise missing required argument, unknown flag, invalid choice, malformed scalar and --help. Help remains successful human-readable output; user errors follow approved JSON stdout taxonomy. Audit other namespace parsers for same cause.

## Existing coverage
Current error/namespace acceptance requires structured errors. Search found no dedicated current filesystem parser-error defect.

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
