---
id: DEV-014
type: development
title: 'DEV-014: implement foundry-orchestration CLI (20 operations)'
status: Closed
created: 2026-08-09
updated: 2026-08-10
priority: High
assignee: python-developer
reporter: architect
estimated_hours: 16
time_spent_hours: 16
---

# DEV-014: implement foundry-orchestration CLI (20 operations)

## Description

Implement the foundry-orchestration namespace CLI per DESIGN-014 (design deliverable .ept/docs/deliverables/architecture/DESIGN-014-orchestration-cli.md). Expose all 20 Orchestration API v2 operations (Build 6, Job 2, Schedule 10, ScheduleVersion 2, ScheduleRun 0) as a subprocess-invocable CLI with kebab-case command names and snake_case OP_SPECS catalog keys, reusing the EPIC-001 common library.

## Acceptance Criteria

- [ ] OP_SPECS catalog contains exactly 20 unique entries mapping to the authoritative catalog in DEV-STORY-014 (comment 20260809-200456-architect).
- [ ] Parser supports `orchestration <client> <operation> [flags]` with the shared --timeout, --format, --pretty options.
- [ ] Nested SDK dispatch: Build, Job, Schedule, ScheduleVersion via foundry_sdk v2 orchestration clients; ScheduleRun client has no public methods (no dispatch entries).
- [ ] JSON arguments parsed and validated locally before client creation for schedule.create, schedule.replace, and build.create; optional SDK args omitted when not provided.
- [ ] AccessControlGuard integration: 8-step precedence; the 8 mutating operations blocked under readonly; exit code 8 with denying rule on stderr.
- [ ] Metadata-only policy packaged: 12 PERMITTED / 8 BLOCKED per the metadata allow-list; namespace and operation controls evaluated before client construction.
- [ ] PaginationHelper integrated for exactly build.jobs, build.search, schedule.runs (page_size, page_token, --all, --max-pages, exact-page pattern); batch get_batch and search are single-call.
- [ ] RetryHandler with ADR-002 transient-only conditions; at-least-once disclosure for mutating operations (create/replace/run/cancel/pause/unpause/delete).
- [ ] OutputFormatter (ADR-004 JSON/TOON auto-selection), ErrorSerializer (ADR-001), LogSetup (ADR-005 NDJSON stderr), TracingProvider (SDK-native B3, include_attribution=False).
- [ ] Console entry point registered in pyproject.toml and package data includes the skill.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-014-orchestration-cli.md
- DEV-STORY-014 comment 20260809-200456-architect (technical scope)
- .ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/orchestration/

## Notes

No binary download operations — BinaryDownloadHandler not required.
