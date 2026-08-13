---
name: pal-found-media-sets
description: Run Foundry Media Sets API v2 operations across the MediaSet client: transaction lifecycle (create/commit/abort/clear), media item metadata, content reads/downloads, transformation jobs, and binary uploads.
---

# Foundry Media Sets

## Capability and source

Foundry Media Sets stores binary media with metadata, references, transaction
lifecycle, retrieval, and transformation operations. This CLI exposes all 19
MediaSet v2 operations and applies bounded file transfer handling.

Source: [Palantir Foundry documentation](https://www.palantir.com/docs/foundry); reviewed 2026-08-13.

Run `pal-found-media-sets --help` for syntax. The CLI exposes exactly 19 Media Sets v2 operations: `media-set abort|calculate|clear|commit|create|get|get-result|get-rid-by-path|get-status|info|metadata|read|read-original|reference|register|retrieve|transform|upload|upload-media`.

Transactional media sets require an explicit open-create-commit cycle: `media-set create` opens a transaction and returns a `TransactionId`; `media-set upload` accepts `--transaction-id`; `media-set commit` makes items visible; `media-set abort` deletes them; `media-set clear` requires `--transaction-id` for transactional media sets. The CLI passes these through as flags; it does not auto-manage transactions.

Binary downloads (`media-set get-result`, `read`, `read-original`, `retrieve`) are streamed and persisted bounded by the FR-DL limit via BinaryDownloadHandler; `--output` selects the target path and a JSON envelope (`file_path`, `file_size`, `checksum_md5`, `checksum_sha256`, `mime_type`, `truncated`, `source_size`, `source_size_at_least`) is emitted to stdout. Binary uploads (`media-set upload`, `media-set upload-media`) read the `--file` content (bounded at 16 MiB). Structured options use a `-json` suffix (`--transformation-json`) and are validated locally before any client is created.

Access control runs before client and filesystem effects. The write set is `abort`, `calculate`, `clear`, `commit`, `create`, `register`, `transform`, `upload`, and `upload_media` (9 operations); read-only mode blocks them before any work. `get-result`, `read`, `read-original`, and `retrieve` are semantic reads but are blocked under metadata-only mode because they expose file content. Metadata-only policy is fail closed: exactly 5 operations (`get`, `get-rid-by-path`, `get-status`, `info`, `metadata`) are permitted and the other 14 are blocked.

Client creation and invocation scope use `include_attribution=True` per FR-ATTR-4; attribution RIDs are read from `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS` and passed only when enabled. SDK-native B3 context remains active across client creation and every retry, then restores the caller's prior context. Retries have at-least-once semantics; retrying create/commit/abort/upload/register/transform can duplicate items, re-run transformations, or cost. Do not add another automatic retry loop after this CLI exhausts its policy.

Successful results go only to stdout. Logs and errors must not contain credentials, tokens, attribution RIDs, or media content.

### Parameters and JSON

Every operation accepts `--timeout`, `--format json|toon|auto`, and `--pretty`.
The positional identifiers are the media-set RID, media-item RID,
transaction ID, and transformation-job ID shown by `--help`. Transaction
operations use `--transaction-id` and, where supported, `--branch-name` or
`--branch-rid`; path lookups and registration use `--media-item-path`.
`media-set upload` requires `--file` and may accept `--media-item-rid`,
`--media-item-path`, `--transaction-id`, or view/branch selectors.
View selection uses `--view-rid`.
`media-set upload-media` requires `--file` and `--filename` and may accept
`--media-item-rid`.

`media-set transform` requires `--transformation-json`; `--token` is used by
transformation-job reads, while media content reads use `--read-token`.
Downloads (`get-result`, `read`, `read-original`, and `retrieve`) use
`--output`. `media-set register` requires `--physical-item-name`.
`--preview` is available on operations that expose the SDK preview option.
