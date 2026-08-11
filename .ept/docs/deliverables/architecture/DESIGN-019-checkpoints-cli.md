# DESIGN-019 - Foundry Checkpoints CLI

| Field | Value |
| --- | --- |
| Story | DEV-STORY-019 |
| Status | Completed; ready for implementation |
| Date | 2026-08-10 |
| Scope | `foundry-checkpoints` CLI and Claude skill, 3 Checkpoints API v2 operations |

## Technical summary

Add a Checkpoints namespace CLI exposing exactly 3 public `foundry_sdk.v2.checkpoints` operations through the single `Record` client path. The CLI uses the SDK's public nested client and excludes preview and internal parameters.

Every command supports the shared `--timeout`, `--format`, and `--pretty` options. JSON-shaped inputs are parsed and validated locally before the client is created. Optional SDK arguments are omitted when the user does not provide them. The client factory and `invocation_scope` use `include_attribution=False`; this namespace is outside FR-ATTR-4 scope and must not add attribution configuration.

> **Operation count note:** The story title and SAD-001 reference "3 operations". The vendored SDK (v1.102.0) exposes exactly **3** public operations on `Record` (`get`, `get_batch`, `search`). The canonical environment-variable reference and the metadata allow-list are concordant at 3 rows each. The count is confirmed accurate; no correction is required.

## Evidence and governing references

This design follows:

- SRS-001 FR-ACL, FR-PAG, FR-TRACE, FR-ASYNC, FR-OUT, FR-ERR, and the privacy requirements;
- SAD-001 namespace packaging and stateless CLI structure (EPIC-007, DEV-STORY-019 entry);
- DESIGN-005 tracing, retry, pagination, and common-component integration contracts;
- DESIGN-011 patterns for an immutable operation catalog, exact nested SDK dispatch, packaged policy, and SDK-native error handling;
- DESIGN-012 patterns for JSON argument validation and output contracts;
- DESIGN-013 patterns for cursor pagination via `PaginationHelper`;
- ADR-001 exit codes, ADR-002 timeouts, ADR-004 format selection, ADR-005 logging, ADR-006 configuration search, and ADR-007 read-only precedence;
- the canonical environment-variable reference, which defines operation enablement and read-only overrides (namespace `checkpoints`, 3 rows);
- the canonical metadata allow-list, which permits all 3 operations in tier 3;
- vendored SDK sources under `foundry_sdk/v2/checkpoints/` (`_client.py`, `record.py`).

## Operation catalog

CLI names use kebab-case. Catalog keys and ACL paths use snake_case. `OP_SPECS` contains exactly 3 unique entries.

| # | CLI command | SDK dispatch | Required input | Optional input | HTTP and result |
| ---: | --- | --- | --- | --- | --- |
| 1 | `record get` | `client.checkpoints.Record.get` | `record_rid` | — | `GET /v2/checkpoints/records/{recordRid}`; `Record` |
| 2 | `record get-batch` | `client.checkpoints.Record.get_batch` | `--records-json` | — | `POST /v2/checkpoints/records/getBatch`; `GetRecordsBatchResponse` |
| 3 | `record search` | `client.checkpoints.Record.search` | `--where-json` | `--page-size`, `--page-token`, `--all`, `--max-pages`, `--sort-direction` | `POST /v2/checkpoints/records/search`; `SearchCheckpointRecordsResponse` |

The Checkpoints namespace has a single `Record` resource client with no nested sub-clients; all 3 operations route directly through `client.checkpoints.Record`. `preview` parameters are excluded. The `get_batch` body is a JSON list of `{"recordRid": "ri.checks.main.record.xxx"}` elements, bounded at 100 by the SDK contract.

### Paging contract

`record search` returns `SearchCheckpointRecordsResponse` with `data` (list of `Record`) and an optional `next_page_token`. It is the only paged operation; it uses `PaginationHelper` and accepts `--page-size`, `--page-token`, `--all`, and `--max-pages`. `record get` and `record get-batch` have no cursor and must not expose invented pagination flags.

### Access and runtime policy

All 3 operations are semantic reads. `record get_batch` and `record search` use POST but read only; they must not inherit write classification. The Checkpoints namespace has **zero** write operations, so no new write-verb entries are required in the shared `AccessControlGuard`.

Metadata-only policy is fail closed but the allow-list permits exactly 3 operations (`record.get`, `record.get_batch`, `record.search`). Namespace and exact-operation controls are evaluated before the client is constructed.

Use SDK-native B3 tracing through `invocation_scope` and restore context after success and failure. Retry only the ADR-approved transient conditions; all three operations are safe to retry because they have no mutating or billable side effects. `record search` preserves local cursor state across page retries.

## Component breakdown

- `src/foundry_cli/checkpoints/` — command catalog, parser, dispatch, JSON validator for `--where-json`/`--records-json`, pagination integration, packaged metadata-only policy.
- Claude skill and launcher for `foundry-checkpoints`.
- Focused unit and integration test modules.
- `pyproject.toml` console entry point, package data, and quality-tool scope.

## Estimates and sprint fit

| Sub-task | Assignee | Estimated hours |
| --- | --- | --- |
| DESIGN-019 | tech-lead | 6 |
| DEV-019 | python-developer | 16 |
| UNITTEST-019 | python-developer | 12 |
| CODEREVIEW-019 | tech-lead | 6 |
| TESTCASE-019 | qa-engineer | 8 |
| TESTEXEC-019 | qa-engineer | 8 |
| DEVOPS-019 | devops-engineer | 3 |
| **Total** | | **59** |

The story fits within one sprint (3 operations on a single client path with one paged command). No split into additional stories is required.

## Risks

SDK schema drift on the checkpoint `Record` model; search `where` filter complexity (discriminated filter union) validated locally; pagination cursor state across retries; packaged-policy drift; and shared ACL classification changes.
