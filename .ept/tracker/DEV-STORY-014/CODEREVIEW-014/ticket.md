---
id: CODEREVIEW-014
type: codereview
title: 'CODEREVIEW-014: code review of foundry-orchestration CLI'
status: Closed
created: 2026-08-09
updated: 2026-08-10
priority: High
assignee: tech-lead
reporter: architect
estimated_hours: 6
---

## Description

Review the DEV-014 implementation of the foundry-orchestration CLI (20 Orchestration v2 operations) against DESIGN-014 and the DEV-STORY-014 technical scope (comment 20260809-200456-architect). Reviewer: tech-lead (Architect reviews developer work per Grooming policy). The review stays blocked on DEV-014 until DEV-014 is Resolved.

## Acceptance Criteria

- [ ] OP_SPECS catalog reviewed: exactly 20 entries, correct SDK dispatch paths, no ScheduleRun entries.
- [ ] Parser and dispatch reviewed for correctness, kebab-case/snake_case conventions, and argument validation.
- [ ] Access control reviewed: 8-step precedence, readonly blocking the 8 mutating operations (exit code 8), metadata-only 12/8 policy.
- [ ] Pagination reviewed: build.jobs, build.search, schedule.runs use PaginationHelper with the exact-page pattern; no invented pagination flags elsewhere.
- [ ] Retry/timeout reviewed per ADR-002 with at-least-once disclosure for mutating operations.
- [ ] Error serialization (ADR-001), output formats (ADR-004), NDJSON logging (ADR-005), B3 tracing with include_attribution=False verified.
- [ ] SOLID/KISS/DRY/YAGNI check; OWASP Top-10 and prompt-injection awareness; security controls confirmed.
- [ ] pyproject.toml console entry point and package data verified.
- [ ] Review findings posted as comments on DEV-014 with actionable feedback; approval recorded when clean.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-014-orchestration-cli.md
- DEV-STORY-014 comment 20260809-200456-architect
- src/foundry_cli/orchestration/ (implementation)

## Notes

Bidirectional RelatesTo links with DEV-014 plus a Blocks link (CODEREVIEW-014 blocked until DEV-014 Resolved).
