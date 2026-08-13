---
name: pal-found-aip-agents
description: Manage Foundry AIP agents, versions, sessions, content, and traces through local session aliases.
---

# Foundry AIP Agents

Run `pal-found-aip-agents --help` for command syntax. The namespace exposes 15 SDK v2 operations plus local `session purge`.

## Capability and source

Foundry AIP agents provide agent/version metadata plus aliased sessions for
blocking, streaming, cancellation, RAG context, content, titles, and traces.
The CLI exposes the 15 SDK operations listed below; `session purge` is local
cleanup, not an SDK operation.

Source: [Palantir AIP overview](https://www.palantir.com/docs/foundry/aip/overview); reviewed 2026-08-13.

Operations: `agent all-sessions|get`; `agent-version get|list`; `content get`;
`session blocking-continue|cancel|create|delete|get|list|rag-context|
streaming-continue|update-title`; `session-trace get`.

Create a session with `session create --alias NAME --agent-rid RID`. Later session, content, and trace commands use that alias; they do not accept raw session IDs. Aliases are normalized and stored under the configured session path. Cleanup runs once per command. `session delete` marks local state completed, while `session purge` removes unlocked local records without deleting remote sessions.

Paged commands are `agent all-sessions`, `agent-version list`, and `session list`. They fetch one server page by default. Use `--batch-pages` for up to 40 pages and read continuation metadata from stderr.

`session streaming-continue` receives eager bytes from the current SDK, writes only the configured file-size prefix, and returns JSON checksums and file metadata. The write limit does not bound memory already allocated by the SDK.

ACL checks run before alias access, SDK calls, downloads, and purge. Metadata-only mode permits six metadata routes from the packaged policy. AIP Agents requests suppress attribution while preserving the caller's prior SDK context. Prompts, contexts, response bytes, and tokens must not enter logs.

Success data and structured errors go to stdout. Logs and pagination metadata go to stderr. Objects, purge results, and download envelopes use JSON; uniform non-empty lists may use TOON in auto mode.

### Parameters and JSON

All remote commands accept `--timeout`, `--format json|toon|auto`, and
`--pretty`; paged commands add `--page-size`, `--page-token`, and
`--batch-pages`. `session purge` accepts `--format` and `--pretty`, but no
timeout. `--alias` is required for session, content, and trace commands;
`agent get` accepts optional `--version`, and session create requires
`--agent-rid` with optional `--agent-version`.

The exchange commands require JSON object inputs `--parameter-inputs-json`
and `--user-input-json`. `session blocking-continue` and
`session streaming-continue` also accept optional list
`--contexts-override-json`; streaming accepts `--message-id`,
`--session-trace-id`, and `--output-filename`. `session cancel` requires
`--message-id` and optionally accepts `--response`; `session update-title`
requires `--title`; trace get requires `--session-trace-id`.
`agent-version get` uses positional `agent_rid agent_version_string`; session
list uses positional `agent_rid`.
