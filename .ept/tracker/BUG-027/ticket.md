---
id: BUG-027
type: bug
title: Admin and Filesystem TypeError envelope disagrees with process exit
status: Closed
affected_version: pal_found_cli_tool-bfdee738-dirty
created: 2026-10-13
updated: 2026-10-14
priority: Medium
resolution: Done
assignee: project-manager
reporter: tech-lead
component: error-handling
---

# BUG-027: Admin and Filesystem TypeError envelope disagrees with process exit

## Description

# Defect
Admin and Filesystem `main` generic exception handlers call ErrorSerializer, then replace classified exit 1 with process exit 6. ErrorSerializer classifies TypeError as user input exit 1. New pagination collectors raise TypeError if SDK iterator lacks `_page_iterator`, so that path emits an envelope with exit_code 1 but process exits 6. Other TypeError paths can do the same.

# Reproduction
On current worktree, invoke `_collect_async_iterator` with an async iterator lacking `_page_iterator`: it raises TypeError. `common/error_serializer.py` maps TypeError to 1. `pal_found_admin_cli.py:592-596` and `pal_found_filesystem_cli.py:652-656` return 6 whenever serializer returns 1. No Foundry call needed. Tech Lead evidence: TASK-006 comment 20261013-172639-@tech-lead.

# Expected
ADR-001 exit code in stdout error envelope equals process exit code. Unsupported SDK iterator shape should be classified consistently and should not silently truncate data.

# Acceptance criteria
- Make envelope and process exit agree for TypeError in Admin and Filesystem.
- Choose an explicit classification for missing SDK page boundaries and test both namespaces.
- Preserve normal SDK 403 exit 3 and CLI policy denial exit 8.
- Independent QA verifies error envelope and process code.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
