# DESIGN-021 - Foundry Third-Party Applications CLI

| Field | Value |
| --- | --- |
| Story | DEV-STORY-021 |
| Status | Completed; ready for implementation |
| Date | 2026-08-10 |
| Scope | `foundry-third-party-applications` CLI and Claude skill, 9 Third-Party Applications API v2 operations |

## Technical summary

Add a Third-Party Applications namespace CLI exposing exactly 9 public `foundry_sdk.v2.third_party_applications` operations across the `ThirdPartyApplication`, `Website`, and `Version` client paths. The CLI uses the SDK's public nested clients and excludes preview and internal parameters.

Every command supports the shared `--timeout`, `--format`, and `--pretty` options. JSON-shaped inputs are parsed and validated locally before the client is created. Optional SDK arguments are omitted when the user does not provide them. The client factory and `invocation_scope` use `include_attribution=False`; this namespace is outside FR-ATTR-4 scope and must not add attribution configuration.

> **Operation count note:** The story title and SAD-001 reference "9 operations". The vendored SDK (v1.102.0) exposes exactly **9** public operations (`ThirdPartyApplication` 1: get; `Website` 3: deploy, get, undeploy; `Version` 5: delete, get, list, upload, upload_snapshot). The canonical environment-variable reference and the metadata allow-list are concordant at 9 rows each. The count is confirmed accurate; no correction is required.

## Evidence and governing references

This design follows:

- SRS-001 FR-ACL, FR-PAG, FR-TRACE, FR-ASYNC, FR-OUT, FR-ERR, and the privacy requirements;
- SAD-001 namespace packaging and stateless CLI structure (EPIC-007, DEV-STORY-021 entry);
- DESIGN-005 tracing, retry, and common-component integration contracts;
- DESIGN-011 patterns for an immutable operation catalog, exact nested SDK dispatch, packaged policy, and SDK-native error handling;
- DESIGN-012 patterns for JSON argument validation and output contracts;
- DESIGN-013 patterns for cursor pagination via `PaginationHelper`;
- DESIGN-017/018 patterns for bounded binary uploads (bounded file read after the access-control decision, before client construction);
- ADR-001 exit codes, ADR-002 timeouts, ADR-004 format selection, ADR-005 logging, ADR-006 configuration search, and ADR-007 read-only precedence;
- the canonical environment-variable reference, which defines operation enablement and read-only overrides (namespace `third_party_applications`, 9 rows);
- the canonical metadata allow-list, which blocks 5 of the 9 operations in tier 3;
- vendored SDK sources under `foundry_sdk/v2/third_party_applications/` (`_client.py`, `third_party_application.py`, `website.py`, `version.py`).

## Operation catalog

CLI names use kebab-case. Catalog keys and ACL paths use snake_case. `OP_SPECS` contains exactly 9 unique entries.

| # | CLI command | SDK dispatch | Required input | Optional input | HTTP and result |
| ---: | --- | --- | --- | --- | --- |
| 1 | `third-party-application get` | `client.third_party_applications.ThirdPartyApplication.get` | `third_party_application_rid` | — | `GET /v2/thirdPartyApplications/{thirdPartyApplicationRid}`; `ThirdPartyApplication` |
| 2 | `website deploy` | `client.third_party_applications.Website.deploy` | `third_party_application_rid`, `--version` | — | `POST /v2/thirdPartyApplications/{rid}/website/deploy`; `Website` |
| 3 | `website get` | `client.third_party_applications.Website.get` | `third_party_application_rid` | — | `GET /v2/thirdPartyApplications/{rid}/website`; `Website` |
| 4 | `website undeploy` | `client.third_party_applications.Website.undeploy` | `third_party_application_rid` | — | `POST /v2/thirdPartyApplications/{rid}/website/undeploy`; `Website` |
| 5 | `version delete` | `client.third_party_applications.Website.Version.delete` | `third_party_application_rid`, `version_version` | — | `DELETE /v2/thirdPartyApplications/{rid}/website/versions/{version}`; None |
| 6 | `version get` | `client.third_party_applications.Website.Version.get` | `third_party_application_rid`, `version_version` | — | `GET /v2/thirdPartyApplications/{rid}/website/versions/{version}`; `Version` |
| 7 | `version list` | `client.third_party_applications.Website.Version.list` | `third_party_application_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages` | `GET /v2/thirdPartyApplications/{rid}/website/versions`; `ResourceIterator[Version]` |
| 8 | `version upload` | `client.third_party_applications.Website.Version.upload` | `third_party_application_rid`, `--version`, `--file` | — | `POST /v2/thirdPartyApplications/{rid}/website/versions/upload`; `Version` |
| 9 | `version upload-snapshot` | `client.third_party_applications.Website.Version.upload_snapshot` | `third_party_application_rid`, `--version`, `--file` | `--snapshot-identifier` | `POST /v2/thirdPartyApplications/{rid}/website/versions/uploadSnapshot`; `Version` |

The Third-Party Applications namespace routes through `client.third_party_applications.ThirdPartyApplication`, with `website` operations dispatched through the `Website` accessor and `version` operations through the nested `Website.Version` accessor. `preview` parameters are excluded. The `version list` response (`ListVersionsResponse`) carries `data` plus a `nextPageToken` cursor.

### Paging contract

`version list` is the only paged operation; it returns a `ResourceIterator` with a server cursor. It uses `PaginationHelper` and accepts `--page-size`, `--page-token`, `--all`, and `--max-pages`. No other operation exposes pagination flags.

### Binary upload contract

`version upload` and `version upload-snapshot` accept the Website build as a zip file. The SDK signature is `upload(third_party_application_rid, body: bytes, *, version, ...)` with `body` as a positional bytes argument. The CLI reads `--file` with a bounded read (16 MiB) AFTER the access-control decision and BEFORE the client is constructed (precedent: connectivity JDBC-driver upload, media-sets `upload`). The `--file` flag is consumed by the CLI and never forwarded; `--version` is passed as the SDK `version` query parameter. `upload_snapshot` also accepts `--snapshot-identifier` (optional). Snapshot versions are auto-deleted after two days — disclosed in skill documentation.

### Access and runtime policy

The write set is `website.deploy`, `website.undeploy`, `version.delete`, `version.upload`, and `version.upload_snapshot` (5 operations). `version.delete` is a DELETE classified by the shared write-verb set. `deploy`, `undeploy`, `upload`, and `upload_snapshot` are mutating POSTs that require write classification: add the operation-specific verbs to the shared `AccessControlGuard` write set (precedent: `launch`, `promote_version`, `upload`, `calculate` from the models/media-sets batches). `third_party_application.get`, `website.get`, `version.get`, and `version.list` are semantic reads. Read-only mode blocks the complete write set unless a canonical override permits it.

Metadata-only policy is fail closed. It permits exactly 4 operations (`third_party_application.get`, `website.get`, `version.get`, `version.list`) and blocks the remaining 5 (`website.deploy`, `website.undeploy`, `version.delete`, `version.upload`, `version.upload_snapshot`), matching the canonical allow-list. Namespace and exact-operation controls are evaluated before the client is constructed.

Use SDK-native B3 tracing through `invocation_scope` and restore context after success and failure. Retry only the ADR-approved transient conditions and disclose at-least-once behavior: retrying `website.deploy`/`website.undeploy` re-applies the same version (idempotent target state), but retrying `version.upload` can create a duplicate version record, so the duplicate-safety caveat must be documented.

## Component breakdown

- `src/foundry_cli/third_party_applications/` — command catalog, parser, dispatch, bounded file-read for uploads, pagination integration, packaged metadata-only policy.
- Claude skill and launcher for `foundry-third-party-applications`.
- Focused unit and integration test modules.
- `pyproject.toml` console entry point, package data, and quality-tool scope.

## Estimates and sprint fit

| Sub-task | Assignee | Estimated hours |
| --- | --- | --- |
| DESIGN-021 | tech-lead | 6 |
| DEV-021 | python-developer | 16 |
| UNITTEST-021 | python-developer | 12 |
| CODEREVIEW-021 | tech-lead | 6 |
| TESTCASE-021 | qa-engineer | 8 |
| TESTEXEC-021 | qa-engineer | 8 |
| DEVOPS-021 | devops-engineer | 3 |
| **Total** | | **59** |

The story fits within one sprint (9 operations across three client paths, one paged command, two bounded uploads). No split into additional stories is required.

## Risks

SDK schema drift on the `ThirdPartyApplication`/`Website`/`Version` models; duplicate version effects under at-least-once retries for `upload`; undeploy state transitions surfaced as SDK errors; packaged-policy drift; shared ACL write-verb classification changes; and zip file size/format validation for uploads.
