---
name: pal-found-checkpoints
description: Run Foundry Checkpoints API v2 operations through the Record client: single-record get, batch get, and cursor-paged record search.
---

# Foundry Checkpoints

Run `pal-found-checkpoints --help` for syntax. The CLI exposes exactly 3 Checkpoints v2 operations: `record get`, `record get-batch`, and `record search`.

`record get` takes one positional `record_rid`. `record get-batch` takes the required `--records-json` flag (a JSON array of `{"recordRid": "ri.checks.main.record.xxx"}` elements, bounded at 100 by the SDK contract) and dispatches its body positionally. `record search` takes the required `--where-json` flag (the search filter object) plus the optional `--sort-direction`.

`record search` returns a `SearchCheckpointRecordsResponse` with a `next_page_token` cursor and is the only paged operation. It accepts the ADR-003 cursor-paged flags `--page-size`, `--page-token`, `--all`, and `--max-pages` (at most 40 actual pages). `record get` and `record get-batch` have no cursor and expose no pagination flags. Structured options use the `-json` suffix and are validated locally before any client is created.

All 3 operations are semantic reads. `record get_batch` and `record search` use POST but read only; the namespace has zero write operations and read-only mode permits everything. Metadata-only policy is fail closed and permits exactly all 3 operations (`record.get`, `record.get_batch`, `record.search`).

Client creation and invocation scope use `include_attribution=False`. SDK-native B3 context remains active across client creation and every retry, then restores the caller's prior context. Retries cover only ADR-002 transient conditions; all 3 operations are safe to retry (no mutating or billable side effects). Do not add another automatic retry loop after this CLI exhausts its policy.

Successful results go only to stdout. Logs and errors must not contain credentials, tokens, or record content.
