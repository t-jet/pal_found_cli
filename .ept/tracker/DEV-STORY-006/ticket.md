---
id: DEV-STORY-006
type: dev_story
title: foundry-filesystem skill (31 operations)
status: Closed
feature_request: FEATURE-001
epic: EPIC-002
created: 2026-04-13
updated: 2026-07-29
priority: High
resolution: Done
assignee: architect
reporter: architect
story_points: 8
release_notes: Foundry filesystem CLI skill exposing all 31 operations of the foundry_sdk.v2.filesystem namespace (Folder 5, Project 7, Resource 11, ResourceRole 3, Space 5) through a subprocess-invocable Python CLI. Integrates the shared common-layer infrastructure (ConfigLoader, AuthProvider, AsyncClientFactory, RetryHandler, ErrorSerializer, OutputFormatter, LogSetup, AccessControlGuard, PaginationHelper) following the established DEV-STORY-005 namespace-skill pattern. Five paginated operations (folder children, project organizations, resource markings, resource-role list, space list) are wired through PaginationHelper. Ships as a console entry point (foundry-filesystem) and a Claude Code skill package (.claude/skills/foundry-filesystem/) with JSON/TOON output, ADR-001 exit codes, and B3-enabled tracing.
---

# DEV-STORY-006: foundry-filesystem skill (31 operations)

## Description

Generate and validate all 31 filesystem namespace operations as a Claude Code skill package. The foundry-filesystem skill exposes every operation in the `foundry_sdk.v2.filesystem` namespace (Folder, Project, Resource, ResourceRole, Space resource clients) via a subprocess-invocable Python CLI. Operations cover folder navigation/management, project lifecycle, resource operations (markings, path resolution, delete/restore), resource role management, and space management in the Foundry Compass filesystem.

### Operation Catalog (31 operations across 5 resource clients)

| Resource | Operations | Count |
|---|---|---|
| **folder** | children, create, get, get-batch, replace | 5 |
| **project** | add-organizations, create, create-from-template, get, organizations, remove-organizations, replace | 7 |
| **resource** | add-markings, delete, get, get-access-requirements, get-batch, get-by-path, get-by-path-batch, markings, permanently-delete, remove-markings, restore | 11 |
| **resource-role** | add, list, remove | 3 |
| **space** | create, delete, get, list, replace | 5 |

**Paginated operations** (5): folder children, project organizations, resource markings, resource-role list, space list.

## Acceptance Criteria

### Skill Packaging (FR-SKILL)

- **AC-FS-PKG-1 — Skill structure**: Given the skill package `.claude/skills/foundry-filesystem/`, when inspected, then it contains `SKILL.md` and a `scripts/` directory with `foundry_filesystem_cli.py` per FR-SKILL-1/FR-SKILL-2.
- **AC-FS-PKG-2 — SKILL.md frontmatter and content**: Given the skill SKILL.md, when read, then it has YAML frontmatter (`name`, `description`) per FR-SKILL-5, documents all 31 operations grouped by resource client with counts, documents usage examples, common options, exit codes, access-control precedence, output behavior, and file location.
- **AC-FS-PKG-3 — Console entry point**: Given `pyproject.toml`, when checked, then a `foundry-filesystem` console script entry point is registered mapping to the CLI main function, and the package installs and runs with `foundry-filesystem --help` returning exit code 0.

### Operation Coverage (31/31)

- **AC-FS-OP-ALL**: Given the `foundry_filesystem_cli.py` dispatch table, when all 31 subcommands are invoked with `--help`, then each returns exit code 0 showing its resource/operation and supported options. Zero documented CLI operations are missing from the table.
- **AC-FS-OP-FOLDER**: Given folder operations, when invoked, then `children` (paginated via ResourceIterator), `create`, `get`, `get-batch`, and `replace` are all wireable and callable against the async SDK Folder client.
- **AC-FS-OP-PROJECT**: Given project operations, when invoked, then `add-organizations`, `create`, `create-from-template`, `get`, `organizations` (paginated), `remove-organizations`, and `replace` are all wireable and callable against the async SDK Project client.
- **AC-FS-OP-RESOURCE**: Given resource operations, when invoked, then `add-markings`, `delete`, `get`, `get-access-requirements`, `get-batch`, `get-by-path`, `get-by-path-batch`, `markings` (paginated), `permanently-delete`, `remove-markings`, and `restore` are all wireable and callable against the async SDK Resource client.
- **AC-FS-OP-RESOURCE-ROLE**: Given resource-role operations, when invoked, then `add`, `list` (paginated), and `remove` are wireable and callable against the async SDK Resource.Language client.
- **AC-FS-OP-SPACE**: Given space operations, when invoked, then `create`, `delete`, `get`, `list` (paginated), and `replace` are wireable and callable against the async SDK Space client.

### Shared Infrastructure Integration

- **AC-FS-INFRA-COMMON**: Given the `src/foundry_cli/common/` modules, when the filesystem CLI runs, then it integrates ConfigLoader, AuthProvider, AsyncClientFactory, RetryHandler, ErrorSerializer, OutputFormatter, LogSetup, AccessControlGuard, and PaginationHelper per DEV-STORY-001 through DEV-STORY-004, matching the established pattern in DEV-STORY-005 (foundry-datasets).
- **AC-FS-INFRA-RETRY**: Given a transient SDK error (HTTP 429/503) on any filesystem operation, when the operation is invoked, then RetryHandler applies exponential backoff with jitter per ADR-002 and `FOUNDRY_AGENTIC_CLI_RETRY_*` environment variables, logging each retry attempt to stderr as NDJSON per ADR-005.
- **AC-FS-INFRA-ERROR**: Given an SDK exception on any filesystem operation, when it propagates, then ErrorSerializer maps it to the correct exit code (0–9) per ADR-001 and emits a structured JSON error envelope on stdout regardless of the `--format` setting.
- **AC-FS-INFRA-OUTPUT**: Given the `--format json|toon|auto` option or `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT`, when a filesystem operation returns, then OutputFormatter renders JSON or TOON on stdout per the ADR-004 auto-selection algorithm, with pagination metadata emitted to stderr behind the `# ---metadata-start---` separator.
- **AC-FS-INFRA-ACL**: Given access-control environment variables (ENABLED, READONLY, METADATA_ONLY at operation/namespace/global levels), when a filesystem operation is invoked, then AccessControlGuard applies the 8-step precedence model per ADR-007 and returns exit code 8 (AccessControlError) on a blocked operation with a structured JSON error.
- **AC-FS-INFRA-PAGINATION**: Given a paginated filesystem operation (folder children, project organizations, resource markings, resource-role list, space list), when `--page-size`, `--page-token`, or `--batch-pages` is supplied, then PaginationHelper manages defaults, emits next-page-token metadata to stderr, aggregates batch pages, and enforces the max batch-pages limit.
- **AC-FS-INFRA-TRACING**: Given tracing is disabled by default, when `ENABLE_ATTRIBUTION=true` and tracing is enabled, then TracingProvider generates valid W3C trace/span IDs, binds SDK context, and does not leak across concurrent or back-to-back calls.

### Exit Code and Error Contract (ADR-001)

- **AC-FS-EXIT-SUCCESS**: Given a successful filesystem operation, when completed, then exit code is 0 and stdout contains valid JSON or TOON.
- **AC-FS-EXIT-AUTH**: Given an invalid or missing FOUNDRY_TOKEN, when any operation is invoked, then exit code is 2 and stdout contains `{"error": {"type": "AuthenticationError", ...}}`.
- **AC-FS-EXIT-NOTFOUND**: Given a non-existent RID/path, when an operation is invoked, then exit code is 4 and stdout contains the corresponding NotFound error.
- **AC-FS-EXIT-CONFIG**: Given a missing required environment variable, when the CLI starts, then exit code is 9 and stdout contains `{"error": {"type": "ConfigurationError", ...}}`.

### Quality

- **AC-FS-QUALITY-COVERAGE**: Given the test suite targeted at the filesystem skill, when executed, then ≥80% branch coverage is maintained and all targeted filesystem tests pass.
- **AC-FS-QUALITY-LINT-TYPE**: Given the implementation, when `ruff` and `mypy` are run, then no lint or type errors are reported.
- **AC-FS-QUALITY-PATTERN-CONSISTENCY**: Given the implementation, when compared to DEV-STORY-005 (foundry-datasets), then the file layout, parser structure, dispatch table shape, and integration wiring follow the same established namespace-skill pattern.

## Related Documentation

- [SRS-001 — Software Requirements Specification](.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md) — FR-SKILL, FR-ACL, FR-OUT, FR-ERR, FR-PAG, FR-ASYNC, NFR-IFACE, NFR-DIST, NFR-MAINT
- [SAD-001 — Solution Architecture Document](.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md) — §4 Component Diagram, §5 Code Structure, §6 Sequence Diagrams, §10 Phase 2 EPIC-002 roadmap
- [ADR-001 — Exit Code Taxonomy](.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md) — Exit codes 0–9
- [ADR-002 — Call Timeout Defaults](.ept/docs/deliverables/architecture/adr/ADR-002-call-timeout-defaults.md) — Timeout/retry configuration
- [ADR-004 — Format Auto-Selection Algorithm](.ept/docs/deliverables/architecture/adr/ADR-004-format-auto-algorithm.md) — JSON/TOON selection
- [ADR-005 — Log Format](.ept/docs/deliverables/architecture/adr/ADR-005-log-format.md) — NDJSON stderr logging
- [ADR-006 — .env File Search Path](.ept/docs/deliverables/architecture/adr/ADR-006-env-file-search-path.md) — ConfigLoader search path
- [ADR-007 — Operation-Level READONLY Independence](.ept/docs/deliverables/architecture/adr/ADR-007-operation-level-readonly.md) — Per-operation ACL override
- [Canonical Environment Variable Reference](.ept/docs/deliverables/architecture/canonical-env-var-reference.md)
- [Metadata Allow-list](.ept/docs/deliverables/architecture/metadata-allow-list.md)
- SDK source: `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/filesystem/` (Folder, Project, Resource, ResourceRole, Space)
- Pattern reference: DEV-STORY-005 foundry-datasets skill (`.claude/skills/foundry-datasets/`)
- Upstream dependencies: DEV-STORY-001 through DEV-STORY-004 (common infrastructure, all Closed)

## Notes

- Foundry Compass filesystem operations: folders, projects, resources (with markings), resource roles, and spaces. RID and path-based addressing supported.
- `folder.children`, `project.organizations`, `resource.markings`, `resource_role.list`, and `space.list` are paginated endpoint returning ResourceIterator / ListResponse types and require PaginationHelper integration.
- The `Resource.role.add/list/remove` operations are nested under the Resource resource client as `Resource.Role` in the SDK.
- The operation count (31) was verified against the in-repo SDK copy (`foundry_sdk.v2.filesystem`) at triage time.
