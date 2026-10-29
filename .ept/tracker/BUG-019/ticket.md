---
id: BUG-019
type: bug
title: Third Party Applications and Widgets list skills misstate CLI output shape
status: Closed
affected_version: pal_found_cli_skills-419b261-dirty
created: 2026-10-13
updated: 2026-10-13
priority: Medium
resolution: Done
assignee: project-manager
reporter: qa-engineer
component: skills
---

# BUG-019: Third Party Applications and Widgets list skills misstate CLI output shape

## Description

# Defect
The offline records for version.list and release.list say the response has a data array and optional nextPageToken. The CLI instead prints a bare list of collected Version or Release items to stdout and writes pagination metadata, including next_page_token when present, to stderr. The public async SDK returns AsyncResourceIterator, while a raw SDK page decodes to ListVersionsResponse or ListReleasesResponse.

# Reproduction
On current skills HEAD 419b261 and tool HEAD bfdee738, inspect pal-found-third-party-applications/references/01-applications.md version.list and pal-found-widgets/references/01-repository.md release.list. Compare with CLI main and _paginate_operation in the matching namespace modules and SDK async list method plus raw page models. Run the parser examples with mocked raw page responses, including a next cursor.

# Expected
Agent guidance distinguishes SDK iterator, raw server page, CLI stdout item array, and stderr continuation metadata; it tells reader where next_page_token is found.

# Actual
Both records promise a data/nextPageToken response that the CLI does not print. Agent expecting that object cannot read continuation from stdout.

# Test reference
TASK-006 / WORK-005 design comment 20261013-113622-@qa-engineer; Tech Lead approval 20261013-113755-@tech-lead.

# Acceptance criteria
Correct both records and verify copied bundle, parser examples, and current CLI/SDK result semantics. No runtime API change required.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
