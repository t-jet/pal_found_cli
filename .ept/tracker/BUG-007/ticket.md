---
id: BUG-007
type: bug
title: Comment author names ending in numeric suffix are misattributed
status: Closed
affected_version: current-workspace-tracker
created: 2026-10-12
updated: 2026-10-12
priority: High
resolution: Done
assignee: qa-engineer
reporter: qa-engineer
component: tracker
---

# BUG-007: Comment author names ending in numeric suffix are misattributed

## Description

## Defect
BUG-005 same-second comment fix parses a base comment ID for author service_001 as author service. The _NNN collision suffix is ambiguous with valid author characters.

## Reproduction
On current uncommitted comments.py, create a comment with author service_001 in an isolated tracker fixture. The first ID is YYYYMMDD-HHMMSS-service_001. Run comment get or comment list and inspect author. Direct parser reproduction with a comment fixture at .ept/tmp/20261006-162954-service_001.md returned comment_id 20261006-162954-service_001 and author service.

## Expected
First comment by service_001 reports author service_001. Later same-second writes keep distinct IDs and preserve correct author identity. Existing BUG-005 comment IDs remain readable.

## Actual
_parse_comment_metadata uses regex ^(\\d{8}-\\d{6})-(.+?)(?:_\\d{3})?$ and strips _001 from the valid base author name. This misattributes audit and approval comments.

## Test execution reference
Independent BUG-005 QA review on 2026-10-12: SameSecond tests 6 passed, tracker suite 432 passed, targeted parser fixture failed. No existing test covers numeric-suffix author names.

## Acceptance criteria
- Given valid author service_001, first and later comments list and get with author service_001.
- Given same-second comments from service and service_001, each comment keeps correct author and text.
- Existing base and suffixed BUG-005 IDs continue to resolve.
- Automated isolated tests cover these cases.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
