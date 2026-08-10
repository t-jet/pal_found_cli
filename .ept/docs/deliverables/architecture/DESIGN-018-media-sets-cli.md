# DESIGN-018 - Foundry Media Sets CLI

| Field | Value |
| --- | --- |
| Story | DEV-STORY-018 |
| Status | Completed; ready for implementation |
| Date | 2026-08-10 |
| Scope | `foundry-media-sets` CLI and Claude skill, 19 Media Sets API v2 operations |

## Technical summary

Add a Media Sets namespace CLI exposing exactly 19 public `foundry_sdk.v2.media_sets` operations across the single `MediaSet` client path. The CLI uses the SDK's public nested client and excludes preview and internal parameters.

Every command supports the shared `--timeout`, `--format`, and `--pretty` options. JSON-shaped inputs are parsed and validated locally before the client is created. Optional SDK arguments are omitted when the user does not provide them. The client factory and `invocation_scope` use `include_attribution=True` because FR-ATTR-4 explicitly lists `media_sets.media_set.*`; attribution RIDs are read from `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS` and passed only when enabled.

> **Operation count note:** The story title and SAD-001 reference "19 operations". The vendored SDK (v1.102.0) exposes exactly **19** public operations on `MediaSet`. The canonical environment-variable reference and the metadata allow-list are concordant at 19 rows each. The count is confirmed accurate; no correction is required.

## Evidence and governing references

This design follows:

- SRS-001 FR-ACL, FR-DL, FR-ERR, FR-OUT, FR-PAG, FR-TRACE, FR-ASYNC, FR-ATTR-4, and the privacy requirements;
- SAD-001 namespace packaging and stateless CLI structure (EPIC-007, DEV-STORY-018 entry);
- DESIGN-005 tracing, retry, binary-download, and common-component integration contracts;
- DESIGN-011 patterns for an immutable operation catalog, exact nested SDK dispatch, packaged policy, and SDK-native error handling;
- DESIGN-012 patterns for JSON argument validation and output contracts;
- DESIGN-015 patterns for bounded binary downloads via `BinaryDownloadHandler`;
- ADR-001 exit codes, ADR-002 timeouts, ADR-004 format selection, ADR-005 logging, ADR-006 configuration search, and ADR-007 read-only precedence;
- the canonical environment-variable reference, which defines operation enablement and read-only overrides (namespace `media_sets`, 19 rows);
- the canonical metadata allow-list, which blocks 14 of the 19 operations in tier 3;
- vendored SDK sources under `foundry_sdk/v2/media_sets/` (`_client.py`, `media_set.py`).

## Operation catalog

CLI names use kebab-case. Catalog keys and ACL paths use snake_case. `OP_SPECS` contains exactly 19 unique entries.

| # | CLI command | SDK dispatch | Required input | Optional input | HTTP and result |
| ---: | --- | --- | --- | --- | --- |
| 1 | `media-set abort` | `client.media_sets.MediaSet.abort` | `media_set_rid`, `transaction_id` | `--preview` | `POST /v2/mediasets/{mediaSetRid}/transactions/{transactionId}/abort`; None |
| 2 | `media-set calculate` | `client.media_sets.MediaSet.calculate` | `media_set_rid`, `media_item_rid` | `--preview`, `--read-token` | `POST /v2/mediasets/{mediaSetRid}/items/{mediaItemRid}/transform/imagery/thumbnail/calculate`; `TrackedTransformationResponse` |
| 3 | `media-set clear` | `client.media_sets.MediaSet.clear` | `media_set_rid`, `--media-item-path` | `--branch-name`, `--branch-rid`, `--preview`, `--transaction-id`, `--view-rid` | `DELETE /v2/mediasets/{mediaSetRid}/items/clearAtPath`; None |
| 4 | `media-set commit` | `client.media_sets.MediaSet.commit` | `media_set_rid`, `transaction_id` | `--preview` | `POST /v2/mediasets/{mediaSetRid}/transactions/{transactionId}/commit`; None |
| 5 | `media-set create` | `client.media_sets.MediaSet.create` | `media_set_rid` | `--branch-name`, `--preview` | `POST /v2/mediasets/{mediaSetRid}/transactions`; `TransactionId` |
| 6 | `media-set get` | `client.media_sets.MediaSet.get` | `media_set_rid` | `--preview` | `GET /v2/mediasets/{mediaSetRid}`; `GetMediaSetResponse` |
| 7 | `media-set get-result` | `client.media_sets.MediaSet.get_result` | `media_set_rid`, `media_item_rid`, `transformation_job_id`, `--output` | `--preview`, `--token` | `GET /v2/mediasets/{mediaSetRid}/items/{mediaItemRid}/transformationJobs/{transformationJobId}/result`; bytes (download) |
| 8 | `media-set get-rid-by-path` | `client.media_sets.MediaSet.get_rid_by_path` | `media_set_rid`, `--media-item-path` | `--branch-name`, `--branch-rid`, `--preview`, `--view-rid` | `GET /v2/mediasets/{mediaSetRid}/items/getRidByPath`; `GetMediaItemRidByPathResponse` |
| 9 | `media-set get-status` | `client.media_sets.MediaSet.get_status` | `media_set_rid`, `media_item_rid`, `transformation_job_id` | `--preview`, `--token` | `GET /v2/mediasets/{mediaSetRid}/items/{mediaItemRid}/transformationJobs/{transformationJobId}`; `GetTransformationJobStatusResponse` |
| 10 | `media-set info` | `client.media_sets.MediaSet.info` | `media_set_rid`, `media_item_rid` | `--preview`, `--read-token` | `GET /v2/mediasets/{mediaSetRid}/items/{mediaItemRid}`; `GetMediaItemInfoResponse` |
| 11 | `media-set metadata` | `client.media_sets.MediaSet.metadata` | `media_set_rid`, `media_item_rid` | `--preview`, `--read-token` | `GET /v2/mediasets/{mediaSetRid}/items/{mediaItemRid}/metadata`; `MediaItemMetadata` |
| 12 | `media-set read` | `client.media_sets.MediaSet.read` | `media_set_rid`, `media_item_rid`, `--output` | `--preview`, `--read-token` | `GET /v2/mediasets/{mediaSetRid}/items/{mediaItemRid}/content`; bytes (download) |
| 13 | `media-set read-original` | `client.media_sets.MediaSet.read_original` | `media_set_rid`, `media_item_rid`, `--output` | `--preview`, `--read-token` | `GET /v2/mediasets/{mediaSetRid}/items/{mediaItemRid}/original`; bytes (download) |
| 14 | `media-set reference` | `client.media_sets.MediaSet.reference` | `media_set_rid`, `media_item_rid` | `--preview`, `--read-token` | `GET /v2/mediasets/{mediaSetRid}/items/{mediaItemRid}/reference`; `MediaReference` |
| 15 | `media-set register` | `client.media_sets.MediaSet.register` | `media_set_rid`, `--physical-item-name` | `--branch-name`, `--media-item-path`, `--preview`, `--transaction-id`, `--view-rid` | `POST /v2/mediasets/{mediaSetRid}/items/register`; `RegisterMediaItemResponse` |
| 16 | `media-set retrieve` | `client.media_sets.MediaSet.retrieve` | `media_set_rid`, `media_item_rid`, `--output` | `--preview`, `--read-token` | `GET /v2/mediasets/{mediaSetRid}/items/{mediaItemRid}/transform/imagery/thumbnail/retrieve`; bytes (download) |
| 17 | `media-set transform` | `client.media_sets.MediaSet.transform` | `media_set_rid`, `media_item_rid`, `--transformation-json` | `--preview`, `--token` | `POST /v2/mediasets/{mediaSetRid}/items/{mediaItemRid}/transform`; `TransformMediaItemResponse` |
| 18 | `media-set upload` | `client.media_sets.MediaSet.upload` | `media_set_rid`, `--file` | `--branch-name`, `--branch-rid`, `--media-item-path`, `--media-item-rid`, `--preview`, `--transaction-id`, `--view-rid` | `POST /v2/mediasets/{mediaSetRid}/items`; `PutMediaItemResponse` |
| 19 | `media-set upload-media` | `client.media_sets.MediaSet.upload_media` | `--file`, `--filename` | `--media-item-rid`, `--preview` | `PUT /v2/mediasets/media/upload`; `MediaReference` |

### Transaction contract

Transactional media sets require an explicit open-create-commit cycle:

- `media-set create` opens a transaction and returns a `TransactionId`.
- `media-set upload` accepts `--transaction-id` for transactional media sets.
- `media-set commit` makes uploaded items visible; `media-set abort` deletes them.
- `media-set clear` requires `--transaction-id` for transactional media sets.

The CLI passes these through as optional flags; it does not auto-manage transactions.

### Paging contract

No operation in the Media Sets namespace returns a `ResourceIterator` or a next-page token. `PaginationHelper` and `--page-size`/`--page-token`/`--all`/`--max-pages` flags are not required.

### Binary handling

Four operations return raw `bytes` (`get_result`, `read`, `read_original`, `retrieve`). The CLI dispatches these through `with_streaming_response` and writes them via `BinaryDownloadHandler`, bounded by the FR-DL size limit with the JSON envelope (`file_path`, `file_size`, `checksum_md5`, `checksum_sha256`, `mime_type`, `truncated`, nullable `source_size`, nullable `source_size_at_least`) emitted to stdout. `--output` selects the target path.

Two operations accept a binary `bytes` body (`upload`, `upload_media`). The CLI reads the file from `--file` after the ACL decision and before client construction, bounded by the standard upload size limit.

## Access and runtime policy

The write set is `abort`, `calculate`, `clear`, `commit`, `create`, `register`, `transform`, `upload`, and `upload_media` (9 operations). Read-only mode blocks the complete write set unless a canonical override permits it. `get_result`, `read`, `read_original`, and `retrieve` are semantic reads (they consume content but do not mutate media-set state) and are classified as reads; however, because they expose file content they are blocked under metadata-only mode.

Metadata-only policy is fail closed. It permits exactly 5 operations (`get`, `get_rid_by_path`, `get_status`, `info`, `metadata`) and blocks the remaining 14 (all mutations and all content reads/downloads), matching the canonical allow-list. Namespace and exact-operation controls are evaluated before the client is constructed.

Use SDK-native B3 tracing through `invocation_scope` and restore context after success and failure. Retry only the ADR-approved transient conditions and disclose at-least-once behavior because retrying `create`/`commit`/`abort`/`upload`/`register`/`transform` can duplicate items, re-run transformations, or cost.

## Component breakdown

- `src/foundry_cli/media_sets/` — command catalog, parser, dispatch, JSON validators, bounded binary download integration, packaged metadata-only policy.
- Claude skill and launcher for `foundry-media-sets`.
- Focused unit and integration test modules.
- `pyproject.toml` console entry point, package data, and quality-tool scope.

## Estimates and sprint fit

| Sub-task | Assignee | Estimated hours |
| --- | --- | --- |
| DESIGN-018 | tech-lead | 6 |
| DEV-018 | python-developer | 16 |
| UNITTEST-018 | python-developer | 12 |
| CODEREVIEW-018 | tech-lead | 6 |
| TESTCASE-018 | qa-engineer | 8 |
| TESTEXEC-018 | qa-engineer | 8 |
| DEVOPS-018 | devops-engineer | 3 |
| **Total** | | **59** |

The story fits within one sprint (19 operations; one client path with four binary downloads, two binary uploads, and a transaction lifecycle). No split into additional stories is required.

## Risks

Binary download volume bounded by `BinaryDownloadHandler` (FR-DL limits); binary upload size limits; transactional media-set semantics (create/commit/abort lifecycle, clear requires transaction id); transformation job tracking (calculate/get-status/get-result); attribution privacy requirements (FR-ATTR-4, `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS`); packaged-policy drift; and shared ACL classification changes.
