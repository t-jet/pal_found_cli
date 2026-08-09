Subject: Implementation plan
Created: 2026-07-29T13:06:26
Updated: 2026-07-29T13:06:26
---
## Implementation plan

Status before: `Open`. Related docs reviewed: `.ept/docs/document_index.md`, `SRS-001-foundry-cli.md`, `SAD-001-foundry-cli.md`, `canonical-env-var-reference.md`, `metadata-allow-list.md`, `TESTCASE-006-test-cases.md`, `TESTEXEC-006-execution-log.md`.

Plan:
- Implement `src/foundry_cli/filesystem/scripts/foundry_filesystem_cli.py` using the approved ontologies `OP_SPECS` pattern.
- Add package `__init__.py` files for `foundry_cli.filesystem` and `foundry_cli.filesystem.scripts`.
- Register the `foundry-filesystem` console script in `pyproject.toml`.
- Add `.claude/skills/foundry-filesystem/SKILL.md` and launcher copy under `.claude/skills/foundry-filesystem/scripts/`.
- Cover 31 operations, nested `client.filesystem.Resource.Role`, five paginated operations, shared config/auth/client factory/retry/error/output/logging/ACL/pagination/tracing flow, and no network work at import.

Acceptance criteria confirmed: 31 operation catalog present; parser exposes folder/project/resource/resource-role/space operations; access control runs before SDK invocation; pagination helper wraps folder children, project organizations, resource markings, resource-role list, and space list; CLI errors serialize to project exit codes; `console_main()` returns `asyncio.run(main())`; no implementation outside DEV-007 owned surfaces.
