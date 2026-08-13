---
name: pal-found-sql-queries
description: Run Foundry SQL Queries API v2 operations: cancel, execute, execute-ontology, get-results, and get-status.
---

# Foundry SQL Queries

## Capability and source

Foundry SQL Queries runs ad-hoc SQL, including ontology-aware queries, status
and cancellation, and bounded Arrow result downloads. This CLI exposes all
five `SqlQuery` operations.

Source: [Palantir SQL queries API](https://www.palantir.com/docs/foundry/api/v2/general/overview); reviewed 2026-08-13.

Run `pal-found-sql-queries --help` for syntax. The CLI exposes exactly 5 SqlQueries v2 operations on the `query` resource: `query cancel`, `query execute`, `query execute-ontology`, `query get-results`, `query get-status`.

Structured public options use a `-json` suffix (`--fallback-branch-ids-json`, `--parameters-json`) and are validated locally before any client is created. `query execute-ontology` and `query get-results` return Arrow bytes: both write bounded content atomically under the configured download path and emit a metadata envelope; they never print content bytes. `query get-results` long-polls the server (up to 1 minute) and can be safely retried while the query is still running.

Access control runs before client and filesystem effects. The write set is `cancel`, `execute`, and `execute-ontology`; read-only mode blocks them before any work. Metadata-only policy is fail closed: exactly 1 operation (`query get-status`) is permitted and the other 4 are blocked.

Client creation and invocation scope use `include_attribution=False`. SDK-native B3 context remains active across client creation and every retry, then restores the caller's prior context. Retries have at-least-once semantics; retrying `execute`, `execute-ontology`, or `cancel` can duplicate billable work or cost. Do not add another automatic retry loop after this CLI exhausts its policy.

Successful results or metadata envelopes go only to stdout. Logs and errors must not contain prompts, queries, downloaded bytes, credentials, tokens, or attribution RIDs.

### Parameters and JSON

All commands accept `--timeout`, `--format json|toon|auto`, and `--pretty`.
`query execute` requires scalar `--query` and optionally accepts
`--fallback-branch-ids-json`; `query execute-ontology` requires `--query` and
optionally accepts `--parameters-json`, `--dry-run`, and `--row-limit`.
`query cancel`, `query get-status`, and `query get-results` take positional
`sql_query_id`; get-results optionally accepts `--output`. JSON inputs are
validated before client creation.
