Subject: Implementation plan
Created: 2026-08-10T02:24:55
Updated: 2026-08-10T02:24:55
---
## Implementation plan — foundry-sql-queries CLI (5 operations)

### Deliverables (Acceptance Criteria)
- `src/foundry_cli/sql_queries/__init__.py`
- `src/foundry_cli/sql_queries/scripts/__init__.py`
- `src/foundry_cli/sql_queries/scripts/foundry_sql_queries_cli.py` — the packaged CLI
- `src/foundry_cli/sql_queries/metadata-allow-list.md` — packaged 1/4 policy
- `.claude/skills/foundry-sql-queries/SKILL.md` + `.claude/skills/foundry-sql-queries/scripts/foundry_sql_queries_cli.py` thin launcher
- `pyproject.toml` updates: console entry point `foundry-sql-queries`, package-data, ruff E402 scope

### Catalog (OP_SPECS, snake_case keys; CLI kebab-case, resource subcommand `query`)
1. sql_query.cancel — cancel — positional sql_query_id — WRITE
2. sql_query.execute — execute — required --query; optional --fallback-branch-ids-json — WRITE
3. sql_query.execute_ontology — execute-ontology — required --query; optional --dry-run, --parameters-json, --row-limit — WRITE (Arrow bytes → BinaryDownloadHandler)
4. sql_query.get_results — get-results — positional sql_query_id; optional --output — READ (Arrow bytes → BinaryDownloadHandler)
5. sql_query.get_status — get-status — positional sql_query_id — READ

### Key design decisions
- Resource CLI subcommand is `query` (alias of snake_case `sql_query`); ACL and env keys keep `sql_query.*`.
- DOWNLOAD_OPS = {("sql_query","execute_ontology"), ("sql_query","get_results")}; both use `with_streaming_response` → `BinaryDownloadHandler.save` with namespace="sql_queries", atomic write, metadata envelope on stdout.
- No pagination (no ResourceIterator in namespace).
- ACL: write set = cancel/execute/execute_ontology (verbs already classified as writes in shared `_WRITE_VERBS`); read-only blocks them; metadata-only permits only get_status.
- include_attribution=False on client factory and invocation_scope.
- JSON args: fallback_branch_ids (list of strings), parameters (object).
- Parser `_ArgumentParser` raising CLIInputError; `_validate_timeout` ADR-002 1..3600; `_serialize_error` privacy-safe envelopes.

### Verification plan
- compileall exit 0; ruff; mypy; unit tests via UNITTEST-015 (100% pass, ≥80% branch).
- Commit all changes to the repository.
