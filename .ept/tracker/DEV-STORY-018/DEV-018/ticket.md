---
id: DEV-018
type: development
title: DEV-018 - foundry-media-sets CLI implementation
status: Closed
created: 2026-08-10
updated: 2026-08-10
priority: High
assignee: python-developer
reporter: architect
estimated_hours: 16
time_spent_hours: 16
---

# DEV-018: DEV-018 - foundry-media-sets CLI implementation

## Description

## Description

Implement the foundry-media-sets CLI and Claude skill per DESIGN-018-media-sets-cli.md (19 media sets API v2 operations).

## Acceptance Criteria
- OP_SPECS contains exactly 19 unique entries (single MediaSet client path).
- Nested client dispatch matches the catalog exactly.
- read/read_original/retrieve/get_result use with_streaming_response + BinaryDownloadHandler (bounded, FR-DL envelope).
- upload/upload_media read file bounded after ACL decision.
- AccessControlGuard with 9-op write set; packaged metadata-only policy 5 PERMITTED / 14 BLOCKED.
- include_attribution=True per FR-ATTR-4; B3 tracing via invocation_scope.
- pyproject entry point foundry-media-sets; ruff/mypy clean.

## Deliverables
- src/foundry_cli/media_sets/
- .claude/skills/foundry-media-sets/

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
