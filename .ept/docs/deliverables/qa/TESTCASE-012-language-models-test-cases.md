# TESTCASE-012 - Foundry Language Models CLI QA test cases

## Scope

These cases cover DEV-STORY-012 and the complete approved surface of
`foundry-language-models`: Anthropic messages and OpenAI embeddings. They verify
exact nested SDK dispatch, every required and optional input, local and SDK
validation boundaries, access control, attribution, B3 tracing, retry and error
behavior, privacy, structural exclusions, packaging, and delivery gates.

Routine acceptance uses mocked async SDK transport and actual installed SDK
models and exception classes. Live credentials and live Foundry access are not
required. An approved non-production smoke is optional and cannot replace the
mandatory mocked evidence.

## Source baseline

- [DESIGN-012](../architecture/DESIGN-012-language-models-cli.md), completed for
  DEV-STORY-012.
- DESIGN-005 and the shared ADR-001, ADR-002, ADR-004, ADR-005, ADR-006, and
  ADR-007 contracts referenced by DESIGN-012.
- Implementation in `src/foundry_cli/language_models/`,
  `.claude/skills/foundry-language-models/`, shared common components, and
  `pyproject.toml`.
- Developer tests in `tests/test_foundry_language_models_cli.py` and
  `tests/test_language_models_console_wrapper.py`. Their fixtures may be reused,
  but their prior results are not independent TESTEXEC evidence.

## Preconditions and evidence contract

- Run mandatory cases in isolated Python 3.11 and 3.12 environments containing
  the project, development dependencies, and pinned `foundry-sdk`.
- Use a nested fake rooted at `client.language_models` with distinct
  `AnthropicModel.messages` and `OpenAiModel.embeddings` async methods. A wrong,
  flattened, raw, or streaming route must fail the fixture.
- Use actual installed SDK model validators for nested invalid-input checks and
  actual `foundry_sdk._errors` classes for error taxonomy checks. Mock network
  transport; no service call or billable inference is permitted.
- Set retry delay to zero, disable jitter, and use two retries unless a case
  states otherwise. Capture attempt number, timeout, attribution, and B3 values.
- Capture stdout, stderr, logs, SDK arguments, context variables, network/client
  constructors, and filesystem changes independently. Do not retain prompt,
  response, vector, credential, token, or attribution sentinel values.
- Use a fresh empty temporary directory for import and packaging cases. Wheel and
  editable checks run without `PYTHONPATH` and install with `--no-deps` from a
  locally built artifact.
- Unless a case states otherwise, success writes one result to stdout, writes no
  application data to stderr, exits `0`, creates no command-specific file, and
  restores all patched arguments, environment variables, contexts, fakes, and
  temporary paths during cleanup.
- TESTEXEC-012 records the commit, dirty/clean worktree state, OS, Python and SDK
  versions, environment type, exact command, expected and actual stdout, stderr,
  exit code, SDK calls, filesystem result, cleanup result, evidence reference,
  and PASS/FAIL/BLOCKED status for every case.

## Test data

| Name | Fixture |
|---|---|
| Anthropic model ID | ` qa-anthropic-model `; original whitespace is forwarded after non-empty validation |
| Embedding model ID | `qa-embedding-model` |
| Minimal messages | `[{"role":"USER","content":[{"type":"text","text":"qa prompt"}]}]` |
| Required messages values | `--max-tokens 64`, default timeout `30` |
| Anthropic optionals | output config `{"effort":"HIGH"}`; stops `["STOP"]`; system object list; temperature `0.2`; thinking `{"type":"disabled"}`; tool choice `{"type":"auto"}`; tools object list; top K `4`; top P `0.9` |
| Embedding input | `["first document","second document"]` |
| Embedding optionals | dimensions `8`; encoding `FLOAT` and `BASE64` |
| Timeout boundaries | `1`, `3600`, invalid `0`, `3601`, and non-integer text |
| Context fixtures | prior attribution `ri.attribution.main.qa.outer`; configured values with surrounding whitespace and empty entries; distinct concurrent RIDs |
| B3 fixtures | valid fixed trace ID, span ID, and sampled value; distinct outer and concurrent contexts |
| Privacy sentinels | `sentinel-prompt-secret`, `sentinel-system-secret`, `sentinel-tool-secret`, `sentinel-image-secret`, `sentinel-document-secret`, `sentinel-vector-secret`, `sentinel-response-secret`, `sentinel-token-secret`, `sentinel-attribution-secret` |

## Command and input inventory

Both rows are exercised with the default and explicit timeout plus JSON, TOON,
auto, and pretty output where applicable.

| CLI command | Exact SDK target | Required input | Optional input |
|---|---|---|---|
| `anthropic-model messages MODEL_ID` | `client.language_models.AnthropicModel.messages` | positional model ID, `--max-tokens`, `--messages-json` | `--output-config-json`, `--stop-sequences-json`, `--system-json`, `--temperature`, `--thinking-json`, `--tool-choice-json`, `--tools-json`, `--top-k`, `--top-p`, `--timeout`, `--format`, `--pretty` |
| `open-ai-model embeddings MODEL_ID` | `client.language_models.OpenAiModel.embeddings` | positional model ID, `--input-json` | `--dimensions`, `--encoding-format FLOAT\|BASE64`, `--timeout`, `--format`, `--pretty` |

Neither call may receive `attribution`, `preview`, `_sdk_internal`, an absent
optional set to `None`, or any unsupported paging, file, session, raw-response,
or streaming argument.

ACL cases use only the supported global, namespace, and operation scopes:

| Control | Canonical variables |
|---|---|
| Enablement | `FOUNDRY_AGENTIC_CLI_ENABLED`; `FOUNDRY_AGENTIC_CLI_LANGUAGE_MODELS_ENABLED`; `FOUNDRY_AGENTIC_CLI_LANGUAGE_MODELS_ANTHROPIC_MODEL_MESSAGES_ENABLED`; `FOUNDRY_AGENTIC_CLI_LANGUAGE_MODELS_OPEN_AI_MODEL_EMBEDDINGS_ENABLED` |
| Read-only | `FOUNDRY_AGENTIC_CLI_READONLY`; `FOUNDRY_AGENTIC_CLI_LANGUAGE_MODELS_READONLY`; `FOUNDRY_AGENTIC_CLI_LANGUAGE_MODELS_ANTHROPIC_MODEL_MESSAGES_READONLY`; `FOUNDRY_AGENTIC_CLI_LANGUAGE_MODELS_OPEN_AI_MODEL_EMBEDDINGS_READONLY` |
| Metadata-only | `FOUNDRY_AGENTIC_CLI_METADATA_ONLY`; `FOUNDRY_AGENTIC_CLI_LANGUAGE_MODELS_METADATA_ONLY` |

## Test cases

### LM-TC-001 - Catalog, parser, help, and exact surface

- Prerequisites: installed package and thin Claude launcher; guarded config,
  client, network, and filesystem constructors.
- Inputs: inspect `OP_SPECS`; run root, resource, and operation help; parse both
  inventory commands; try missing resource/operation/required fields, unknown
  commands and flags, invalid numeric types, invalid encoding/format, and blank
  model ID.
- Action: exercise the packaged parser through module and console boundaries.
- Expected SDK arguments: no SDK lookup or call for help or invalid syntax.
- Expected stdout, stderr, and exit: help exits `0` and names exactly two
  operations; invalid syntax emits one safe ADR-001 JSON envelope to stdout and
  exits `1`; stderr contains no argparse usage dump, input value, or traceback.
- Filesystem and cleanup: no path or context change; restore argv and guards.
- Traceability: AC 1, 4, 12; catalog, parser, and structural-exclusions matrix.

### LM-TC-002 - Anthropic required-only dispatch

- Prerequisites: distinct nested resource fakes; decoded response fixture.
- Inputs: the minimal messages fixture, `--max-tokens 64`, the whitespace-bearing
  model ID, default timeout, and `--format json`.
- Action: invoke `anthropic-model messages` through `main()`.
- Expected SDK arguments: exactly
  `AnthropicModel.messages(" qa-anthropic-model ", max_tokens=64,
  messages=<decoded list>, request_timeout=30)` once; no optional or private
  keyword and no flattened resource access.
- Expected stdout, stderr, and exit: one decoded JSON response on stdout, empty
  application stderr, exit `0`.
- Filesystem and cleanup: no files; reset fake and arguments.
- Traceability: AC 2, 10; Anthropic dispatch and output matrix.

### LM-TC-003 - Every Anthropic optional input

- Prerequisites: direct `_invoke_sdk` fake that records keyword presence and
  values without imposing nested SDK schemas.
- Inputs: all Anthropic required fields and every optional fixture from the test
  data, `--timeout 12`, `--format toon`, and `--pretty`.
- Action: parse, validate, and invoke the messages specification; repeat with
  each optional omitted individually and with all optionals absent.
- Expected SDK arguments: decoded `output_config`, `stop_sequences`, `system`,
  `thinking`, `tool_choice`, and `tools`; unchanged numeric values for
  `temperature`, `top_k`, and `top_p`; `request_timeout=12`; absent keys omitted.
  `attribution`, `preview`, and `_sdk_internal` are never passed.
- Expected stdout, stderr, and exit: one formatted result on stdout, no response
  content on stderr, exit `0` for every valid combination.
- Filesystem and cleanup: no files; clear captured calls and JSON fixtures.
- Traceability: AC 2, 10; Anthropic inputs and output matrix.

### LM-TC-004 - Embeddings required and optional inputs

- Prerequisites: distinct `OpenAiModel` fake and decoded vector response.
- Inputs: the two-string input list; no optionals; dimensions `8`; each encoding
  `FLOAT` and `BASE64`; explicit timeout `8`; each format and pretty mode.
- Action: invoke every supported embeddings combination, including dimensions
  with each encoding and both optionals omitted.
- Expected SDK arguments: exactly
  `OpenAiModel.embeddings("qa-embedding-model", input=<unchanged strings>,
  request_timeout=8, dimensions=8?, encoding_format=...?)`; absent optionals are
  omitted and BASE64 is not decoded locally.
- Expected stdout, stderr, and exit: one decoded response on stdout, no vector or
  input on stderr, exit `0`.
- Filesystem and cleanup: no binary or other output file; reset fake and argv.
- Traceability: AC 3, 10; embeddings dispatch, inputs, and output matrix.

### LM-TC-005 - Local JSON shape validation and non-disclosure

- Prerequisites: client, invocation-scope, SDK-call, and network constructors
  instrumented to fail if reached.
- Inputs: malformed JSON for every JSON flag; arrays for object fields
  `output_config`, `thinking`, and `tool_choice`; objects or mixed-item arrays for
  object-list fields `messages`, `system`, and `tools`; objects or mixed-item
  arrays for string-list fields `stop_sequences` and embedding `input`; blank
  model ID; secret sentinels embedded in each rejected value.
- Action: run each invalid command through `main()` after configuration loading.
- Expected SDK arguments: none; validation finishes before invocation scope,
  client creation, SDK model construction, or transport.
- Expected stdout, stderr, and exit: one field-specific safe JSON error on stdout,
  exit `1`; stderr/logs contain no rejected value, sentinel, or traceback.
- Filesystem and cleanup: no files or contexts; clear sentinels and patches.
- Traceability: AC 4, 10; JSON validation and privacy matrix.

### LM-TC-006 - SDK-owned nested validation and numeric boundaries

- Prerequisites: installed generated SDK models with transport blocked; client
  construction and attempt count observable.
- Inputs: outer-valid messages with invalid role, content discriminator, camelCase
  alias, tool schema, and thinking shape; numeric constraints declared by the
  installed SDK models; timeout `1`, `3600`, `0`, and `3601`; invalid parser
  numeric text. Service-only semantic constraints are not asserted offline.
- Action: pass nested-invalid values through the real decoded SDK boundary and
  exercise local timeout/parser boundaries separately.
- Expected SDK arguments: nested-invalid cases reach one decoded SDK call but no
  transport request; local timeout/parser failures make no client or SDK call;
  valid boundary timeouts are forwarded unchanged.
- Expected stdout, stderr, and exit: nested SDK validation and local invalid
  values exit `1` with one safe stdout envelope; valid timeout boundaries exit
  `0`; no supplied content appears on stderr, logs, or errors.
- Filesystem and cleanup: no files; restore SDK transport and configuration.
- Traceability: AC 2 through 4, 9, 10; validation and SDK-errors matrix.

### LM-TC-007 - Enablement precedence for both operations

- Prerequisites: real `AccessControlGuard`, packaged policy, and clean ACL
  environment; client and scope constructors guarded.
- Inputs: global, `LANGUAGE_MODELS` namespace, and each canonical operation
  `_ENABLED` variable in true/false and conflicting parent/child combinations.
- Action: evaluate both catalog rows through the guard and CLI boundary.
- Expected SDK arguments: allowed combinations invoke only their selected nested
  method; denial occurs before invocation scope, client, SDK, or transport.
- Expected stdout, stderr, and exit: allowed calls exit `0`; strongest disabled
  scope emits one ACL envelope on stdout and exits `8`; stderr has no request data.
- Filesystem and cleanup: no files; remove every ACL variable.
- Traceability: AC 5, 6; ACL write-classification and Tier-3 matrix.

### LM-TC-008 - Read-only writes and canonical overrides

- Prerequisites: real guard and complete shared AccessControlGuard regression
  suite; both SDK fakes guarded.
- Inputs: global and namespace read-only modes; both operations; parent read-only
  with namespace `_READONLY=false`; parent/namespace read-only with each exact
  operation `_READONLY=false`; conflicting enablement denial.
- Action: verify `messages` and `embeddings` are classified as writes and apply
  canonical precedence at guard and CLI boundaries.
- Expected SDK arguments: blocked cases make no client call; approved overrides
  invoke exactly the selected operation once with normal arguments.
- Expected stdout, stderr, and exit: blocked writes exit `8` with one safe stdout
  envelope; approved overrides exit `0`; stderr contains no prompt/input.
- Filesystem and cleanup: no files; clear all three supported ACL scopes and run
  unrelated guard regressions to confirm unchanged decisions.
- Traceability: AC 5; ACL write-classification matrix and ADR-007.

### LM-TC-009 - Tier-3 exact 0/2 policy and fail-closed behavior

- Prerequisites: installed package policy, temporary missing and malformed policy
  paths, and guarded client/filesystem constructors.
- Inputs: global and namespace metadata-only modes; both catalog rows; correct,
  missing, malformed, duplicate, and unexpectedly permitted policy rows.
- Action: load policy from the package outside the repository CWD and check both
  operations through the real guard and CLI.
- Expected SDK arguments: exactly zero operations permitted and two blocked;
  missing or malformed policy fails closed before scope/client/SDK work.
- Expected stdout, stderr, and exit: each denial emits one safe ACL envelope to
  stdout and exits `8`; stderr has no command input or policy contents.
- Filesystem and cleanup: no command files; remove temporary policy fixtures and
  metadata-only variables.
- Traceability: AC 6, 12; Tier-3 and packaging matrix.

### LM-TC-010 - Attribution enablement, normalization, and retry stability

- Prerequisites: actual SDK attribution context variable; factory and retry fake
  capture client-construction and per-attempt values.
- Inputs: attribution enabled with whitespace, empty entries, and two valid RIDs;
  one retryable failure followed by success for each operation.
- Action: enter `invocation_scope(..., include_attribution=True)`, create the
  client with the same flag, and execute all attempts inside that scope.
- Expected SDK arguments: normalized RIDs are present during client construction
  and every attempt; operation kwargs contain no `attribution`; retry timeout and
  inference inputs remain unchanged.
- Expected stdout, stderr, and exit: only the final success appears on stdout,
  retry diagnostics are safe NDJSON on stderr, exit `0`.
- Filesystem and cleanup: no files; reset SDK context tokens and retry settings.
- Traceability: AC 7, 9, 10; attribution and retry matrix.

### LM-TC-011 - Attribution disabled, nesting, concurrency, and restoration

- Prerequisites: distinct outer and per-task attribution contexts; formatter and
  SDK paths can raise success, SDK failure, timeout, cancellation, and formatter
  failure.
- Inputs: attribution disabled; enabled with an empty RID list; nested scopes;
  concurrent tasks with distinct RIDs; every exit path.
- Action: observe the value before, during, and after client construction and
  invocation for each scenario.
- Expected SDK arguments: disabled/empty configuration supplies scoped `None`;
  enabled tasks see only their own RIDs; no attribution keyword reaches either
  SDK operation.
- Expected stdout, stderr, and exit: success `0`; mapped failure exits; cancellation
  `5`; one stdout result/envelope only; stderr/logs contain no attribution RID.
- Filesystem and cleanup: no files; every caller's prior context is restored in
  `finally`, then outer tokens are reset.
- Traceability: AC 7, 9, 11; attribution, privacy, and concurrency matrix.

### LM-TC-012 - B3 context across client creation and retries

- Prerequisites: SDK-native tracing provider with deterministic B3 fixture and
  retry attempt capture.
- Inputs: B3 enabled and sampled; one recovery sequence and one exhausted
  sequence for each operation.
- Action: observe tracing during client construction and every attempt within one
  invocation scope.
- Expected SDK arguments: identical `X-B3-TraceId`, `X-B3-SpanId`, and
  `X-B3-Sampled` context covers construction and all attempts; inference kwargs
  are unchanged; no trace keyword is passed.
- Expected stdout, stderr, and exit: recovery emits one success and exits `0`;
  exhaustion emits one mapped error; safe retry diagnostics may use stderr; no
  partial result or W3C `traceparent`/`tracestate` claim appears.
- Filesystem and cleanup: no files; reset deterministic tracing and retry patches.
- Traceability: AC 8, 9; B3 and retry matrix.

### LM-TC-013 - B3 disabled, nesting, concurrency, and restoration

- Prerequisites: outer and per-task B3 contexts plus controllable SDK, formatter,
  timeout, and cancellation failures.
- Inputs: tracing disabled; nested enabled scopes; concurrent invocations with
  distinct B3 values; all exit paths.
- Action: inspect values before, during, and after each invocation.
- Expected SDK arguments: disabled tracing contributes no B3 value; concurrent
  tasks never observe a sibling context; no W3C context or tracing keyword reaches
  the operation.
- Expected stdout, stderr, and exit: normal or mapped exit for each injected path;
  one stdout result/envelope; no trace leakage in stderr or logs.
- Filesystem and cleanup: no files; prior B3 contexts restored after success,
  error, timeout, cancellation, and formatter failure.
- Traceability: AC 8, 9, 11; B3, privacy, and concurrency matrix.

### LM-TC-014 - Retry recovery, exhaustion, and duplicate-cost warning

- Prerequisites: real `RetryHandler` configured for three total attempts with zero
  delay/jitter; attempt-aware SDK callable; Claude skill available for inspection.
- Inputs: native SDK timeout and connection failures, HTTP 429 and 503, each with
  fail-then-success and always-fail sequences; non-retryable bad request control.
- Action: execute both operations and inspect skill guidance after exhaustion.
- Expected SDK arguments: retryable recovery uses the exact expected attempt
  count and unchanged timeout/input/context; exhaustion stops after three;
  non-retryable error makes one attempt.
- Expected stdout, stderr, and exit: one final success or safe error only; timeout
  exits `5`, connection/503 exits `6`, 429 exits `7`; retry diagnostics do not
  include inference data. The skill warns that retries are at-least-once, may
  duplicate billable inference or vary output, and must not suggest an automatic
  application retry after CLI exhaustion.
- Filesystem and cleanup: no files; reset retry environment and attempt logs.
- Traceability: AC 9, 10; retry and duplicate-cost matrix.

### LM-TC-015 - Actual SDK error taxonomy and ADR envelopes

- Prerequisites: installed `foundry_sdk._errors`, real serializer, and retry
  handler set to three total attempts.
- Inputs: construct `UnauthorizedError({})`, `NotAuthenticated("qa")`,
  `PermissionDeniedError({})`, `NotFoundError({})`, `ApiNotFoundError("qa")`,
  `BadRequestError({})`, `ConflictError({})`, SDK `TimeoutError("qa")`, SDK
  `ConnectionError("qa")`, `EnvironmentNotConfigured("qa")`,
  `SDKInternalError("qa")`, `RateLimitError("qa", "qa")`, and
  `ServiceUnavailable("qa", "qa")`; also inject `asyncio.CancelledError`.
- Action: raise each class through the real retry/CLI error boundary and record
  constructor compatibility, attempts, HTTP status when supplied, and call ID.
- Expected SDK arguments: auth, permission, input, not-found, configuration, and
  internal errors make one attempt; timeout, connection, 429, and 503 make three
  when exhausted; cancellation is converted once and not retried.
- Expected stdout, stderr, and exit: auth `2`; permission `3`; not found `4`;
  bad request/conflict `1`; timeout/cancellation `5`; connection/internal/503
  `6`; 429 `7`; configuration `9`. Exactly one ADR-001 JSON envelope is written
  to stdout; diagnostics on stderr are safe; SDK messages and sentinels are not
  public and no traceback appears.
- Filesystem and cleanup: no files; clear exception and retry fixtures.
- Traceability: AC 9, 10; actual SDK errors and privacy matrix.

### LM-TC-016 - Anthropic union output and format selection

- Prerequisites: decoded SDK response fixtures for text, tool use, thinking, and
  redacted-thinking content plus usage and stop fields.
- Inputs: each union response under JSON, TOON, auto, and pretty modes.
- Action: adapt and format each response through the full success boundary.
- Expected SDK arguments: one normal messages call; output processing makes no
  follow-up SDK call and does not reinterpret union members.
- Expected stdout, stderr, and exit: one complete decoded result on stdout, auto
  chooses JSON for the object response, stderr has no content/usage data, exit
  `0`; no pagination or binary metadata is added.
- Filesystem and cleanup: no files; clear response objects and captures.
- Traceability: AC 10; output matrix and ADR-004.

### LM-TC-017 - Embedding vectors and BASE64 request handling

- Prerequisites: decoded response fixtures with multiple float vectors, model,
  and usage fields.
- Inputs: FLOAT and BASE64 requests under JSON, TOON, auto, and pretty modes.
- Action: format the SDK-returned object without local vector or BASE64 decoding.
- Expected SDK arguments: selected encoding is forwarded unchanged; one SDK call
  only; output processing receives the decoded SDK model as returned.
- Expected stdout, stderr, and exit: one result on stdout with vectors preserved,
  no vector/input on stderr or logs, exit `0`; no binary envelope or file path.
- Filesystem and cleanup: no files; clear vector fixtures and captures.
- Traceability: AC 3, 10; embeddings output and privacy matrix.

### LM-TC-018 - Privacy sentinels and generic failures

- Prerequisites: capture stdout, stderr, logs, traceback state, and retained test
  artifacts; generic unexpected failure can be injected after receiving inputs.
- Inputs: place unique sentinels in messages, system prompt, stop sequence, tool
  input/schema, thinking, image/document/base64 content, embedding input/vector,
  model response, credential/token, configured attribution, malformed JSON, and
  exception text.
- Action: run success, local validation, SDK validation, retry, ACL, formatter,
  and unexpected-error paths for both operations.
- Expected SDK arguments: allowed success paths receive intended input only;
  rejected paths stop at their documented boundary; no diagnostic callback gets
  a raw argument or response.
- Expected stdout, stderr, and exit: requested success content may appear only in
  stdout; no sentinel appears in stderr, logs, error envelopes, tracebacks, or
  retained metadata; unexpected errors use the generic Language Models message
  and exit `6`.
- Filesystem and cleanup: no command files; remove captures and secret fixtures.
- Traceability: AC 4, 7 through 11; privacy matrix.

### LM-TC-019 - Structural exclusions and import side effects

- Prerequisites: source/catalog inspection and guarded configuration, context,
  client, network, event-loop, and filesystem constructors.
- Inputs: import the package and Claude launcher; inspect parser, catalog, and
  public module symbols; try excluded flags and command names.
- Action: verify absence of list, metadata, pagination, raw, streaming, binary,
  session, alias, local-state, per-command attribution/preview, provider choice,
  and custom schema behavior.
- Expected SDK arguments: no SDK call on import or excluded syntax; catalog uses
  decoded `messages` and `embeddings` only.
- Expected stdout, stderr, and exit: imports are silent; excluded syntax exits
  `1` with a safe stdout envelope and no traceback; no unsupported help text.
- Filesystem and cleanup: imports do not load config, change contexts, create a
  client, start an event loop, access network, or create files; restore guards.
- Traceability: AC 1, 12; structural exclusions and imports matrix.

### LM-TC-020 - Wheel, editable install, launchers, and empty CWD

- Prerequisites: clean source snapshot, local build dependencies, two disposable
  environments, and an empty working directory without `PYTHONPATH`.
- Inputs: build and inspect a wheel; install wheel and editable forms with
  `--no-deps`; run console and absolute Claude launcher help/import; run installed
  0/2 policy probe; snapshot existing console entry points.
- Action: validate both install forms independently of repository-relative paths.
- Expected SDK arguments: help/import/policy denial makes no SDK call; installed
  policy blocks both rows before client construction.
- Expected stdout, stderr, and exit: both help paths exit `0` and show exactly two
  operations; policy denials exit `8` with safe stdout; imports are silent; no
  traceback or dependency on repository CWD.
- Filesystem and cleanup: wheel contains
  `foundry_cli/language_models/metadata-allow-list.md` and the
  `foundry-language-models` entry while preserving prior entries; empty CWD stays
  empty; remove only disposable build/install artifacts.
- Traceability: AC 6, 12; packaging, imports, and Tier-3 matrix.

### LM-TC-021 - Python matrix, regression, and delivery gates

- Prerequisites: clean, fully provisioned Python 3.11 and 3.12 environments with
  project-defined development and build dependencies.
- Inputs: focused Language Models tests, full active suite, dormant common suite,
  branch coverage, scoped Ruff, mypy, Bandit, build validation, `pip check`, and
  clean outside-CWD import/help probes.
- Action: run the focused suite and full regression separately on each Python;
  run canonical commands including `python -m ruff check src tests
  .claude/skills/foundry-language-models`, `python -m mypy src`,
  `python -m bandit -q -r src`, and pytest with `--cov-branch` and
  `--cov-fail-under=80`.
- Expected SDK arguments: all tests remain mocked; no live transport or credential
  lookup; existing namespace routes and console entries remain unchanged.
- Expected stdout, stderr, and exit: every canonical gate exits `0`; full suite
  and focused counts are recorded separately per interpreter; branch coverage is
  at least 80%; warnings are classified and contain no sensitive data.
- Filesystem and cleanup: remove temporary coverage/build/install artifacts;
  retain only sanitized TESTEXEC evidence.
- Traceability: AC 12; regression and delivery-gates matrix.

### LM-TC-022 - Optional approved non-production smoke

- Prerequisites: explicit approval, least-privilege non-production credentials,
  synthetic non-sensitive prompts, known cost limit, timeout, and evidence cleanup
  plan. Skip when any prerequisite is absent.
- Inputs: at most one bounded invocation of each operation with synthetic data;
  never use production prompts, documents, tools, or credentials in evidence.
- Action: exercise installed authentication and routing without adding an
  application-level retry.
- Expected SDK arguments: exact installed routes and bounded inputs only; no raw,
  streaming, or unsupported operation.
- Expected stdout, stderr, and exit: record success or a correctly mapped service
  error; sanitize all retained streams. A skipped/blocked optional smoke does not
  block mocked acceptance.
- Filesystem and cleanup: no command file; remove test-owned artifacts and revoke
  temporary credentials if issued.
- Traceability: optional environment supplement for AC 2, 3, 9, 10, and 12.

## Traceability matrix

| Requirement area | Story criteria | Cases |
|---|---|---|
| Exactly two operations, parser, inputs, exact nested dispatch | AC 1 through 4 | LM-TC-001 through 006 |
| Both operations are writes; enablement/read-only overrides | AC 5 | LM-TC-007, 008 |
| Tier-3 exact 0 permitted/2 blocked; missing policy fails closed | AC 6 | LM-TC-007 through 009, 020 |
| Attribution enablement, normalization, retry, nesting, concurrency, restoration | AC 7, 11 | LM-TC-010, 011, 018 |
| SDK-native B3 only, retry stability, nesting, concurrency, restoration | AC 8, 11 | LM-TC-012, 013, 018 |
| Retry recovery/exhaustion, at-least-once cost warning, SDK taxonomy | AC 9 | LM-TC-006, 010, 012, 014, 015 |
| Output formats, union content, vectors, stream separation, privacy | AC 10 | LM-TC-002 through 004, 016 through 018 |
| Structural exclusions and import-time safety | AC 1, 12 | LM-TC-001, 019 |
| Wheel/editable installs, console/Claude launchers, empty CWD, policy | AC 12 | LM-TC-009, 019, 020 |
| Python 3.11/3.12, full regression, static/security gates, coverage | AC 12 | LM-TC-021 |
| Approved non-production option | Supporting evidence | LM-TC-022 |

All 12 story acceptance criteria and every DESIGN-012 QA matrix row have positive
coverage plus the applicable negative, boundary, security, concurrency, privacy,
failure-path, or compatibility evidence.

## Execution and approval gate

TESTEXEC-012 must execute LM-TC-001 through LM-TC-021. LM-TC-022 is optional and
must remain skipped unless the stated approval and environment prerequisites are
met. Developer test results may guide fixture reuse but do not replace independent
QA execution evidence.

For every case, record PASS, FAIL, or BLOCKED with the required environment,
command, streams, exit code, SDK argument/attempt evidence, filesystem result,
cleanup, and retained artifact reference. Create a BUG-SUB for each functional
failure before TESTEXEC-012 completes. QA sign-off requires every mandatory case
to pass, linked defects to be terminal, all 12 acceptance criteria to have passing
evidence, and branch coverage to remain at least 80%.

Reviewer: `tech-lead`, acting as the named Tech Lead/Architect reviewer.
TESTCASE-012 blocks TESTEXEC-012. TESTEXEC-012 must not start until this reviewer
records approval of the complete case set.
