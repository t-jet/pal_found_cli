Subject: Implementation plan
Created: 2026-08-10T11:15:48
Updated: 2026-08-10T11:15:48
---
## Implementation plan

Design: DESIGN-017-connectivity-cli.md (DESIGN-017 Closed, tech-lead). Canonical structure from sql_queries/streams CLIs.

Files to create:
- `src/foundry_cli/connectivity/__init__.py`
- `src/foundry_cli/connectivity/scripts/__init__.py`
- `src/foundry_cli/connectivity/scripts/foundry_connectivity_cli.py` (OP_SPECS 20 ops; PAGINATED_OPS = file_import.list/table_import.list via PaginationHelper with --page-size/--page-token/--all/--max-pages; bounded binary upload for upload-custom-jdbc-drivers with .jar file-name validation after ACL; include_attribution=False; secrets never echoed; B3 tracing via invocation_scope; 13-op write set; metadata allow-list 7 PERMITTED/13 BLOCKED)
- `src/foundry_cli/connectivity/metadata-allow-list.md` (7/13 matching canonical)
- `.claude/skills/foundry-connectivity/SKILL.md`
- `.claude/skills/foundry-connectivity/scripts/foundry_connectivity_cli.py` (thin launcher)

pyproject.toml: entry point foundry-connectivity, package-data, ruff per-file-ignores.

Verification: compileall, ruff, mypy, unit tests (UNITTEST-017).
