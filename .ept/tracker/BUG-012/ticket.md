---
id: BUG-012
type: bug
title: Admin and Filesystem list pagination can skip records within SDK pages
status: Closed
affected_version: pal_found_cli_tool-worktree
created: 2026-10-12
updated: 2026-10-13
priority: High
resolution: Done
assignee: python-developer
reporter: project-manager
component: pagination
---

# BUG-012: Admin and Filesystem list pagination can skip records within SDK pages

## Description

# Defect
Admin and Filesystem CLIs collect AsyncResourceIterator items until page_size * batch_pages, then resume with the iterator's next page token. Foundry may return a page larger than requested. Stopping mid-page and resuming at that cursor skips unconsumed items; small server pages can also cause batch_pages to fetch more actual pages than requested.

## Reproduction
Admin local SDK iterator with requested page_size 2, first server page [0,1,2] and cursor next, second page [3]: first call returns [0,1], resumed call returns [3], losing 2. Probe .ept/tmp/admin_pagination_repro.py. Filesystem uses the same collector pattern; independent reproduction pending.

## Expected
Every record remains reachable across continuation calls; batch_pages and pages_fetched reflect actual fetched pages. No silent loss on oversized or short pages.

## Acceptance criteria
- Correct Admin and Filesystem iterator collectors without losing records or miscounting pages.
- Tests cover oversized and short SDK pages, token resume, empty pages, and batch limits.
- Independent QA verifies both namespaces and truthful skill guidance.

Related: FEATURE-012, WORK-005.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
