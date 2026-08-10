---
id: DEV-017
type: development
title: DEV-017 - foundry-connectivity CLI implementation
status: Closed
created: 2026-08-10
updated: 2026-08-10
priority: High
assignee: python-developer
reporter: architect
estimated_hours: 16
time_spent_hours: 16
---

# DEV-017: DEV-017 - foundry-connectivity CLI implementation

## Description

## Description

Implement the foundry-connectivity CLI and Claude skill per DESIGN-017-connectivity-cli.md (20 connectivity API v2 operations).

## Acceptance Criteria
- OP_SPECS contains exactly 20 unique entries (Connection 7, FileImport 6, TableImport 6, VirtualTable 1).
- Nested client dispatch matches the catalog exactly.
- file-import list and table-import list use PaginationHelper (--page-size/--page-token/--all/--max-pages).
- upload-custom-jdbc-drivers reads file bounded after ACL decision.
- AccessControlGuard with 13-op write set; packaged metadata-only policy 7 PERMITTED / 13 BLOCKED.
- include_attribution=False; B3 tracing via invocation_scope.
- pyproject entry point foundry-connectivity; ruff/mypy clean.

## Deliverables
- src/foundry_cli/connectivity/
- .claude/skills/foundry-connectivity/

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
