Subject: P1 fix applied + P3 limit validation — Claude skill and launcher added (CODEREVIEW-020)
Created: 2026-08-10T19:30:16
Updated: 2026-08-10T19:30:16
---
## P1 corrective action — missing skill deliverable (2026-08-10)

### Root cause
`.claude/skills/foundry-data-health/` did not exist — no `SKILL.md`, no launcher. DESIGN-020 Component breakdown lists "Claude skill and launcher for `foundry-data-health`" as a deliverable, and every prior namespace ships `.claude/skills/<ns>/SKILL.md` + thin launcher in its DEV commit (e.g. `62c269f` for connectivity/media-sets). The DEV-020 commit `b0df380` shipped the CLI but omitted the skill deliverable.

### Fix applied (commit f63a12c)
- Created `.claude/skills/foundry-data-health/SKILL.md` — documents the exact 6-op catalog (`check create/delete/get/replace`; `check-report get/get-latest`), the `--config-json` flag for the `CheckConfig`/`ReplaceCheckConfig` discriminated union, the `--limit` bound on `check-report get-latest`, the write set (`check.create`/`check.delete`/`check.replace`) with metadata-only permitting exactly 3 and blocking 3, `include_attribution=False`, at-least-once retry disclosure (retrying create/replace can duplicate checks), and privacy rules.
- Created `.claude/skills/foundry-data-health/scripts/foundry_data_health_cli.py` — thin launcher re-exporting `build_parser`, `console_main`, `main` from `foundry_cli.data_health.scripts.foundry_data_health_cli` (mirrors the connectivity launcher pattern).
- Added `tests/test_data_health_console_wrapper.py` — launcher delegation test (importlib: launcher re-exports packaged interfaces, no business logic) and launcher `--help` exit 0 subprocess test.

## P3 (non-blocking) — local `--limit` bounds validation (implemented)

`src/foundry_cli/data_health/scripts/foundry_data_health_cli.py`: added `_validate_limit` enforcing `1 <= limit <= 100` with a privacy-safe generic message ("limit must be between 1 and 100", never echoing the value), called from `_validate_inputs` so it fails fast (ADR-001 exit 1) before ACL check or client construction. The installed SDK exposes `CheckReportLimit` as a plain int alias (no Annotated bounds); the server previously returned 400 for out-of-range values. Added 3 unit tests: bounds acceptance/rejection (`1`/`100` accepted; `0`/`101`/`-1`/`True` rejected), message-never-echoes-value, and `--limit 0` stops before client creation (exit 1, `factory.create_calls == 0`).

### Verification
- Launcher `--help` exits 0 and lists `check`/`check-report`.
- `compileall -q src` exit 0; ruff clean; mypy source 0 errors.
- Focused suites: `tests/test_foundry_data_health_cli.py` (30, incl. 3 new limit tests) + wrapper (3) = 33 passed.
- Full suite: **1276 passed, 0 failed** (was 1267 before this correction; +9 new tests).

### Impact
No CLI surface change (`--limit` flag unchanged). Only the missing skill deliverable, its coverage, and the local `--limit` bound check were added.

Requesting re-review. Moving CODEREVIEW-020 Correction → Corrected, reassigned to tech-lead.
