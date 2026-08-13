---
name: pal-found-aip-agents
description: Manage Foundry AIP agents, versions, sessions, content, and traces through local session aliases.
---

# Foundry AIP Agents

Run `pal-found-aip-agents --help` for command syntax. The namespace exposes 15 SDK v2 operations plus local `session purge`.

Create a session with `session create --alias NAME --agent-rid RID`. Later session, content, and trace commands use that alias; they do not accept raw session IDs. Aliases are normalized and stored under the configured session path. Cleanup runs once per command. `session delete` marks local state completed, while `session purge` removes unlocked local records without deleting remote sessions.

Paged commands are `agent all-sessions`, `agent-version list`, and `session list`. They fetch one server page by default. Use `--batch-pages` for up to 40 pages and read continuation metadata from stderr.

`session streaming-continue` receives eager bytes from the current SDK, writes only the configured file-size prefix, and returns JSON checksums and file metadata. The write limit does not bound memory already allocated by the SDK.

ACL checks run before alias access, SDK calls, downloads, and purge. Metadata-only mode permits six metadata routes from the packaged policy. AIP Agents requests suppress attribution while preserving the caller's prior SDK context. Prompts, contexts, response bytes, and tokens must not enter logs.

Success data and structured errors go to stdout. Logs and pagination metadata go to stderr. Objects, purge results, and download envelopes use JSON; uniform non-empty lists may use TOON in auto mode.
