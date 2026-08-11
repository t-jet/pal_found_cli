Subject: Implementation plan — foundry-checkpoints CLI (3 ops)
Created: 2026-08-10T17:53:30
Updated: 2026-08-10T17:53:30
---
## Implementation plan (DEV-019)
Implements the `foundry-checkpoints` CLI per DESIGN-019 (approved) with a 3-operation catalog on the single `Record` client path.

### Scope
- `record get` (positional `record_rid`) — GET /v2/checkpoints/records/{recordRid}; returns `Record`
- `record get-batch` (`--records-json`) — POST /v2/checkpoints/records/getBatch; body is a JSON list of `{"recordRid": ...}` elements (max 100); returns `GetRecordsBatchResponse`
- `record search` (`--where-json` required; optional `--page-size`, `--page-token`, `--all`, `--max-pages`, `--sort-direction`) — POST /v2/checkpoints/records/search; the only paged operation, routed through `PaginationHelper` via `with_raw_response` (next_page_token cursor)
- All 3 operations are semantic reads; zero writes. Metadata-only allow-list permits exactly 3/3. `include_attribution=False` (outside FR-ATTR-4).
- `preview` parameters excluded; optional SDK kwargs omitted when absent; every command supports `--timeout`, `--format`, `--pretty`.

### Files
- `src/foundry_cli/checkpoints/__init__.py` — package exports (`build_parser`, `main`, `console_main`)
- `src/foundry_cli/checkpoints/scripts/__init__.py` — scripts package marker
- `src/foundry_cli/checkpoints/scripts/foundry_checkpoints_cli.py` — OP_SPECS, parser, JSON validation (`--where-json`, `--records-json`), pagination integration, ACL guard, tracing, retry, output
- `src/foundry_cli/checkpoints/metadata-allow-list.md` — 3/3 PERMITTED (matches canonical allow-list)
- `pyproject.toml` — console entry point `foundry-checkpoints`, package-data, ruff E402 per-file-ignore
- Tests under `tests/` in UNITTEST-019

### Sequencing
- [ ] Write CLI module + package files + allow-list
- [ ] Update `pyproject.toml`
- [ ] Implement, then verify with UNITTEST-019 test suite
- [ ] Compile + lint + type check + full focused test run
- [ ] OWASP self-review comment, files/verification comment, time report
- [ ] In Progress → Resolved (blocks on CODEREVIEW-019)
