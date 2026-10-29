---
id: BUG-SUB-019
type: bug_subtask
title: Repair Datasets paginated SDK iterator handling
status: Closed
created: 2026-10-04
updated: 2026-10-05
priority: High
assignee: python-developer
reporter: project-manager
time_spent_hours: 0.75
---

# Repair Datasets paginated SDK iterator handling

## Description
Datasets dataset.jobs and file.list SDK v2 return AsyncResourceIterator. Current CLI awaits that value and then applies PaginationHelper, which expects page response items and a cursor. Calls can fail before returning records. Review other Datasets paginated operations for the same failure.

## Acceptance Criteria
- Datasets paginated calls use documented SDK public behavior without awaiting a non-awaitable iterator.
- CLI returns bounded records and truthful continuation behavior for page-size, page-token, and batch-pages.
- Regression tests use realistic SDK iterator behavior and cover empty/next-page cases.
- Skill operation records describe the working CLI result and limits.

## Related Documentation
- .ept/docs/customer_input/foundry-platform-python/foundry_sdk/_core/resource_iterator.py
- pal_found_cli_tool/src/pal_found_cli/common/pagination_helper.py
- pal_found_cli_tool/src/pal_found_cli/datasets/scripts/pal_found_datasets_cli.py
