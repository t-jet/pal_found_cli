# TESTCASE-008 - Foundry Functions CLI QA test cases

## Scope

These test cases cover DEV-STORY-008, the `foundry-functions` CLI for seven `foundry_sdk.v2.functions` operations:

- `query`: `execute`, `get`, `get-by-rid`, `get-by-rid-batch`, `streaming-execute`
- `value-type`: `get`
- `version-id`: `get`

The cases cover parser exposure, help output, SDK dispatch, JSON argument decoding, boolean flags, `FUNCTIONS` ACL namespace checks, output formats, byte response handling for `streaming_execute`, ADR-001 exit codes, console entry point metadata, and `.claude` skill launcher behavior.

## Preconditions

- Python 3.11+ environment with project dependencies installed.
- Repo root is the working directory.
- Implementation files exist after DEV-008:
  - `src/foundry_cli/functions/scripts/foundry_functions_cli.py`
  - `.claude/skills/foundry-functions/SKILL.md`
  - `.claude/skills/foundry-functions/scripts/foundry_functions_cli.py`
  - `tests/test_foundry_functions_cli.py`
  - `tests/test_functions_console_wrapper.py`
- `pyproject.toml` exposes `foundry-functions = "foundry_cli.functions.scripts.foundry_functions_cli:console_main"` under `[project.scripts]`.
- Unit and QA execution may use mocked SDK clients, auth/config, ACL, retry, and output formatting. Live Foundry credentials are not required for this test design.

## Test scenarios

| ID | Scenario | Given | When | Then |
|---|---|---|---|---|
| FN-TC-001 | Operation catalog completeness | The functions CLI module is imported | Inspect `OP_SPECS` | Exactly seven unique `(resource, operation)` pairs exist and match DESIGN-008. |
| FN-TC-002 | Parser accepts every operation | `build_parser()` is available | Parse each command with required positionals and representative options | Parser accepts all seven commands and maps kebab-case CLI names to SDK operation names. |
| FN-TC-003 | Help paths | Parser is available | Parse root help, resource help, and operation help with `--help` | Each help path exits `0` and prints usage without loading config or SDK clients. |
| FN-TC-004 | Query execute dispatch | Mocked `client.functions.Query.execute` is awaitable | Run `query execute query-name --parameters '{"x":1}' --attribution '{"job":"qa"}' --branch master --preview --version v1` | SDK method is awaited once with decoded JSON args, optional strings, `preview=True`, and `request_timeout`. |
| FN-TC-005 | Query get dispatch | Mocked `client.functions.Query.get` is awaitable | Run `query get query-name --preview --version v1` | SDK method receives `query_api_name`, `preview=True`, `version`, and `request_timeout`. |
| FN-TC-006 | Query get-by-rid dispatch | Mocked `client.functions.Query.get_by_rid` is awaitable | Run `query get-by-rid --rid ri.function.query.test --include-prerelease --preview --version v1` | SDK method receives `rid`, `include_prerelease=True`, `preview=True`, `version`, and `request_timeout`. |
| FN-TC-007 | Query get-by-rid-batch dispatch | Mocked `client.functions.Query.get_by_rid_batch` is awaitable | Run `query get-by-rid-batch '{"rids":["ri.function.query.test"]}' --preview` | Body is JSON-decoded before dispatch; SDK method receives body, `preview=True`, and `request_timeout`. |
| FN-TC-008 | Query streaming-execute dispatch | Mocked `client.functions.Query.streaming_execute` returns bytes | Run `query streaming-execute query-name --parameters '{"limit":1}' --ontology ontology --preview` | SDK method receives decoded JSON args, `ontology`, `preview=True`, and `request_timeout`; stdout emits byte-length envelope, not raw bytes. |
| FN-TC-009 | ValueType routing | Mocked `client.functions.ValueType.get` is awaitable | Run `value-type get ri.functions.value-type.test --preview` | Client routing resolves `ValueType`; SDK method receives `value_type_rid`, `preview=True`, and `request_timeout`. |
| FN-TC-010 | VersionId nested routing | Mocked `client.functions.ValueType.VersionId.get` is awaitable | Run `version-id get ri.functions.value-type.test 1 --preview` | Client routing resolves nested `ValueType.VersionId`; SDK method receives both positionals, `preview=True`, and `request_timeout`. |
| FN-TC-011 | Boolean defaults | Parser receives commands without boolean flags | Run representative `query get`, `query get-by-rid`, and `value-type get` commands | `preview` and `include_prerelease` are omitted or false; SDK kwargs do not send unintended truthy values. |
| FN-TC-012 | JSON argument coverage | Commands expose `parameters`, `attribution`, and `body` | Run valid JSON inputs for `execute`, `streaming-execute`, and `get-by-rid-batch` | Each structured argument is decoded to Python data before SDK dispatch. |
| FN-TC-013 | No pagination hooks | CLI constants are imported | Inspect `PAGINATED_OPS` and parser options | `PAGINATED_OPS` is empty; no operation exposes `--page-size`, `--page-token`, or `--batch-pages`. |
| FN-TC-014 | ACL namespace | `AccessControlGuard.check` is patched to capture args | Run any valid function command | ACL check uses namespace `FUNCTIONS` and the operation key such as `query.execute` before SDK dispatch. |
| FN-TC-015 | ACL blocks operation | `AccessControlGuard.check` raises `AccessControlError` | Run `query get query-name` | SDK is not called; stdout contains serialized error JSON; exit code is `8`. |
| FN-TC-016 | Metadata-only allow-list | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` | Run `query get`, `query get-by-rid`, `query get-by-rid-batch`, `value-type get`, and `version-id get` | Allow-listed metadata reads pass ACL. |
| FN-TC-017 | Metadata-only blocks execution | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` | Run `query execute` and `query streaming-execute` | ACL blocks both execution operations and CLI exits `8`. |
| FN-TC-018 | JSON output mode | SDK returns dict-like data | Run a successful operation with `--format json` | Stdout is valid JSON; exit code is `0`. |
| FN-TC-019 | TOON output mode | SDK returns a uniform list of dicts | Run a successful operation with `--format toon` | Stdout is TOON-compatible tabular text; exit code is `0`. |
| FN-TC-020 | Auto output selection | SDK returns dicts, empty arrays, scalar arrays, uniform dict arrays, and mixed dict arrays | Run with `--format auto` | Uniform non-empty dict arrays use TOON; other shapes use JSON per ADR-004. |
| FN-TC-021 | Model conversion | SDK returns Pydantic-like objects, dicts, lists, bytes, and `None` | Call `_model_to_dict()` | Output is JSON-serializable; bytes become a byte-length envelope. |
| FN-TC-022 | Missing command | No resource or no operation is provided | Run `main()` | CLI prints help and exits `1`; no SDK client is created. |
| FN-TC-023 | Retry wrapper | First SDK call raises retryable error and second call succeeds | Run valid command through `main()` | Retry handler is used; final stdout contains success payload and exit code is `0`. |
| FN-TC-024 | B3 invocation scope | Async client factory exposes `invocation_scope` | Run a successful operation | CLI enters invocation scope before SDK client creation and leaves it after the call. |
| FN-TC-025 | Console wrapper | `main()` is monkeypatched to return a sentinel code | Call `console_main()` | Console wrapper returns the sentinel code. |
| FN-TC-026 | Packaged module help | Package is importable from `src` | Run `python -m foundry_cli.functions.scripts.foundry_functions_cli --help` | Process exits `0` and lists `query`, `value-type`, and `version-id`. |
| FN-TC-027 | Claude skill launcher | `.claude/skills/foundry-functions/scripts/foundry_functions_cli.py` exists | Run launcher with `--help` | Process exits `0` and delegates to the packaged parser. |
| FN-TC-028 | Editable install console script | Project is installed editable | Run `foundry-functions --help` | Console script exits `0` and prints functions CLI usage. |

## Edge cases

- Empty structured JSON (`{}`) is accepted for `parameters`, `attribution`, and `body`.
- Nested JSON objects and arrays are preserved during dispatch.
- Large parameter payloads near test runner memory limits serialize without truncation.
- `streaming_execute` byte payloads of `b""`, small NDJSON bytes, and non-UTF-8 bytes all produce byte-length envelopes.
- Boolean flags set `True` only when present; repeated flags do not alter semantics.
- Optional trace fields (`trace_parent`, `trace_state`, `transaction_id`) pass through to SDK kwargs without rewriting.
- Timeout uses CLI `--timeout` when present; otherwise config/env defaults apply.
- Concurrent mocked invocations do not share parsed argument state.

## Negative cases

| ID | Case | Expected result |
|---|---|---|
| FN-NEG-001 | Unknown resource or operation | Argparse rejects input or CLI exits `1`; no SDK call occurs. |
| FN-NEG-002 | Missing required positional argument | Parser exits `2` before `main()` dispatch, or `main()` maps user input error to `1` where wrapped. |
| FN-NEG-003 | Malformed JSON for `parameters`, `attribution`, or `body` | Error JSON on stdout; exit `1`; no SDK call occurs. |
| FN-NEG-004 | Missing token or malformed config | Error JSON on stdout; exit `9`. |
| FN-NEG-005 | Authentication failure from SDK | Error JSON on stdout; exit `2`. |
| FN-NEG-006 | Permission denied from SDK | Error JSON on stdout; exit `3`. |
| FN-NEG-007 | Function query or value type not found | Error JSON on stdout; exit `4`. |
| FN-NEG-008 | Timeout from SDK or retry layer | Error JSON on stdout; exit `5`. |
| FN-NEG-009 | Server failure after retry policy | Error JSON on stdout; exit `6`. |
| FN-NEG-010 | Rate limit exhausted | Error JSON on stdout; exit `7`. |
| FN-NEG-011 | ACL disabled, readonly, or metadata-only block | Error JSON on stdout; exit `8`. |

## Expected outputs

- Success: exit `0`; result payload on stdout in JSON, TOON, or auto-selected format.
- User input error: exit `1`; JSON error envelope on stdout.
- Authentication error: exit `2`; JSON error envelope on stdout.
- Permission denied: exit `3`; JSON error envelope on stdout.
- Not found: exit `4`; JSON error envelope on stdout.
- Timeout: exit `5`; JSON error envelope on stdout.
- Server error: exit `6`; JSON error envelope on stdout.
- Rate limit exhausted: exit `7`; JSON error envelope on stdout.
- Access control block: exit `8`; JSON error envelope on stdout.
- Configuration error: exit `9`; JSON error envelope on stdout.
- Byte responses: JSON object containing byte length metadata, not raw byte data.
- Diagnostic logs: NDJSON on stderr and separate from stdout result data.

## Test data

| Name | Value |
|---|---|
| Query API name | `qa.query.sample` |
| Query RID | `ri.function.query.test` |
| Value type RID | `ri.functions.value-type.test` |
| Version ID | `1` |
| Parameters JSON | `{"customerId":"cust-001","limit":1}` |
| Attribution JSON | `{"source":"qa","ticket":"TESTCASE-008"}` |
| Batch body JSON | `{"rids":["ri.function.query.test"]}` |
| Branch | `master` |
| Ontology | `qa-ontology` |
| Version | `v1` |
| Trace parent | `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-00` |
| Trace state | `vendor=value` |
| Transaction ID | `qa-transaction-008` |
| JSON output payload | `{"rid":"ri.function.query.test","apiName":"qa.query.sample"}` |
| TOON output payload | `[{"name":"alpha","type":"string"},{"name":"beta","type":"integer"}]` |
| Streaming bytes | `b'{"event":"row","value":1}\\n'` |

## Review requirement

TESTCASE-008 can move to Resolved only after Tech Lead or Architect approval confirms these scenarios are valid against DEV-STORY-008 and DESIGN-008. Test execution must not begin from this design until that approval is recorded.
