---
id: DEV-STORY-012
type: dev_story
title: foundry-language-models skill (2 operations)
status: Closed
feature_request: FEATURE-001
epic: EPIC-005
created: 2026-04-13
updated: 2026-08-09
priority: High
resolution: Done
assignee: architect
reporter: architect
story_points: 5
release_notes: Adds the foundry-language-models CLI and Claude skill for Anthropic message generation and OpenAI embeddings through Foundry API v2. The skill validates structured model inputs, supports opt-in attribution and SDK-native B3 tracing, applies namespace and operation controls, retries transient failures, and returns structured JSON results and errors.
---

# DEV-STORY-012: foundry-language-models skill (2 operations)

## Description

Implement the complete public `foundry_sdk.v2.language_models` surface. The existing placeholder description of listing language models and retrieving model metadata is incorrect: this namespace exposes Anthropic message generation and OpenAI embeddings, with no discovery or metadata operation.

### Authoritative operation catalog

| # | CLI route | SDK call | HTTP endpoint | Required inputs | Optional inputs | Return | Tier 3 |
|---|---|---|---|---|---|---|---|
| 1 | `anthropic-model messages` | `client.language_models.AnthropicModel.messages` | `POST /v2/languageModels/anthropic/{anthropicModelModelId}/messages` | Positional `anthropic_model_model_id`; `max_tokens` integer; `--messages-json` array of objects | `--output-config-json` object; `--stop-sequences-json` array of strings; `--system-json` array of objects; `temperature` float; `--thinking-json` object; `--tool-choice-json` object; `--tools-json` array of objects; `top_k` integer; `top_p` float | `AnthropicMessagesResponse` | BLOCKED |
| 2 | `open-ai-model embeddings` | `client.language_models.OpenAiModel.embeddings` | `POST /v2/languageModels/openAi/{openAiModelModelId}/embeddings` | Positional `open_ai_model_model_id`; `--input-json` array of strings | `dimensions` integer; `encoding_format` enum `FLOAT` or `BASE64` | `OpenAiEmbeddingsResponse` | BLOCKED |

Public structured flags use the explicit `-json` names above. After validation, the CLI forwards them under the exact SDK keyword names: `messages`, `input`, `output_config`, `stop_sequences`, `system`, `thinking`, `tool_choice`, and `tools`.

Both commands support the common timeout, output-format, and pretty-print options. They use configured attribution and SDK-native tracing. They do not expose `preview`, raw-response, or streaming flags. Neither operation uses pagination, binary transfer, or session state.

## Acceptance Criteria

### AC-1: Complete catalog

- The parser and operation registry expose exactly `anthropic-model messages` and `open-ai-model embeddings` for this namespace.
- No list, discovery, metadata, or other invented operation is present.

### AC-2: Anthropic messages contract

- `anthropic-model messages` resolves `client.language_models.AnthropicModel.messages` and calls the documented POST endpoint.
- It requires the model ID, integer `max_tokens`, and `--messages-json` as an array of objects; accepts only the cataloged optional values through `--output-config-json`, `--stop-sequences-json`, `--system-json`, `--thinking-json`, `--tool-choice-json`, `--tools-json`, and scalar flags; forwards exact SDK keyword names; and returns `AnthropicMessagesResponse`.

### AC-3: OpenAI embeddings contract

- `open-ai-model embeddings` resolves `client.language_models.OpenAiModel.embeddings` and calls the documented POST endpoint.
- It requires the model ID and `--input-json` as an array of strings, accepts optional integer `dimensions` and `FLOAT` or `BASE64` encoding, forwards the SDK keyword `input`, and returns `OpenAiEmbeddingsResponse`.

### AC-4: Input validation

- Missing required inputs, invalid JSON, wrong container or element types, invalid integers or floats, and unsupported enum values return ADR-001 exit code 1 with a structured error.
- Validation finishes before configuration-dependent client creation or any SDK call.

### AC-5: Access control

- `AccessControlGuard` evaluates global, `language_models` namespace, and operation controls before client creation or SDK work; `ENABLED=false` denies both operations before client creation.
- `messages` and `embeddings` are inference writes because they trigger billable execution. Read-only blocks both unless the canonical namespace or operation `READONLY=false` override permits them. Metadata-only blocks both, and Tier 3 blocks both exactly as the metadata allow-list specifies.
- `messages` and `embeddings` are added to `AccessControlGuard._WRITE_VERBS`, with tests for default denial, namespace and operation overrides, metadata-only denial, Tier 3 denial, and guard-before-client ordering.

### AC-6: Attribution

- The invocation scope and client factory are both called with `include_attribution=True`.
- When attribution is enabled, configured attribution reaches each attempt; prior SDK attribution context is restored after success, failure, timeout, or cancellation.

### AC-7: B3 tracing

- When tracing is enabled, valid SDK-native B3 trace, span, and sampled values remain stable across retries and prior SDK context is restored on every exit path.
- When tracing is disabled, SDK trace context is unchanged; the skill does not claim W3C `traceparent` or `tracestate` support.

### AC-8: Errors, retries, and timeouts

- Authentication, permission, input, not-found, conflict, timeout, cancellation, rate-limit, service, and unexpected SDK failures follow ADR-001 structured errors and exit codes.
- ADR-002 retry and timeout behavior applies only to retryable transient failures and never duplicates successful output.

### AC-9: Output and privacy

- Successful SDK model responses are serialized as structured JSON through the common formatter; `--pretty` affects presentation only.
- Results go to stdout and safe diagnostics to stderr without exposing tokens, prompts, message content, embedding inputs, response content, or attribution values in logs.

### AC-10: Packaging and installed execution

- The console entry, packaged metadata allow-list, Claude skill, and launcher are included in wheel and editable installs.
- Console and launcher help, imports, policy lookup, and representative commands work from an empty working directory without repository-relative imports.

### AC-11: Compatibility and quality gates

- Parser, dispatch, both exact SDK calls, JSON flag validation, ACL modes and overrides, attribution, B3 context, retries, errors, JSON output, privacy, console entry, and Claude launcher are covered on Python 3.11 and 3.12.
- The canonical Ruff, mypy, Bandit, package, full-regression, and branch-coverage gates pass, with branch coverage at or above 80%.

## Related Documentation

- `.ept/docs/document_index.md`
- `.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md` — FR-AUTH, FR-OUT, FR-ASYNC, FR-ERR, FR-ATTR, FR-TRACE, FR-ACL, FR-SKILL, and NFR sections
- `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md` — Language Models namespace, shared cross-cutting components, and EPIC-005 roadmap context
- `.ept/docs/deliverables/architecture/canonical-env-var-reference.md` — both `language_models` operation rows
- `.ept/docs/deliverables/architecture/metadata-allow-list.md` — both `language_models` operations blocked in Tier 3
- `.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md`
- `.ept/docs/deliverables/architecture/adr/ADR-002-call-timeout-defaults.md`
- `.ept/docs/deliverables/architecture/adr/ADR-004-format-auto-algorithm.md`
- `.ept/docs/deliverables/architecture/adr/ADR-005-log-format.md`
- `.ept/docs/deliverables/architecture/adr/ADR-006-env-file-search-path.md`
- `.ept/docs/deliverables/architecture/adr/ADR-007-operation-level-readonly.md`
- `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/language_models/`

## Technical Scope

- Add `src/foundry_cli/language_models/`, its CLI module, and packaged metadata allow-list.
- Add `.claude/skills/foundry-language-models/SKILL.md` and its launcher.
- Add parser, routing, JSON validation, ACL, attribution, tracing, retry, error, output, packaging, console-wrapper, and installed-package tests.
- Add the `foundry-language-models` console entry, package data, and namespace-specific Ruff configuration in `pyproject.toml`.
- Add `messages` and `embeddings` to `AccessControlGuard._WRITE_VERBS`; treat both as billable inference writes. Read-only blocks them unless the canonical namespace or operation override sets `READONLY=false`; metadata-only and Tier 3 block both.
- Reuse `ConfigLoader`, `AccessControlGuard`, the async client factory, `RetryHandler`, `OutputFormatter`, `ErrorSerializer`, and `LogSetup`.
- Use the exact nested `AnthropicModel` and `OpenAiModel` clients. Both `invocation_scope` and `create` use `include_attribution=True`.

## Boundaries

- No model discovery, listing, or metadata retrieval.
- No sessions, prompt persistence, streaming or raw responses, pagination, binary transfer, Foundry API v1, OAuth flow, local state, W3C tracing claim, or changes to other namespace catalogs.

## Notes

The SDK source, canonical environment reference, and metadata allow-list agree on the two-operation count and contracts. No stakeholder question remains open. Preserve the fields supplied by `AnthropicMessagesResponse` and `OpenAiEmbeddingsResponse` during SDK-model serialization; do not invent a manual response envelope or log response fields.
