---
id: DESIGN-007
type: design
title: 'DEV-STORY-006 DESIGN: filesystem skill technical spec, estimation & OP_SPECS design'
status: Closed
created: 2026-07-29
updated: 2026-07-29
priority: High
assignee: tech-lead
reporter: architect
time_spent_hours: 4
---

# DESIGN-007: DEV-STORY-006 DESIGN: filesystem skill technical spec, estimation & OP_SPECS design

## Description

**Technical summary**
`foundry-filesystem` CLI skill exposes all 31 operations of `foundry_sdk.v2.filesystem` (Folder 5, Project 7, Resource 11, ResourceRole 3, Space 5) through a subprocess-invocable Python CLI. It mirrors the DEV-STORY-007 foundry-ontologies refined pattern and ships both the `foundry-filesystem` console entry point and the `.claude/skills/foundry-filesystem/` skill package.

**Architecture decision**
1. Pattern: DEV-STORY-007 ontologies refined pattern using OP_SPECS plus `_get_client` nested-sub-client dispatch, not datasets per-op wrappers. `Resource.Role` (`resource-role` add/list/remove) is a nested sub-client accessed via `client.filesystem.Resource.Role`, matching the ontologies nested client pattern.
2. Entry point: `console_main`, wrapping `async def main()`, matching the newer ontologies convention.
3. Error mapping: no new mapping. `src/foundry_cli/common/error_serializer.py:_register_sdk_exceptions()` already maps SDK base exceptions; filesystem exceptions subclass those bases. BadRequestError is covered through ValidationError behavior, so the CLI should let exceptions propagate to `ErrorSerializer.serialize()`.

**Component breakdown**
- `src/foundry_cli/filesystem/__init__.py`
- `src/foundry_cli/filesystem/scripts/__init__.py`
- `src/foundry_cli/filesystem/scripts/foundry_filesystem_cli.py` with argparse, OP_SPECS, `_get_client`, per-resource subparsers, `async def main()`, and `def console_main()`
- `.claude/skills/foundry-filesystem/SKILL.md` with frontmatter, 31-operation catalog, usage, options, architecture refs, exit codes, ACL flow, output, and config
- `.claude/skills/foundry-filesystem/scripts/foundry_filesystem_cli.py` thin launcher
- `pyproject.toml` console entry point plus coverage and ruff consistency updates
- `tests/test_foundry_filesystem_cli.py`
- `tests/test_filesystem_console_wrapper.py`

**Interface contracts**
- `def console_main() -> int`: synchronous entry, calls `asyncio.run(main())`.
- `async def main(argv: list[str] | None = None) -> int`: builds parser, resolves resource and operation, invokes shared infra, returns ADR-001 exit code.
- `_get_client(args, cfg) -> ResourceClient`: returns Folder, Project, Resource, Resource.Role, or Space client based on `args.resource`; `resource-role` returns `client.filesystem.Resource.Role`.
- `OP_SPECS: dict[tuple[str, str], OpSpec]`: keyed by `(resource, operation)` and declares pagination, positional RID/path args, and keyword options.

**Integration points**
ConfigLoader (ADR-006 .env search) -> AuthProvider (FOUNDRY_TOKEN) -> AsyncClientFactory -> `.filesystem` namespace client -> per-op wrapper -> RetryHandler (429/503, ADR-002) -> ErrorSerializer (ADR-001) -> OutputFormatter (ADR-004 JSON/TOON auto) -> LogSetup NDJSON stderr (ADR-005) -> AccessControlGuard 8-step (ADR-007) -> PaginationHelper for the 5 paginated ops -> TracingProvider (ENABLE_ATTRIBUTION, W3C/B3).

**Estimates**
DEV-STORY-006 story points: 8. Sub-task hours: DESIGN 4h, DEV 16h, UNITTEST 8h, CODEREVIEW 4h, TESTCASE 6h, TESTEXEC 6h, DEVOPS 3h. Total: 47h, one sprint.

## Acceptance Criteria

- [ ] AC-FS-PKG-1: Skill package contains `.claude/skills/foundry-filesystem/SKILL.md` and a `scripts/` directory with `foundry_filesystem_cli.py`.
- [ ] AC-FS-PKG-2: SKILL.md has YAML frontmatter, documents all 31 operations grouped by resource client with counts, documents usage examples, common options, exit codes, access-control precedence, output behavior, and file location.
- [ ] AC-FS-PKG-3: `pyproject.toml` registers `foundry-filesystem` to the CLI `console_main`, and `foundry-filesystem --help` exits 0 after install.
- [ ] AC-FS-OP-ALL: All 31 filesystem subcommands are present in the dispatch table and each `--help` path exits 0.
- [ ] AC-FS-OP-FOLDER: Folder `children`, `create`, `get`, `get-batch`, and `replace` are callable through the async SDK Folder client.
- [ ] AC-FS-OP-PROJECT: Project `add-organizations`, `create`, `create-from-template`, `get`, `organizations`, `remove-organizations`, and `replace` are callable through the async SDK Project client.
- [ ] AC-FS-OP-RESOURCE: Resource `add-markings`, `delete`, `get`, `get-access-requirements`, `get-batch`, `get-by-path`, `get-by-path-batch`, `markings`, `permanently-delete`, `remove-markings`, and `restore` are callable through the async SDK Resource client.
- [ ] AC-FS-OP-RESOURCE-ROLE: Resource-role `add`, `list`, and `remove` are callable through `client.filesystem.Resource.Role`.
- [ ] AC-FS-OP-SPACE: Space `create`, `delete`, `get`, `list`, and `replace` are callable through the async SDK Space client.
- [ ] AC-FS-INFRA-COMMON: Filesystem CLI integrates ConfigLoader, AuthProvider, AsyncClientFactory, RetryHandler, ErrorSerializer, OutputFormatter, LogSetup, AccessControlGuard, and PaginationHelper using the established namespace-skill pattern.
- [ ] AC-FS-INFRA-RETRY: HTTP 429/503 errors use RetryHandler backoff and NDJSON retry logging.
- [ ] AC-FS-INFRA-ERROR: SDK exceptions serialize through ErrorSerializer with ADR-001 exit codes and structured JSON errors.
- [ ] AC-FS-INFRA-OUTPUT: `--format json|toon|auto` and default format config route through OutputFormatter, with pagination metadata on stderr after the metadata separator.
- [ ] AC-FS-INFRA-ACL: ACL env vars apply the ADR-007 8-step precedence model and blocked operations return exit code 8 with structured JSON.
- [ ] AC-FS-INFRA-PAGINATION: Folder children, project organizations, resource markings, resource-role list, and space list support `--page-size`, `--page-token`, and `--batch-pages` through PaginationHelper.
- [ ] AC-FS-INFRA-TRACING: ENABLE_ATTRIBUTION tracing creates valid W3C trace/span IDs, binds SDK context, and does not leak between calls.
- [ ] AC-FS-EXIT-SUCCESS: Successful operations exit 0 and emit valid JSON or TOON.
- [ ] AC-FS-EXIT-AUTH: Missing or invalid FOUNDRY_TOKEN exits 2 with AuthenticationError JSON.
- [ ] AC-FS-EXIT-NOTFOUND: Missing RID or path exits 4 with the matching NotFound error.
- [ ] AC-FS-EXIT-CONFIG: Missing required environment exits 9 with ConfigurationError JSON.
- [ ] AC-FS-QUALITY-COVERAGE: Targeted filesystem tests pass and maintain at least 80% branch coverage.
- [ ] AC-FS-QUALITY-LINT-TYPE: ruff and mypy report no lint or type errors.
- [ ] AC-FS-QUALITY-PATTERN-CONSISTENCY: Layout, parser structure, dispatch table shape, and integration wiring match the established namespace-skill pattern.

## Related Documentation

- `.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md`
- `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md`
- `.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md`
- `.ept/docs/deliverables/architecture/adr/ADR-002-call-timeout-defaults.md`
- `.ept/docs/deliverables/architecture/adr/ADR-004-format-auto-algorithm.md`
- `.ept/docs/deliverables/architecture/adr/ADR-005-log-format.md`
- `.ept/docs/deliverables/architecture/adr/ADR-006-env-file-search-path.md`
- `.ept/docs/deliverables/architecture/adr/ADR-007-operation-level-readonly.md`
- `.ept/docs/deliverables/architecture/canonical-env-var-reference.md`
- `.ept/docs/deliverables/architecture/metadata-allow-list.md`
- `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/filesystem/`
- DEV-STORY-005 foundry-datasets pattern and DEV-STORY-007 foundry-ontologies refined pattern

## Notes

No implementation work is included in this design correction. Upstream dependencies DEV-STORY-001 through DEV-STORY-004, BA-DES-001, and SA-DES-001 are closed; no QUESTION blockers are recorded.
