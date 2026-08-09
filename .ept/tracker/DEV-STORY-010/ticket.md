---
id: DEV-STORY-010
type: dev_story
title: foundry-audit skill (2 operations)
status: Closed
feature_request: FEATURE-001
epic: EPIC-004
created: 2026-04-13
updated: 2026-08-01
priority: High
resolution: Done
assignee: python-developer
reporter: architect
story_points: 8
release_notes: Added the foundry-audit CLI skill exposing the 2-operation Palantir Foundry Audit API v2 (audit.log_file.list pagination via PaginationHelper; audit.log_file.content bounded binary download via BinaryDownloadHandler, default-BLOCKED in metadata tier). Routes through the nested audit.Organization.LogFile 3-level SDK client chain, with the common-layer AccessControlGuard, RetryHandler, OutputFormatter, and ErrorSerializer. Packaged as the foundry-audit console script under src/foundry_cli/audit/.
---

# DEV-STORY-010: foundry-audit skill (2 operations)

## Description

Generate and validate the 2 `audit` namespace operations exposing the Palantir Foundry Audit API v2 to AI agents via a Claude Code skill. The `audit` namespace is the smallest skill in EPIC-004 (2 operations) and covers audit log file enumeration and binary content retrieval. It reuses the common library established in EPIC-001.

### Authoritative operation catalog (2 operations)

Sourced from the SDK source (`foundry_sdk/v2/audit/`), the Canonical Env Var Reference, and the Metadata Allow-list:

| # | SDK Path | SDK Method | HTTP | Returns | ACL Tier-3 | Attribution (FR-ATTR-4) |
|---|---|---|---|---|---|---|
| 1 | `audit.log_file.list` | `Organization.LogFile.list` | GET `/v2/audit/organizations/{organizationRid}/logFiles` | `ResourceIterator[LogFile]` (paged) | PERMITTED | Not required |
| 2 | `audit.log_file.content` | `Organization.LogFile.content` | GET `/v2/audit/organizations/{organizationRid}/logFiles/{logFileId}/content` | `bytes` (octet-stream) | BLOCKED | Not required |

SDK client routing is nested: root client `.audit` (AuditClient) exposes an `Organization` sub-client (OrganizationClient), which in turn exposes the `LogFile` sub-client (LogFileClient). This nested pattern is structurally identical to the filesystem `Resource.Role` routing solved in DEV-STORY-006.

## Acceptance Criteria

### AC-1: Operation catalog completeness
- **Given** the `foundry-audit` skill is installed under `.claude/skills/foundry-audit/`
- **When** the skill's operation catalog is inspected
- **Then** exactly the 2 operations listed above are exposed, no more and no less, each mapping to its documented SDK path

### AC-2: Nested SDK client routing
- **Given** the audit namespace uses a nested sub-client chain (`audit.Organization.LogFile`)
- **When** the CLI entry point dispatches an `audit log_file <operation>` command
- **Then** the dispatcher resolves the three-level client path correctly and reaches `LogFileClient.list` / `LogFileClient.content` without intermediate attribute errors

### AC-3: Access control precedence (SRS §4.2, 8-step model)
- **Given** the 8-step `AccessControlGuard` precedence model
- **When** any of the 2 operations is invoked
- **Then** the operation is evaluated against global -> namespace -> operation controls (`FOUNDRY_AGENTIC_CLI_AUDIT_ENABLED`, `_READONLY`, `_METADATA_ONLY`, and per-operation `_ENABLED`/`_READONLY`) and returns exit code 8 when a control denies access, with the denying rule emitted to stderr

### AC-4: Metadata-only tier enforcement (Metadata Allow-list)
- **Given** `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` (Tier-3)
- **When** `audit.log_file.content` is invoked
- **Then** the call is BLOCKED (binary/content excluded from metadata tier) and a structured access-denied error is returned with exit code 8
- **And When** `audit.log_file.list` is invoked
- **Then** the call is PERMITTED and returns the list of LogFile descriptors (metadata only)

### AC-5: Pagination for log_file.list (ADR-005)
- **Given** `audit.log_file.list` is a paged endpoint returning `ListLogFilesResponse` with `nextPageToken`
- **When** the operation is invoked
- **Then** the `PaginationHelper` manages `page_size` / `page_token` / `batch-pages`, emits pagination metadata to stderr (per ADR-005), and iterates across pages when `start_date` is supplied
- **And When** `start_date` is omitted on the initial request (no `page_token`)
- **Then** the SDK `MissingStartDate` error is mapped by `ErrorSerializer` to the ADR-001 exit-code taxonomy

### AC-6: Binary content handling for log_file.content
- **Given** `audit.log_file.content` returns an `application/octet-stream` byte payload
- **When** the operation is permitted (Tier-3 BLOCKED overridden by explicit enable) and invoked
- **Then** the `BinaryDownloadHandler` streams the bounded byte response to the configured output sink with integrity and size guards matching DEV-STORY-004 patterns
- **And** access to this operation remains default-BLOCKED unless explicitly enabled via `FOUNDRY_AGENTIC_CLI_AUDIT_LOG_FILE_CONTENT_ENABLED`

### AC-7: Attribution NOT applied (FR-ATTR-4)
- **Given** attribution is enabled (`FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION=true`)
- **When** either audit operation is invoked
- **Then** NO attribution headers are injected, because FR-ATTR-4 scope (`functions.query.*`, `ontologies.query.*`, `media_sets.media_set.*`, `language_models.*`) excludes the audit namespace

### AC-8: Retry, timeout, and error serialization (ADR-001, ADR-002)
- **Given** a transient failure occurs on either operation
- **When** the `RetryHandler` exhausts the configured attempts (default 4 total)
- **Then** the final error is mapped to the ADR-001 exit-code taxonomy via `ErrorSerializer` and emitted as structured output
- **And** permission errors (`GetLogFileContentPermissionDenied`, `ListLogFilesPermissionDenied`) map deterministically without retry

### AC-9: SDK-native B3 propagation

Given tracing is disabled, when either audit operation runs, then the CLI does not set B3 context and emits no generated B3 headers. Given tracing is enabled, when either audit operation invokes the Foundry SDK, then the outbound request contains valid X-B3-TraceId, X-B3-SpanId, and X-B3-Sampled headers. Given a retry occurs, when another attempt is sent, then every attempt uses the same B3 context. Given the invocation completes or fails, then prior SDK context values are restored. The CLI must not claim or emit W3C traceparent or tracestate support.

### AC-10: Parser, dispatch, and entry point
- **Given** the CLI entry point `foundry_audit_cli.py` with a packaged console script `foundry-audit`
- **When** a user invokes `audit log_file <operation> [flags]`
- **Then** the parser routes to the correct nested SDK method, applies the common-layer guards, and returns a deterministic exit code

## Related Documentation

- `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md` — EPIC-004 scope; DEV-STORY-010 entry (Phase 3 roadmap)
- `.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md` — §4.2 FR-ACL (8-step access control); FR-ATTR-4 (attribution scope — audit excluded)
- `.ept/docs/deliverables/architecture/canonical-env-var-reference.md` — Namespace `audit` operation table (2 rows); env vars `FOUNDRY_AGENTIC_CLI_AUDIT_LOG_FILE_CONTENT_*`, `FOUNDRY_AGENTIC_CLI_AUDIT_LOG_FILE_LIST_*`
- `.ept/docs/deliverables/architecture/metadata-allow-list.md` — `audit` namespace classification (1 PERMITTED: `log_file.list`; 1 BLOCKED: `log_file.content`)
- `.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md` — Exit-code mapping
- `.ept/docs/deliverables/architecture/adr/ADR-002-call-timeout-defaults.md` — Retry/timeout defaults
- `.ept/docs/deliverables/architecture/adr/ADR-004-format-auto-algorithm.md` — JSON/TOON auto-selection
- `.ept/docs/deliverables/architecture/adr/ADR-005-log-format.md` — NDJSON stderr logging
- `.ept/docs/deliverables/architecture/adr/ADR-007-operation-level-readonly.md` — Operation-level readonly independence
- `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/audit/` — SDK source (log_file.py, organization.py, _client.py, models.py, errors.py)
- Parent EPIC-004 — Admin & Security Skills combined scope (DEV-STORY-009 + DEV-STORY-010)
- Reference implementation DEV-STORY-006 (foundry-filesystem) — nested `Resource.Role` client routing pattern

## Technical Scope

- **Namespace:** `audit` (2 operations)
- **SDK classes:** `LogFile` (2 ops) accessed via nested `audit.Organization.LogFile` dispatch
- **Common-layer integration:** reuses `AccessControlGuard`, `RetryHandler`, `OutputFormatter`, `ErrorSerializer`, `LogSetup`, `TracingProvider`, `PaginationHelper`, and `BinaryDownloadHandler` from `src/foundry_cli/common/`
- **Paged operation:** `audit.log_file.list` requires `PaginationHelper` (page_size/page_token/batch-pages; `start_date` required)
- **Binary operation:** `audit.log_file.content` requires `BinaryDownloadHandler` (bounded octet-stream)
- **Attribution:** NOT applicable (audit is outside the FR-ATTR-4 scope)
- **Deployment target:** `.claude/skills/foundry-audit/` with CLI entry `src/foundry_cli/audit/scripts/foundry_audit_cli.py`
- **Follows the EPIC-001 common pattern** established by `foundry-datasets` / `foundry-ontologies`; nested-client routing per the `foundry-filesystem` (DEV-STORY-006) precedent

When FOUNDRY_AGENTIC_CLI_ENABLE_TRACING=true, the audit CLI must enter AsyncClientFactory.invocation_scope(cfg) before constructing AsyncFoundryClient and keep that scope active through all retry attempts. The Foundry SDK must emit X-B3-TraceId, X-B3-SpanId, and X-B3-Sampled on outbound requests. W3C traceparent and tracestate are not supported by this story.

## Notes

Sibling skill DEV-STORY-009 (`foundry-admin`) is Resolved. EPIC-004 combined scope is 68 operations (66 admin + 2 audit). The audit skill is the smallest in the project and represents low implementation risk.
