---
id: DEV-STORY-008
type: dev_story
title: foundry-functions skill (7 operations)
status: Closed
feature_request: FEATURE-001
epic: EPIC-003
created: 2026-04-13
updated: 2026-07-29
priority: High
resolution: Done
assignee: architect
reporter: architect
release_notes: 'Adds the foundry-functions skill exposing all 7 Functions API v2 operations across
  3 SDK classes (query: execute, get, get_by_rid, get_by_rid_batch, streaming_execute;
  value_type.get; version_id.get) as a subprocess-invocable CLI that reuses the EPIC-001
  common library (AccessControlGuard, RetryHandler, OutputFormatter, ErrorSerializer,
  LogSetup, TracingProvider). Attribution headers are injected on the 5 functions.query.*
  operations per FR-ATTR-4 when FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION=true; value_type
  and version_id operations are exempt. Under the metadata-only tier, query.execute
  and query.streaming_execute are blocked (computation), while the 5 descriptor operations
  are permitted.'
---

# DEV-STORY-008: foundry-functions skill (7 operations)

## Description

Generate and validate all 7 `functions` namespace operations exposing the Palantir Foundry Functions API v2 to AI agents via a Claude Code skill. Covers function/query versioning, descriptor retrieval, and query execution. The `functions` namespace is the smallest EPIC-003 skill (7 operations across 3 SDK classes: `query`, `value_type`, `version_id`) and reuses the common library established in EPIC-001.

### Authoritative operation catalog (7 operations)

Sourced from the Canonical Env Var Reference and the Metadata Allow-list:

| # | SDK Path | Class | ACL Tier-3 | Attribution (FR-ATTR-4) |
|---|---|---|---|---|
| 1 | `functions.query.execute` | query | BLOCKED (computation) | Required |
| 2 | `functions.query.get` | query | PERMITTED | Required |
| 3 | `functions.query.get_by_rid` | query | PERMITTED | Required |
| 4 | `functions.query.get_by_rid_batch` | query | PERMITTED | Required |
| 5 | `functions.query.streaming_execute` | query | BLOCKED (computation) | Required |
| 6 | `functions.value_type.get` | value_type | PERMITTED | Not required |
| 7 | `functions.version_id.get` | version_id | PERMITTED | Not required |

## Acceptance Criteria

### AC-1: Operation catalog completeness
- **Given** the `foundry-functions` skill is installed under `.claude/skills/foundry-functions/`
- **When** the skill's operation catalog is inspected
- **Then** exactly the 7 operations listed above are exposed, no more and no less, each mapping to its documented SDK path

### AC-2: Access control precedence (SRS §4.2, 8-step model)
- **Given** the 8-step `AccessControlGuard` precedence model
- **When** any of the 7 operations is invoked
- **Then** the operation is evaluated against global → namespace → operation controls (`_ENABLED`, `_READONLY`, `_METADATA_ONLY`) and returns exit code 8 when a control denies access, with the denying rule emitted to stderr

### AC-3: Metadata-only tier enforcement (Metadata Allow-list)
- **Given** `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` (Tier-3)
- **When** `functions.query.execute` or `functions.query.streaming_execute` is invoked
- **Then** the call is BLOCKED (computation/execution excluded from metadata tier) and a structured access-denied error is returned
- **And When** one of `functions.query.get`, `functions.query.get_by_rid`, `functions.query.get_by_rid_batch`, `functions.value_type.get`, or `functions.version_id.get` is invoked
- **Then** the call is PERMITTED and returns resource descriptors

### AC-4: Attribution injection (FR-ATTR-4)
- **Given** attribution is enabled (`FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION=true`)
- **When** any `functions.query.*` operation is invoked (operations 1–5)
- **Then** the configured attribution RIDs are injected into the request headers
- **And** `functions.value_type.*` and `functions.version_id.*` operations do NOT receive attribution

### AC-5: Retry, timeout, and error serialization (ADR-001, ADR-002)
- **Given** a transient failure occurs on any of the 7 operations
- **When** the `RetryHandler` exhausts the configured attempts (default 4 total)
- **Then** the final error is mapped to the ADR-001 exit-code taxonomy via `ErrorSerializer` and emitted as structured output

### AC-6: Output format (ADR-004)
- **Given** the response shape from a descriptor operation (`get`, `get_by_rid`, etc.)
- **When** `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT=auto`
- **Then** the `OutputFormatter` selects JSON for single-resource responses and TOON for tabular/batch responses (`get_by_rid_batch`)

### AC-7: Structured logging and tracing (ADR-005)
- **Given** any operation is executed
- **When** logging is emitted
- **Then** NDJSON structured logs are written to stderr including operation, status, latency, and (when enabled) B3/W3C trace propagation headers

### AC-8: Parser and dispatch
- **Given** the CLI entry point `foundry_functions_cli.py`
- **When** a user invokes `functions <class> <operation> [flags]`
- **Then** the parser routes to the correct SDK method, applies the common-layer guards, and returns a deterministic exit code

## Related Documentation

- `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md` — EPIC-003 scope, DEV-STORY-008 entry (§Phase 2 roadmap)
- `.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md` — §2.2 Product Functions; §4.2 FR-ACL (8-step access control); FR-ATTR-4 (attribution on `functions.query.*`)
- `.ept/docs/deliverables/architecture/canonical-env-var-reference.md` — Namespace `functions` operation table (7 rows, authoritative source)
- `.ept/docs/deliverables/architecture/metadata-allow-list.md` — `functions` namespace classification (5 PERMITTED, 2 BLOCKED)
- `.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md` — Exit-code mapping
- `.ept/docs/deliverables/architecture/adr/ADR-002-call-timeout-defaults.md` — Retry/timeout defaults
- `.ept/docs/deliverables/architecture/adr/ADR-004-format-auto-algorithm.md` — JSON/TOON auto-selection
- `.ept/docs/deliverables/architecture/adr/ADR-005-log-format.md` — NDJSON stderr logging
- `.ept/docs/deliverables/architecture/adr/ADR-007-operation-level-readonly.md` — Operation-level readonly independence
- Parent EPIC-003 — combined scope and acceptance criteria for both EPIC-003 skills

## Technical Scope

- **Namespace:** `functions` (7 operations)
- **SDK classes:** `query` (5 ops), `value_type` (1 op), `version_id` (1 op)
- **Common-layer integration:** reuses `AccessControlGuard`, `RetryHandler`, `OutputFormatter`, `ErrorSerializer`, `LogSetup`, `TracingProvider` from `src/foundry_cli/common/`
- **No list operations** → `PaginationHelper` is not required for this skill
- **No binary content operations** → `BinaryDownloadHandler` is not required
- **Computation operations:** `functions.query.execute` and `functions.query.streaming_execute` are blocked under the metadata-only tier and require attribution
- **Deployment target:** `.claude/skills/foundry-functions/` with CLI entry `src/foundry_cli/functions/scripts/foundry_functions_cli.py`
- **Follows the EPIC-001 common pattern** established by `foundry-datasets` and `foundry-ontologies`

## Notes

Sibling skill DEV-STORY-007 (`foundry-ontologies`) is Closed and serves as the reference implementation for the common-layer pattern. EPIC-003 combined scope is 74 operations (67 ontology + 7 functions).
