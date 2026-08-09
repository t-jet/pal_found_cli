---
id: DEV-STORY-011
type: dev_story
title: foundry-aip-agents skill (13 operations + session management)
status: Closed
feature_request: FEATURE-001
epic: EPIC-005
created: 2026-04-13
updated: 2026-08-09
priority: High
resolution: Done
assignee: architect
reporter: architect
story_points: 13
release_notes: Adds the foundry-aip-agents CLI and Claude skill with all 15 AIP Agents v2 operations. The skill supports paginated agent and session queries, local aliases for multi-turn sessions, seven-day session cleanup and purge, bounded persistence for streaming responses, three-tier access controls, retries, structured output and errors, and opt-in SDK-native B3 tracing.
---

# DEV-STORY-011: foundry-aip-agents skill (15 SDK operations plus session management)

## Description

Implement and validate the `foundry-aip-agents` Claude Code skill for all 15 public operations in `foundry_sdk.v2.aip_agents`. The CLI must support agent inspection, agent-version lookup, stateful conversations, session content and trace retrieval, and local alias-based session management. It reuses the common components completed under EPIC-001.

### Authoritative operation catalog

The SDK source, Canonical Environment Variable Reference, and Metadata Allow-list each define the same 15 operations. SDK signatures below omit the internal-only `_sdk_internal` parameter. `preview` and `request_timeout` remain optional for every SDK operation.

| # | CLI route and SDK path | Public SDK signature | Return | HTTP | Tier 3 |
|---|---|---|---|---|---|
| 1 | `agent all-sessions` → `aip_agents.agent.all_sessions` | `all_sessions(*, page_size=None, page_token=None, preview=None, request_timeout=None)` | `ResourceIterator[Session]` | GET | BLOCKED |
| 2 | `agent get` → `aip_agents.agent.get` | `get(agent_rid, *, preview=None, version=None, request_timeout=None)` | `Agent` | GET | PERMITTED |
| 3 | `agent-version get` → `aip_agents.agent_version.get` | `get(agent_rid, agent_version_string, *, preview=None, request_timeout=None)` | `AgentVersion` | GET | PERMITTED |
| 4 | `agent-version list` → `aip_agents.agent_version.list` | `list(agent_rid, *, page_size=None, page_token=None, preview=None, request_timeout=None)` | `ResourceIterator[AgentVersion]` | GET | PERMITTED |
| 5 | `session blocking-continue` → `aip_agents.session.blocking_continue` | `blocking_continue(agent_rid, session_rid, *, parameter_inputs, user_input, contexts_override=None, preview=None, session_trace_id=None, request_timeout=None)` | `SessionExchangeResult` | POST | BLOCKED |
| 6 | `session cancel` → `aip_agents.session.cancel` | `cancel(agent_rid, session_rid, *, message_id, preview=None, response=None, request_timeout=None)` | `CancelSessionResponse` | POST | BLOCKED |
| 7 | `session create` → `aip_agents.session.create` | `create(agent_rid, *, agent_version=None, preview=None, request_timeout=None)` | `Session` | POST | BLOCKED |
| 8 | `session delete` → `aip_agents.session.delete` | `delete(agent_rid, session_rid, *, preview=None, request_timeout=None)` | `None` | DELETE | BLOCKED |
| 9 | `session get` → `aip_agents.session.get` | `get(agent_rid, session_rid, *, preview=None, request_timeout=None)` | `Session` | GET | PERMITTED |
| 10 | `session list` → `aip_agents.session.list` | `list(agent_rid, *, page_size=None, page_token=None, preview=None, request_timeout=None)` | `ResourceIterator[Session]` | GET | PERMITTED |
| 11 | `session rag-context` → `aip_agents.session.rag_context` | `rag_context(agent_rid, session_rid, *, parameter_inputs, user_input, preview=None, request_timeout=None)` | `AgentSessionRagContextResponse` | PUT | BLOCKED |
| 12 | `session streaming-continue` → `aip_agents.session.streaming_continue` | `streaming_continue(agent_rid, session_rid, *, parameter_inputs, user_input, contexts_override=None, message_id=None, preview=None, session_trace_id=None, request_timeout=None)` | `bytes` (`application/octet-stream`) | POST | BLOCKED |
| 13 | `session update-title` → `aip_agents.session.update_title` | `update_title(agent_rid, session_rid, *, title, preview=None, request_timeout=None)` | `None` | PUT | BLOCKED |
| 14 | `content get` → `aip_agents.content.get` | `get(agent_rid, session_rid, *, preview=None, request_timeout=None)` | `Content` | GET | BLOCKED |
| 15 | `session-trace get` → `aip_agents.session_trace.get` | `get(agent_rid, session_rid, session_trace_id, *, preview=None, request_timeout=None)` | `SessionTrace` | GET | PERMITTED |

SDK routing is nested: `aip_agents.Agent`, `aip_agents.Agent.AgentVersion`, `aip_agents.Agent.Session`, `aip_agents.Agent.Session.Content`, and `aip_agents.Agent.Session.SessionTrace`. The CLI exposes kebab-case resource and operation names while preserving exact SDK parameter names as kebab-case flags. Structured request values use validated JSON arguments. The local `session purge` command is required session management, not a sixteenth SDK operation.

## Acceptance Criteria

### AC-1: Complete catalog and nested dispatch

- **Given** the `foundry-aip-agents` skill is installed
- **When** its parser and operation registry are inspected
- **Then** it exposes exactly the 15 SDK operations in the catalog, no more and no less
- **And** each route resolves the correct nested async SDK client and method

### AC-2: Exact argument contract

- **Given** any cataloged route
- **When** required positional values, optional flags, or JSON request values are supplied
- **Then** the CLI validates them and calls the matching SDK method with the cataloged public signature
- **And** `parameter_inputs`, `user_input`, and `contexts_override` accept validated JSON values of the documented SDK shapes
- **And** optional `response` accepts a scalar `AgentMarkdownResponse`/string through `--response` and is forwarded unchanged; `--response-json` is not exposed, and no object or array validation is applied
- **And** `_sdk_internal` is never exposed as a CLI argument

### AC-3: Access control and metadata-only policy

- **Given** the SRS eight-step access-control precedence model
- **When** any AIP Agents operation runs
- **Then** the CLI evaluates global, `aip_agents` namespace, and per-operation controls before client creation, SDK calls, or operation-specific filesystem changes
- **And** a denial returns ADR-001 exit code 8 with a structured `AccessControlError`
- **And** Tier 3 permits only `agent.get`, `agent_version.get`, `agent_version.list`, `session.get`, `session.list`, and `session_trace.get`
- **And** Tier 3 blocks the other nine operations exactly as the Metadata Allow-list specifies

### AC-4: Pagination

- **Given** `agent all-sessions`, `agent-version list`, or `session list`
- **When** the operation is invoked with `--page-size`, `--page-token`, or `--batch-pages`
- **Then** `PaginationHelper` returns the first page by default, retrieves at most the requested bounded page count, and caps `--batch-pages` at 40
- **And** stdout contains aggregated records while stderr contains ADR-005 pagination metadata and the next token

### AC-5: Alias-backed session creation

- **Given** a valid `--alias` and `agent_rid`
- **When** `session create` succeeds remotely
- **Then** `SessionManager` atomically persists `Session.rid` as `session_id`, the agent RID, null `session_token`, timestamps, active status, and empty tool history under `.foundry-data/sessions/`
- **And** aliases follow DESIGN-005 normalization and locking rules
- **And** an active alias collision returns `SessionAliasConflictError` without creating a second remote session
- **And** a local persistence failure attempts one compensating remote delete and preserves the original error

### AC-6: Alias-backed continuation and lifecycle

- **Given** an active persisted alias
- **When** `session blocking-continue`, `cancel`, `delete`, `get`, `rag-context`, `streaming-continue`, `update-title`, `content get`, or `session-trace get` is invoked with that alias
- **Then** the CLI loads `agent_rid` and `session_id` from `SessionManager` and passes them to the exact SDK signature
- **And** it updates `last_used_at` and appends a secret-free outcome to `tool_history`
- **And** successful deletion marks the local state completed
- **And** continuation requests for one session are not run concurrently

### AC-7: Cleanup and purge

- **Given** local session state exists
- **When** any CLI command starts
- **Then** expired records older than seven days are cleaned up under alias locks and locked records are skipped with an NDJSON warning
- **And When** `session purge` is invoked
- **Then** all unlocked local session records are removed, the deleted count is returned, and no remote delete is implied
- **And** more than five active sessions for one Foundry agent produces a warning but does not block creation

### AC-8: Bounded streaming response

- **Given** `session streaming-continue` returns `application/octet-stream` bytes
- **When** the response is handled
- **Then** `BinaryDownloadHandler` applies the configured size limit, writes through a temporary file, publishes atomically, reads no more than one probe byte past the limit, and emits the SRS FR-DL JSON envelope
- **And** cancellation or stream failure leaves no published or temporary file

### AC-9: Output, errors, retry, and timeout

- **Given** any non-binary operation succeeds
- **When** output format is `auto`
- **Then** `OutputFormatter` uses JSON for objects and empty or heterogeneous lists, and TOON only for uniform non-empty record lists
- **And** results are written to stdout while logs and pagination metadata remain on stderr
- **Given** a retryable 429 or 503, timeout, authentication failure, permission failure, invalid input, or cancellation
- **When** handling completes
- **Then** retry, timeout, structured error output, and exit codes follow ADR-001 and ADR-002 without leaking tokens, request bodies, response content, or session tokens

### AC-10: SDK-native B3 tracing

- **Given** tracing is disabled
- **When** an operation runs
- **Then** SDK trace context remains unchanged
- **Given** tracing is enabled
- **When** the CLI constructs the async client and sends one or more retry attempts
- **Then** the same valid `X-B3-TraceId`, `X-B3-SpanId`, and `X-B3-Sampled` values reach every outbound attempt
- **And** prior SDK context is restored on success, failure, timeout, or cancellation
- **And** the skill does not claim or emit W3C `traceparent` or `tracestate` support

### AC-11: Attribution exclusion

- **Given** attribution is enabled globally
- **When** any AIP Agents operation runs
- **Then** no attribution header is injected because SRS FR-ATTR-4 does not include the `aip_agents` namespace

### AC-12: Packaging and regression safety

- **Given** the implementation is complete
- **When** tests and package checks run on Python 3.11 and 3.12
- **Then** parser, dispatch, all 15 operations, three paged routes, Tier-3 classification, session locking and persistence, bounded byte handling, B3 transport headers, cancellation, error mapping, console entry, and Claude launcher are covered
- **And** the repository lint, type, security, package, and branch-coverage gates pass without regressing existing namespace CLIs

## Related Documentation

- `.ept/docs/document_index.md`
- `.ept/docs/customer_input/task_description.md` section 3.8
- `.ept/docs/customer_input/open_questions.md` A4.4
- `.ept/docs/customer_input/open_questions_2.md` A(Q2(R2).8)
- `.ept/docs/customer_input/open_questions_3.md` A(Q3(R3).5)
- `.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md` FR-AUTH, FR-OUT, FR-ASYNC, FR-PAG, FR-ERR, FR-DL, FR-SESSION, FR-TRACE, FR-SKILL, FR-ACL, and NFR sections
- `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md` sections 5, 6.5, 8.4, 9, and 10
- `.ept/docs/deliverables/architecture/DESIGN-005-common-components.md`
- `.ept/docs/deliverables/architecture/canonical-env-var-reference.md` namespace `aip_agents` (15 rows)
- `.ept/docs/deliverables/architecture/metadata-allow-list.md` namespace `aip_agents` (15 rows)
- `.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md`
- `.ept/docs/deliverables/architecture/adr/ADR-002-call-timeout-defaults.md`
- `.ept/docs/deliverables/architecture/adr/ADR-004-format-auto-algorithm.md`
- `.ept/docs/deliverables/architecture/adr/ADR-005-log-format.md`
- `.ept/docs/deliverables/architecture/adr/ADR-006-env-file-search-path.md`
- `.ept/docs/deliverables/architecture/adr/ADR-007-operation-level-readonly.md`
- `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/aip_agents/`

## Technical Scope

- Namespace: `aip_agents`, 15 SDK operations across Agent, AgentVersion, Session, Content, and SessionTrace clients.
- Paged operations: `agent.all_sessions`, `agent_version.list`, and `session.list`.
- Byte response: `session.streaming_continue`, handled by `BinaryDownloadHandler`.
- Session state: alias-based local mapping through the completed `SessionManager`; automatic expiry cleanup and explicit local purge.
- Common dependencies: `AccessControlGuard`, `PaginationHelper`, `RetryHandler`, `OutputFormatter`, `ErrorSerializer`, `LogSetup`, `AsyncClientFactory`/`TracingProvider`, `BinaryDownloadHandler`, and `SessionManager` from `src/foundry_cli/common/`.
- Attribution: excluded by FR-ATTR-4.
- Implementation artifacts: `src/foundry_cli/aip_agents/__init__.py`, `src/foundry_cli/aip_agents/scripts/__init__.py`, `src/foundry_cli/aip_agents/scripts/foundry_aip_agents_cli.py`, `src/foundry_cli/aip_agents/metadata-allow-list.md`, `.claude/skills/foundry-aip-agents/SKILL.md`, `.claude/skills/foundry-aip-agents/scripts/foundry_aip_agents_cli.py`, `tests/test_foundry_aip_agents_cli.py`, `tests/test_aip_agents_console_wrapper.py`, and the `foundry-aip-agents` console entry in `pyproject.toml`.
- Prerequisites: completed EPIC-001 common components from DEV-STORY-002, DEV-STORY-003, and DEV-STORY-004; installed `foundry-platform-sdk`; supported Python 3.11/3.12.
- Boundaries: no Foundry API v1, OAuth2 flow, remote shared session store, W3C trace-context claim, attribution injection, or changes to other namespace operation catalogs.

## Notes

SAD-001's roadmap entry still says 13 operations. That count is stale. The checked-in SDK source, Canonical Environment Variable Reference, and Metadata Allow-list independently agree on 15. This story uses 15 as the implementation and test contract. No stakeholder question remains open.
