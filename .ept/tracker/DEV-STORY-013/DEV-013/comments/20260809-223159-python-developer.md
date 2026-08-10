Subject: Files created and verification evidence
Created: 2026-08-09T22:31:59
Updated: 2026-08-09T22:31:59
---
## Files created / modified (DEV-013)

Created:
- `src/foundry_cli/models/__init__.py`
- `src/foundry_cli/models/scripts/__init__.py`
- `src/foundry_cli/models/scripts/foundry_models_cli.py` — 23-op catalog, parser, dispatch, JSON validators, pagination (4 cursor-paged), downloads (3 streamed), ACL, B3 tracing, retry, output/error contracts
- `src/foundry_cli/models/metadata-allow-list.md` — packaged 12 PERMITTED / 11 BLOCKED policy
- `.claude/skills/foundry-models/SKILL.md` + `.claude/skills/foundry-models/scripts/foundry_models_cli.py` (thin launcher)
- `tests/test_foundry_models_cli.py` — 33 unit/integration tests

Modified:
- `pyproject.toml` — console entry point `foundry-models`, package-data for the allow-list, ruff per-file-ignore E402
- `src/foundry_cli/common/access_control_guard.py` — added `launch`, `promote`, `pause`, `unpause` to `_WRITE_VERBS` (mandated by DESIGN-013/014)
- `tests/test_access_control_guard.py` — 4 new write-classification cases
- `.ept/docs/document_index.md` — Major Change note updated

## Mandatory verification (per development In Progress DoD)

- File existence: all files verified present via directory listing/file search.
- Compile: `python -m compileall src/foundry_cli` → COMPILE OK (exit 0).
- Wheel build: `pip wheel . --no-deps` succeeded; wheel contains `foundry_cli/models/metadata-allow-list.md` and the `foundry-models` console entry point.
- Tests: `pytest tests/test_foundry_models_cli.py` → 33 passed; full suite 1089 passed (0 failed).
- Branch coverage on models namespace: 89% (models CLI module); repository total 85.5% (>= 80% gate).
- ruff: all checks passed. mypy: no issues in 45 source files.
- Console smoke: `foundry-models --help` lists all 10 resource clients; entry point registered.
- ACL verification: read-only blocks transform_json/creates/promote_version/launch with exit 8; experiment search stays a semantic read; metadata-only permits exactly 12 / blocks 11.
- Commit: bd13955.
- Time reported in frontmatter.

## Decisions
- Used `--all`/`--max-pages` exact-page pagination flags (per TESTCASE-013), not legacy `--batch-pages`.
- `--offset`/`--page-size` on series/artifact-table JSON are service slicing (forwarded once, never via PaginationHelper).
- OWASP Top-10 self-review: no hardcoded credentials, inputs never echoed, error envelopes omit sensitive content, download filenames validated before publication; completed as part of this implementation.
