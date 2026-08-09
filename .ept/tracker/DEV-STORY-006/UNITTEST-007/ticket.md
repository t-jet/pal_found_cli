---
id: UNITTEST-007
type: unittest
title: 'DEV-STORY-006 UNITTEST: filesystem CLI dispatch/parser/ops/nested-subclient + exit-code
  tests'
status: Closed
created: 2026-07-29
updated: 2026-07-29
priority: High
assignee: python-developer
reporter: architect
estimated_hours: 8
time_spent_hours: 4
---

# UNITTEST-007: DEV-STORY-006 UNITTEST: filesystem CLI dispatch/parser/ops/nested-subclient + exit-code tests

## Description

**Scope**: `tests/test_foundry_filesystem_cli.py` (dispatch/parser/ops) + `tests/test_filesystem_console_wrapper.py` (console_main).

**Acceptance Criteria**: Given/When/Then — (1) all 31 ops present in dispatch table, each returns exit 0 on `--help`; (2) resource-role `_get_client` returns `client.filesystem.Resource.Role`; (3) 5 paginated ops wire PaginationHelper and emit next-page-token to stderr; (4) exit codes auth→2, notfound→4, acls→8, config→9 via stubbed exceptions (no new serializer entries); (5) --format json|toon|auto per op; (6) console_main returns int and propagates exit code; (7) ≥80% branch coverage maintained; (8) all targeted filesystem tests pass. Mirror `test_foundry_ontologies_cli.py` and `test_ontologies_console_wrapper.py`. Estimated 8h.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
