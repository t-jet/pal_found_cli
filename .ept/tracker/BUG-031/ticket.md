---
id: BUG-031
type: bug
title: Admin search counts response envelopes instead of search results
status: Closed
affected_version: bfdee738+dirty-20261014
created: 2026-10-14
updated: 2026-10-14
priority: High
resolution: Done
assignee: python-developer
reporter: qa-engineer
---

# BUG-031: Admin search counts response envelopes instead of search results

## Description

## Scope
Admin group search and user search via local SDK SearchGroupsResponse and SearchUsersResponse. Found during approved WORK-005 semantic recheck.

## Reproduction
Run python .ept/tmp/repro_admin_search.py from workspace with current CLI source. Mock each search response as data=[a,b], nextPageToken=page-2; second as data=[c], nextPageToken=null; use --page-size 2 --batch-pages 2. No credential needed.

## Expected
CLI emits three search result records and pagination metadata pages_fetched=2, total_items=3. Skill and SDK document search result data with continuation.

## Actual
CLI emits two page envelopes containing nested data; pages_fetched=2, total_items=2. Both group.search and user.search affected. PaginationHelper._extract_items reads items, while SDK Search*Response exposes data.

## Evidence
WORK-005; CLI admin _paginate_page_envelopes lines 428-450; PaginationHelper._extract_items lines 126-140; SDK admin models.py lines 867-888; skill Admin search records.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
