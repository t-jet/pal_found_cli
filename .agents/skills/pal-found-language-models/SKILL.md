---
name: pal-found-language-models
description: Run Foundry Anthropic messages and OpenAI embeddings inference.
---

# Foundry Language Models

## Capability and source

Foundry language-model APIs provide Anthropic message inference and OpenAI
embedding generation. This CLI exposes exactly those two provider operations;
both may incur model usage charges.

Source: [Palantir AIP overview](https://www.palantir.com/docs/foundry/aip/overview); reviewed 2026-08-13.

Run `pal-found-language-models --help` for syntax. Supported commands are `anthropic-model messages` and `open-ai-model embeddings`.

All structured public options use a `-json` suffix. The CLI validates outer JSON containers locally; the SDK validates nested message, tool, and provider schemas. Both commands are cost-bearing writes. Read-only and metadata-only policy can block them before client creation.

Configured attribution and B3 context remain active across client creation and every retry, then restore the caller's prior context. Retries have at-least-once semantics. A provider may finish inference before a transport failure reaches the CLI, so retrying can repeat cost or return different content. Do not add another automatic retry loop after this CLI exhausts its policy.

Successful content or vectors go only to stdout. Logs and errors must not contain prompts, tools, documents, images, vectors, credentials, tokens, or attribution RIDs. This namespace has no pagination, binary, session, raw-response, or streaming commands.

### Parameters and JSON

Both commands accept positional `model_id`, `--timeout`,
`--format json|toon|auto`, and `--pretty`. Anthropic `messages` requires
`--max-tokens` and `--messages-json`; optional JSON variants are
`--output-config-json`, `--stop-sequences-json`, `--system-json`,
`--thinking-json`, `--tool-choice-json`, and `--tools-json`, plus scalar
`--temperature`, `--top-k`, and `--top-p`. OpenAI `embeddings` requires
`--input-json` and optionally accepts integer `--dimensions` and choice
`--encoding-format FLOAT|BASE64`.
