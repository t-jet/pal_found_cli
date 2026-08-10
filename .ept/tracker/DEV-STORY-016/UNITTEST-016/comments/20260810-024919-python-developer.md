Subject: Unit tests complete - results and coverage
Created: 2026-08-10T02:49:19
Updated: 2026-08-10T02:49:19
---
## Unit tests complete (UNITTEST-016)

### Deliverables
- `tests/test_foundry_streams_cli.py` — 28 test functions, all real unit tests (all SDK transport mocked; no live Foundry connection anywhere).
- `tests/test_access_control_guard.py` — reset-verb write-classification regression tests added.

### Coverage areas (per DESIGN-016 acceptance criteria)
- Exact 15-operation catalog with per-op spec structure (dataset/stream/subscriber resources)
- Parser surface: every declared argument accepted; unknown operation → exit 1 envelope; --max-records bounds enforced
- Nested dispatch: `client.streams.Dataset/Stream/Subscriber.<method>` routing with exact kwargs for all 15 ops
- ADR-003 batch reads: `--max-records` (default 100) mapped to SDK `limit`; get_records max 10,000; read_records max 1,000; out-of-range → exit 1 before client
- Binary publish: file read bounded; missing/oversized file rejected before client; bytes passed as SDK positional
- JSON validation: invalid JSON / wrong shapes → CLIInputError before client creation
- Access control: READONLY blocks the 10-op write set (exit 8, zero client creation); semantic reads permitted; reset verbs stay write-classified under narrow overrides (regression); metadata-only permits exactly 3 (3/12 policy parsed from packaged allow-list)
- Attribution suppression (include_attribution=False on factory + scope)
- Streams timeout: default 120s when env absent; env override FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S; invalid → exit 1 before ACL/client
- Output formats (json/toon), privacy (sensitive values never echoed), console boundary (asyncio.run mocked)

### Results
- **Pass rate**: 28/28 passed, 0 failed (100%).
- **Coverage**: streams namespace 90% branch — exceeds the ≥80% project gate.
- **Full regression**: 1146 passed, 0 failed, total 86.09% branch.
- **Command**: `pytest tests/test_foundry_streams_cli.py --cov=foundry_cli.streams --cov-report=term-missing -q`
- **Commit**: `0c88063`.

### Time reported
estimated_hours: 12, time_spent_hours: 6.
