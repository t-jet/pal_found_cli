Subject: Test plan
Created: 2026-08-09T22:05:56
Updated: 2026-08-09T22:05:56
---
## Test Plan — UNITTEST-014 orchestration CLI unit tests

### Scope
Unit + integration tests for the foundry-orchestration CLI (DEV-014) per DESIGN-014, DEV-STORY-014 AC, and TESTCASE-014 pattern.

### Test module
- `tests/test_foundry_orchestration_cli.py` — catalog (exactly 20 OP_SPECS entries, each with valid SDK dispatch path, NO ScheduleRun entries), parser (`orchestration <client> <operation> [flags]` routes; unknown client/operation/flag exits 1 with usage error JSON envelope), dispatch (each op calls correct mocked SDK method with right args; optional args omitted when absent), JSON validation (schedule.create, schedule.replace, build.create: invalid JSON rejected before client creation), ACL (8-step precedence; readonly blocks the 8 mutating ops with exit 8 and denying rule on stderr; build.search and schedule.get_affected_resources semantic reads), metadata-only 12/8 exact match, pagination (build jobs, build search, schedule runs: --page-size/--page-token/--all/--max-pages, exact-page, EOF, 40-page cap; get_batch single-call no paging), retry/error serialization (ADR-001/002; transient only; at-least-once disclosure), output formats (ADR-004), NDJSON stderr logs (ADR-005), tracing (include_attribution=False; B3 via invocation_scope), console entry point smoke for foundry-orchestration.

### Conventions
- Mock foundry_sdk orchestration methods; never hit a live Foundry instance.
- Real installed SDK error classes; AsyncMock for async methods; monkeypatch module globals.
- Coverage ≥80% branch on `foundry_cli/orchestration` (pyproject gate); 100% pass rate.

### Verification
- Run `python -m pytest tests/test_foundry_orchestration_cli.py -v` and full suite; record counts and coverage in closing comment.
