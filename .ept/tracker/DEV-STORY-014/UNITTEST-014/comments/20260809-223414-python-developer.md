Subject: Test results and coverage evidence
Created: 2026-08-09T22:34:14
Updated: 2026-08-09T22:34:14
---
## Test results and coverage (UNITTEST-014)

### Test files
- `tests/test_foundry_orchestration_cli.py` — 32 tests covering: exact 20-op catalog (no ScheduleRun entries), parser surface (`orchestration <client> <operation>` routing, unknown client/op/flag exit 1), nested SDK dispatch (Build/Job/Schedule/ScheduleVersion) with exact arguments + optional omission, JSON validation (schedule.create/replace, build.create, get_batch rids lists) before client creation, three cursor-paged commands (build jobs, build search, schedule runs via raw-response exact-page), single-call get_batch (no paging), ACL 8-step precedence + read-only blocking of the 8 mutating ops + semantic reads (build search, get_affected_resources), metadata-only 12/8 exact policy, ADR-001 error taxonomy (1-6), timeout bounds, output/attribution (include_attribution=False), console asyncio boundary, thin launcher.

### Results
- `pytest tests/test_foundry_orchestration_cli.py` → **32 passed, 0 failed**.
- Full repository suite → **1089 passed, 0 failed**.
- Branch coverage on `foundry_cli/orchestration`: **91%** (orchestration CLI module); repository total **85.5%** (>= 80% required).
- All tests are real unit tests: SDK orchestration methods mocked, no live Foundry connections.

### Acceptance criteria mapping
- 20-entry OP_SPECS catalog with valid dispatch paths, no ScheduleRun. ✓
- Parser routes correctly; unknown exits non-zero usage error. ✓
- Dispatch calls correct mocked SDK method with right args; optionals omitted. ✓
- JSON validation for schedule.create/replace, build.create. ✓
- ACL precedence + readonly blocks 8 writes exit 8 with denying rule. ✓
- Metadata-only 12/8 exact. ✓
- Pagination for build.jobs/build.search/schedule.runs; get_batch single-call. ✓
- Retry/error serialization (ADR-001/002), output formats (ADR-004), NDJSON stderr (ADR-005). ✓
- include_attribution=False; B3 via invocation_scope. ✓
- Console entry point smoke for foundry-orchestration. ✓
- 100% pass rate; >= 80% branch coverage on orchestration namespace. ✓ (91%)
- Time reported in frontmatter. ✓
