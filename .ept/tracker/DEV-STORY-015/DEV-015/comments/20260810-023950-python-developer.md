Subject: Implementation complete - files and verification evidence
Created: 2026-08-10T02:39:50
Updated: 2026-08-10T02:39:50
---
## Files created/modified (DEV-015)

### Created
- `src/foundry_cli/sql_queries/__init__.py` — package re-export
- `src/foundry_cli/sql_queries/scripts/__init__.py`
- `src/foundry_cli/sql_queries/scripts/foundry_sql_queries_cli.py` — the 5-op CLI
- `src/foundry_cli/sql_queries/metadata-allow-list.md` — packaged 1/4 policy
- `.claude/skills/foundry-sql-queries/SKILL.md` — Claude skill doc
- `.claude/skills/foundry-sql-queries/scripts/foundry_sql_queries_cli.py` — thin launcher

### Modified
- `pyproject.toml` — console entry point `foundry-sql-queries`, package-data, ruff E402 scope
- `tests/test_foundry_sql_queries_cli.py` — created under UNITTEST-015 scope

## Verification evidence

- **File existence**: verified via directory listing and git status (all 6 files tracked in commit `0c88063`).
- **Compile**: `python -m compileall -q src/foundry_cli/sql_queries` exit 0.
- **Lint**: `ruff check src/foundry_cli/sql_queries` — All checks passed.
- **Types**: `mypy src/foundry_cli/sql_queries` — Success, no issues found.
- **CLI surface**: `foundry-sql-queries --help` exit 0; parser exposes `query` resource with exactly `cancel`, `execute`, `execute-ontology`, `get-results`, `get-status`.
- **Unit tests**: `tests/test_foundry_sql_queries_cli.py` — 29 passed, 0 failed. Coverage sql_queries 89% branch (gate ≥80% met).
- **Full regression**: 1146 passed (1089 prior + 57 new), total coverage 86.09% branch, exit 0.
- **Runtime probes**: unknown op exit 1; missing op exit 1; metadata-only blocks cancel/execute/execute_ontology exit 8; permitted `get-status` passes ACL (reaches network, exit 6 with dummy creds); FOUNDRY_INCLUDE_TRACEBACK=false suppresses tracebacks; privacy-safe envelopes never echo inputs.
- **Commit**: `0c88063` (HEAD, all changes committed).
- **OWASP self-review**: no hardcoded credentials; input validation before client creation; no secrets echoed in errors; bounded downloads via BinaryDownloadHandler; no network on import.

## Decisions

- CLI resource subcommand is `query` (DESIGN-015 contract) while canonical ACL/env keys stay `sql_query.*`; implemented via a CLI-name alias map.
- `execute_ontology` has no `--output` option (Arrow bytes are always persisted via BinaryDownloadHandler); only `get-results` accepts `--output` for a friendly filename.

## Time reported

estimated_hours: 16, time_spent_hours: 8 (documented in frontmatter).
