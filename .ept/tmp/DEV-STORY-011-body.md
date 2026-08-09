# DEV-STORY-011: foundry-aip-agents skill (15 operations + session management)

## Description

Generate and validate all `aip_agents` namespace operations exposing the Palantir Foundry AIP Agents API v2 to AI agents via a subprocess-invocable CLI skill. Covers conversation session lifecycle (create/get/list/delete/continue/cancel/trace), agent descriptor retrieval, and version listing. The skill integrates with the `SessionManager` (`src/foundry_cli/common/session_manager.py`) for atomic local persistence of AIP agent session RIDs, and reuses the common library established in EPIC-001.

**Scope correction:** The ticket title referenced "13 operations", but authoritative cross-validation across three independent sources (SDK source, Canonical Env Var Reference, Metadata Allow-list) confirms **15 operations**. The 2-operation delta is `session.update_title` and `session_trace.get`, both present in all three sources.

### Authoritative operation catalog (15 operations)

Sourced from the Canonical Env Var Reference and the Metadata Allow-list (both rows identical to the SDK `foundry_sdk/v2/aip_agents/` module tree):

| # | SDK Path | SDK Accessor | HTTP | Return Type | ACL Tier-3 | Notes |
|---|---|---|---|---|---|---|
| 1 | `aip_agents.agent.all_sessions` | `Agent.all_sessions` | GET | `ResourceIterator[Session]` (paged) | BLOCKED | Paged; needs PaginationHelper |
| 2 | `aip_agents.agent.get` | `Agent.get` | GET | `Agent` | PERMITTED | Metadata descriptor |
| 3 | `aip_agents.agent_version.get` | `Agent.AgentVersion.get` | GET | `AgentVersion` | PERMITTED | Metadata descriptor |
| 4 | `aip_agents.agent_version.list` | `Agent.AgentVersion.list` | GET | `ResourceIterator[AgentVersion]` (paged) | PERMITTED | Paged; needs PaginationHelper |
| 5 | `aip_agents.content.get` | `Session.Content.get` | GET | `Content` | BLOCKED | Response data content |
| 6 | `aip_agents.session.blocking_continue` | `Session.blocking_continue` | POST | `SessionExchangeResult` | BLOCKED | AI execution; mutable |
| 7 | `aip_agents.session.cancel` | `Session.cancel` | POST | `CancelSessionResponse` | BLOCKED | Cancels in-progress stream; mutable |
| 8 | `aip_agents.session.create` | `Session.create` | POST | `Session` | BLOCKED | Mutator; integrates SessionManager |
| 9 | `aip_agents.session.delete` | `Session.delete` | DELETE | `None` | BLOCKED | Mutator; clears local alias |
| 10 | `aip_agents.session.get` | `Session.get` | GET | `Session` | PERMITTED | Metadata descriptor |
| 11 | `aip_agents.session.list` | `Session.list` | GET | `ResourceIterator[Session]` (paged) | PERMITTED | Paged; needs PaginationHelper |
| 12 | `aip_agents.session.rag_context` | `Session.rag_context` | PUT | `AgentSessionRagContextResponse` | BLOCKED | Retrieval execution |
| 13 | `aip_agents.session.streaming_continue` | `Session.streaming_continue` | POST | `bytes` (octet-stream) | BLOCKED | Streaming; needs BinaryDownloadHandler |
| 14 | `aip_agents.session.update_title` | `Session.update_title` | PUT | `None` | BLOCKED | Mutator |
| 15 | `aip_agents.session_trace.get` | `Session.SessionTrace.get` | GET | `SessionTrace` | PERMITTED | Metadata descriptor |

**Nested SDK routing** (mirrors the `Resource.Role` pattern proven in DEV-STORY-006):
- `Agent` → `Agent.AgentVersion` (2-level chain)
- `Agent.Session` (2-level chain, the per-agent session client)
- `Session.Content` (3-level chain: `Agent.Session.Content`)
- `Session.SessionTrace` (3-level chain: `Agent.Session.SessionTrace`)

**Attribution (FR-ATTR-4):** Scope is `functions.query.*`, `ontologies.query.*`, `media_sets.media_set.*`, `language_models.*`. The `aip_agents` namespace is **explicitly NOT** in the attribution scope — no `aip_agents.*` operation injects attribution headers.

## Acceptance Criteria

### AC-1: Operation catalog completeness
- **Given** the `foundry-aip-agents` skill is installed under `.claude/skills/foundry-aip-agents/`
- **When** the skill's operation catalog is inspected
- **Then** exactly the 15 operations listed above are exposed, no more and no less, each mapping to its documented SDK path through the correct nested accessor chain

### AC-2: Access control precedence (SRS §4.2, 8-step model)
- **Given** the 8-step `AccessControlGuard` precedence model
- **When** any of the 15 operations is invoked
- **Then** the operation is evaluated against global → namespace → operation controls (`_ENABLED`, `_READONLY`, `_METADATA_ONLY`) and returns exit code 8 when a control denies access, with the denying rule emitted to stderr

### AC-3: Metadata-only tier enforcement (Metadata Allow-list)
- **Given** `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` (Tier-3)
- **When** any BLOCKED operation (ops 1, 5, 6, 7, 8, 9, 12, 13, 14) is invoked
- **Then** the call returns a structured access-denied error with exit code 8
- **And When** any PERMITTED descriptor operation (ops 2, 3, 4, 10, 11, 15) is invoked
- **Then** the call is PERMITTED and returns resource descriptors / metadata

### AC-4: Attribution exemption (FR-ATTR-4)
- **Given** attribution is enabled (`FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION=true`)
- **When** any `aip_agents.*` operation is invoked
- **Then** NO attribution header is injected, because the `aip_agents` namespace is outside the FR-ATTR-4 scope (`functions.query.*`, `ontologies.query.*`, `media_sets.media_set.*`, `language_models.*`)

### AC-5: SessionManager integration (session create/delete lifecycle)
- **Given** the `SessionManager` (`src/foundry_cli/common/session_manager.py`)
- **When** `aip_agents.session.create` succeeds
- **Then** the resulting `Session` RID + agent RID are atomically persisted to local state with an alias, and meaningful `tool_history` entries are appended across continues
- **And When** `aip_agents.session.delete` succeeds
- **Then** the alias is removed from local state and the lock is released
- **And** a session-persistence failure (remote OK / local write fails) returns exit code 6 (`SessionPersistenceError`) without leaving orphan state

### AC-6: Pagination (operations 1, 4, 11)
- **Given** the paged `ResourceIterator`-returning operations (`agent.all_sessions`, `agent_version.list`, `session.list`)
- **When** page size / page token flags are supplied
- **Then** the `PaginationHelper` drives iteration and emits page metadata to stderr

### AC-7: Binary streaming (operation 13)
- **Given** `aip_agents.session.streaming_continue` returns `bytes` (octet-stream)
- **When** the operation is invoked
- **Then** the `BinaryDownloadHandler` writes the streamed Agent response to the configured output path with bounded streaming per DESIGN-005

### AC-8: Retry, timeout, and error serialization (ADR-001, ADR-002)
- **Given** a transient failure (e.g., `RateLimitExceeded`, `RetryAttemptsExceeded`, `RetryDeadlineExceeded`) occurs on any of the 15 operations
- **When** the `RetryHandler` exhausts the configured attempts
- **Then** the final error is mapped to the ADR-001 exit-code taxonomy via `ErrorSerializer` (including the rich aip_agents-specific throwable errors such as `AgentNotFound`, `SessionNotFound`, `SessionExecutionFailed`, `ContextSizeExceededLimit`)

### AC-9: Output format (ADR-004)
- **Given** the response shape from a descriptor operation (`agent.get`, `session.get`, etc.)
- **When** `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT=auto`
- **Then** the `OutputFormatter` selects JSON for single-resource responses and TOON for tabular/aggregated responses

### AC-10: Structured logging and tracing (ADR-005)
- **Given** any operation is executed
- **When** logging is emitted
- **Then** NDJSON structured logs are written to stderr including operation, status, latency, and (when enabled) B3/W3C trace propagation headers

### AC-11: Parser and dispatch
- **Given** the CLI entry point `foundry_aip_agents_cli.py`
- **When** a user invokes `aip-agents <class> <operation> [flags]`
- **Then** the parser routes to the correct SDK method through the nested accessor chain, applies the common-layer guards (incl. SessionManager for create/delete), and returns a deterministic exit code

## Related Documentation

- `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md` — EPIC-005 scope, DEV-STORY-011 entry (implementation roadmap)
- `.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md` — §2.2 Product Functions; §4.2 FR-ACL (8-step access control); FR-ATTR-4 (attribution scope — `aip_agents` excluded)
- `.ept/docs/deliverables/architecture/canonical-env-var-reference.md` — Namespace `aip_agents` operation table (15 rows, authoritative source)
- `.ept/docs/deliverables/architecture/metadata-allow-list.md` — `aip_agents` namespace classification (6 PERMITTED, 9 BLOCKED)
- `.ept/docs/deliverables/architecture/DESIGN-005-common-components.md` — `SessionManager`, `BinaryDownloadHandler`, `TracingProvider` contracts
- `.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md` — Exit-code mapping
- `.ept/docs/deliverables/architecture/adr/ADR-002-call-timeout-defaults.md` — Retry/timeout defaults
- `.ept/docs/deliverables/architecture/adr/ADR-004-format-auto-algorithm.md` — JSON/TOON auto-selection
- `.ept/docs/deliverables/architecture/adr/ADR-005-log-format.md` — NDJSON stderr logging
- `.ept/docs/deliverables/architecture/adr/ADR-007-operation-level-readonly.md` — Operation-level readonly independence
- `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/aip_agents/` — SDK source (`_client.py`, `agent.py`, `agent_version.py`, `session.py`, `content.py`, `session_trace.py`, `errors.py`, `models.py`)
- `src/foundry_cli/common/session_manager.py` — Session persistence layer to be integrated by `session.create`/`session.delete`
- Parent EPIC-005 (AI & Models Skills) — combined scope (DEV-STORY-011 aip-agents + DEV-STORY-012 language-models + DEV-STORY-013 models)

## Technical Scope

- **Namespace:** `aip_agents` (15 operations)
- **SDK classes (nested):** `Agent` (2 ops) + `Agent.AgentVersion` (2 ops) + `Session` aka `Agent.Session` (9 ops) + `Session.Content` (1 op) + `Session.SessionTrace` (1 op). 4 SDK client files, 1 nested dispatcher input.
- **Common-layer integration:** reuses `AccessControlGuard`, `RetryHandler`, `OutputFormatter`, `ErrorSerializer`, `LogSetup`, `TracingProvider`, `PaginationHelper`, `BinaryDownloadHandler`, and `SessionManager` from `src/foundry_cli/common/`
- **Pagination:** 3 paged operations (ops 1, 4, 11) → `PaginationHelper` required
- **Binary streaming:** 1 `bytes` operation (op 13 `streaming_continue`) → `BinaryDownloadHandler` required (octet-stream)
- **SessionManager integration:** `session.create` writes a local alias; `session.delete` removes it; `session.blocking_continue`/`session.streaming_continue`/`session.cancel` update `tool_history`; this is the primary stateful integration point of the namespace
- **Attribution:** NOT applicable to any `aip_agents.*` operation (outside FR-ATTR-4 scope)
- **AI-execution class:** `blocking_continue`, `streaming_continue`, `cancel`, `rag_context` are AI/computation operations → BLOCKED under metadata-only tier
- **Write/mutator class:** `create`, `delete`, `update_title`, `cancel` mutate state → require `_READONLY=false` override to be invoked
- **Deployment target:** `.claude/skills/foundry-aip-agents/` with CLI entry `src/foundry_cli/aip_agents/scripts/foundry_aip_agents_cli.py` (following the `OP_SPECS` + `_get_client` nested dispatcher pattern from DEV-STORY-006/008)
- **Follows the EPIC-001 common pattern** established by `foundry-datasets` and `foundry-ontologies`

## Notes

Sibling skills DEV-STORY-007 (`foundry-ontologies`) and DEV-STORY-006 (`foundry-filesystem`) are Closed and serve as the reference implementation for the nested-sub-client dispatcher pattern. EPIC-005 combined scope covers DEV-STORY-011 (aip-agents, 15 ops) + DEV-STORY-012 (language-models, 2 ops) + DEV-STORY-013 (models, 23 ops). The "13 operations" in the original title is stale; 15 is the authoritative count.
