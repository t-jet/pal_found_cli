Subject: Test results — 42 passed, 87% branch, full regression 1318 passed
Created: 2026-08-11T00:19:02
Updated: 2026-08-11T00:19:02
---
## Test results (UNITTEST-021)

Tests written and committed in `74094bc` alongside DEV-021.

### Files
- `tests/test_foundry_third_party_applications_cli.py` — 40 tests (catalog, parser, dispatch ×9 ops, validation, binary upload ×5, pagination ×2, ACL, metadata-only policy, attribution, errors/timeouts/output, console).
- `tests/test_third_party_applications_console_wrapper.py` — 3 tests (asyncio boundary, launcher delegation, launcher --help).
- `tests/test_access_control_guard.py` — +2 deploy/undeploy verb regression (DESIGN-021 write classification).

### Execution results (all green)
- Focused suite: `pytest tests/test_foundry_third_party_applications_cli.py tests/test_third_party_applications_console_wrapper.py` → **42 passed**.
- Namespace coverage: **87% branch** (threshold 80%; missing lines are error/edge branches).
- ACL guard suite: **78 passed** (incl. new verb regression).
- Full regression: **1318 passed, 0 failed**; repo **86.61% branch**.
- No external connections: all SDK transport mocked (AsyncMock/SimpleNamespace doubles); env scrubbed (FOUNDRY_TOKEN/HOSTNAME/METADATA_ONLY/READONLY cleared) before suite run.

### Acceptance criteria status
- 100% pass rate: MET.
- Coverage >= 80% branch on new namespace: MET (87%).
- No real network calls: MET.
- Tests committed: MET (74094bc).

Closing as Resolved → Closed.
