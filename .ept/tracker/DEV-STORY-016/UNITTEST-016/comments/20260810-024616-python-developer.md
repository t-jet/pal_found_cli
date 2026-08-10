Subject: Test plan
Created: 2026-08-10T02:46:16
Updated: 2026-08-10T02:46:16
---
## Test plan — foundry-streams CLI unit tests

### Deliverables
- `tests/test_foundry_streams_cli.py` — real unit tests (all SDK transport mocked; no live connections)
- `tests/test_access_control_guard.py` — reset-verb write-classification regression tests (stream.reset, subscriber.reset_offsets)

### Coverage areas (per DESIGN-016 + DEV-016 catalog)
- Exact 15-operation catalog and per-op spec structure (resources dataset/stream/subscriber)
- Parser surface: every declared argument accepted; unknown operation → CLIInputError; --max-records bounds
- Nested dispatch: client.streams.Dataset/Stream/Subscriber routing with exact kwargs for all 15 ops
- ADR-003 batch reads: --max-records (default 100) mapped to SDK limit; get_records max 10,000, read_records max 1,000; out-of-range → exit 1 before client
- Binary publish: file read bounded; missing/oversized file rejected before client; content passed as bytes positional
- JSON validation: invalid JSON / wrong shapes → CLIInputError before client creation
- Access control: READONLY blocks the 10-op write set (exit 8, zero client creation); semantic reads get_records/read_records/get_read_position/get/get_end_offsets permitted; reset verbs stay write-classified under narrow overrides (regression); metadata-only permits exactly 3 (3/12 policy parsed from packaged allow-list)
- Attribution suppression (include_attribution=False)
- Streams timeout: default 120s when env absent; env FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S override; --timeout override; invalid → exit 1
- Output formats (json/toon), privacy, console boundary (asyncio.run mocked)
- Coverage ≥80% branch on the new namespace required

### Verification
- Run: `pytest tests/test_foundry_streams_cli.py --cov=foundry_cli.streams --cov-report=term-missing`
- Document pass count and coverage in the results comment.
