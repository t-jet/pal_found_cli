Subject: Review request — DEV-017 Resolved
Created: 2026-08-10T11:38:27
Updated: 2026-08-10T11:38:27
---
## Review request

DEV-017 (foundry-connectivity CLI, 20 operations) is Resolved at commit 62c269f. Implementation files verified on disk and compiling.

- Catalog: OP_SPECS exactly 20 (Connection 7, FileImport 6, TableImport 6, VirtualTable 1); nested dispatch via client.connectivity.Connection(.FileImport|.TableImport|.VirtualTable).
- Pagination: file-import list / table-import list via PaginationHelper (with_raw_response, --page-size/--page-token/--all/--max-pages).
- ACL: 13-op write set; get_configuration_batch semantic read; packaged metadata allow-list 7 PERMITTED / 13 BLOCKED.
- Binary upload: upload-custom-jdbc-drivers bounded 16 MiB read after ACL before client; .jar validation.
- include_attribution=False; B3 tracing via invocation_scope; secrets never echoed.
- Verification: compileall 0, ruff clean, mypy clean (57 files), bandit clean, 33 focused tests pass (88% branch), full suite 1214 passed 86.28% branch.

Files: src/foundry_cli/connectivity/, .claude/skills/foundry-connectivity/. Reviewer: tech-lead.
