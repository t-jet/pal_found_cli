---
id: UNITTEST-017
type: unittest
title: UNITTEST-017 - foundry-connectivity CLI unit tests
status: Closed
created: 2026-08-10
updated: 2026-08-10
priority: High
assignee: python-developer
reporter: architect
estimated_hours: 12
time_spent_hours: 12
---

# UNITTEST-017: UNITTEST-017 - foundry-connectivity CLI unit tests

## Description

## Description

Unit tests for the foundry-connectivity CLI (20 operations), mirroring established namespace test conventions.

## Acceptance Criteria
- All 20 operations exercised (catalog exact count asserted).
- Pagination tested for file_import.list and table_import.list.
- ACL write/read classification tested (13 writes, get_configuration_batch semantic read).
- Metadata-only policy tested (7 permitted, 13 blocked).
- 100% pass rate; >=80% branch coverage on new namespace.

## Deliverables
- tests/test_foundry_connectivity_cli.py

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
