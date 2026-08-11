Subject: Implementation plan — foundry-data-health CLI (6 ops)
Created: 2026-08-10T17:53:36
Updated: 2026-08-10T17:53:36
---
## Implementation plan (DEV-020)
Implements the `foundry-data-health` CLI per DESIGN-020 (approved) with a 6-operation catalog (corrected from the stale story title of 4).

### Scope
- `check create` (`--config-json` required, `--intent` optional) — POST /v2/dataHealth/checks; `config` is the `CheckConfig` discriminated union; returns `Check`
- `check delete` (positional `check_rid`) — DELETE /v2/dataHealth/checks/{checkRid}; returns None
- `check get` (positional `check_rid`) — GET /v2/dataHealth/checks/{checkRid}; returns `Check`
- `check replace` (positional `check_rid`, `--config-json` required, `--intent` optional) — PUT /v2/dataHealth/checks/{checkRid}; `config` is the `ReplaceCheckConfig` discriminated union
- `check-report get` (positional `check_rid`, `check_report_rid`) — GET .../checkReports/{checkReportRid}
- `check-report get-latest` (positional `check_rid`, `--limit` optional int 1..100) — GET .../checkReports/getLatest; no cursor, no PaginationHelper
- Write set = `check.create` / `check.delete` / `check.replace` (replace inherits replace-class write classification). Metadata allow-list 3 PERMITTED (get, check_report.get, check_report.get_latest) / 3 BLOCKED. `include_attribution=False`.
- Nested dispatch: `client_path ("Check",)` and `("Check", "CheckReport")` under `client.data_health.Check`.

### Files
- `src/foundry_cli/data_health/__init__.py`
- `src/foundry_cli/data_health/scripts/__init__.py`
- `src/foundry_cli/data_health/scripts/foundry_data_health_cli.py`
- `src/foundry_cli/data_health/metadata-allow-list.md` — 3/3 PERMITTED/BLOCKED (matches canonical allow-list)
- `pyproject.toml` — entry point `foundry-data-health`, package-data, ruff E402
- Tests under `tests/` in UNITTEST-020

### Sequencing
- [ ] Write CLI module + package files + allow-list
- [ ] Update `pyproject.toml`
- [ ] Implement, then verify with UNITTEST-020 test suite
- [ ] Compile + lint + type check + full focused test run
- [ ] OWASP self-review comment, files/verification comment, time report
- [ ] In Progress → Resolved (blocks on CODEREVIEW-020)
