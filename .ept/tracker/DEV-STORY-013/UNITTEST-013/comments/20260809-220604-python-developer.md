Subject: Test plan
Created: 2026-08-09T22:06:04
Updated: 2026-08-09T22:06:04
---
## Test Plan — UNITTEST-013 models CLI unit tests

### Scope
Unit + integration tests for the foundry-models CLI (DEV-013) per DESIGN-013, DEV-STORY-013 AC, and TESTCASE-013 pattern.

### Test modules (all under tests/)
- `tests/test_foundry_models_cli.py` — catalog (exactly 23 OP_SPECS entries with exact resource/operation/client_path/method), parser surface (all 23 commands parse; unknown client/operation/flag exits 1 with JSON envelope; help exits 0), dispatch (nested routing to ten public sub-clients via _get_client; required args forwarded; absent optionals omitted), JSON validation (valid input decoded; invalid JSON/wrong shape rejected before client creation; no payload echo), pagination (exactly 4 cursor-paged ops; --all/--max-pages exact-page, EOF stop, 40-page cap, retry restarts cursor-local helper without duplicate counts), slicing (series/artifact JSON --offset/--page-size forwarded once, never via PaginationHelper; trainer list no pagination flags), ACL (read-only blocks 9 writes exit 8 with denying rule; experiment search semantic read; launch/promote_version never read), metadata-only 12/11 exact; fail-closed malformed policy; downloads (series parquet, artifact json/parquet: below/above byte limit, atomic cleanup on failure/cancellation, unsafe filename rejection), attribution (include_attribution=False on scope+create; no env handling; context restored), tracing (B3 multi-header via transport), retry (transient only; permanent not retried; at-least-once disclosure), error taxonomy (ADR-001 codes 1..9), timeout bounds (1..3600; invalid stops before ACL/client), output formats (JSON/TOON/auto/pretty), privacy (no secrets/bodies/content in stdout/stderr/logs).
- `tests/test_foundry_models_console.py` or extend above — console entry point smoke, thin launcher reexports, imports create no side effects.

### Conventions
- Real installed foundry_sdk error classes; mock transport/network (no live connections).
- AsyncMock for async SDK methods; monkeypatch module globals (ConfigLoader, AsyncClientFactory, RetryHandler, LogSetup).
- Coverage: ≥80% branch on `foundry_cli/models` namespace (pyproject gate).
- 100% pass rate required.

### Verification
- Run `python -m pytest tests/test_foundry_models*.py -v` and full suite; record counts and coverage in closing comment.
