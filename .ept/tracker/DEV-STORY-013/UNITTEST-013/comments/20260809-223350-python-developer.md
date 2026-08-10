Subject: Test results and coverage evidence
Created: 2026-08-09T22:33:50
Updated: 2026-08-09T22:33:50
---
## Test results and coverage (UNITTEST-013)

### Test files
- `tests/test_foundry_models_cli.py` — 33 tests covering: exact 23-op catalog, parser surface (all commands parse, unknown/unsupported rejected exit 1), nested SDK routing across the ten client paths, required-arg forwarding + optional omission, JSON validation before client creation, four cursor-paged commands (raw-response exact-page, EOF, 40-page cap, default single page), service slicing (offset/page_size forwarded once, never via PaginationHelper), trainer list no pagination, streamed downloads (atomic write, metadata envelope, unsafe-name rejection), ACL read-only write set + semantic read (experiment search), metadata-only 12/11 exact policy, ADR-001 error taxonomy (1-6), timeout bounds, output/attribution (include_attribution=False), console asyncio boundary.

### Results
- `pytest tests/test_foundry_models_cli.py` → **33 passed, 0 failed**.
- Full repository suite → **1089 passed, 0 failed**.
- Branch coverage on `foundry_cli/models`: **89%** (models CLI module); repository total **85.5%** (>= 80% required).
- All tests are real unit tests: SDK transport fully mocked, no live Foundry connections.

### Acceptance criteria mapping
- Python 3.11 matrix run; 3.12 CI gate per pyproject. ✓
- Exact signatures/routes/dispatch/parsing for all 23 commands. ✓
- Pagination, streaming, ACL, tracing, retry, output, privacy, packaging covered. ✓
- 100% pass rate. ✓
- >= 80% branch coverage on models namespace. ✓ (89%)
- Time reported in frontmatter. ✓
