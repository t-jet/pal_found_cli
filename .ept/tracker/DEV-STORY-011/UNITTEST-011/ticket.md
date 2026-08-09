---
id: UNITTEST-011
type: unittest
title: Add Foundry AIP Agents CLI unit and integration tests
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: python-developer
reporter: workflow-mgr
estimated_hours: 16
time_spent_hours: 16
---

# UNITTEST-011: Add Foundry AIP Agents CLI unit and integration tests

## Description

Add unit and integration coverage for the complete AIP Agents contract and installed package behavior. Include the corrected session cancel response contract from DESIGN-011.

## Acceptance Criteria

- Tests verify the exact catalog, routes, signatures, parser, JSON inputs, aliases, history, cleanup, purge, pagination, retry, eager-byte handling, ACL order, B3 tracing, attribution exclusion, output, and errors.
- Tests cover all 15 SDK operations and local purge without counting purge as an SDK operation.
- Session cancel tests prove that optional --response accepts a scalar markdown string and forwards it unchanged to the SDK.
- Parser tests reject the obsolete response-json option and do not apply JSON/object validation to response.
- Import, console entry, launcher, and wheel behavior pass from an empty working directory.
- Tier 3 tests prove six permitted and nine blocked SDK operations, with purge blocked by read-only and metadata-only policies.
- The project coverage gate passes on supported Python versions.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-011-aip-agents-cli.md
- DEV-STORY-011

## Notes

AgentMarkdownResponse is a string alias in the source SDK.
