# DESIGN-012 - Foundry Language Models CLI

| Field | Value |
|---|---|
| Story | DEV-STORY-012 |
| Status | Completed; ready for implementation |
| Date | 2026-08-09 |
| Scope | `foundry-language-models` CLI and Claude skill, two Language Models API v2 operations |

## Technical summary

Add a small Language Models namespace CLI for Anthropic messages and OpenAI embeddings. Both operations run model inference. They are writes for access-control purposes and are blocked in metadata-only mode.

The CLI uses decoded async SDK methods. It has no list, metadata, pagination, binary, or session operation. Structured inputs arrive as JSON command arguments, receive local outer-shape validation, and then pass to the generated SDK for typed model validation.

Attribution is enabled for this namespace when the global attribution setting and RID list are present. One invocation scope covers client construction, attribution, B3 context, and every retry, then restores the caller's prior contexts. Retries are at-least-once: a response lost after provider execution may cause another billable inference.

## Evidence and governing references

This design follows:

- SRS-001 FR-ACL, FR-ATTR, FR-ERR, FR-OUT, FR-TRACE, and the privacy requirements;
- SAD-001 namespace packaging and stateless CLI structure;
- DESIGN-005 tracing and common-component integration contracts;
- DESIGN-011 patterns for an immutable operation catalog, exact nested SDK dispatch, context restoration, packaged policy, and native SDK error handling;
- ADR-001 exit codes, ADR-002 timeouts, ADR-004 format selection, ADR-005 logging, ADR-006 configuration search, and ADR-007 read-only precedence;
- the canonical environment-variable reference, which defines operation enablement and read-only overrides for both routes;
- the canonical metadata allow-list, which blocks both Language Models operations in tier 3;
- vendored SDK sources `foundry_sdk/v2/language_models/anthropic_model.py`, `open_ai_model.py`, `models.py`, `errors.py`, `_client.py`, and `foundry_sdk/v2/client.py`.

The vendored async client exposes `language_models.AnthropicModel` and `language_models.OpenAiModel`. Each resource has one public operation in this story. Generated raw and streaming wrappers exist but are not part of the approved CLI surface.

## Operation catalog

CLI names use kebab-case. Catalog keys and ACL paths use snake_case. `OP_SPECS` contains exactly two unique entries.

| CLI command | Exact SDK route | Method | Required input | Optional input | Return type |
|---|---|---|---|---|---|
| `anthropic-model messages MODEL_ID` | `client.language_models.AnthropicModel` | `messages` | `MODEL_ID`, `--max-tokens`, `--messages-json` | output config, stop sequences, system, temperature, thinking, tool choice, tools, top K, top P | `AnthropicMessagesResponse` |
| `open-ai-model embeddings MODEL_ID` | `client.language_models.OpenAiModel` | `embeddings` | `MODEL_ID`, `--input-json` | dimensions, encoding format | `OpenAiEmbeddingsResponse` |

Both commands also accept `--timeout`, `--format json|toon|auto`, and `--pretty`. They do not accept page controls, output filenames, session aliases, or binary options.

### Authoritative SDK signatures

The adapter preserves these public async SDK contracts:

```python
# client.language_models.AnthropicModel
def messages(
    anthropic_model_model_id: LanguageModelApiName,
    *,
    max_tokens: int,
    messages: list[AnthropicMessage],
    attribution: Attribution | None = None,
    output_config: AnthropicOutputConfig | None = None,
    preview: bool | None = None,
    stop_sequences: list[str] | None = None,
    system: list[AnthropicSystemMessage] | None = None,
    temperature: float | None = None,
    thinking: AnthropicThinkingConfig | None = None,
    tool_choice: AnthropicToolChoice | None = None,
    tools: list[AnthropicTool] | None = None,
    top_k: int | None = None,
    top_p: float | None = None,
    request_timeout: Timeout | None = None,
    _sdk_internal: SdkInternal = {},
) -> Awaitable[AnthropicMessagesResponse]: ...

# client.language_models.OpenAiModel
def embeddings(
    open_ai_model_model_id: LanguageModelApiName,
    *,
    input: list[str],
    attribution: Attribution | None = None,
    dimensions: int | None = None,
    encoding_format: Literal["FLOAT", "BASE64"] | None = None,
    preview: bool | None = None,
    request_timeout: Timeout | None = None,
    _sdk_internal: SdkInternal = {},
) -> Awaitable[OpenAiEmbeddingsResponse]: ...
```

The CLI does not expose `attribution`, `preview`, or `_sdk_internal`:

- `AsyncClientFactory` supplies configured attribution through the SDK context variable;
- shared client construction already enables preview support;
- `_sdk_internal` is private generated-SDK plumbing.

The implementation must not pass these three keyword arguments. It forwards `request_timeout` on every attempt and omits absent optional request fields rather than sending explicit `None` values.

### Return contracts

`AnthropicMessagesResponse` contains `content`, `id`, `model`, `role`, optional stop fields, and token usage. Completion content is a discriminated union that may contain text, tool use, thinking, or redacted thinking.

`OpenAiEmbeddingsResponse` contains `data: list[list[float]]`, `model`, and prompt-token usage. The CLI serializes the decoded SDK model as returned. It does not reinterpret a `BASE64` request, decode vectors, or introduce a binary output path.

## Command and data contracts

### Anthropic messages

```text
foundry-language-models anthropic-model messages MODEL_ID
  --max-tokens INT
  --messages-json JSON_ARRAY
  [--output-config-json JSON_OBJECT]
  [--stop-sequences-json JSON_STRING_ARRAY]
  [--system-json JSON_OBJECT_ARRAY]
  [--temperature FLOAT]
  [--thinking-json JSON_OBJECT]
  [--tool-choice-json JSON_OBJECT]
  [--tools-json JSON_OBJECT_ARRAY]
  [--top-k INT]
  [--top-p FLOAT]
  [--timeout SECONDS]
  [--format json|toon|auto]
  [--pretty]
```

Minimal message input:

```json
[
  {
    "role": "USER",
    "content": [{"type": "text", "text": "Summarize this note."}]
  }
]
```

The CLI validates the outer containers. The SDK validates roles, discriminators, aliases such as `budgetTokens`, tool schemas, and nested content. The CLI must not copy the generated model hierarchy into local Pydantic models.

### OpenAI embeddings

```text
foundry-language-models open-ai-model embeddings MODEL_ID
  --input-json JSON_STRING_ARRAY
  [--dimensions INT]
  [--encoding-format FLOAT|BASE64]
  [--timeout SECONDS]
  [--format json|toon|auto]
  [--pretty]
```

Example input:

```json
["first document", "second document"]
```

### Validation boundary

Parser types handle integers, floats, the encoding enum, format, and timeout. A second validation stage checks:

| Field | Local contract |
|---|---|
| model ID | Non-empty string after trimming for validation; forward original value |
| `messages` | JSON array containing only objects |
| `output_config`, `thinking`, `tool_choice` | JSON object |
| `stop_sequences`, embedding `input` | JSON array containing only strings |
| `system`, `tools` | JSON array containing only objects |

Malformed JSON and wrong outer shapes return exit 1 before client construction. Error text names the field and expected shape but never includes the supplied value. Numeric semantic constraints remain with the generated SDK and service unless the SDK model declares a local constraint.

## Components and interfaces

### Package layout

```text
src/foundry_cli/language_models/
├── __init__.py
├── metadata-allow-list.md
└── scripts/
    ├── __init__.py
    └── foundry_language_models_cli.py

.claude/skills/foundry-language-models/
├── SKILL.md
└── scripts/
    └── foundry_language_models_cli.py
```

`pyproject.toml` adds:

```toml
foundry-language-models = "foundry_cli.language_models.scripts.foundry_language_models_cli:console_main"
```

Package data includes `foundry_cli.language_models/metadata-allow-list.md`. Existing entry points and package-data declarations remain unchanged.

### Operation specification

```python
OperationSpec = dict[str, Any]

OP_SPECS: tuple[OperationSpec, ...] = (
    {
        "resource": "anthropic_model",
        "operation": "messages",
        "client_path": ("AnthropicModel",),
        "method": "messages",
        "positional": ("model_id",),
        "required": ("max_tokens", "messages"),
        "optional": (
            "output_config",
            "stop_sequences",
            "system",
            "temperature",
            "thinking",
            "tool_choice",
            "tools",
            "top_k",
            "top_p",
        ),
    },
    {
        "resource": "open_ai_model",
        "operation": "embeddings",
        "client_path": ("OpenAiModel",),
        "method": "embeddings",
        "positional": ("model_id",),
        "required": ("input",),
        "optional": ("dimensions", "encoding_format"),
    },
)
```

JSON shape metadata may be embedded in each spec or held in immutable lookup sets. There must still be one source of truth for dispatch and argument forwarding.

### Module interfaces

```python
def build_parser() -> argparse.ArgumentParser: ...
def _spec_for(resource: str, operation: str) -> OperationSpec: ...
def _required_text(value: Any, *, field: str) -> str: ...
def _parse_json_object(value: str, *, field: str) -> dict[str, Any]: ...
def _parse_json_object_list(value: str, *, field: str) -> list[dict[str, Any]]: ...
def _parse_json_string_list(value: str, *, field: str) -> list[str]: ...
def _validate_inputs(spec: OperationSpec, args: argparse.Namespace) -> None: ...
def _validate_timeout(value: int) -> int: ...
def _get_client(root_client: Any, client_path: tuple[str, ...]) -> Any: ...
def _model_to_dict(value: Any) -> Any: ...
def _serialize_error(exception: BaseException) -> int: ...
async def _invoke_sdk(
    spec: OperationSpec,
    client: Any,
    args: argparse.Namespace,
    timeout: int,
) -> Any: ...
async def main() -> int: ...
def console_main() -> int: ...
```

Public functions carry full type annotations and docstrings. `console_main()` is the only `asyncio.run()` boundary. Importing the package or Claude launcher must not read configuration, change context variables, create a client, write files, or make a network call.

### Nested dispatch

Start from `root_client.language_models`, then traverse the one-element `client_path`. Exact dispatch is:

```python
namespace = root_client.language_models
client = getattr(namespace, spec["client_path"][0])
result = await getattr(client, spec["method"])(
    args.model_id,
    **kwargs,
    request_timeout=timeout,
)
```

Do not flatten resources onto `language_models`, use lowercase generated resource names, or call `with_raw_response` or `with_streaming_response`.

## Runtime order

One invocation follows this order:

1. Build the parser and parse one resource and operation.
2. Load configuration through `ConfigLoader` and configure `LogSetup`.
3. Resolve the operation spec and validate scalar and JSON input shapes.
4. Resolve and validate the effective ADR-002 timeout.
5. Call `AccessControlGuard(cfg, "LANGUAGE_MODELS", packaged_policy).check(resource, operation)`.
6. Create an `AsyncClientFactory`.
7. Enter `factory.invocation_scope(cfg, include_attribution=True)`.
8. Create the root client with `factory.create(cfg, include_attribution=True)`.
9. Resolve the exact nested Language Models resource.
10. Run the complete SDK call through `RetryHandler(timeout_s=timeout)`.
11. Convert and format the successful SDK model while no failed-attempt result has been published.
12. Leave the invocation scope, restoring prior attribution and B3 contexts.
13. Write one success result to stdout.

Parser and input failures occur before client creation. ACL denial occurs before entering the SDK scope. The implementation writes no command-specific files.

## Access control

Both operations perform AI execution and may incur cost. Treat `messages` and `embeddings` as write verbs in `AccessControlGuard`. This is a required common correction, not a namespace-local workaround.

| SDK path | Read-only | Metadata-only |
|---|---|---|
| `language_models.anthropic_model.messages` | Blocked unless canonical `_READONLY=false` override applies | Blocked |
| `language_models.open_ai_model.embeddings` | Blocked unless canonical `_READONLY=false` override applies | Blocked |

The packaged policy contains both rows as `BLOCKED`: exactly zero permitted and two blocked. A missing or malformed packaged policy fails closed in metadata-only mode. Tests cover global, namespace, and operation enablement, parent read-only with namespace or operation override, and metadata-only precedence.

The canonical operation variables are:

- `FOUNDRY_AGENTIC_CLI_LANGUAGE_MODELS_ANTHROPIC_MODEL_MESSAGES_ENABLED`
- `FOUNDRY_AGENTIC_CLI_LANGUAGE_MODELS_ANTHROPIC_MODEL_MESSAGES_READONLY=false`
- `FOUNDRY_AGENTIC_CLI_LANGUAGE_MODELS_OPEN_AI_MODEL_EMBEDDINGS_ENABLED`
- `FOUNDRY_AGENTIC_CLI_LANGUAGE_MODELS_OPEN_AI_MODEL_EMBEDDINGS_READONLY=false`

Adding the two write verbs changes shared classification. Run the full AccessControlGuard regression suite so unrelated operations keep their established decisions.

## Attribution and B3 tracing

Language Models is an attribution-enabled namespace. Use both calls explicitly:

```python
with factory.invocation_scope(cfg, include_attribution=True):
    root_client = factory.create(cfg, include_attribution=True)
```

When attribution is enabled and configured RIDs are present, the factory trims empty entries and sets the SDK attribution context for client construction and every retry. Disabled attribution or an empty RID list sets the scoped value to `None`. The SDK HTTP layer injects the header; operation dispatch does not pass an `attribution` keyword.

The scope keeps the context-variable token and restores the prior value in `finally`. Restoration is required after success, SDK failure, exhausted retry, timeout, cancellation, and formatter failure. Nested and concurrent invocations must not leak values between tasks.

`TracingProvider` supplies SDK-native B3 multi-headers only: `X-B3-TraceId`, `X-B3-SpanId`, and `X-B3-Sampled`. One B3 context covers client construction and every retry. Disabled tracing adds no B3 values. The scope restores prior tracing context on every exit path. Do not add or claim W3C `traceparent` or `tracestate` support.

## Retry and error handling

Use the shared `RetryHandler` and centralized SDK error mapping. Retry configured transport failures, native SDK timeout and connection failures, HTTP 429, and HTTP 503. Authentication, permission, bad request, conflict, and not-found errors do not retry.

Both model calls have at-least-once attempt semantics. A provider may complete inference before the client observes a transport failure. Retrying can repeat cost and may produce a different message. The CLI cannot promise exactly-once inference, deduplicate requests, or recover a lost response because neither SDK method accepts an idempotency key. The Claude skill must state this behavior without suggesting automatic application-level retries after the CLI has exhausted its own policy.

Language Models service errors inherit the SDK's common classes:

| Error family | ADR exit |
|---|---:|
| invalid request, unavailable model, unsupported prompt/tool shape | 1 |
| missing or invalid authentication | 2 |
| model or operation permission denied | 3 |
| model or API not found | 4 |
| timeout or cancellation | 5 |
| connection failure after retries, SDK internal error, exhausted 503 | 6 |
| exhausted 429 | 7 |
| ACL denial | 8 |
| missing SDK, credentials, hostname, or malformed configuration | 9 |

Terminal failures write one ADR-001 JSON envelope to stdout. Safe NDJSON diagnostics go to stderr. SDK and unexpected errors use generic public messages; logs may contain exception class, HTTP status, and call ID, but never request or response content.

## Output and privacy

Use the common model-to-dict adapter and `OutputFormatter`. ADR-004 applies: auto mode emits JSON for these object responses. Explicit supported formats remain available. There is no pagination metadata or binary envelope.

Successful model content and embedding vectors are intended stdout data. They must not be copied to stderr or logs. Never log:

- message content, system prompts, stop sequences, tool inputs, tool schemas, or thinking blocks;
- image, document, or base64 content embedded in Anthropic messages;
- embedding inputs or returned vectors;
- model responses, token values, credentials, or attribution RIDs;
- raw command arguments or validation payloads.

Errors must not echo malformed JSON. Tracebacks remain disabled unless the existing controlled debug policy permits them, and retained diagnostics must still exclude sensitive values.

## Explicit exclusions

This story does not add:

- list or metadata operations;
- raw-page or pagination adapters;
- binary upload, download, or persistence;
- session aliases, cleanup, or local state;
- SDK streaming response wrappers;
- per-command attribution or preview flags;
- custom language-model schemas, token counting, response transformation, or provider selection;
- idempotency or cross-invocation retry coordination.

These exclusions should have structural tests so later refactoring cannot silently widen the surface.

## Implementation sequence

1. Add this design to the document index and close the design gate.
2. Add `messages` and `embeddings` to shared write classification with focused and full ACL regression tests.
3. Add the Language Models package and packaged two-row blocked policy.
4. Add the two-entry catalog, parser, and typed outer-shape JSON validators.
5. Add exact nested SDK dispatch and optional-key omission.
6. Wire timeout, retry, real SDK errors, attribution-enabled invocation scope, B3, formatting, and safe logging.
7. Add the Claude skill, thin launcher, console entry point, and package data.
8. Complete unit tests, independent code review, QA, clean-install checks, and repository regression gates.

## QA traceability matrix

| Area | Cases | Required evidence |
|---|---|---|
| Catalog and parser | Exact count, help, missing and unknown syntax | Two unique specs; no unsupported resource or operation |
| Anthropic dispatch | Required-only and all-option calls | Exact `AnthropicModel.messages`, positional model ID, correct keyword names, omitted absent values |
| Embeddings dispatch | Required-only, dimensions, both encoding literals | Exact `OpenAiModel.embeddings`; string-array input unchanged |
| JSON validation | Malformed JSON, wrong container, mixed items, nested SDK rejection | Exit 1 before client; error omits supplied content |
| ACL write classification | Global and namespace read-only, both canonical overrides | Both inference operations block as writes unless approved override applies |
| Tier 3 | Both catalog rows, packaged and missing policy | Exactly 0 permitted and 2 blocked; missing policy fails closed before client |
| Attribution | Enabled, disabled, empty list, nested and concurrent scopes | Configured RIDs present during client/retries; prior value restored on all exits |
| B3 | Enabled, disabled, retry, failure, cancellation, concurrency | Stable B3 values per invocation; prior context restored; no W3C values |
| Retry semantics | Recovery and exhaustion for native timeout, connection, 429, and 503 | Exact attempt counts; one final result or error; duplicate-cost limitation documented |
| SDK errors | Real SDK base and language-specific subclasses | ADR exits 1 through 9 as applicable; non-retryable failures make one attempt |
| Output | Anthropic union content, embedding vectors, JSON/TOON/auto, pretty | One stdout result; no pagination or binary metadata |
| Privacy | Sentinels in every sensitive field and configured attribution | No sentinel in logs, stderr, error messages, or tracebacks |
| Structural exclusions | Imports, catalog, parser, filesystem observation | No pagination, download, session, raw, or streaming implementation |
| Packaging | Wheel, editable install, empty CWD, import, both launchers | Console and Claude help return 0; packaged policy resolves; no import side effects |
| Regression | Python 3.11/3.12, full suite, Ruff, mypy, Bandit, coverage | All gates pass; repository branch coverage remains at least 80% |

Routine tests use nested async SDK fakes and actual installed SDK exception classes. Live credentials are not required. An optional smoke test may use an approved non-production environment with synthetic prompts and a cleanup plan; retained evidence must exclude credentials and prompt content.

## Grooming decomposition and dependencies

All children use DEV-STORY-012 as parent through `ParentChild`.

| Type | Exact title | Role | Estimate | Completion contract |
|---|---|---|---:|---|
| DESIGN | Design Foundry Language Models CLI and inference controls | `tech-lead` | 4 h | DESIGN-012 is indexed, approved, closed, and leaves no implementation question open. |
| DEV | Implement Foundry Language Models CLI and Claude skill | `python-developer` | 10 h | Add package, two operations, JSON validation, ACL correction, attribution scope, policy, skill, launcher, and entry point; Ruff and mypy pass. |
| UNITTEST | Add Foundry Language Models CLI unit and integration tests | `python-developer` | 8 h | Assert every QA matrix row with real SDK errors and installed-policy tests; targeted tests pass and branch coverage stays at least 80%. |
| CODEREVIEW | Review Foundry Language Models CLI implementation | `tech-lead` | 3 h | Review exact DEV result for SDK accuracy, ACL, contexts, at-least-once risk, privacy, packaging, and compatibility; resolve or track findings. |
| TESTCASE | Design Foundry Language Models CLI QA cases | `qa-engineer` | 4 h | Create executable, traceable cases for both operations and every story criterion; a named Tech Lead/Architect approves the full set before TESTEXEC. |
| TESTEXEC | Execute Foundry Language Models CLI QA suite | `qa-engineer` | 3 h | Record environment, commands, actual results, streams, exit codes, SDK evidence, and cleanup; defects receive BUG-SUB tickets; no blocker remains. |
| DEVOPS | Package and verify Foundry Language Models entry points | `devops-engineer` | 2 h | Verify clean wheel/editable installs, console and Claude launchers, packaged policy, Python matrix, existing entry points, security gates, and additive rollback. |

Dependency plan:

- DESIGN blocks implementation and test activation until it is approved and closed.
- DEV and UNITTEST may proceed together after DESIGN. TESTCASE may run in parallel.
- DEV relates to and blocks CODEREVIEW until the exact implementation result is ready. CODEREVIEW also requires UNITTEST evidence.
- The Tech Lead code reviewer must differ from the Python developer who implemented DEV.
- TESTCASE blocks TESTEXEC. TESTEXEC cannot start until a named Tech Lead/Architect records approval of the completed case set.
- TESTEXEC also depends on DEV, UNITTEST, and CODEREVIEW.
- DEVOPS depends on successful TESTEXEC and is required because the story adds an entry point, launcher, package, and policy asset.

## Estimate and sprint fit

Story estimate: 5 points, 34 planned role-hours.

| Work | Hours |
|---|---:|
| Design | 4 |
| Development | 10 |
| Unit tests | 8 |
| Code review | 3 |
| QA case design | 4 |
| QA execution | 3 |
| Packaging verification | 2 |
| Total | 34 |

The work fits one 10-day sprint. Only two SDK methods are added, and no stateful or streaming protocol is involved. Structured Anthropic input, shared write classification, attribution restoration, and privacy tests account for most of the estimate. TESTCASE can overlap development. The estimate assumes the pinned SDK signatures and common context interfaces remain stable.

## Risks and decisions

| Risk or decision | Treatment |
|---|---|
| Guard treats unfamiliar operation names as reads | Add `messages` and `embeddings` to shared write verbs and run full ACL regressions. |
| Retried inference may duplicate cost or produce a different message | State at-least-once semantics; use only common retry policy; do not claim idempotency. |
| Anthropic JSON has deep discriminated unions | Validate outer shapes locally and delegate nested validation to the pinned SDK. |
| Prompt, tool, document, image, and thinking data are sensitive | Keep them out of logs, stderr, errors, metadata, and retained test artifacts. |
| Large embeddings can produce large stdout objects | Stream handling is out of scope; serialize the decoded SDK response without making bounded-memory claims. |
| `BASE64` is accepted while the generated response model declares float vectors | Forward the documented enum unchanged and trust the pinned SDK response model; do not add a local decoder. |
| Attribution context could leak between invocations | Use `include_attribution=True` scope and client creation; test nesting, concurrency, and every failure path. |
| Packaged policy may work only from repository CWD | Resolve policy from the installed package and test from an empty working directory. |

No open technical question blocks implementation.

## Story acceptance criteria

1. **Given** an installed CLI, **when** root and operation help are inspected, **then** exactly `anthropic-model messages` and `open-ai-model embeddings` are exposed and no list, pagination, binary, session, raw, or streaming command exists.
2. **Given** valid Anthropic inputs, **when** `messages` runs, **then** it calls `client.language_models.AnthropicModel.messages` with the positional model ID, exact documented keywords, timeout, and no absent or private keyword.
3. **Given** valid embedding inputs, **when** `embeddings` runs, **then** it calls `client.language_models.OpenAiModel.embeddings` with the positional model ID, unchanged string array, requested dimensions and encoding, and timeout.
4. **Given** malformed JSON, a wrong outer shape, an invalid enum, or missing required input, **when** validation runs, **then** the command exits 1 before client construction and does not echo input content.
5. **Given** read-only mode, **when** either inference operation runs, **then** it exits 8 before client creation unless the canonical namespace or operation override permits the write.
6. **Given** metadata-only mode, **when** the two-entry catalog is evaluated, **then** exactly zero operations are permitted and both are blocked by the packaged policy before client creation.
7. **Given** configured attribution RIDs, **when** either operation runs or retries, **then** the SDK attribution context contains the normalized RIDs and the caller's prior context is restored after success, failure, timeout, cancellation, and formatter error.
8. **Given** B3 tracing and a retryable failure, **when** an operation retries, **then** client creation and all attempts share one SDK-native B3 context, no W3C context is claimed, and the prior context is restored.
9. **Given** native SDK timeout, connection, 429, 503, authentication, permission, validation, not-found, internal, or configuration failure, **when** retry policy terminates, **then** attempt counts and ADR-001 exit codes are correct and stdout contains one safe JSON error.
10. **Given** a successful model response, **when** output is formatted, **then** stdout contains one decoded result, stderr contains no response data, and logs contain no prompt, tool, document, image, vector, credential, token, or attribution RID.
11. **Given** concurrent or nested invocations, **when** they complete on any exit path, **then** attribution and B3 values remain isolated and each caller's previous context is restored.
12. **Given** a clean wheel or editable install, **when** console help, Claude launcher help, imports, and metadata-only checks run outside the repository CWD, **then** both operations and the packaged 0/2 policy work without changing existing entry points or causing import-time side effects.

## Completion state

DESIGN-012 is complete and ready for implementation. The two SDK signatures, CLI inputs, ACL correction, Tier-3 policy, attribution behavior, tracing, retry semantics, privacy boundary, package layout, work breakdown, and QA evidence are defined above.
