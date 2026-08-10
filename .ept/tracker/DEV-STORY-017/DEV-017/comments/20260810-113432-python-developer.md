Subject: Implementation complete — files and verification
Created: 2026-08-10T11:34:32
Updated: 2026-08-10T11:34:32
---
## Files created/modified

- src/foundry_cli/connectivity/__init__.py
- src/foundry_cli/connectivity/scripts/__init__.py
- src/foundry_cli/connectivity/scripts/foundry_connectivity_cli.py (OP_SPECS 20 ops: Connection 7, FileImport 6, TableImport 6, VirtualTable 1)
- src/foundry_cli/connectivity/metadata-allow-list.md (7 PERMITTED / 13 BLOCKED)
- .claude/skills/foundry-connectivity/SKILL.md
- .claude/skills/foundry-connectivity/scripts/foundry_connectivity_cli.py (thin launcher)
- pyproject.toml (entry point foundry-connectivity, package-data, ruff per-file-ignores)
- .ept/docs/document_index.md (Namespace Skill Scripts rows + Implementation Change footer)

## Key decisions
- file-import list / table-import list use PaginationHelper via with_raw_response (--page-size/--page-token/--all/--max-pages), matching DESIGN-017.
- upload-custom-jdbc-drivers: bounded 16 MiB file read after ACL decision before client construction; --file-name must end with .jar.
- allow_schema_changes registered as store_true boolean (SDK TableImportAllowSchemaChanges = bool).
- virtual_table config is a JSON object arg (--config-json).
- include_attribution=False; B3 tracing via invocation_scope; secrets never echoed (update-secrets/update-export-settings).

## Verification (MANDATORY DoD)
- Files verified on disk via file search (8 files in src/foundry_cli/connectivity/ + 2 skill files).
- compileall: exit 0. ruff: All checks passed. mypy: Success, 57 source files, no issues.
- Unit tests: tests/test_foundry_connectivity_cli.py 33 tests pass, 88% branch coverage; full suite 1214 passed 86.28% branch (previously 1148).
- bandit: clean (exit 0). CLI --help exit 0; launcher exit 0.
- Committed at 62c269f (workflow_tuning_checkpoint-01).
- OWASP self-review: no secrets hardcoded; secrets inputs never logged; bounded file reads; ACL before client/file effects; allow-list fail-closed.
