# DESIGN-011 - Foundry AIP Agents CLI

| Field | Value |
|---|---|
| Story | DEV-STORY-011 |
| Status | Completed; DESIGN closed |
| Date | 2026-08-09 |
| Scope | `foundry-aip-agents` CLI and Claude skill, 15 AIP Agents API v2 operations, plus local session purge |

## Technical summary

Add an AIP Agents namespace CLI that exposes the complete 15-operation SDK v2 surface approved for this story. The CLI also adds `session purge`, a local maintenance command backed by `SessionManager`; purge is not an SDK operation and does not change the authoritative SDK count.

The implementation reuses the common configuration, access control, async client, retry, output, logging, pagination, download, session, tracing, and error components. Two focused common changes are required:

- classify `purge` as a write in `AccessControlGuard`, so read-only and metadata-only modes block it before local deletion;
- let `AsyncClientFactory` suppress attribution for this namespace while restoring any prior SDK attribution context afterward.

Tracing uses SDK-native B3 multi-headers only. AIP Agents requests must not carry attribution RIDs. `streaming_continue()` returns eager `bytes` in the current SDK; the download adapter bounds persisted output, not SDK response memory.

## Evidence and governing references

This design follows:

- SRS-001 FR-SESSION-1 through FR-SESSION-7, FR-ACL, FR-PAG, FR-DL, FR-ERR, FR-OUT, and FR-TRACE;
- SAD-001 session lifecycle and namespace packaging structure;
- DESIGN-005 contracts for `SessionManager`, `BinaryDownloadHandler`, and `TracingProvider`;
- ADR-001 exit codes, ADR-002 timeouts, ADR-004 format selection, ADR-005 stderr metadata and logging, ADR-006 configuration search, and ADR-007 operation-level read-only precedence;
- the canonical metadata allow-list, which permits six and blocks nine AIP Agents SDK operations in tier 3;
- vendored SDK v2 clients in `foundry_sdk/v2/aip_agents/agent.py`, `agent_version.py`, `session.py`, `content.py`, and `session_trace.py`.

The SDK sources expose two `Agent` methods, two `AgentVersion` methods, nine `Session` methods, one `Content` method, and one `SessionTrace` method: 15 total. The older SAD roadmap title saying 13 operations is stale and does not define this story's scope.

## Operation catalog

CLI resource and operation names use kebab-case. Catalog keys and ACL paths use snake_case. `OP_SPECS` must contain exactly 15 unique SDK entries. Local purge lives in a separate local-operation spec or explicit branch, so it cannot inflate the SDK contract count.

| CLI command | Exact SDK route | SDK method | Required arguments | Optional arguments | Result |
|---|---|---|---|---|---|
| `agent all-sessions` | `client.aip_agents.Agent` | `all_sessions` | none | paging controls | List of sessions |
| `agent get` | `client.aip_agents.Agent` | `get` | `agent_rid` | `--version` | Agent |
| `agent-version get` | `client.aip_agents.Agent.AgentVersion` | `get` | `agent_rid`, `agent_version_string` | none | Agent version |
| `agent-version list` | `client.aip_agents.Agent.AgentVersion` | `list` | `agent_rid` | paging controls | List of agent versions |
| `session blocking-continue` | `client.aip_agents.Agent.Session` | `blocking_continue` | `--alias`, `--parameter-inputs-json`, `--user-input-json` | `--contexts-override-json`, `--session-trace-id` | Session exchange result |
| `session cancel` | `client.aip_agents.Agent.Session` | `cancel` | `--alias`, `--message-id` | `--response` | Cancel response |
| `session create` | `client.aip_agents.Agent.Session` | `create` | `--alias`, `--agent-rid` | `--agent-version` | Local session state with alias |
| `session delete` | `client.aip_agents.Agent.Session` | `delete` | `--alias` | none | Empty success result |
| `session get` | `client.aip_agents.Agent.Session` | `get` | `--alias` | none | Session |
| `session list` | `client.aip_agents.Agent.Session` | `list` | `agent_rid` | paging controls | List of sessions for agent |
| `session rag-context` | `client.aip_agents.Agent.Session` | `rag_context` | `--alias`, `--parameter-inputs-json`, `--user-input-json` | none | RAG context response |
| `session streaming-continue` | `client.aip_agents.Agent.Session` | `streaming_continue` | `--alias`, `--parameter-inputs-json`, `--user-input-json` | `--contexts-override-json`, `--message-id`, `--session-trace-id`, `--output-filename` | JSON download envelope |
| `session update-title` | `client.aip_agents.Agent.Session` | `update_title` | `--alias`, `--title` | none | Empty success result |
| `content get` | `client.aip_agents.Agent.Session.Content` | `get` | `--alias` | none | Session content |
| `session-trace get` | `client.aip_agents.Agent.Session.SessionTrace` | `get` | `--alias`, `--session-trace-id` | none | Session trace |

The local command is:

| CLI command | Local route | Required arguments | Result |
|---|---|---|---|
| `session purge` | `SessionManager.purge()` | none | `{ "purged_sessions": integer }` |

### SDK signatures

The namespace adapter must preserve these public SDK contracts. `preview` remains configured on the shared client and is not exposed per command.

```python
# client.aip_agents.Agent
def all_sessions(
    *,
    page_size: int | None = None,
    page_token: str | None = None,
    request_timeout: Timeout | None = None,
) -> AsyncResourceIterator[Session]: ...

def get(
    agent_rid: str,
    *,
    version: str | None = None,
    request_timeout: Timeout | None = None,
) -> Awaitable[Agent]: ...

# client.aip_agents.Agent.AgentVersion
def get(
    agent_rid: str,
    agent_version_string: str,
    *,
    request_timeout: Timeout | None = None,
) -> Awaitable[AgentVersion]: ...

def list(
    agent_rid: str,
    *,
    page_size: int | None = None,
    page_token: str | None = None,
    request_timeout: Timeout | None = None,
) -> AsyncResourceIterator[AgentVersion]: ...

# client.aip_agents.Agent.Session
def blocking_continue(
    agent_rid: str,
    session_rid: str,
    *,
    parameter_inputs: dict[str, Any],
    user_input: dict[str, Any],
    contexts_override: list[dict[str, Any]] | None = None,
    session_trace_id: str | None = None,
    request_timeout: Timeout | None = None,
) -> Awaitable[SessionExchangeResult]: ...

def cancel(
    agent_rid: str,
    session_rid: str,
    *,
    message_id: str,
    response: str | None = None,
    request_timeout: Timeout | None = None,
) -> Awaitable[CancelSessionResponse]: ...

def create(
    agent_rid: str,
    *,
    agent_version: str | None = None,
    request_timeout: Timeout | None = None,
) -> Awaitable[Session]: ...

def delete(
    agent_rid: str,
    session_rid: str,
    *,
    request_timeout: Timeout | None = None,
) -> Awaitable[None]: ...

def get(
    agent_rid: str,
    session_rid: str,
    *,
    request_timeout: Timeout | None = None,
) -> Awaitable[Session]: ...

def list(
    agent_rid: str,
    *,
    page_size: int | None = None,
    page_token: str | None = None,
    request_timeout: Timeout | None = None,
) -> AsyncResourceIterator[Session]: ...

def rag_context(
    agent_rid: str,
    session_rid: str,
    *,
    parameter_inputs: dict[str, Any],
    user_input: dict[str, Any],
    request_timeout: Timeout | None = None,
) -> Awaitable[AgentSessionRagContextResponse]: ...

def streaming_continue(
    agent_rid: str,
    session_rid: str,
    *,
    parameter_inputs: dict[str, Any],
    user_input: dict[str, Any],
    contexts_override: list[dict[str, Any]] | None = None,
    message_id: str | None = None,
    session_trace_id: str | None = None,
    request_timeout: Timeout | None = None,
) -> Awaitable[bytes]: ...

def update_title(
    agent_rid: str,
    session_rid: str,
    *,
    title: str,
    request_timeout: Timeout | None = None,
) -> Awaitable[None]: ...

# client.aip_agents.Agent.Session.Content
def get(
    agent_rid: str,
    session_rid: str,
    *,
    request_timeout: Timeout | None = None,
) -> Awaitable[Content]: ...

# client.aip_agents.Agent.Session.SessionTrace
def get(
    agent_rid: str,
    session_rid: str,
    session_trace_id: str,
    *,
    request_timeout: Timeout | None = None,
) -> Awaitable[SessionTrace]: ...
```

CLI JSON dictionaries and lists are passed to the generated SDK, which performs model decoding and validation. The CLI still validates JSON syntax and top-level shape before client creation.

## CLI and data contracts

Every SDK command accepts `--timeout`, `--format {json,toon,auto}`, and `--pretty`. The three paged commands also accept `--page-size`, `--page-token`, and `--batch-pages`. `session purge` accepts format and pretty options but no timeout because it performs no network call.

Required values must not be empty or whitespace-only. Pagination integers and timeout must be positive integers. JSON arguments follow these shapes:

| Option | Required top-level type |
|---|---|
| `--parameter-inputs-json` | object |
| `--user-input-json` | object |
| `--contexts-override-json` | array of objects |

Malformed JSON, wrong top-level types, invalid pagination values, missing subcommands, and missing required values are user-input errors. They must produce the standard JSON error envelope on stdout with exit code 1. A custom `ArgumentParser.error()` must raise into normal error serialization instead of writing argparse's default unstructured stderr message.

`session cancel --response` accepts an optional markdown string and passes it unchanged as `response: str | None`. It is not JSON and must not be decoded as an object. An omitted option passes `None`, which tells the SDK not to add a client-provided response to the session exchange.

Aliases are the public identifier for commands bound to one persisted session. Those commands do not accept raw `agent_rid` or `session_rid`; the CLI obtains both from `SessionManager.load(alias)`. The two remote list commands and agent/version reads retain the SDK's direct agent arguments because they do not operate on one local alias.

## Component breakdown and interfaces

### Package layout

- `src/foundry_cli/aip_agents/__init__.py` and `src/foundry_cli/aip_agents/scripts/__init__.py`: package markers.
- `src/foundry_cli/aip_agents/scripts/foundry_aip_agents_cli.py`: catalog, parser, validation, dispatch, session integration, pagination, byte persistence, output, and error boundary.
- `src/foundry_cli/aip_agents/metadata-allow-list.md`: packaged tier-3 policy used outside repository working directories.
- `.claude/skills/foundry-aip-agents/SKILL.md`: concise command, alias, ACL, pagination, output, and recovery contract.
- `.claude/skills/foundry-aip-agents/scripts/foundry_aip_agents_cli.py`: thin launcher delegating to packaged `console_main()`.
- `pyproject.toml`: additive console entry point, package data, and established Ruff/coverage configuration.

### Namespace interfaces

```python
OperationSpec = dict[str, Any]

def build_parser() -> argparse.ArgumentParser: ...
def _spec_for(resource: str, operation: str) -> OperationSpec: ...
def _get_client(root_client: Any, client_path: tuple[str, ...]) -> Any: ...
def _parse_json_object(value: str, *, field: str) -> dict[str, Any]: ...
def _parse_json_list(value: str, *, field: str) -> list[dict[str, Any]]: ...
def _model_to_dict(value: Any) -> Any: ...

async def _fetch_page(
    method: Any,
    *,
    page_size: int,
    page_token: str | None,
    request_timeout: int | None,
    call_kwargs: dict[str, Any],
) -> dict[str, Any]: ...

async def _paginate_operation(
    method: Any,
    args: argparse.Namespace,
    timeout: int | None,
    call_kwargs: dict[str, Any],
) -> tuple[list[Any], PaginationHelper]: ...

async def _one_bytes_chunk(payload: bytes) -> AsyncIterator[bytes]: ...
def _load_alias(manager: SessionManager, alias: str) -> SessionState: ...
def _record_session_use(
    manager: SessionManager,
    alias: str,
    state: SessionState,
    *,
    operation: str,
    succeeded: bool,
    completed: bool = False,
) -> None: ...

async def _invoke_sdk(...) -> Any: ...
async def _purge_sessions(...) -> dict[str, int]: ...
async def main() -> int: ...
def console_main() -> int: ...
```

Only `build_parser`, `main`, and `console_main` are external module interfaces. All public functions and classes require full annotations and project-style docstrings. `console_main()` owns the single `asyncio.run(main())` event-loop boundary.

### Common attribution override

Current `AsyncClientFactory.create(cfg)` reads global attribution configuration and sets the SDK `ATTRIBUTION_VAR`. That behavior conflicts with the approved AIP Agents constraint when attribution is enabled globally. Add an optional, backward-compatible override:

```python
def create(
    self,
    cfg: ConfigLoader,
    *,
    include_attribution: bool | None = None,
) -> AsyncFoundryClient: ...

@contextmanager
def invocation_scope(
    self,
    cfg: ConfigLoader,
    supplied: B3Context | None = None,
    *,
    include_attribution: bool | None = None,
) -> Iterator[B3Context | None]: ...
```

`None` preserves existing namespace behavior. AIP Agents passes `False` to both calls. The invocation scope sets attribution to `None`, retains the SDK context-variable token, and restores the previous value in `finally`. Client creation must not overwrite the scoped `None`. This is an additive API change; existing callers need no edits.

## Access control

Every command calls `AccessControlGuard(cfg, "AIP_AGENTS").check(resource, operation)` before alias loading, client creation, download directory creation, purge, or any other command-specific filesystem action.

The 15 SDK operations have this exact tier-3 policy:

| SDK path | Metadata-only result | Read-only classification |
|---|---|---|
| `aip_agents.agent.all_sessions` | `BLOCKED` | Read |
| `aip_agents.agent.get` | `PERMITTED` | Read |
| `aip_agents.agent_version.get` | `PERMITTED` | Read |
| `aip_agents.agent_version.list` | `PERMITTED` | Read |
| `aip_agents.content.get` | `BLOCKED` | Read |
| `aip_agents.session.blocking_continue` | `BLOCKED` | Write |
| `aip_agents.session.cancel` | `BLOCKED` | Write |
| `aip_agents.session.create` | `BLOCKED` | Write |
| `aip_agents.session.delete` | `BLOCKED` | Write |
| `aip_agents.session.get` | `PERMITTED` | Read |
| `aip_agents.session.list` | `PERMITTED` | Read |
| `aip_agents.session.rag_context` | `BLOCKED` | Write |
| `aip_agents.session.streaming_continue` | `BLOCKED` | Write |
| `aip_agents.session.update_title` | `BLOCKED` | Write |
| `aip_agents.session_trace.get` | `PERMITTED` | Read |

This is exactly six permitted and nine blocked SDK operations. `session purge` is a separate local write. Add `purge` to the guard's write verbs and document `aip_agents.session.purge` as blocked in tier 3. Both read-only and metadata-only modes must reject purge with exit code 8 before `SessionManager.purge()` runs.

The packaged allow-list is authoritative at runtime for this namespace. It must resolve relative to the installed package, not the process working directory. Missing package policy fails closed in metadata-only mode.

## Session lifecycle

### Persisted state and aliases

Use the existing `SessionState` schema unchanged:

```python
@dataclass
class SessionState:
    session_id: str
    agent_rid: str
    session_token: str | None
    created_at: str
    last_used_at: str
    status: Literal["active", "completed", "expired"]
    tool_history: list[dict[str, Any]]
```

`session_id` stores SDK `Session.rid`. New records write `session_token=null`; readers continue accepting missing, null, or string token fields. Resume operations use only `agent_rid` and `session_id`. The token must never appear in output, logs, error details, or history.

Alias normalization, containment, cross-process alias locks, atomic JSON replacement, corrupt-record cleanup, restrictive permissions, and reserved-name rejection remain owned by `SessionManager` per DESIGN-005.

### Create and compensation

`session create` calls `SessionManager.create(alias, agent_rid, create_remote, delete_remote)`. The alias lock covers collision checking, remote creation, and local publication. The `create_remote` callback runs the SDK create call through `RetryHandler`. If remote creation succeeds but local persistence fails, `SessionManager` attempts `delete_remote(session_id)` once, preserves the original persistence error, and records only the RID in diagnostic metadata if compensation also fails.

The success object adds the canonical alias to the serialized local state. Creation warns, but does not fail, when the agent has more than five active local sessions.

### Load, use, and completion

Alias-bound commands load state only after ACL approval. On a successful remote call, update `last_used_at` and append one sanitized history record containing timestamp, operation name, and success status. Do not store arguments, prompt text, contexts, response data, exception text, or tokens. `session delete` also changes local status to `completed` after remote deletion succeeds.

For a failed remote call, history recording is best effort and must not replace the primary SDK exception. Local persistence failure after a successful remote operation is a filesystem/server failure under the existing error mapping.

`SessionManager` serializes each file read or write, but the CLI does not hold a filesystem lock across ordinary remote operations. A concurrent purge is point-in-time: it deletes records present and unlocked during its scan; an already running command may persist a later usage update. The CLI must not claim transaction isolation across separate processes.

### Cleanup and purge

After argument parsing and logging setup, instantiate `SessionManager` and call `cleanup_expired()` once for every real command invocation. Cleanup precedes command-specific ACL because it is namespace maintenance required on every invocation, not the requested operation. It removes records marked expired or inactive for seven days, locks each alias before mutation, skips locked aliases with a warning, and logs only counts and canonical aliases.

`session purge` deletes all currently unlocked local session records and returns their count. It is idempotent, performs no SDK call, does not delete remote sessions, and does not require a timeout. ACL must run before purge.

## Exact-page pagination

`agent all-sessions`, `agent-version list`, and `session list` are the only paged routes. Their normal SDK methods return `AsyncResourceIterator` objects that can silently fetch further pages. Use each client's `with_raw_response` wrapper to fetch one server page per call, then decode:

```python
raw_response = await client.with_raw_response.list(
    **call_kwargs,
    page_size=page_size,
    page_token=page_token,
    request_timeout=request_timeout,
)
page = raw_response.decode()
return {
    "items": list(page.data or []),
    "next_page_token": page.next_page_token,
}
```

For `all_sessions`, call `with_raw_response.all_sessions` with the same page arguments. The three decoded models are `AgentsSessionsPage`, `ListAgentVersionsResponse`, and `ListSessionsResponse`; each exposes `data` and `next_page_token`.

Create a fresh `PaginationHelper` inside every retry attempt. Fetch one page by default, stop at EOF, and cap batches at 40 pages. Forward the cursor returned by the previous decoded page. Emit metadata once, after successful stdout output, with accurate `pages_fetched`, `total_items`, `page_size`, and remaining `next_page_token`. Never estimate page count from item count or inspect private SDK iterator fields.

## Eager bytes from streaming continue

The current async SDK signature for `streaming_continue()` is `Awaitable[bytes]`. Unlike Audit content, this route has no approved streamed-response contract for this story. Call the documented eager method, verify the result is `bytes`, and adapt it to `BinaryDownloadHandler`:

```python
async def _one_bytes_chunk(payload: bytes) -> AsyncIterator[bytes]:
    yield payload

result = await BinaryDownloadHandler(config=cfg).save(
    _one_bytes_chunk(payload),
    original_filename=args.output_filename,
    namespace="aip_agents",
    operation="session.streaming_continue",
    content_length=None,
    content_encoding=None,
    mime_type=None,
)
```

The handler limits bytes written, uses contained UUID directories, publishes atomically, and returns checksums for the stored prefix. It cannot limit memory already allocated when the SDK decodes the response. Documentation, logs, tests, and release notes must not claim bounded SDK response memory or network streaming for this operation. A future SDK with a documented streaming API requires separate review.

The result is always the standard JSON download envelope, even when `--format toon` is supplied. No response bytes are written to stdout or logs.

## Invocation, retry, tracing, output, and errors

Execution order is fixed:

1. Parse arguments through the structured parser boundary.
2. Load configuration and configure `LogSetup`.
3. Run expired-session cleanup once.
4. Resolve operation spec and validate scalar and JSON inputs.
5. Run `AccessControlGuard`.
6. For purge, delete local records, format the count as JSON, and return.
7. For alias-bound commands, load local state and derive `agent_rid` and `session_rid`.
8. Enter `AsyncClientFactory.invocation_scope(cfg, include_attribution=False)`.
9. Create the client with `include_attribution=False` and resolve the exact nested resource.
10. Run the complete logical SDK attempt through `RetryHandler`, including all requested pages for a paged command.
11. Persist sanitized session-use metadata after alias-bound calls.
12. Leave invocation scope, restoring B3 and prior attribution context in every exit path.
13. Write one formatted success result to stdout; emit successful pagination metadata once on stderr.
14. Serialize failures through `ErrorSerializer` without raw tracebacks.

One B3 context covers client creation and all retry attempts. Generated headers are `X-B3-TraceId`, `X-B3-SpanId`, and `X-B3-Sampled` through SDK context variables. Do not emit or claim W3C `traceparent` or `tracestate` support.

Retry configured transport failures, HTTP 429, and HTTP 503 through `RetryHandler`. Keep retries inside the B3 and no-attribution scope. Preserve ADR-001 exit codes: success 0, input 1, authentication 2, permission 3, not found 4, timeout/cancellation 5, server/filesystem failure 6, exhausted rate limit 7, ACL 8, and configuration 9.

Model results use the established model-to-dict adapter. ADR-004 applies: uniform non-empty lists may use TOON in auto mode; empty or heterogeneous lists and all objects use JSON. Error envelopes, purge output, and binary download metadata always use JSON. Success data and errors go to stdout. NDJSON logs and pagination metadata go to stderr.

## Security and privacy controls

- Run ACL before alias reads, SDK calls, download publication, and purge.
- Validate JSON and scalar inputs before client creation.
- Use `SessionManager` alias normalization; never derive paths from unvalidated input.
- Never log prompts, `user_input`, parameter values, context overrides, response bodies, content, tokens, or attribution RIDs.
- Keep session and download file permissions and atomic replacement rules from DESIGN-005.
- Do not access SDK private fields or private response objects.
- Clear attribution for every AIP Agents request and restore prior context afterward.
- Keep one isolated B3 context per invocation; restore prior context on success, error, cancellation, and formatter failure.
- Importing package or launcher must not read configuration, create directories, set context variables, construct clients, or make network calls.
- Treat missing packaged metadata policy as deny-by-default in metadata-only mode.

## Packaging and compatibility

Append this console entry point without changing existing entries:

```toml
foundry-aip-agents = "foundry_cli.aip_agents.scripts.foundry_aip_agents_cli:console_main"
```

Package `foundry_cli.aip_agents/metadata-allow-list.md`. Add only the established namespace-specific Ruff and coverage settings needed by the implementation. The Claude launcher imports and delegates to packaged `build_parser`, `main`, and `console_main`; it contains no copied business logic.

Wheel and editable installations must expose `foundry-aip-agents`. Package-policy tests must execute from an empty working directory to prove tier-3 decisions do not depend on repository `.ept/docs`. Existing console entry points and common defaults remain compatible. The optional attribution parameter is additive and defaults to current behavior.

## Implementation sequence

1. Use the completed, closed DESIGN-011 as the implementation baseline; keep its document-index entry current.
2. Add `purge` write classification and tests in the access guard.
3. Add the backward-compatible attribution override and restoration tests.
4. Add AIP Agents package markers, packaged allow-list, entry point, Claude skill, and launcher.
5. Implement the exact 15-entry SDK catalog, local purge branch, parser, and JSON validation.
6. Implement nested dispatch and three raw-page adapters.
7. Integrate aliases, create compensation, cleanup, use history, completion, and purge.
8. Add eager-byte persistence with the explicit memory limitation.
9. Wire retry, B3, output, logging, and error serialization.
10. Complete unit, review, QA, clean-install, and regression gates.

## Test and QA traceability matrix

| Requirement area | Required coverage | Expected evidence |
|---|---|---|
| Catalog | Exactly 15 unique SDK specs plus separate local purge | Catalog count, uniqueness, and local-count tests |
| Nested routing | Every operation reaches exact `Agent`, `AgentVersion`, `Session`, `Content`, or `SessionTrace` object | Route identity tests that fail on flattened clients |
| Parser | All 16 commands, help, missing command/argument, invalid choice/type, and optional cancel response string | Console-boundary stdout JSON and exit-code assertions |
| JSON inputs | Valid object/list payloads, malformed JSON, wrong top-level type; cancel response excluded from JSON decoding | No client construction on invalid JSON input; `--response` forwarded unchanged |
| Agent | `all-sessions` and `get`, with optional version and failures | Dispatch, output, pagination, ACL evidence |
| Agent versions | `get` and `list` | Exact arguments, page/cursor evidence |
| Session create | Alias normalization, collision, optional version, missing RID, compensation, >5 warning | Local state and remote-call assertions |
| Alias-bound operations | All nine post-create alias commands resolve stored IDs and reject missing/corrupt aliases | SDK argument and structured-error evidence |
| Session state | `last_used_at`, sanitized history, delete completion, token redaction | State-file and captured-log assertions |
| Cleanup | Seven-day boundary, expired records, corrupt records, locked alias skip, once per invocation | Deterministic clock and lock tests |
| Purge | All unlocked files, locked skip, idempotency, no SDK call | Deletion count and filesystem evidence |
| Purge ACL | Namespace/operation disabled, read-only, metadata-only | Exit 8 before filesystem mutation |
| Tier 3 | Six permitted and nine blocked SDK operations; local purge blocked separately | Full decision matrix |
| Read-only | Seven remote writes and local purge blocked; reads permitted unless overridden | Full classification matrix |
| Pagination | Three raw routes, one page default, cursor resume, exact N pages, EOF, 40-page cap | Accurate stderr page metadata |
| Pagination retry | Failure on later page followed by retry | Fresh counters, no duplicate output or metadata |
| Eager bytes | Empty, below, equal, and above file limit; invalid type; write failure | Download envelope, checksums, cleanup, no memory-bound claim |
| Retry/errors | 429 exhaustion, 503 retry, 403, 404, timeout, auth, config, unexpected SDK failure | ADR-001 codes and JSON envelopes |
| B3 | Enabled/disabled, same values across retries, concurrent and failed scopes | Context restoration assertions |
| Attribution | Globally configured RIDs with AIP opt-out, nested scopes, failures | No AIP attribution; previous value restored |
| Output | JSON/TOON selection, object JSON, binary JSON, purge JSON, stderr separation | Captured stdout/stderr assertions |
| Privacy | Prompts, contexts, response bytes, token values, exception details | Negative log/output assertions |
| Imports | Package and launcher import | No network, config, directory, or context side effects |
| Packaging | Wheel/editable console and Claude help; allow-list outside repo cwd | Clean-install smoke evidence |
| Regression | Python 3.11/3.12, Ruff, mypy, Bandit, full pytest | Branch coverage at least 80% |

Routine QA can use mocked SDK transport or an approved non-production Foundry environment. Live credentials are not required for normal acceptance evidence.

## Grooming decomposition and dependencies

All children use DEV-STORY-011 as parent through `ParentChild`.

| Type | Exact title | Role | Estimate | Completion contract |
|---|---|---|---:|---|
| DESIGN | Design Foundry AIP Agents CLI and session lifecycle | `tech-lead` | 8 h | DESIGN-011 covers all contracts in this document, is indexed, reviewed, and closed before Development. |
| DEV | Implement Foundry AIP Agents CLI, session lifecycle, and Claude skill | `python-developer` | 26 h | Add package, 15 SDK operations, local purge, nested routing, exact pages, aliases, eager-byte persistence, ACL and attribution common changes, skill, and entry point; Ruff and mypy pass. |
| UNITTEST | Add Foundry AIP Agents CLI unit and integration tests | `python-developer` | 16 h | Assert every row in the traceability matrix, including package policy outside repo cwd; targeted tests pass and repository branch coverage remains at least 80%. |
| CODEREVIEW | Review Foundry AIP Agents CLI implementation | `tech-lead` | 5 h | Review exact DEV result for correctness, SDK protocols, session concurrency, OWASP controls, ACL, B3, attribution, packaging, and compatibility; resolve or track all findings. |
| TESTCASE | Design Foundry AIP Agents CLI QA cases | `qa-engineer` | 6 h | Create cases for all 16 commands and every story criterion with inputs, expected stdout/stderr, exit code, filesystem effect, prerequisites, and cleanup; `tech-lead` reviews and approves the completed case set before TESTEXEC. |
| TESTEXEC | Execute Foundry AIP Agents CLI QA suite | `qa-engineer` | 8 h | Record environment, commands, expected and actual results, and evidence; create BUG-SUB for failures; no blocking defect remains at sign-off. |
| DEVOPS | Package and verify Foundry AIP Agents entry points | `devops-engineer` | 3 h | Validate clean wheel/editable installs, console and Claude launchers, package policy, existing entry points, Python matrix, security gates, and rollback. |

Dependency plan:

- DESIGN-011 is completed and closed; its implementation-readiness gate is satisfied.
- DEV and UNITTEST may proceed together after DESIGN; TESTCASE may run in parallel.
- DEV has `RelatesTo` and an active blocking relationship to CODEREVIEW until its result is ready. CODEREVIEW also requires UNITTEST evidence.
- TESTCASE blocks TESTEXEC. TESTEXEC cannot start until the completed QA case set has recorded approval from `tech-lead` acting as Tech Lead/Architect reviewer.
- TESTEXEC also depends on DEV, UNITTEST, and CODEREVIEW.
- DEVOPS depends on successful TESTEXEC.
- The tech-lead reviewer must differ from the Python developer implementing DEV.

DEVOPS is required because the story adds a console script, packaged policy asset, and Claude launcher that need clean-install verification.

## Estimate and sprint fit

Story estimate: 13 points, 72 planned role-hours.

| Work | Hours |
|---|---:|
| Design | 8 |
| Development | 26 |
| Unit tests | 16 |
| Code review | 5 |
| QA case design | 6 |
| QA execution | 8 |
| Packaging and deployment verification | 3 |
| Total | 72 |

The work fits one 10-day sprint. TESTCASE overlaps development, while the main sequential path is about 66 hours: design, development and unit testing by the shared developer role, review, QA execution, then packaging verification. This estimate assumes no SDK upgrade and no redesign of common session or download schemas.

## Risks and decisions

| Risk or decision | Treatment |
|---|---|
| SAD roadmap says 13 operations | Ignore stale title; enforce 15-entry SDK catalog from source. |
| Purge looks like a read to current guard | Add `purge` write classification and pre-mutation denial tests. |
| Global attribution can leak into AIP requests | Add explicit opt-out with context restoration; test configured global RIDs. |
| SDK returns eager bytes | Bound only persisted output; make no SDK-memory or network-streaming claim. |
| SDK iterators can fetch beyond requested page count | Use raw response wrappers and decoded page models. |
| Pagination retry can retain counters | Construct helper inside each complete retry attempt. |
| Alias data contains sensitive state | Use existing contained paths, locks, atomic writes, permissions, and redacted history. |
| Concurrent remote commands are not transactionally serialized | State exact point-in-time purge and per-file atomicity semantics; do not claim cross-process transaction isolation. |
| Package allow-list may work only from repository cwd | Package the policy and test installed execution from an empty directory. |
| Complex generated SDK models may evolve | Validate JSON shape locally, delegate field validation to pinned supported SDK, and treat SDK contract changes as separate review. |

No open design question blocks implementation. The B3-only, no-attribution, 15-operation, local-purge, and eager-byte constraints are treated as approved architectural inputs.

## Story acceptance criteria

1. **Given** the installed namespace, **when** its catalog is inspected, **then** it contains exactly 15 unique SDK v2 operations with the nested routes in this document, while local `session purge` is counted separately.
2. **Given** valid input for any catalog command, **when** dispatch runs, **then** it calls the exact SDK method and forwards only the documented arguments and timeout.
3. **Given** any of the three paged commands, **when** one page or `--batch-pages N` is requested, **then** the CLI fetches that many actual server pages or stops at EOF, never exceeds 40, and emits accurate continuation metadata once.
4. **Given** an alias-bound command, **when** a valid alias is supplied, **then** the CLI uses persisted `agent_rid` and `session_id`, updates sanitized usage state, and never exposes `session_token`.
5. **Given** session creation, **when** an active alias already exists, **then** creation fails without a second remote create; **when** persistence fails after remote success, **then** one compensation delete is attempted and the original error remains primary.
6. **Given** a real CLI invocation, **when** expired or corrupt local records exist, **then** cleanup runs once under alias locks without exposing record contents.
7. **Given** read-only or metadata-only mode, **when** `session purge` is requested, **then** the command exits 8 before deleting a file; **when** permitted normally, **then** it deletes unlocked local records only and returns a JSON count without an SDK call.
8. **Given** metadata-only mode, **when** all 15 SDK operations are evaluated, **then** exactly six are permitted and nine blocked according to the canonical table.
9. **Given** `session streaming-continue`, **when** the SDK returns eager bytes, **then** the CLI passes them through `BinaryDownloadHandler`, persists no more than its configured limit, returns the standard JSON checksums and size envelope, and makes no bounded-memory claim.
10. **Given** tracing enabled and retries required, **when** an AIP request runs, **then** one SDK-native B3 context spans client creation and every attempt, no W3C headers are claimed, and prior trace context is restored.
11. **Given** global attribution configuration, **when** an AIP request runs, **then** no attribution RID reaches the request and the prior SDK attribution context is restored on success, failure, timeout, cancellation, and formatter error.
12. **Given** malformed input, ACL denial, missing alias, SDK failure, timeout, configuration failure, or filesystem failure, **when** the command exits, **then** stdout contains one structured JSON error, the ADR-001 exit code is correct, stderr contains only approved diagnostics, and no prompt, content, response bytes, or token leaks.
13. **Given** wheel or editable installation from a clean archive, **when** `foundry-aip-agents --help`, the Claude launcher help, and metadata-only checks run outside repository cwd, **then** all succeed with packaged policy and existing entry points unchanged.
14. **Given** supported Python versions, **when** delivery gates run, **then** Python 3.11/3.12 tests, Ruff, mypy, Bandit, packaging checks, and the full regression suite pass with branch coverage at least 80%.
