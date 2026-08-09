# TESTCASE-011 - Foundry AIP Agents CLI QA test cases

## Scope

These cases cover DEV-STORY-011, the 15 SDK v2 commands in `foundry-aip-agents`, and local `session purge`. They verify parser and nested dispatch contracts, exact-page pagination, session aliases and cleanup, ACL policy, eager-byte persistence, retry and error behavior, B3 tracing, attribution suppression, privacy, packaging, and regression gates.

The test design uses mocked SDK transport for routine behavior and permits an approved non-production Foundry environment for optional smoke checks. Live credentials and live service access are not required for acceptance evidence.

## Source baseline

- [DESIGN-011](../architecture/DESIGN-011-aip-agents-cli.md), completed and closed for DEV-STORY-011.
- [DESIGN-005](../architecture/DESIGN-005-common-components.md), covering session, download, and tracing contracts.
- [ADR-001](../architecture/adr/ADR-001-exit-code-taxonomy.md), [ADR-002](../architecture/adr/ADR-002-call-timeout-defaults.md), [ADR-004](../architecture/adr/ADR-004-format-auto-algorithm.md), and [ADR-005](../architecture/adr/ADR-005-log-format.md).
- Implementation in `src/foundry_cli/aip_agents/`, `.claude/skills/foundry-aip-agents/`, shared common components, and `pyproject.toml`.
- Developer tests in `tests/test_foundry_aip_agents_cli.py` and `tests/test_aip_agents_console_wrapper.py`. These provide reusable fixture patterns but are not QA execution evidence.

## Preconditions and environments

- Python 3.11 and 3.12 environments contain the project and development dependencies.
- Routine cases use a nested async SDK fake with public resources `aip_agents.Agent`, `Agent.AgentVersion`, `Agent.Session`, `Agent.Session.Content`, and `Agent.Session.SessionTrace`.
- Paged calls use `with_raw_response` fakes whose decoded models expose `data` and `next_page_token`.
- Retry delay and jitter are disabled while attempt order, timeout, and B3 values remain observable.
- Each session or download case uses fresh temporary directories. Tests use real `SessionManager` locking and atomic file operations where practical.
- stdout, stderr, logs, SDK calls, context variables, and filesystem changes are captured independently.
- Packaging cases build a clean local archive, install with `--no-deps`, and run from an empty working directory without `PYTHONPATH`.
- Any optional live smoke uses an approved non-production Foundry tenant, synthetic records, least-privilege credentials, and a cleanup plan. Credentials must never enter retained evidence.
- TESTEXEC records commit, OS, Python version, environment type, exact command, expected and actual result, stdout, stderr, exit code, filesystem result, cleanup result, and PASS/FAIL/BLOCKED status for each case.

## Test data

| Name | Value |
|---|---|
| Agent RID | `ri.aip-agents..agent.732cd5b4-7ca7-4219-aabb-6e976faf63b1` |
| Agent version | `1.0` |
| Alias inputs | `Demo Alias`, `demo-alias`, `locked-alias`, `missing-alias` |
| Session RID | `ri.aip-agents..session.292db3b2-b653-4de6-971c-7e97a7b881d6` |
| Message ID | `00f8412a-c29d-4063-a417-8052825285a5` |
| Trace ID | `12345678-1234-5678-1234-123456789abc` |
| Cancel response | `**Stopped by operator**` |
| Parameter inputs | `{}` |
| User input | `{"text": "sentinel-prompt-secret"}` |
| Context override | `[]` and `[{"type":"functionRetrievedContext","functionRid":"ri.functions.main.function.01234567-89ab-cdef-0123-456789abcdef","functionVersion":"1.0","retrievedPrompt":"sentinel-context-secret"}]` |
| Pagination | page size `2`, initial token `cursor-001`, batch sizes `1`, `2`, `40`, `41` |
| Download limit | `5` bytes |
| Byte payloads | empty; `abc`; `abcde`; `abcdefghi` |
| Secret sentinels | `sentinel-token-secret`, `sentinel-prompt-secret`, `sentinel-context-secret`, `sentinel-response-secret`, `sentinel-attribution-rid` |
| Session age boundaries | 6 days 23:59:59; exactly 7 days; more than 7 days |

## Command and route inventory

Every inventory row is exercised by AIP-TC-001 through AIP-TC-008. Unless a case states otherwise, success writes one formatted result to stdout, writes no application data to stderr, exits `0`, leaves only documented session/download effects, and removes temporary fixtures during cleanup.

| CLI command | Exact public SDK route and method | Required forwarding checks |
|---|---|---|
| `agent all-sessions` | `client.aip_agents.Agent.with_raw_response.all_sessions` | Paging options and `request_timeout` only |
| `agent get ri.aip-agents..agent.732cd5b4-7ca7-4219-aabb-6e976faf63b1 --version 1.0` | `client.aip_agents.Agent.get` | `agent_rid`, optional `version`, timeout |
| `agent-version get ri.aip-agents..agent.732cd5b4-7ca7-4219-aabb-6e976faf63b1 1.0` | `client.aip_agents.Agent.AgentVersion.get` | Both positionals and timeout |
| `agent-version list ri.aip-agents..agent.732cd5b4-7ca7-4219-aabb-6e976faf63b1` | `client.aip_agents.Agent.AgentVersion.with_raw_response.list` | Agent RID, paging options, timeout |
| `session blocking-continue --alias demo-alias --parameter-inputs-json ... --user-input-json ...` | `client.aip_agents.Agent.Session.blocking_continue` | Stored agent/session RIDs, decoded objects, optional context list and trace ID |
| `session cancel --alias demo-alias --message-id 00f8412a-c29d-4063-a417-8052825285a5 --response "**Stopped by operator**"` | `client.aip_agents.Agent.Session.cancel` | Stored RIDs, message ID, scalar response unchanged, timeout |
| `session create --alias "Demo Alias" --agent-rid ri.aip-agents..agent.732cd5b4-7ca7-4219-aabb-6e976faf63b1 --agent-version 1.0` | `client.aip_agents.Agent.Session.create` | Agent RID, optional version, timeout |
| `session delete --alias demo-alias` | `client.aip_agents.Agent.Session.delete` | Stored RIDs and timeout |
| `session get --alias demo-alias` | `client.aip_agents.Agent.Session.get` | Stored RIDs and timeout |
| `session list ri.aip-agents..agent.732cd5b4-7ca7-4219-aabb-6e976faf63b1` | `client.aip_agents.Agent.Session.with_raw_response.list` | Agent RID, paging options, timeout |
| `session rag-context --alias demo-alias --parameter-inputs-json ... --user-input-json ...` | `client.aip_agents.Agent.Session.rag_context` | Stored RIDs and decoded objects |
| `session streaming-continue --alias demo-alias --parameter-inputs-json ... --user-input-json ...` | `client.aip_agents.Agent.Session.streaming_continue` | Stored RIDs, decoded inputs, optional fields, timeout; eager bytes go to download handler |
| `session update-title --alias demo-alias --title "QA title"` | `client.aip_agents.Agent.Session.update_title` | Stored RIDs, title, timeout |
| `content get --alias demo-alias` | `client.aip_agents.Agent.Session.Content.get` | Stored RIDs and timeout |
| `session-trace get --alias demo-alias --session-trace-id 12345678-1234-5678-1234-123456789abc` | `client.aip_agents.Agent.Session.SessionTrace.get` | Stored RIDs, trace ID positional, timeout |
| `session purge` | `SessionManager.purge()` | No SDK client, timeout, or remote deletion |

## Test cases

### AIP-TC-001 - Catalog, parser, help, and local count

- Type: positive, structural, negative parser.
- Given the installed module and launcher, when the catalog and parser are inspected, then exactly 15 unique SDK specifications and one separate local purge command exist.
- Inputs/commands: inspect `OP_SPECS`; parse every inventory command; run root, resource, and operation `--help`; run missing resource/operation, missing required arguments, invalid choices/types, empty required text, and unknown flags.
- Expected: all help commands exit `0`; all 16 commands parse; purge is absent from `OP_SPECS`; invalid syntax writes one JSON error envelope to stdout and exits `1` before config/client/filesystem work; stderr has no argparse usage error or traceback.
- Filesystem/cleanup: no paths created; restore arguments and capture streams.
- Traceability: story AC 1, 2, 12, 13; catalog and parser matrix rows.

### AIP-TC-002 - Agent command dispatch

- Type: positive, negative SDK failure.
- Given public `Agent` fakes, when `agent all-sessions` and `agent get` run, then each resolves the exact `Agent` object and forwards only documented values.
- Inputs/commands: inventory commands with and without `--version`, CLI timeout override, and default timeout; inject representative 404 on `get`.
- Expected: successful model/list output appears once on stdout with exit `0`; page metadata appears once on stderr for `all-sessions`; `get` forwards no paging fields; 404 produces structured exit `4`; no client flattening or extra keyword is accepted.
- Filesystem/cleanup: cleanup runs once; no session/download mutation; reset SDK fake.
- Traceability: story AC 2, 3, 12; Agent matrix row.

### AIP-TC-003 - Agent-version command dispatch

- Type: positive and route identity.
- Given distinct `Agent` and `Agent.AgentVersion` fakes, when version `get` and `list` run, then neither call can succeed through a flattened or sibling client.
- Inputs/commands: inventory version commands, optional pagination fields, timeout override.
- Expected: `get(agent_rid, agent_version_string, request_timeout=...)`; raw `list(agent_rid, page_size=..., page_token=..., request_timeout=...)`; stdout and stderr separation follows the common contract; exit `0`.
- Filesystem/cleanup: cleanup once, no command-specific file mutation; clear calls.
- Traceability: story AC 1 through 3; nested routing and Agent versions matrix rows.

### AIP-TC-004 - Session create, canonical alias, and optional version

- Type: positive, boundary.
- Given no active canonical alias, when session create returns a Session RID, then local state is atomically published under the normalized alias.
- Inputs/commands: create inventory command with `Demo Alias`, with and without version; remote model has `rid: ri.aip-agents..session.292db3b2-b653-4de6-971c-7e97a7b881d6`; active-session counts of five and six.
- Expected: exact `Agent.Session.create(agent_rid, agent_version?, request_timeout)` call; stdout JSON contains canonical alias and safe state but no `session_token`; exit `0`; six active sessions produce only the approved warning; state file has restrictive permissions, `active` status, null token, and contained canonical path.
- Filesystem/cleanup: load and verify state, then purge temporary sessions.
- Traceability: story AC 2, 4, 5, 12; session-create and state matrix rows.

### AIP-TC-005 - Nine alias-bound routes and sanitized use state

- Type: positive, structural, privacy.
- Given one valid alias record, when each of the nine post-create alias commands runs, then it loads stored `agent_rid` and `session_id`, reaches the exact nested route, and records sanitized usage.
- Inputs/commands: blocking-continue, cancel, delete, get, rag-context, streaming-continue, update-title, content get, and session-trace get from the inventory.
- Expected: exact arguments from stored state; only documented optional fields forwarded; one history item with timestamp, operation, and success boolean; `last_used_at` advances; delete marks state `completed`; history excludes arguments, prompts, contexts, responses, exception text, and tokens; success output/metadata follow each command contract; exit `0`.
- Filesystem/cleanup: compare state before/after each isolated command; delete temporary session and download roots.
- Traceability: story AC 2, 4, 12; alias-bound, state, nested-routing, and privacy matrix rows.

### AIP-TC-006 - Cancel response is an unchanged scalar

- Type: positive, boundary, regression.
- Given `session cancel`, when `--response` is omitted, empty, plain text, or Markdown, then the CLI never JSON-decodes it.
- Inputs/commands: cancel without response; `--response ""`; `--response "Stopped"`; inventory Markdown value; JSON-looking string `'{"x":1}'`.
- Expected: omitted option forwards `None` by omission; supplied values reach `response: str` byte-for-character, including empty and JSON-looking strings; message ID remains required; stdout contains cancel result; stderr contains no response text; exit `0` unless SDK rejects the scalar, in which case its mapped structured error remains primary.
- Filesystem/cleanup: usage history contains no response value; remove alias fixture.
- Traceability: story AC 2, 4, 12; parser and JSON-input matrix rows.

### AIP-TC-007 - JSON input shapes and pre-client rejection

- Type: positive, negative, boundary.
- Given exchange commands, when structured input is parsed, then object fields accept objects, context override accepts only an array of objects, and cancel response remains outside JSON validation.
- Inputs/commands: empty/non-empty objects; empty/list-of-object contexts; malformed JSON; array for object; scalar or mixed array for contexts.
- Expected: valid values reach SDK as decoded Python objects; every invalid value writes one JSON user-input envelope to stdout, exits `1`, and performs no ACL scope, client construction, SDK call, alias read, or download creation; stderr contains no input contents.
- Filesystem/cleanup: assert no command-specific file change; clear sentinel inputs.
- Traceability: story AC 2, 12; JSON-input and privacy matrix rows.

### AIP-TC-008 - Required scalars and timeout boundaries

- Type: negative and boundary.
- Given documented scalar arguments and timeouts, when values are validated, then whitespace-only required values and timeouts outside 1 through 3600 are rejected.
- Inputs/commands: every required scalar as whitespace where parser permits; timeouts `1`, `30`, `3600`, `0`, `3601`, negative, and non-integer; purge with an attempted `--timeout`.
- Expected: valid boundaries reach retry and SDK unchanged; invalid values exit `1` with one stdout JSON envelope before client work; purge rejects timeout as parser input because it is local; stderr has no traceback or secrets.
- Filesystem/cleanup: cleanup may perform only mandatory expired-record maintenance after successful parsing/config; no command-specific mutation on validation failure.
- Traceability: story AC 2, 12; invocation and parser contracts.

### AIP-TC-009 - Alias collision and missing or corrupt records

- Type: negative, filesystem.
- Given an active canonical alias, missing alias, or corrupt record, when an alias command runs, then the CLI fails without unsafe remote work.
- Inputs/commands: create `Demo Alias` followed by create `demo-alias`; alias-bound get for missing and corrupt aliases; reserved/traversal alias inputs.
- Expected: collision exits with structured input/conflict mapping and makes no second remote create; missing alias exits `4`; corrupt/unsafe alias follows SessionManager's structured mapping; no prompt/token leak; ACL has already approved, but client and SDK calls do not occur for load failures.
- Filesystem/cleanup: original active record remains unchanged; corrupt records follow cleanup contract; remove temporary root.
- Traceability: story AC 4, 5, 12; session-create and alias-bound matrix rows.

### AIP-TC-010 - Persistence failure and compensation delete

- Type: negative, recovery.
- Given remote create succeeds but atomic local persistence fails, when compensation runs, then it attempts exactly one remote delete and preserves the persistence error as primary.
- Inputs/commands: create with injected replace/write failure; compensation succeeds, fails, or times out.
- Expected: one create and one non-retried compensation delete with agent/session RIDs; stdout has one server/filesystem error and exit `6`; compensation failure never replaces primary error; logs may include safe RID metadata but no token, response body, or prompt; no partial state file remains.
- Filesystem/cleanup: assert temporary file removal, restore permissions/fault injection, remove root.
- Traceability: story AC 5, 12; session-create compensation matrix row.

### AIP-TC-011 - Session-use failure and persistence precedence

- Type: negative and error precedence.
- Given an alias-bound SDK failure, when failed-use history is recorded, then history persistence is best effort and cannot replace the SDK error; given a successful SDK call followed by state-write failure, the filesystem error becomes primary.
- Inputs/commands: injected 404 plus history-write failure; successful get plus history-write failure.
- Expected: first path exits `4` with no state-write exception leak; second exits `6`; logs contain only approved alias/operation metadata; stdout contains one structured error; no raw SDK data appears.
- Filesystem/cleanup: no corrupt replacement or partial file remains; remove fixture.
- Traceability: story AC 4, 12; state and retry/error matrix rows.

### AIP-TC-012 - Cleanup age, expired status, corruption, and once-per-invocation rule

- Type: boundary, negative, lifecycle.
- Given active, completed, expired, stale, and corrupt records, when any real command runs, then cleanup executes once after logging setup and before command ACL.
- Inputs/commands: ages below, at, and above seven days; explicit expired status; corrupt JSON; one ordinary read and one purge invocation.
- Expected: below-boundary active record remains; expired/inactive-at-boundary records follow the DESIGN-011 seven-day rule; corrupt records are removed safely; cleanup call count is one; logs contain counts and canonical aliases only; requested command then follows its own ACL/result path.
- Filesystem/cleanup: inspect remaining records and locks, then delete temporary session root.
- Traceability: story AC 6, 12; cleanup matrix row.

### AIP-TC-013 - Locked cleanup and point-in-time concurrency

- Type: concurrency and edge.
- Given one alias lock held by another process/thread, when cleanup or purge scans, then it skips the locked alias with a safe warning and processes unlocked records.
- Inputs/commands: locked active/expired aliases, unlocked expired aliases, purge during a command that later writes usage state.
- Expected: no deadlock; locked file survives scan; unlocked eligible files are deleted; purge count includes only deleted unlocked records; a running command may publish a later state update; neither output nor documentation claims transaction isolation.
- Filesystem/cleanup: release all locks in `finally`, purge remaining records, verify no lock artifact remains.
- Traceability: story AC 6, 7; cleanup and purge matrix rows.

### AIP-TC-014 - Local purge success, idempotency, and no SDK work

- Type: positive, boundary.
- Given zero or several unlocked local records, when `session purge` runs, then it deletes current records only and returns their count without remote work.
- Inputs/commands: purge on empty root, populated root, and second invocation; `--format toon` and `--pretty`.
- Expected: JSON stdout always contains `purged_sessions`; counts are exact; exit `0`; no client factory, SDK method, timeout, remote delete, or download creation; stderr contains only safe cleanup/purge diagnostics.
- Filesystem/cleanup: verify removed files and retained locked files; release locks and remove root.
- Traceability: story AC 1, 7; purge and output matrix rows.

### AIP-TC-015 - Purge ACL and pre-mutation ordering

- Type: security and negative.
- Given namespace/operation disabled, read-only, or metadata-only mode, when purge is requested, then ACL denies before `SessionManager.purge()`.
- Inputs/commands: each ACL mode and operation-level override with a seeded record.
- Expected: stdout has structured ACL error and exit `8`; seeded files and prior context remain unchanged; no SDK/client/download action; stderr contains no record contents.
- Filesystem/cleanup: clear every ACL variable, then remove seeded records.
- Traceability: story AC 7, 12; purge-ACL matrix row.

### AIP-TC-016 - Complete metadata-only 6/9 decision matrix

- Type: security, positive and negative.
- Given metadata-only mode and packaged policy, when all SDK operations are checked, then exactly six are permitted and nine blocked; purge is blocked separately.
- Inputs/commands: evaluate every catalog row plus purge through the real guard and CLI boundary.
- Expected: permitted are `agent.get`, both `agent_version` operations, `session.get`, `session.list`, and `session_trace.get`; blocked are the other nine SDK operations; purge exits `8`; denial occurs before alias/client/filesystem work; missing packaged policy fails closed.
- Filesystem/cleanup: no denied-operation mutation; restore policy/environment state.
- Traceability: story AC 7, 8, 12, 13; Tier-3 and purge-ACL matrix rows.

### AIP-TC-017 - Read-only classification and ACL precedence

- Type: security and full decision matrix.
- Given read-only mode, when every command is evaluated, then seven remote writes and local purge are blocked while reads remain permitted unless a stronger namespace/operation disable applies.
- Inputs/commands: all inventory commands under the three supported ACL scopes: global, namespace, and operation.
- Expected: writes blocked are blocking-continue, cancel, create, delete, rag-context, streaming-continue, update-title, and purge; reads follow policy; strongest override wins; denial exits `8` before alias read, client scope, SDK call, or command-specific mutation.
- Filesystem/cleanup: clear ACL variables and temporary state.
- Traceability: story AC 7, 8, 12; read-only matrix row and ADR-007.

### AIP-TC-018 - One page, continuation, EOF, and metadata

- Type: positive and edge.
- Given each of the three raw paged routes, when no batch count or a continuation token is supplied, then exactly one decoded server page is fetched and the returned cursor is preserved.
- Inputs/commands: agent all-sessions, agent-version list, and session list; populated and empty pages; initial and resumed cursors.
- Expected: exact raw method and positional arguments; one decode and one server call; stdout contains items once; stderr emits metadata once after stdout with exact `pages_fetched`, `total_items`, `page_size`, and remaining token; exit `0`; no private iterator fields are read.
- Filesystem/cleanup: clear page fakes and captured streams.
- Traceability: story AC 3, 12; pagination and output matrix rows.

### AIP-TC-019 - Exact batch count, early EOF, and 40-page cap

- Type: positive and boundary.
- Given deterministic cursor chains, when `--batch-pages` requests 2, 40, or 41 pages, then calls follow returned cursors, stop at EOF, and never fetch page 41.
- Inputs/commands: all three paged commands with full and early-EOF chains.
- Expected: exact actual call count; 41 request capped at 40; stdout has no duplicate items; stderr reports successful totals once and retains page-41 cursor when applicable; exit `0`.
- Filesystem/cleanup: reset cursor chains and captures.
- Traceability: story AC 3; pagination matrix row.

### AIP-TC-020 - Pagination retry restarts complete attempt

- Type: resilience.
- Given page two fails transiently after page one succeeds, when RetryHandler retries, then a fresh helper restarts from the original cursor.
- Inputs/commands: each paged route with call order page one success, page two 503, page one success, page two success.
- Expected: no partial stdout/stderr from failed attempt; no duplicate final items; metadata reports only two successful pages once; B3 values remain stable across attempts; exit `0`.
- Filesystem/cleanup: clear retry/cursor state.
- Traceability: story AC 3, 10, 12; pagination-retry, retry, and B3 matrix rows.

### AIP-TC-021 - Eager-byte persistence boundaries and forced JSON

- Type: positive and boundary.
- Given `streaming_continue()` returns eager bytes, when payload length is empty, below, equal to, or above the configured limit, then BinaryDownloadHandler stores at most the limit and returns its standard JSON envelope.
- Inputs/commands: byte payload table, limit five, all format choices, safe output filename.
- Expected: SDK returns before adapter starts; handler receives one async byte chunk and unavailable headers as `None`; empty/below/equal payloads preserve their available bytes; above-limit stores `abcde` and reports truncation/checksums per handler contract; stdout is JSON even with `--format toon`; no payload bytes appear in stdout/stderr/logs; exit `0`; no bounded SDK-memory or network-streaming claim is made.
- Filesystem/cleanup: verify atomic published file and checksums, then remove download/session roots.
- Traceability: story AC 9, 12; eager-bytes and output matrix rows.

### AIP-TC-022 - Invalid eager type and download failure cleanup

- Type: negative, filesystem, cancellation.
- Given streaming continue returns a non-byte value or publication fails, when persistence runs, then the CLI emits the mapped error and leaves no partial file.
- Inputs/commands: `str`, `bytearray`, `None`; permission/write/replace failure; cancellation during save; unsafe output filenames.
- Expected: a non-bytes SDK result is an unexpected SDK contract failure and exits `6`; an unsafe user filename exits `1`; filesystem failure exits `6`; cancellation exits `5`; one JSON error appears on stdout; stderr/logs contain no payload, prompt, context, token, traceback, or temporary path; no partial publication remains.
- Filesystem/cleanup: restore permissions and cancellation state, remove temporary roots.
- Traceability: story AC 9, 12; eager-bytes, retry/errors, and privacy matrix rows.

### AIP-TC-023 - Real SDK exceptions, retry exhaustion, and ADR-001 errors

- Type: negative, resilience, and installed-SDK compatibility.
- Given real exception factories from installed `foundry_sdk._errors`, when commands run with `RetryHandler(max_retries=2, base_delay=0, jitter=False)`, then only transport, 429, and 503 failures retry and each terminal error uses the required ADR-001 exit code.
- Inputs/commands: import `foundry_sdk._errors` and construct a fresh exception for every attempt with the exact factories below. Use the installed permission export, `PermissionDeniedError`, rather than a stand-in named `PermissionDenied`.

| Installed SDK exception factory | Retry expectation | Terminal CLI expectation |
|---|---|---|
| `UnauthorizedError({})` | No retry; one attempt | Authentication exit `2` |
| `NotAuthenticated()` | No retry; one attempt | Authentication exit `2` |
| `PermissionDeniedError({})` | No retry; one attempt | Permission exit `3` |
| `NotFoundError({})` | No retry; one attempt | Not-found exit `4` |
| `ApiNotFoundError("not found")` | No retry; one attempt | Not-found exit `4` |
| `BadRequestError({})` | No retry; one attempt | User-input exit `1` |
| `ConflictError({})` | No retry; one attempt | User-input exit `1` |
| `TimeoutError()` from `foundry_sdk._errors` | Retry as transport timeout; success on attempt three exits `0`; persistent failure makes three attempts | Timeout exit `5` after exhaustion |
| `ConnectionError()` from `foundry_sdk._errors` | Retry as transport failure; success on attempt three exits `0`; persistent failure makes three attempts | Server/transport exit `6` after exhaustion |
| `EnvironmentNotConfigured("missing environment")` | No retry; one attempt | Configuration exit `9` |
| `SDKInternalError("internal")` | No retry; one attempt | Server exit `6` |
| `RateLimitError("rate limited", "test")` | HTTP 429 retries; success on attempt three exits `0`; persistent failure makes three attempts | Exhausted-rate-limit exit `7`, with `http_status: 429` |
| `ServiceUnavailable("unavailable", "test")` | HTTP 503 retries; success on attempt three exits `0`; persistent failure makes three attempts | Server exit `6`, with `http_status: 503`, after exhaustion |

- Expected: each non-retryable factory produces one SDK attempt. Each retryable recovery produces one result only, no failed-attempt stdout, and exactly three attempts. Each exhausted retry produces one JSON error envelope on stdout after three attempts. Local parser/input, ACL, filesystem, and cancellation fixtures still cover exits `1`, `8`, `6`, and `5`. Diagnostics are safe NDJSON on stderr; no exception secret, raw traceback, or duplicate result appears.
- Filesystem/cleanup: assert failed attempts leave no partial download or session state; restore retry configuration and clear exception factories, output captures, and fault injection.
- Traceability: story AC 10, 12; retry/errors matrix row.

### AIP-TC-024 - B3 enabled, disabled, retry stability, and restoration

- Type: tracing, concurrency, failure isolation.
- Given tracing configurations and prior SDK context, when client creation and calls run, then one SDK-native B3 context covers creation and all retries and prior values are restored.
- Inputs/commands: enabled/disabled tracing; concurrent invocations; recovered retry; SDK error, timeout, cancellation, and formatter failure; preset prior B3 values.
- Expected: enabled outbound captures contain valid `X-B3-TraceId`, `X-B3-SpanId`, and `X-B3-Sampled`; values match across one invocation's attempts; disabled calls add none; concurrent calls stay isolated; no `traceparent` or `tracestate`; prior values restore after every path.
- Filesystem/cleanup: reset ContextVar tokens in `finally` and clear tracing variables.
- Traceability: story AC 10, 12; B3 matrix row.

### AIP-TC-025 - Attribution opt-out and nested-scope restoration

- Type: privacy and context isolation.
- Given global attribution RIDs and an existing attribution context, when any AIP request runs, then factory scope and client creation both suppress attribution and restore the prior value.
- Inputs/commands: one read and one write; nested include-attribution scope; success, SDK failure, timeout, cancellation, and formatter failure.
- Expected: no AIP request contains an attribution RID; scoped value is `None`; nested scope restores outer AIP suppression; invocation exit restores the pre-existing value exactly; B3 remains independent; no configured RID appears in stdout/stderr/logs.
- Filesystem/cleanup: reset attribution ContextVar tokens and variables.
- Traceability: story AC 11, 12; attribution and privacy matrix rows.

### AIP-TC-026 - Output selection and stream separation

- Type: positive, output, privacy.
- Given objects, empty/uniform/heterogeneous lists, purge output, and binary metadata, when formats are selected, then ADR-004 and fixed-JSON rules apply.
- Inputs/commands: `--format json|toon|auto`, `--pretty`, all result shapes, remaining pagination cursor.
- Expected: objects and empty/heterogeneous lists use JSON in auto; uniform non-empty lists may use TOON; purge and streaming metadata always use JSON; success/error data is on stdout; pagination metadata and NDJSON diagnostics only are on stderr; each appears once in defined order; exit `0` for success.
- Filesystem/cleanup: clear captures and remove any generated files.
- Traceability: story AC 3, 7, 9, 12; output matrix row.

### AIP-TC-027 - Privacy and import side effects

- Type: security and structural.
- Given secret sentinels and guarded side-effect constructors, when commands fail or packages/launchers import, then sensitive values and import-time side effects are absent.
- Inputs/commands: import package and Claude launcher; inject prompts, contexts, response bytes, session token, attribution RID, cursor, and exception secret through success and failure paths.
- Expected: imports do not load config, create directories, set SDK contexts, create clients, open network connections, or write output; stdout/stderr/logs/history exclude all secret sentinels except user-requested safe result fields; unexpected errors use generic message; no traceback.
- Filesystem/cleanup: compare directory and context snapshots, clear sentinels.
- Traceability: story AC 4, 6, 10 through 13; privacy and imports matrix rows.

### AIP-TC-028 - Wheel, editable install, empty CWD, and entry points

- Type: packaging and compatibility.
- Given clean wheel and editable installs, when the console, Claude launcher, and metadata-only probe run from an empty directory, then packaged policy and entry points work independently of repository paths.
- Inputs/commands: build clean archive; inspect wheel; install each form with `--no-deps`; run `foundry-aip-agents --help`, launcher help, and tier-3 probe without `PYTHONPATH`; snapshot existing console scripts.
- Expected: package contains `foundry_cli/aip_agents/metadata-allow-list.md`; both help paths exit `0` and show all 16 commands; policy resolves inside package; 6/9 decisions and purge denial match AIP-TC-016; launcher delegates to packaged `build_parser`, `main`, and `console_main`; prior entry points remain unchanged.
- Filesystem/cleanup: delete isolated environments, build output, and empty CWD after evidence capture.
- Traceability: story AC 13; packaging and imports matrix rows.

### AIP-TC-029 - Python matrix, quality gates, and regression

- Type: regression and delivery gate.
- Given clean Python 3.11 and 3.12 environments, when delivery gates run, then focused and full suites and all static, security, and packaging checks pass.
- Inputs/commands: focused AIP tests; full `pytest` with branch coverage; Ruff; mypy; Bandit; build and package validation using project-defined commands.
- Expected: every command exits `0`; no test failure or blocking defect remains; branch coverage is at least 80%; existing namespace tests and console entry points remain compatible; results from each Python/environment are reported separately.
- Filesystem/cleanup: remove build/coverage artifacts created by the run according to repository practice; retain command output only as TESTEXEC evidence.
- Traceability: story AC 14; regression matrix row.

### AIP-TC-030 - Optional approved non-production smoke

- Type: environment smoke, optional.
- Given explicit approval, synthetic data, and least-privilege non-production credentials, when a small read-only subset runs, then installed routing and authentication integrate without weakening mocked acceptance coverage.
- Inputs/commands: approved metadata-safe reads such as `agent get` and `agent-version list`; unique synthetic RID; bounded page count and timeout.
- Expected: documented success or structured service error with correct code; no destructive/write operation, prompt, content retrieval, purge of another user's state, or credential capture; stdout/stderr follow normal separation.
- Filesystem/cleanup: remove only test-owned local aliases/downloads; revoke temporary credential if provisioned. A blocked live environment does not block routine acceptance because DESIGN-011 permits mocked transport.
- Traceability: environment evidence supplement; story AC 2, 3, 12.

## Traceability matrix

| Requirement area | Story criteria | Cases |
|---|---|---|
| 15 SDK commands plus local purge; parser and exact nested routes | AC 1; AC 2 | AIP-TC-001 through 008 |
| Alias resolution, state, collision, compensation, expiry, corruption, locking, purge | AC 4; AC 5; AC 6; AC 7 | AIP-TC-004 through 015 |
| Scalar cancel response and JSON shape validation | AC 2; AC 12 | AIP-TC-006, 007 |
| Tier 3 six permitted/nine blocked plus purge denial; read-only seven writes | AC 7; AC 8; AC 12 | AIP-TC-015 through 017 |
| Three raw paged routes, cursor, exact N, EOF, cap, retry reset | AC 3; AC 10 | AIP-TC-002, 003, 018 through 020 |
| Eager bytes, boundaries, checksums, atomic cleanup, fixed JSON | AC 9; AC 12 | AIP-TC-005, 021, 022, 026 |
| Retry and ADR-001 errors | AC 10; AC 12 | AIP-TC-011, 020, 022, 023 |
| B3 only, no attribution, concurrency, restoration | AC 10; AC 11 | AIP-TC-020, 024, 025 |
| Output, stderr separation, privacy, import safety | AC 4; AC 6; AC 9; AC 10; AC 11; AC 12 | AIP-TC-005 through 007, 021 through 027 |
| Packaging, empty CWD, Python 3.11/3.12, gates, coverage | AC 13; AC 14 | AIP-TC-028, 029 |
| Approved non-production environment option | Supporting evidence | AIP-TC-030 |

All 14 story acceptance criteria and every row in DESIGN-011's QA matrix have positive coverage and applicable negative, boundary, security, concurrency, or failure-path coverage.

## Execution evidence and approval gate

TESTEXEC-011 must execute AIP-TC-001 through AIP-TC-029. AIP-TC-030 is optional unless the approved environment is available and its use is authorized. Do not substitute developer test results for independent QA evidence.

For each case, record PASS, FAIL, or BLOCKED with environment, exact command, expected and actual stdout, stderr, exit code, SDK call evidence, filesystem effect, cleanup result, and retained artifact reference. Create a BUG-SUB for every failure before TESTEXEC-011 can complete. QA sign-off requires all mandatory cases to pass, all linked defects to be terminal, all 14 acceptance criteria to have passing evidence, and branch coverage to remain at least 80%.

Reviewer: `tech-lead`, acting as the required Tech Lead/Architect reviewer. TESTCASE-011 blocks TESTEXEC-011. TESTEXEC-011 must not start until the reviewer records approval of this complete case set.
