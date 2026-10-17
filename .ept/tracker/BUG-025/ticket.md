---
id: BUG-025
type: bug
title: Ontology iterator fallback can skip oversized page records
status: Closed
affected_version: pal_found_cli_tool-bfdee738-dirty
created: 2026-10-13
updated: 2026-10-14
priority: Medium
resolution: Done
assignee: project-manager
reporter: tech-lead
component: ontologies
---

# BUG-025: Ontology iterator fallback can skip oversized page records

## Description

# Defect
`pal_found_ontologies_cli.py` `_iterator_page` falls back to reading `page_size` items when an async iterator has no SDK `_page_iterator` and no raw response client. Item count is not a page boundary.

# Reproduction
On Windows PowerShell with tool HEAD bfdee738 plus current diff, supply an async iterator with values [1,2,3], `next_page_token=p2`, no `_page_iterator`, and call `_iterator_page(iterator, 2)`. Read-only probe returned items [1,2] and cursor p2 while item 3 remained unread in the first page. Resuming at p2 skips item 3. Tech Lead evidence: BUG-011 comment 20261013-172624-@tech-lead.

# Expected
No continuation cursor may be emitted after truncating an unknown SDK page. Use raw one-page response or known SDK page iterator; otherwise fail closed with consistent error classification.

# Acceptance criteria
- Preserve all items on oversized pages in supported iterator paths.
- Reject an iterator whose page boundary cannot be determined; do not infer it from requested item count.
- Test no-raw/no-page-interface case and current SDK AsyncResourceIterator fallback.
- Independent QA verifies no silent record loss and ADR-001 error consistency.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
