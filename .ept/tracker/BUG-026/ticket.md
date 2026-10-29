---
id: BUG-026
type: bug
title: Whole-batch retry inflates pagination item and page metadata
status: Closed
affected_version: pal_found_cli_tool-bfdee738-dirty
created: 2026-10-13
updated: 2026-10-14
priority: Medium
resolution: Done
assignee: project-manager
reporter: tech-lead
component: pagination
---

# BUG-026: Whole-batch retry inflates pagination item and page metadata

## Description

# Defect
Ontology, Admin, and Filesystem `main` pass one mutable PaginationHelper to RetryHandler around the full paginated batch. Helpers count each successful page before a later page can fail. A retry starts the batch again with counters from the failed attempt.

# Reproduction
Windows PowerShell, current tool worktree. A read-only helper and RetryHandler probe configured page 1 as [1] with cursor p2; page 2 raised TimeoutError once; next whole-batch attempt returned [1,2]. Final result contained two items while helper reported pages_fetched=3 and total_items=3. Actual retry loop is in `common/retry.py:440`; helper mutations are in `common/pagination_helper.py:186-187`, Admin and Filesystem collectors at their `_collect_async_iterator`. Tech Lead evidence: BUG-011 comment 20261013-172624-@tech-lead.

# Expected
Successful command metadata describes returned records and completed page requests for that successful batch, with no failed-attempt counts. Keep bounded retries and correct continuation.

# Acceptance criteria
- Reset per-attempt pagination state or retry one page at a time without duplicated accounting.
- Test transient page-two failure then success for Ontology, Admin, and Filesystem.
- Assert stdout item count, stderr ADR-005 page/item counts, and cursor agree.
- Independent QA verifies all three namespaces.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
