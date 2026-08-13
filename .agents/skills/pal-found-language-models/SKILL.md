---
name: pal-found-language-models
description: Run Foundry Anthropic messages and OpenAI embeddings inference.
---

# Foundry Language Models

Run `pal-found-language-models --help` for syntax. Supported commands are `anthropic-model messages` and `open-ai-model embeddings`.

All structured public options use a `-json` suffix. The CLI validates outer JSON containers locally; the SDK validates nested message, tool, and provider schemas. Both commands are cost-bearing writes. Read-only and metadata-only policy can block them before client creation.

Configured attribution and B3 context remain active across client creation and every retry, then restore the caller's prior context. Retries have at-least-once semantics. A provider may finish inference before a transport failure reaches the CLI, so retrying can repeat cost or return different content. Do not add another automatic retry loop after this CLI exhausts its policy.

Successful content or vectors go only to stdout. Logs and errors must not contain prompts, tools, documents, images, vectors, credentials, tokens, or attribution RIDs. This namespace has no pagination, binary, session, raw-response, or streaming commands.
