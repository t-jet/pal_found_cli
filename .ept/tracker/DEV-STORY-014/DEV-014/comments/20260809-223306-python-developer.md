Subject: Files created and verification evidence
Created: 2026-08-09T22:33:06
Updated: 2026-08-09T22:33:06
---
## Files created / modified (DEV-014)

Created:
- `src/foundry_cli/orchestration/__init__.py`
- `src/foundry_cli/orchestration/scripts/__init__.py`
- `src/foundry_cli/orchestration/scripts/foundry_orchestration_cli.py` — 20-op catalog (NO ScheduleRun), parser, dispatch, JSON validators (schedule.create/replace, build.create), pagination (3 cursor-paged), ACL, B3 tracing, retry, output/error contracts
- `src/foundry_cli/orchestration/metadata-allow-list.md` — packaged 12 PERMITTED / 8 BLOCKED policy
- `.claude/skills/foundry-orchestration/SKILL.md` + `.claude/skills/foundry-orchestration/scripts/foundry_orchestration_cli.py` (thin launcher)
- `tests/test_foundry_orchestration_cli.py` — 32 unit/integration tests

Modified:
- `pyproject.toml` — console entry point `foundry-orchestration`, package-data for the allow-list, ruff per-file-ignore E402
- `src/foundry_cli/common/access_control_guard.py` — added `launch`, `promote`, `pause`, `unpause` to `_WRITE_VERBS` (mandated by DESIGN-014)
- `tests/test_access_control_guard.py` — 4 new write-classification cases
- `.ept/docs/document_index.md` — Major Change note updated

## Mandatory verification (per development In Progress DoD)

- File existence: all files verified present via directory listing/file search.
- Compile: `python -m compileall src/foundry_cli` → COMPILE OK (exit 0).
- Wheel build: `pip wheel . --no-deps` succeeded; wheel contains `foundry_cli/orchestration/metadata-allow-list.md` and the `foundry-orchestration` console entry point.
- Tests: `pytest tests/test_foundry_orchestration_cli.py` → 32 passed; full suite 1089 passed (0 failed).
- Branch coverage on orchestration namespace: 91% (orchestration CLI module); repository total 85.5% (>= 80% gate).
- ruff: all checks passed. mypy: no issues in 45 source files.
- Console smoke: `foundry-orchestration --help` lists build/job/schedule/schedule-version clients; entry point registered.
- ACL verification: read-only blocks the 8 mutating operations (build.cancel/create, schedule.create/delete/pause/replace/run/unpause) with exit 8; build.search and schedule.get_affected_resources stay semantic reads; metadata-only permits exactly 12 / blocks 8.
- Commit: bd13955.
- Time reported in frontmatter.

## Decisions
- `get_batch` commands accept flat `--build-rids-json`/`--job-rids-json`/`--schedule-rids-json` lists and translate to the SDK body elements (per TESTCASE-014).
- `retry_backoff_duration` is a JSON object (`{value, unit}`) passed as `--retry-backoff-duration-json`.
- Boolean options (`force_build`, `abort_on_failure`, `notifications_enabled`) are store_true flags.
- OWASP Top-10 self-review: no hardcoded credentials, inputs never echoed, error envelopes omit sensitive content; completed as part of this implementation.
