# DESIGN-016 - Foundry Streams CLI

| Field | Value |
| --- | --- |
| Story | DEV-STORY-016 |
| Status | Completed; ready for implementation |
| Date | 2026-08-10 |
| Scope | `foundry-streams` CLI and Claude skill, 15 Streams API v2 operations (batch strategy per ADR-003) |

## Technical summary

Add a Streams namespace CLI exposing exactly 15 public `foundry_sdk.v2.streams` operations across the `Dataset`, `Stream`, and `Subscriber` client paths. The CLI uses the SDK's public nested clients and excludes preview and internal parameters. Record-reading operations implement the ADR-003 batch-response pattern: retrieve up to `--max-records` records then exit; no persistent streaming or progressive stdout emission.

Every command supports the shared `--timeout`, `--format`, and `--pretty` options. JSON-shaped inputs are parsed and validated locally before the client is created. Optional SDK arguments are omitted when the user does not provide them. The client factory and `invocation_scope` use `include_attribution=False`; this namespace must not add attribution configuration (outside FR-ATTR-4 scope).

> **Operation count note:** The story title, ADR-003, and SAD-001 reference "17 operations". The vendored SDK (v1.102.0) exposes exactly **15** public operations across `Dataset` (1), `Stream` (7), and `Subscriber` (7). The canonical environment-variable reference and the metadata allow-list are concordant at 15 rows each. This design implements the actual SDK surface; the stale "17" count is corrected here and in the story comments.

## Evidence and governing references

This design follows:

- SRS-001 FR-ACL, FR-ERR, FR-OUT, FR-PAG, FR-TRACE, FR-ASYNC, and the privacy requirements;
- SAD-001 namespace packaging and stateless CLI structure (EPIC-006, DEV-STORY-016 entry);
- DESIGN-005 tracing, retry, and common-component integration contracts;
- DESIGN-011 patterns for an immutable operation catalog, exact nested SDK dispatch, packaged policy, and SDK-native error handling;
- DESIGN-012 patterns for JSON argument validation and output contracts;
- ADR-001 exit codes, ADR-002 timeouts, ADR-003 batch-response strategy, ADR-004 format selection, ADR-005 logging, ADR-006 configuration search, and ADR-007 read-only precedence;
- the canonical environment-variable reference, which defines operation enablement and read-only overrides (namespace `streams`, 15 rows, plus `FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S`);
- the canonical metadata allow-list, which blocks 12 of the 15 operations in tier 3;
- vendored SDK sources under `foundry_sdk/v2/streams/` (`_client.py`, `dataset.py`, `stream.py`, `subscriber.py`).

## Operation catalog

CLI names use kebab-case. Catalog keys and ACL paths use snake_case. `OP_SPECS` contains exactly 15 unique entries.

| # | CLI command | SDK dispatch | Required input | Optional input | HTTP and result |
| ---: | --- | --- | --- | --- | --- |
| 1 | `dataset create` | `client.streams.Dataset.create` | `--name`, `--parent-folder-rid`, `--schema-json` | `--branch-name`, `--compressed`, `--partitions-count`, `--stream-type` | `POST /v2/streams/datasets/create`; `Dataset` |
| 2 | `stream create` | `client.streams.Dataset.Stream.create` | `dataset_rid`, `--branch-name`, `--schema-json` | `--compressed`, `--partitions-count`, `--stream-type` | `POST /v2/streams/datasets/{datasetRid}/streams`; `Stream` |
| 3 | `stream get` | `client.streams.Dataset.Stream.get` | `dataset_rid`, `stream_branch_name` | — | `GET /v2/streams/datasets/{datasetRid}/streams/{streamBranchName}`; `Stream` |
| 4 | `stream get-end-offsets` | `client.streams.Dataset.Stream.get_end_offsets` | `dataset_rid`, `stream_branch_name` | `--view-rid` | `GET /v2/highScale/streams/datasets/{datasetRid}/streams/{streamBranchName}/getEndOffsets`; `GetEndOffsetsResponse` |
| 5 | `stream get-records` | `client.streams.Dataset.Stream.get_records` | `dataset_rid`, `stream_branch_name`, `--limit`, `--partition-id` | `--start-offset`, `--view-rid` | `GET /v2/highScale/streams/datasets/{datasetRid}/streams/{streamBranchName}/getRecords`; `GetRecordsResponse` |
| 6 | `stream publish-binary-record` | `client.streams.Dataset.Stream.publish_binary_record` | `dataset_rid`, `stream_branch_name`, `--file` | `--view-rid` | `POST /v2/highScale/streams/datasets/{datasetRid}/streams/{streamBranchName}/publishBinaryRecord`; None |
| 7 | `stream publish-record` | `client.streams.Dataset.Stream.publish_record` | `dataset_rid`, `stream_branch_name`, `--record-json` | `--view-rid` | `POST /v2/highScale/streams/datasets/{datasetRid}/streams/{streamBranchName}/publishRecord`; None |
| 8 | `stream publish-records` | `client.streams.Dataset.Stream.publish_records` | `dataset_rid`, `stream_branch_name`, `--records-json` | `--view-rid` | `POST /v2/highScale/streams/datasets/{datasetRid}/streams/{streamBranchName}/publishRecords`; None |
| 9 | `stream reset` | `client.streams.Dataset.Stream.reset` | `dataset_rid`, `stream_branch_name` | `--schema-json`, `--compressed`, `--partitions-count`, `--stream-type` | `POST /v2/streams/datasets/{datasetRid}/streams/{streamBranchName}/reset`; `Stream` |
| 10 | `subscriber create` | `client.streams.Dataset.Stream.Subscriber.create` | `dataset_rid`, `stream_branch_name`, `--subscriber-id` | `--read-position-json` | `POST /v2/streams/datasets/{datasetRid}/streams/{streamBranchName}/subscribers`; `Subscriber` |
| 11 | `subscriber commit-offsets` | `client.streams.Dataset.Stream.Subscriber.commit_offsets` | `dataset_rid`, `stream_branch_name`, `subscriber_subscriber_id`, `--offsets-json` | `--view-rid` | `POST /v2/highScale/streams/datasets/{datasetRid}/streams/{streamBranchName}/subscribers/{subscriberSubscriberId}/commitOffsets`; `PartitionOffsets` |
| 12 | `subscriber delete` | `client.streams.Dataset.Stream.Subscriber.delete` | `dataset_rid`, `stream_branch_name`, `subscriber_subscriber_id` | — | `DELETE /v2/streams/datasets/{datasetRid}/streams/{streamBranchName}/subscribers/{subscriberSubscriberId}`; None |
| 13 | `subscriber get-read-position` | `client.streams.Dataset.Stream.Subscriber.get_read_position` | `dataset_rid`, `stream_branch_name`, `subscriber_subscriber_id` | `--view-rid` | `GET /v2/highScale/streams/datasets/{datasetRid}/streams/{streamBranchName}/subscribers/{subscriberSubscriberId}/getReadPosition`; `PartitionOffsets` |
| 14 | `subscriber read-records` | `client.streams.Dataset.Stream.Subscriber.read_records` | `dataset_rid`, `stream_branch_name`, `subscriber_subscriber_id` | `--auto-commit`, `--limit`, `--partition-ids-json`, `--view-rid` | `POST /v2/highScale/streams/datasets/{datasetRid}/streams/{streamBranchName}/subscribers/{subscriberSubscriberId}/readRecords`; `ReadSubscriberRecordsResponse` |
| 15 | `subscriber reset-offsets` | `client.streams.Dataset.Stream.Subscriber.reset_offsets` | `dataset_rid`, `stream_branch_name`, `subscriber_subscriber_id`, `--position-json` | — | `POST /v2/highScale/streams/datasets/{datasetRid}/streams/{streamBranchName}/subscribers/{subscriberSubscriberId}/resetOffsets`; `PartitionOffsets` |

### Batch-response contract (ADR-003)

Record-reading operations aggregate into a JSON array (or TOON if uniform) emitted on CLI exit. Records are never emitted progressively.

- `stream get-records` — `--limit` is required by the SDK; expose it as `--max-records` (default 100, max 10,000), mapped to the SDK `limit` argument.
- `subscriber read-records` — `--max-records` (default 100, max 1000 per SDK server limit), mapped to the SDK `limit` argument; offsets are committed only when `--auto-commit` is passed, otherwise the caller commits explicitly via `subscriber commit-offsets`.
- `stream publish-binary-record` — the SDK accepts `bytes`; the CLI reads the file from `--file` and passes the content to the SDK (the SDK streams the upload internally). File size bounded by the standard download/upload limit.
- All other operations are single-call — no change needed.

**Stream read timeout:** `FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S` (default 120s) per ADR-002/ADR-003 overrides the shared default timeout for this namespace.

### Paging contract

No operation in the Streams namespace returns a `ResourceIterator` or a next-page token. `PaginationHelper` and `--page-size`/`--page-token`/`--all`/`--max-pages` flags are not required. Batch reads are bounded by `--max-records`, and callers that need more records call iteratively (for subscribers, using the committed read position).

### Binary handling

No operation returns a streamed file download. `publish_binary_record` uploads local file content via the SDK's internal streaming upload. `BinaryDownloadHandler` is not required for reading, but the file-read for the binary publish must be bounded and validated before client construction.

## Access and runtime policy

The write set is `dataset.create`, `stream.create`, `stream.publish_binary_record`, `stream.publish_record`, `stream.publish_records`, `stream.reset`, `subscriber.create`, `subscriber.commit_offsets`, `subscriber.delete`, and `subscriber.reset_offsets` (10 operations). The shared `AccessControlGuard` write classification must add `reset` (the `stream.reset` and `subscriber.reset_offsets` verbs are not currently in `_WRITE_VERBS`; this is the same class of change as the DESIGN-013/014 additions of `launch`/`promote`/`pause`/`unpause`). `stream.get_records` and `subscriber.read_records` are semantic reads despite `read_records` using POST — they consume data but do not mutate stream state (with `auto_commit=false` default, no offset mutation occurs). Read-only mode blocks the complete write set unless a canonical override permits it.

Metadata-only policy is fail closed. It permits exactly 3 operations (`stream.get`, `stream.get_end_offsets`, `subscriber.get_read_position`) and blocks the remaining 12 (all mutations and all record content reads), matching the canonical allow-list. Namespace and exact-operation controls are evaluated before the client is constructed.

Use SDK-native B3 tracing through `invocation_scope` and restore context after success and failure. Retry only the ADR-approved transient conditions and disclose at-least-once behavior because retrying create, publish, reset, commit, or delete can duplicate records or cost. Offset state is mutated only by explicit `commit_offsets` or `--auto-commit` reads; retried reads without auto-commit are safe.

## Component breakdown

- `src/foundry_cli/streams/` — command catalog, parser, dispatch, JSON validators, batch-read integration, packaged metadata-only policy.
- Claude skill and launcher for `foundry-streams`.
- Focused unit and integration test modules.
- `pyproject.toml` console entry point, package data, and quality-tool scope.

## Estimates and sprint fit

| Sub-task | Assignee | Estimated hours |
| --- | --- | --- |
| DESIGN-016 | tech-lead | 6 |
| DEV-016 | python-developer | 16 |
| UNITTEST-016 | python-developer | 12 |
| CODEREVIEW-016 | tech-lead | 6 |
| TESTCASE-016 | qa-engineer | 8 |
| TESTEXEC-016 | qa-engineer | 8 |
| DEVOPS-016 | devops-engineer | 3 |
| **Total** | | **59** |

The story fits within one sprint (15 operations; 3 client paths with a clear ACL and batch-read contract). No split into additional stories is required.

## Risks

Duplicate records or cost under at-least-once retries (create, publish, reset, commit, delete); batch-read volume bounded by `--max-records`; subscriber offset semantics (explicit commit vs auto-commit); SDK schema drift; the stale "17-operation" count in ADR-003 and SAD-001 (corrected to 15); packaged-policy drift; and shared ACL classification changes.
