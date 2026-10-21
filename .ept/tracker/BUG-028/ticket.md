---
id: BUG-028
type: bug
title: Connectivity offline skill has invalid JDBC example and result gaps
status: Closed
affected_version: 419b261aff38227cd1ed63ec2362c7c39e9f5076
created: 2026-10-13
updated: 2026-10-14
priority: Medium
resolution: Done
assignee: qa-engineer
reporter: qa-engineer
---

# BUG-028: Connectivity offline skill has invalid JDBC example and result gaps

## Description

# Scope and reproduction
FEATURE-012 Connectivity skill at skills worktree 419b261; CLI bfdee738; local SDK v2. WORK-005 / TASK-006 independent review.

1. `connection.create` example in `references/01-connection.md` gives JDBC config with `type`, `url`, `driverClass` but omits required `jdbcProperties`. `pydantic.TypeAdapter(CreateConnectionRequestConnectionConfiguration).validate_python` raises ValidationError `jdbc.jdbcProperties Field required`. Worker example passes validation. Expected an executable example with required fields.
2. `file_import.list` and `table_import.list` records in `references/02-imports.md` say CLI result is `ListFileImportsResponse` / `ListTableImportsResponse`. SDK returns ResourceIterator and CLI `_paginate_operation` decodes raw page `data`, prints list of items, and emits page metadata separately. Expected actual stdout list and cursor interpretation.
3. `connection.update_export_settings` record omits meaning of `exportEnabledWithoutMarkingsValidation` although example includes it. SDK model says enabling bypasses markings validation and shifts compliance responsibility. `connection.update_secrets` omits SDK stated temporary plaintext-in-memory handling after TLS delivery. These are material input/effect decisions under BA-DES-013 section 3.

Actual offline guidance cannot support reliable example invocation or security-sensitive choice. No live Foundry request needed. Severity Medium. Correct the records, then rerun semantic hash review.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
