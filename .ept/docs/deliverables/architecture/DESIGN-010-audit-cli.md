# DESIGN-010 - Foundry Audit CLI

| Field | Value |
|---|---|
| Story | DEV-STORY-010 |
| Status | Approved; DESIGN closed |
| Date | 2026-08-01 |
| Scope | `foundry-audit` CLI and Claude skill, two Audit API v2 operations |

## Technical summary

Add an Audit namespace CLI that lists audit log files and downloads one log file through the Foundry Python SDK. The list operation returns metadata and supports exact page-count pagination. The content operation streams into the shared bounded, atomic download handler; it never writes audit content to stdout or logs.

The implementation uses existing common components without changing their public contracts. It adds one package namespace, one console entry point, one Claude skill launcher, and focused tests.

## Operation catalog

| CLI command | SDK route | SDK method | Positional arguments | Options | Result |
|---|---|---|---|---|---|
| `log-file list` | `client.audit.Organization.LogFile` | `with_raw_response.list` | `organization_rid` | `--start-date`, `--end-date`, `--page-size`, `--page-token`, `--batch-pages`, `--timeout`, `--format`, `--pretty` | List of `{ "id": string }` records plus pagination metadata on stderr |
| `log-file content` | `client.audit.Organization.LogFile` | `with_streaming_response.content` | `organization_rid`, `log_file_id` | `--output-filename`, `--timeout`, `--format`, `--pretty` | Binary download metadata envelope; output is always JSON |

Both commands use kebab-case at the CLI boundary and snake_case internally. `OP_SPECS` must contain exactly two unique entries.

### Date contract

`--start-date` and `--end-date` accept strict ISO calendar dates in `YYYY-MM-DD` form and are converted with `datetime.date.fromisoformat()` before SDK dispatch. `--start-date` is required when `--page-token` is absent. A continuation request may omit it when `--page-token` is present. Invalid dates or a missing initial start date are user-input errors with exit code 1.

## Access control

Call `AccessControlGuard(cfg, "AUDIT").check("log_file", operation)` before creating the SDK client or opening a download path.

The approved tier-3 policy is exact:

| SDK path | Metadata-only result |
|---|---|
| `audit.log_file.list` | `PERMITTED` |
| `audit.log_file.content` | `BLOCKED` |

Both operations are reads, so read-only mode permits them unless a more specific operation or namespace override blocks access. Metadata-only mode remains deny-by-default for any unclassified Audit operation. No audit record IDs, content, tokens, request bodies, or response bodies may appear in logs.

## Component breakdown

### Package and CLI

- `src/foundry_cli/audit/__init__.py` and `src/foundry_cli/audit/scripts/__init__.py`: package markers.
- `src/foundry_cli/audit/scripts/foundry_audit_cli.py`: operation catalog, parser, validation, SDK routing, pagination adapter, streamed download, formatting, and exit handling.
- `.claude/skills/foundry-audit/SKILL.md`: two-operation skill contract, arguments, access rules, output rules, and exit-code guidance.
- `.claude/skills/foundry-audit/scripts/foundry_audit_cli.py`: thin launcher that calls packaged `console_main()`.
- `pyproject.toml`: append `foundry-audit = "foundry_cli.audit.scripts.foundry_audit_cli:console_main"`; add matching Ruff E402 and coverage-omit entries if the established namespace pattern still requires them.

### Internal implementation units

```python
OperationSpec = dict[str, Any]

def build_parser() -> argparse.ArgumentParser: ...
def _spec_for(resource: str, operation: str) -> OperationSpec: ...
def _parse_iso_date(value: str | None, *, field: str) -> date | None: ...
def _validate_list_cursor(start_date: date | None, page_token: str | None) -> None: ...
def _get_client(
    cfg: ConfigLoader,
    resource: str,
    factory: AsyncClientFactory | None = None,
) -> Any: ...
def _model_to_dict(value: Any) -> Any: ...
async def _fetch_list_page(
    client: Any,
    *,
    organization_rid: str,
    start_date: date | None,
    end_date: date | None,
    page_size: int,
    page_token: str | None,
    request_timeout: int | None,
) -> dict[str, Any]: ...
async def _list_log_files(
    client: Any,
    args: argparse.Namespace,
    timeout: int | None,
) -> tuple[list[Any], PaginationHelper]: ...
async def _download_content(
    client: Any,
    args: argparse.Namespace,
    timeout: int | None,
    cfg: ConfigLoader,
) -> dict[str, Any]: ...
async def main() -> int: ...
def console_main() -> int: ...
```

Only `build_parser`, `main`, and `console_main` are module-level callable interfaces used outside tests. They require full type annotations and docstrings. `console_main()` owns the event-loop boundary and calls `asyncio.run(main())` once.

## Pagination design

`log-file list` uses `PaginationHelper` for argument validation, the 40-page cap, cursor tracking, and metadata emission. Use the SDK raw-response wrapper for each page so `--batch-pages N` means N server pages, not an estimated number based on item count:

1. Create a new `PaginationHelper` inside each retry attempt. This prevents counters from leaking from a failed attempt into the successful result.
2. Call `client.with_raw_response.list(...)`, await the `AsyncApiResponse`, and decode its `ListLogFilesResponse`.
3. Adapt `response.data` and `response.next_page_token` to the helper's `{ "items": ..., "next_page_token": ... }` page envelope.
4. Fetch at most `batch_pages` pages. Forward `page_size`, the current `page_token`, parsed dates, and `request_timeout` on every request.
5. Return the successful helper with the collected records, then call `helper.emit_metadata()` once after stdout output.

Default behavior fetches one page. When another page exists, stderr contains the metadata separator and JSON with `next_page_token`, `pages_fetched`, `total_items`, and `page_size`. The list itself follows ADR-004: JSON for empty or non-uniform data, TOON only for a uniform non-empty list when format is `auto`.

## Bounded content download

Calling `LogFile.content()` directly would decode the complete response into `bytes` before the CLI can enforce its limit. Do not use that path.

For every attempt, `_download_content()` must:

1. Create `client.with_streaming_response.content(organization_rid, log_file_id, request_timeout=timeout)`.
2. Enter the returned async context manager.
3. Pass `response.aiter_bytes()` to `BinaryDownloadHandler(config=cfg).save()` with namespace `audit`, operation `log_file.content`, and the optional output filename.
4. Pass `content_length=None`, `content_encoding=None`, and `mime_type=None` with the current SDK. `AsyncStreamedApiResponse` has no public headers accessor. Do not read `response._response` or any other private SDK field. If a later supported SDK release adds a documented public headers API, a separate reviewed change may pass those public values to the handler.
5. Leave the SDK response context on success, truncation, cancellation, or exception.
6. Return `DownloadResult.to_dict()` and format it as JSON regardless of `--format`.

The shared handler therefore treats Audit content as unknown length. It writes at most `FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES` and observes at most one extra byte to distinguish an exact-limit response from a truncated response. It publishes through a contained UUID directory and atomic replace. A failed retry attempt must leave no published partial file or temporary file.

## Invocation, retry, errors, output, and logging

Execution order is fixed:

1. Parse arguments, load configuration, and configure `LogSetup`.
2. Resolve the two-entry operation spec and validate dates/cursor rules.
3. Run `AccessControlGuard`.
4. Create one `AsyncClientFactory` and enter `factory.invocation_scope(cfg)` before `factory.create(cfg)`.
5. Resolve `client.audit.Organization.LogFile` inside the scope.
6. Run the complete list pagination attempt or streamed download attempt through `RetryHandler.execute()` while the same invocation scope remains active.
7. Exit the scope, which restores prior SDK trace context in `finally`.
8. Write one success result to stdout. Emit pagination metadata to stderr only for `list`.

When tracing is enabled, the scope sets only SDK-native B3 multi-header context: one 128-bit trace ID, one 64-bit span ID, and sampled value. The same values cover every retry attempt because retries stay inside one scope. Client construction occurs after context entry, and prior `ContextVar` values are restored on success and every failure. The CLI must not claim W3C `traceparent` or `tracestate` support.

Retry HTTP 429 and 503 plus configured transport/timeouts through the shared handler. Preserve ADR-001 mappings: user input 1, authentication 2, permission 3, not found 4, timeout/cancellation 5, server failure 6, exhausted 429 rate limit 7, ACL 8, and configuration 9. Errors use `ErrorSerializer`; no raw exception traceback or audit content may be written outside its configured envelope. NDJSON diagnostics go to stderr through `LogSetup`. Success data and JSON error envelopes go to stdout.

## Packaging and compatibility

This change is additive. Keep every existing console entry point and common-component API unchanged. Editable and wheel installs must expose `foundry-audit`. The `.claude` launcher must delegate to the packaged module and must not copy CLI logic. Importing the package or launcher must not load configuration, create a client, open a network connection, or create download directories.

## Test strategy

### Unit coverage

- Catalog contains exactly two unique operations with the exact nested client route and SDK method names.
- Parser accepts both commands, all declared flags, and `--help`; missing commands return exit code 1.
- Date parsing accepts real ISO dates, rejects malformed/impossible dates, requires a start date only for an initial list request, and passes `date` objects to the SDK.
- List pagination fetches one page by default, forwards a supplied cursor, fetches exactly the requested number of server pages up to 40, stops at EOF, and emits the remaining cursor once.
- Pagination retry starts with fresh counters and produces no duplicate output or metadata.
- ACL uses namespace `AUDIT`, permits `list` and blocks `content` under metadata-only mode, and runs before client creation.
- Routing reaches `client.audit.Organization.LogFile`; tests fail if a flattened or wrong namespace client is used.
- Content uses `with_streaming_response.content`, enters and closes the async response context, and never calls the eager `content()` method.
- Content passes all three unavailable header values as `None`, never reads `response._response`, obeys configured byte bounds through the unknown-length one-byte probe, returns the standard JSON download envelope, removes failed partial files, and ignores TOON selection for that envelope.
- Invocation scope starts before client creation, keeps one B3 context across all retry attempts, and restores prior context after success, timeout, access failure, SDK failure, and formatter failure.
- Retry and error tests cover 429 exhaustion, retryable 503, 403, 404, timeout, malformed input, missing credentials, and an unexpected server error without leaking content or tokens.
- Imports cause no network or filesystem side effects. `console_main()` uses one `asyncio.run()` boundary.
- Packaged entry point and Claude launcher both expose help and propagate exit codes.
- Full regression suite remains above the configured 80% branch-coverage gate on Python 3.11 and 3.12.

### QA scenarios

QA must cover the two operations end to end with mocked SDK transport or an approved non-production Foundry environment. Include first-page and continuation flows, empty results, a multi-page result, malformed dates, missing initial start date, tier-3 ACL decisions, unknown-length content below, exactly at, and above the byte limit, retry exhaustion, output stream separation, packaged help, and launcher help. The shared handler's existing tests remain responsible for known-length behavior. Live credentials are not required for routine execution evidence.

## Grooming decomposition

All subtasks are children of DEV-STORY-010 through `ParentChild`/containment links.

| Type | Title | Assignee role | Estimate | Description and testable acceptance criteria |
|---|---|---|---:|---|
| DESIGN | Design Foundry Audit CLI | `tech-lead` | 4 h | Produce and approve DESIGN-010. AC: operation, streaming, pagination, ACL, B3, retry, output, packaging, test, risk, and estimate contracts are explicit; document index links the artifact; no unresolved technical question remains. |
| DEV | Implement Foundry Audit CLI and skill | `python-developer` | 10 h | Add Audit package, two-operation CLI, raw-page adapter, streamed bounded download, Claude skill/launcher, and entry point. AC: both routes and inputs match catalog; ACL precedes client creation; invocation scope encloses client/retries; content is never eagerly read; unavailable header values are passed as `None`; no private SDK field is accessed; lint/type checks pass. |
| UNITTEST | Add Audit CLI unit and integration tests | `python-developer` | 7 h | Add `tests/test_foundry_audit_cli.py` and `tests/test_audit_console_wrapper.py`. AC: every unit-coverage item above has an assertion; the stream double exposes only public `AsyncStreamedApiResponse` behavior; tests assert all three handler header arguments are `None` and fail on private-field access; targeted suite passes; repository coverage stays at least 80%. |
| CODEREVIEW | Review Foundry Audit CLI implementation | `tech-lead` | 3 h | Review DEV result for correctness, architecture, OWASP controls, streaming bounds, retries, B3 lifetime, packaging, and maintainability. AC: reviewer is not DEV implementer; all findings are resolved or tracked; approved commit passes targeted tests, Ruff, mypy, and diff checks. |
| TESTCASE | Design Foundry Audit CLI QA cases | `qa-engineer` | 4 h | Create traceable cases from story AC and DESIGN-010. AC: cases cover both operations and every QA scenario above with inputs, expected stdout/stderr, exit code, prerequisites, and cleanup. |
| TESTEXEC | Execute Foundry Audit CLI QA suite | `qa-engineer` | 4 h | Run approved cases after development review. AC: results record command, environment, expected/actual result, and evidence; failures create BUG-SUB children; QA sign-off requires no open blocking defect. |
| DEVOPS | Package and verify Foundry Audit entry points | `devops-engineer` | 2 h | Validate additive packaging and deployment readiness. AC: wheel/editable install exposes `foundry-audit`; packaged and Claude launcher help return 0; existing entry points remain; CI Python 3.11/3.12 gates pass; rollback is removal of additive Audit files/entry point only. |

### Link and dependency plan

- DESIGN blocks activation of DEV, UNITTEST, CODEREVIEW, TESTCASE, TESTEXEC, and DEVOPS until this design is approved and closed.
- DEV and UNITTEST may run together after DESIGN closes.
- Create one `RelatesTo` link between DEV and CODEREVIEW. While development is active, DEV blocks CODEREVIEW; remove or let the terminal-source rule clear that semantic block when DEV is ready for review. CODEREVIEW cannot close before reviewing the exact DEV result.
- TESTCASE may run in parallel with DEV after DESIGN closes.
- TESTEXEC depends on DEV, UNITTEST, CODEREVIEW, and TESTCASE reaching their required completed states.
- DEVOPS depends on successful TESTEXEC and performs deployment-stage packaging verification.
- Reviewer (`tech-lead`) is distinct from implementer (`python-developer`).

## Estimate and sprint fit

Story estimate: 8 points, 34 planned hours across roles.

The work fits one sprint. Only two SDK operations are added, shared infrastructure already exists, and TESTCASE can overlap DEV/UNITTEST. Streaming response handling and exact page pagination account for most of the estimate. The estimate assumes no change to `BinaryDownloadHandler`, `PaginationHelper`, tracing, ACL policy, CI workflows, or Foundry SDK version.

## Risks and assumptions

| Risk or assumption | Treatment |
|---|---|
| Audit content may exceed memory limits if the decoded SDK method is used | Require `with_streaming_response.content` and assert eager method is never called. |
| Current streamed response exposes no public headers accessor | Pass the three handler header values as `None`, rely on the unknown-length probe, and prohibit private SDK field access. |
| Retry after a later-page failure could retain counters | Construct pagination state inside each retry attempt and publish only the successful state. |
| Audit data is security-sensitive | Persist only through bounded contained paths; never print or log content; run ACL before SDK/filesystem work. |
| SDK returns `data`, while shared helper expects `items` | Keep a small namespace adapter; do not modify shared helper for one response shape. |
| A supplied continuation token may replace the initial-date requirement | Enforce SDK contract: start date required only when no page token is supplied. |
| W3C propagation is out of scope | Implement and test B3 multi-header context only, per resolved decision and DESIGN-005. |
| SDK or common-component contract changes | Treat as a separate design review; do not expand this story silently. |

## Story acceptance criteria

1. **Given** valid configuration and an initial `log-file list` request with `--start-date`, **when** the command succeeds, **then** it calls `audit.Organization.LogFile`, returns the requested page data, emits any continuation token on stderr, and exits 0.
2. **Given** `--batch-pages N`, **when** more pages exist, **then** the command fetches at most N actual server pages, never more than 40, aggregates records once, and reports accurate page/item counts.
3. **Given** an initial list request without `--start-date` or a malformed ISO date, **when** validation runs, **then** no client is created, a JSON user-input error is written to stdout, and exit code 1 is returned.
4. **Given** a permitted `log-file content` request with the current SDK, **when** content arrives, **then** the CLI streams through `BinaryDownloadHandler`, passes `None` for content length, content encoding, and MIME type, never accesses `response._response`, stores no more than the configured bound, observes at most one probe byte, closes the response, and returns the standard JSON download envelope.
5. **Given** metadata-only mode, **when** `list` is called, **then** access is permitted; **when** `content` is called, **then** it is blocked before client or filesystem work with exit code 8.
6. **Given** tracing enabled, **when** an SDK request retries, **then** client creation and every attempt share one B3 context, no W3C claim/header is added, and prior context is restored afterward.
7. **Given** an SDK, timeout, configuration, or filesystem failure, **when** the command exits, **then** it uses the ADR-001 code and JSON error envelope, leaves no failed partial download, and exposes no credential or audit content in stdout/stderr logs.
8. **Given** an installed build, **when** users invoke `foundry-audit --help` or the Claude launcher help, **then** both return 0 and list exactly the two operations without changing existing namespace entry points.

## DESIGN completion evidence

- Technical scope: two exact operations and nested SDK routes defined.
- Interfaces: parser, routing, pagination, streaming, and entry-point signatures defined.
- Security: metadata allow-list behavior, bounded persistence, private SDK field prohibition, and sensitive-log exclusions defined.
- Cross-cutting behavior: pagination, retry, ADR exit codes, JSON/TOON, NDJSON, and B3 lifecycle defined.
- Delivery: files, packaging, tests, estimates, roles, links, dependencies, and sprint fit defined.
- Open design questions: none. B3-only tracing is treated as resolved input.
- DEVOPS applicability: yes, because this story adds a packaged console script and Claude launcher that require install and smoke verification.

## Execution-plan comment

Use this comment on DEV-STORY-010 after creating the subtasks:

```markdown
## Grooming execution plan

DESIGN-010 defines both Audit operations and is approved and DESIGN is closed. Planned effort is 8 story points / 34 hours. Work fits one sprint.

- DEV implements the two-operation package, exact-page list pagination, bounded streamed content download, skill launcher, and console entry point.
- UNITTEST covers the catalog, parser, SDK route, pagination/retry isolation, streaming bounds, ACL, B3 scope, errors, imports, and packaging.
- CODEREVIEW is assigned to tech-lead, distinct from python-developer. DEV and CODEREVIEW have RelatesTo; DEV blocks review until its implementation result is ready.
- TESTCASE can proceed after DESIGN closes and in parallel with development. TESTEXEC waits for DEV, UNITTEST, CODEREVIEW, and TESTCASE.
- DEVOPS applies because a new packaged command and Claude launcher need install and smoke verification; it waits for successful TESTEXEC.

All children use DEV-STORY-010 as parent. DESIGN blocks child activation until closed. No open design question remains. B3-only tracing is the approved scope; W3C propagation is excluded.
```
