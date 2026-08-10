# DESIGN-014 - Foundry Orchestration CLI

| Field | Value |
| --- | --- |
| Story | DEV-STORY-014 |
| Status | Completed; ready for implementation |
| Date | 2026-08-09 |
| Scope | `foundry-orchestration` CLI and Claude skill, 20 Orchestration API v2 operations |

## Technical summary

Add an Orchestration namespace CLI exposing exactly 20 public `foundry_sdk.v2.orchestration` operations across Build, Job, Schedule, ScheduleVersion, and ScheduleRun client paths. The CLI uses the SDK's public nested clients and excludes preview and internal parameters.

Every command supports the shared `--timeout`, `--format`, and `--pretty` options. JSON-shaped inputs are parsed and validated locally before the client is created. Optional SDK arguments are omitted when the user does not provide them. The client factory and `invocation_scope` use `include_attribution=False`; this namespace must not add attribution configuration (outside FR-ATTR-4 scope).

## Evidence and governing references

This design follows:

- SRS-001 FR-ACL, FR-ERR, FR-OUT, FR-PAG, FR-TRACE, FR-ASYNC, and the privacy requirements;
- SAD-001 namespace packaging and stateless CLI structure (EPIC-006, DEV-STORY-014 entry);
- DESIGN-005 tracing, retry, and common-component integration contracts;
- DESIGN-011 patterns for an immutable operation catalog, exact nested SDK dispatch, packaged policy, and SDK-native error handling;
- DESIGN-012 patterns for JSON argument validation and output contracts;
- DESIGN-013 patterns for a completed metadata-only policy and nested client dispatch;
- ADR-001 exit codes, ADR-002 timeouts, ADR-004 format selection, ADR-005 logging, ADR-006 configuration search, and ADR-007 read-only precedence;
- the canonical environment-variable reference, which defines operation enablement and read-only overrides (namespace `orchestration`, 20 rows);
- the canonical metadata allow-list, which blocks 8 of the 20 operations in tier 3;
- vendored SDK sources under `foundry_sdk/v2/orchestration/` (`_client.py` and leaf modules for each nested client).

## Operation catalog

CLI names use kebab-case. Catalog keys and ACL paths use snake_case. `OP_SPECS` contains exactly 20 unique entries.

| # | CLI command | SDK dispatch | Required input | Optional input | HTTP and result |
| ---: | --- | --- | --- | --- | --- |
| 1 | `build cancel` | `client.orchestration.Build.cancel` | `build_rid` | — | `POST /v2/orchestration/builds/{buildRid}/cancel`; None |
| 2 | `build create` | `client.orchestration.Build.create` | `--target-json`, `--fallback-branches-json` | `--force-build`, `--retry-count`, `--retry-backoff-duration`, `--abort-on-failure`, `--notifications-enabled`, `--branch-name` | `POST /v2/orchestration/builds/create`; `Build` |
| 3 | `build get` | `client.orchestration.Build.get` | `build_rid` | — | `GET /v2/orchestration/builds/{buildRid}`; `Build` |
| 4 | `build get-batch` | `client.orchestration.Build.get_batch` | `--build-rids-json` | — | `POST /v2/orchestration/builds/getBatch`; `GetBuildsBatchResponse` |
| 5 | `build jobs` | `client.orchestration.Build.jobs` | `build_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages` | `GET /v2/orchestration/builds/{buildRid}/jobs`; `ResourceIterator[Job]` |
| 6 | `build search` | `client.orchestration.Build.search` | — | `--where-json`, `--order-by-json`, `--page-size`, `--page-token`, `--all`, `--max-pages` | `POST /v2/orchestration/builds/search`; `SearchBuildsResponse` |
| 7 | `job get` | `client.orchestration.Job.get` | `job_rid` | — | `GET /v2/orchestration/jobs/{jobRid}`; `Job` |
| 8 | `job get-batch` | `client.orchestration.Job.get_batch` | `--job-rids-json` | — | `POST /v2/orchestration/jobs/getBatch`; `GetJobsBatchResponse` |
| 9 | `schedule create` | `client.orchestration.Schedule.create` | `--action-json`, `--trigger-json`, `--scope-mode-json` | `--display-name`, `--description` | `POST /v2/orchestration/schedules`; `Schedule` |
| 10 | `schedule delete` | `client.orchestration.Schedule.delete` | `schedule_rid` | — | `DELETE /v2/orchestration/schedules/{scheduleRid}`; None |
| 11 | `schedule get` | `client.orchestration.Schedule.get` | `schedule_rid` | — | `GET /v2/orchestration/schedules/{scheduleRid}`; `Schedule` |
| 12 | `schedule get-affected-resources` | `client.orchestration.Schedule.get_affected_resources` | `schedule_rid` | — | `POST /v2/orchestration/schedules/{scheduleRid}/getAffectedResources`; `AffectedResourcesResponse` |
| 13 | `schedule get-batch` | `client.orchestration.Schedule.get_batch` | `--schedule-rids-json` | — | `POST /v2/orchestration/schedules/getBatch`; `GetSchedulesBatchResponse` |
| 14 | `schedule pause` | `client.orchestration.Schedule.pause` | `schedule_rid` | — | `POST /v2/orchestration/schedules/{scheduleRid}/pause`; `Schedule` |
| 15 | `schedule replace` | `client.orchestration.Schedule.replace` | `schedule_rid`, `--action-json`, `--trigger-json`, `--scope-mode-json` | `--display-name`, `--description` | `PUT /v2/orchestration/schedules/{scheduleRid}`; `Schedule` |
| 16 | `schedule run` | `client.orchestration.Schedule.run` | `schedule_rid` | — | `POST /v2/orchestration/schedules/{scheduleRid}/run`; `ScheduleRun` |
| 17 | `schedule runs` | `client.orchestration.Schedule.runs` | `schedule_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages` | `GET /v2/orchestration/schedules/{scheduleRid}/runs`; `ResourceIterator[ScheduleRun]` |
| 18 | `schedule unpause` | `client.orchestration.Schedule.unpause` | `schedule_rid` | — | `POST /v2/orchestration/schedules/{scheduleRid}/unpause`; `Schedule` |
| 19 | `schedule-version get` | `client.orchestration.ScheduleVersion.get` | `schedule_version_rid` | — | `GET /v2/orchestration/scheduleVersions/{scheduleVersionRid}`; `ScheduleVersion` |
| 20 | `schedule-version schedule` | `client.orchestration.ScheduleVersion.schedule` | `schedule_version_rid` | — | `GET /v2/orchestration/scheduleVersions/{scheduleVersionRid}/schedule`; optional `Schedule` |

The ScheduleRun sub-client exists in the SDK but exposes no public methods; it must not appear in `OP_SPECS`.

### Paging contract

The three cursor-paged commands are `build jobs`, `build search`, and `schedule runs`. They use `PaginationHelper`, accept the SDK page size and page token, fetch at most 40 actual pages in batch mode, and retain retry state only for the current page.

The batch `get_batch` commands and `SearchBuildsResponse` are single-call responses and must never route through `PaginationHelper`. No other operation exposes a cursor or pagination flags.

### Binary downloads

No operation in the Orchestration namespace returns streamed bytes. `BinaryDownloadHandler` is not required.

## Access and runtime policy

The write set is `build.cancel`, `build.create`, `schedule.create`, `schedule.delete`, `schedule.pause`, `schedule.replace`, `schedule.run`, and `schedule.unpause` (8 operations). The shared `AccessControlGuard` write classification must classify these as writes. `schedule.get_affected_resources` and `build.search` are semantic reads despite using POST. Read-only mode blocks the complete write set unless a canonical override permits it.

Metadata-only policy is fail closed. It permits exactly 12 operations (build get/get_batch/jobs/search; job get/get_batch; schedule get/get_affected_resources/get_batch/runs; schedule_version get/schedule) and blocks the remaining 8 (all mutations). Namespace and exact-operation controls are evaluated before the client is constructed.

Use SDK-native B3 tracing through `invocation_scope` and restore context after success and failure. Retry only the ADR-approved transient conditions, preserve local cursor state, and disclose at-least-once behavior because retrying create, replace, run, cancel, pause, unpause, or delete can duplicate work or cost.

## Component breakdown

- `src/foundry_cli/orchestration/` — command catalog, parser, dispatch, JSON validators, paging integration, packaged metadata-only policy.
- Claude skill and launcher for `foundry-orchestration`.
- Focused unit and integration test modules.
- `pyproject.toml` console entry point, package data, and quality-tool scope.

## Estimates and sprint fit

| Sub-task | Assignee | Estimated hours |
| --- | --- | --- |
| DESIGN-014 | tech-lead | 6 |
| DEV-014 | python-developer | 16 |
| UNITTEST-014 | python-developer | 12 |
| CODEREVIEW-014 | tech-lead | 6 |
| TESTCASE-014 | qa-engineer | 8 |
| TESTEXEC-014 | qa-engineer | 8 |
| DEVOPS-014 | devops-engineer | 3 |
| **Total** | | **59** |

The story fits within one sprint (the 23-operation models story was also 59h; this 20-operation story scales the same). No split into additional stories is required.

## Risks

Duplicate billable or mutating effects under at-least-once retries (schedule create/replace/run, build create/cancel); schedule trigger and action schemas drift in the SDK; absence of a cursor on batch responses; packaged-policy drift; and shared ACL classification changes.
