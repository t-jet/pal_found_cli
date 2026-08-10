---
id: UNITTEST-014
type: unittest
title: 'UNITTEST-014: unit tests for foundry-orchestration CLI'
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: python-developer
reporter: architect
estimated_hours: 12
time_spent_hours: 12
---

# UNITTEST-014: unit tests for foundry-orchestration CLI

## Description

Write unit and integration tests for the foundry-orchestration CLI (DEV-014) covering the 20-operation catalog, parser and dispatch, nested SDK client routing (Build, Job, Schedule, ScheduleVersion; ScheduleRun absent), JSON argument validation, access control precedence, metadata-only policy, pagination, retry, error serialization, output formats, tracing, and the console entry point. Mock foundry_sdk orchestration methods; never hit a live Foundry instance.

## Acceptance Criteria

- [ ] Test modules mirror sibling suites (e.g. test_foundry_models_cli.py) and pass under pytest with coverage.
- [ ] OP_SPECS catalog test: exactly 20 entries, each with valid SDK dispatch path; no entries for the ScheduleRun client.
- [ ] Parser test: `orchestration <client> <operation> [flags]` routes correctly; unknown client/operation exits non-zero with usage error.
- [ ] Dispatch test: each operation calls the correct mocked SDK method with the right arguments; optional args omitted when absent.
- [ ] JSON validation tests for schedule.create, schedule.replace, build.create inputs (invalid JSON rejected before client creation).
- [ ] AccessControlGuard tests: 8-step precedence, readonly blocks the 8 mutating operations with exit code 8 and denying rule on stderr.
- [ ] Metadata-only policy tests: 12 PERMITTED / 8 BLOCKED exact match to the metadata allow-list.
- [ ] PaginationHelper tests for build.jobs, build.search, schedule.runs (page_size, page_token, --all, --max-pages, exact-page pattern); get_batch single-call no paging.
- [ ] Retry/error-serialization tests per ADR-001/002; output-format tests per ADR-004; NDJSON stderr log tests per ADR-005.
- [ ] Tracing test: include_attribution=False (no attribution headers); B3 propagation via invocation_scope.
- [ ] Console entry point smoke test for foundry-orchestration.

## Related Documentation

- .ept/docs/deliverables/architecture/DESIGN-014-orchestration-cli.md
- DEV-STORY-014 comment 20260809-200456-architect (technical scope)
- tests/test_foundry_models_cli.py (sibling reference)

## Notes

Follow the existing test conventions and coverage thresholds (80% branch minimum per pyproject.toml).
