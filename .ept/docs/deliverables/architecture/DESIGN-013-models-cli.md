# DESIGN-013 - Foundry Models CLI

| Field | Value |
| --- | --- |
| Story | DEV-STORY-013 |
| Status | Completed; ready for implementation |
| Date | 2026-08-09 |
| Scope | `foundry-models` CLI and Claude skill, 23 Models API v2 operations |

## Technical summary

Add a Models namespace CLI exposing exactly 23 public `foundry_sdk.v2.models` operations across live deployments, models, versions, experiments, experiment content, Model Studio, config versions, runs, and trainers. The CLI uses the SDK's public nested clients and excludes preview and internal parameters.

Every command supports the shared `--timeout`, `--format`, and `--pretty` options. JSON-shaped inputs are parsed and validated locally before the client is created. Optional SDK arguments are omitted when the user does not provide them. The client factory and `invocation_scope` use `include_attribution=False`; this namespace must not add attribution configuration.

## Evidence and governing references

This design follows:

- SRS-001 FR-ACL, FR-ERR, FR-OUT, FR-PAG, FR-TRACE, FR-ASYNC, and the privacy requirements;
- SAD-001 namespace packaging and stateless CLI structure;
- DESIGN-005 tracing, retry, binary-download, and common-component integration contracts;
- DESIGN-010 patterns for exact-page pagination and bounded streamed downloads;
- DESIGN-011 patterns for an immutable operation catalog, exact nested SDK dispatch, packaged policy, and SDK-native error handling;
- DESIGN-012 patterns for JSON argument validation and output contracts;
- ADR-001 exit codes, ADR-002 timeouts, ADR-004 format selection, ADR-005 logging, ADR-006 configuration search, and ADR-007 read-only precedence;
- the canonical environment-variable reference, which defines operation enablement and read-only overrides;
- the canonical metadata allow-list, which blocks 11 of the 23 operations in tier 3;
- vendored SDK sources under `foundry_sdk/v2/models/` (`_client.py` and leaf modules for each nested client).

## Operation catalog

CLI names use kebab-case. Catalog keys and ACL paths use snake_case. `OP_SPECS` contains exactly 23 unique entries.

| # | CLI command | SDK dispatch | Required input | Optional input | HTTP and result |
| ---: | --- | --- | --- | --- | --- |
| 1 | `live-deployment transform-json` | `client.models.LiveDeployment.transform_json` | `live_deployment_rid`, `--input-json` | — | `POST /v2/models/liveDeployments/{liveDeploymentRid}/transformJson`; `TransformLiveDeploymentResponse` |
| 2 | `model create` | `client.models.Model.create` | `--name`, `--parent-folder-rid` | — | `POST /v2/models`; `Model` |
| 3 | `model get` | `client.models.Model.get` | `model_rid` | — | `GET /v2/models/{modelRid}`; `Model` |
| 4 | `model promote-version` | `client.models.Model.promote_version` | `model_rid`, `--source-model-version-rid` | — | `POST /v2/models/{modelRid}/promoteVersion`; `ModelVersion` |
| 5 | `model-version create` | `client.models.Model.Version.create` | `model_rid`, `--backing-repositories-json`, `--conda-requirements-json`, `--model-api-json`, `--model-files-json` | — | `POST /v2/models/{modelRid}/versions`; `ModelVersion` |
| 6 | `model-version get` | `client.models.Model.Version.get` | `model_rid`, `model_version_rid` | — | `GET /v2/models/{modelRid}/versions/{modelVersionRid}`; `ModelVersion` |
| 7 | `model-version list` | `client.models.Model.Version.list` | `model_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages` | `GET /v2/models/{modelRid}/versions`; `ResourceIterator[ModelVersion]` |
| 8 | `experiment get` | `client.models.Model.Experiment.get` | `model_rid`, `experiment_rid` | — | `GET /v2/models/{modelRid}/experiments/{experimentRid}`; `Experiment` |
| 9 | `experiment search` | `client.models.Model.Experiment.search` | `model_rid` | `--order-by-json`, `--where-json`, `--page-size`, `--page-token`, `--all`, `--max-pages` | `POST /v2/models/{modelRid}/experiments/search`; `SearchExperimentsResponse` |
| 10 | `experiment-series json` | `client.models.Model.Experiment.Series.json` | `model_rid`, `experiment_rid`, `experiment_series_name` | `--offset`, `--page-size` | `GET /v2/models/{modelRid}/experiments/{experimentRid}/series/{experimentSeriesName}/json`; `Series` |
| 11 | `experiment-series parquet` | `client.models.Model.Experiment.Series.parquet` | `model_rid`, `experiment_rid`, `experiment_series_name`, `--output` | — | `GET /v2/models/{modelRid}/experiments/{experimentRid}/series/{experimentSeriesName}/parquet`; streamed `TableResponse` |
| 12 | `experiment-artifact-table json` | `client.models.Model.Experiment.ArtifactTable.with_streaming_response.json` | `model_rid`, `experiment_rid`, `experiment_artifact_table_name`, `--output` | `--offset`, `--page-size` | `GET /v2/models/{modelRid}/experiments/{experimentRid}/artifactTables/{experimentArtifactTableName}/json`; streamed bytes |
| 13 | `experiment-artifact-table parquet` | `client.models.Model.Experiment.ArtifactTable.with_streaming_response.parquet` | `model_rid`, `experiment_rid`, `experiment_artifact_table_name`, `--output` | — | `GET /v2/models/{modelRid}/experiments/{experimentRid}/artifactTables/{experimentArtifactTableName}/parquet`; streamed `TableResponse` |
| 14 | `model-studio create` | `client.models.ModelStudio.create` | `--name`, `--parent-folder-rid` | — | `POST /v2/models/modelStudios`; `ModelStudio` |
| 15 | `model-studio get` | `client.models.ModelStudio.get` | `model_studio_rid` | — | `GET /v2/models/modelStudios/{modelStudioRid}`; `ModelStudio` |
| 16 | `model-studio launch` | `client.models.ModelStudio.launch` | `model_studio_rid` | — | `POST /v2/models/modelStudios/{modelStudioRid}/launch`; `ModelStudioRun` |
| 17 | `model-studio-config-version create` | `client.models.ModelStudio.ConfigVersion.create` | `model_studio_rid`, `--name`, `--resources-json`, `--trainer-id`, `--worker-config-json` | `--changelog` | `POST /v2/models/modelStudios/{modelStudioRid}/configVersions`; `ModelStudioConfigVersion` |
| 18 | `model-studio-config-version get` | `client.models.ModelStudio.ConfigVersion.get` | `model_studio_rid`, `model_studio_config_version_version` | — | `GET /v2/models/modelStudios/{modelStudioRid}/configVersions/{modelStudioConfigVersionVersion}`; `ModelStudioConfigVersion` |
| 19 | `model-studio-config-version latest` | `client.models.ModelStudio.ConfigVersion.latest` | `model_studio_rid` | — | `GET /v2/models/modelStudios/{modelStudioRid}/configVersions/latest`; optional `ModelStudioConfigVersion` |
| 20 | `model-studio-config-version list` | `client.models.ModelStudio.ConfigVersion.list` | `model_studio_rid` | `--page-size`, `--page-token`, `--all`, `--max-pages` | `GET /v2/models/modelStudios/{modelStudioRid}/configVersions`; `ResourceIterator[ModelStudioConfigVersion]` |
| 21 | `model-studio-run list` | `client.models.ModelStudio.Run.list` | `model_studio_rid` | `--config-version`, `--page-size`, `--page-token`, `--all`, `--max-pages` | `GET /v2/models/modelStudios/{modelStudioRid}/runs`; `ResourceIterator[ModelStudioRun]` |
| 22 | `model-studio-trainer get` | `client.models.ModelStudio.Trainer.get` | `model_studio_trainer_trainer_id` | `--version` | `GET /v2/models/modelStudioTrainers/{modelStudioTrainerTrainerId}`; `ModelStudioTrainer` |
| 23 | `model-studio-trainer list` | `client.models.ModelStudio.Trainer.list` | — | — | `GET /v2/models/modelStudioTrainers`; `ListModelStudioTrainersResponse` |

### Paging contract

The four cursor-paged commands are `experiment search`, `model-version list`, `model-studio-config-version list`, and `model-studio-run list`. They use `PaginationHelper`, accept the SDK page size and page token, fetch at most 40 actual pages in batch mode, and retain retry state only for the current page.

`offset` and `page_size` on series JSON and artifact-table JSON are service-side slicing controls and must never route through `PaginationHelper`. Trainer list has no SDK cursor and must not expose invented pagination flags.

### Streamed downloads

The three file-producing commands are series parquet and artifact-table JSON and parquet. They acquire a streaming SDK response (`with_streaming_response`), pass it to `BinaryDownloadHandler` before opening the destination, write atomically, emit the standard metadata envelope, and close the response on success or failure. Access control runs before any client construction or filesystem effect.

## Access and runtime policy

The write set is `transform_json`, every `create`, `promote_version`, and Model Studio `launch`. The shared `AccessControlGuard` write classification must be corrected so `launch` and `promote_version` cannot inherit read behavior. `experiment search` is a semantic read despite using POST. Read-only mode blocks the complete write set unless a canonical override permits it.

Metadata-only policy is fail closed. It permits exactly 12 operations (experiment get/search; model get; Model Studio config-version get/latest/list; Model Studio run list; Model Studio trainer get/list; model-version get/list) and blocks the remaining 11, including all file downloads and inference or mutation commands. Namespace and exact-operation controls are evaluated before the client and before any output file is touched.

Use SDK-native B3 tracing through `invocation_scope` and restore context after success and failure. Retry only the ADR-approved transient conditions, preserve local cursor state, and disclose at-least-once behavior because retrying create, launch, promotion, or inference can duplicate work or cost.

## Component breakdown

- `src/foundry_cli/models/` — command catalog, parser, dispatch, JSON validators, paging and download integration, packaged metadata-only policy.
- Claude skill and launcher for `foundry-models`.
- Focused unit and integration test modules.
- `pyproject.toml` console entry point, package data, and quality-tool scope.

## Estimates and sprint fit

| Sub-task | Assignee | Estimated hours |
| --- | --- | --- |
| DESIGN-013 | tech-lead | 6 |
| DEV-013 | python-developer | 16 |
| UNITTEST-013 | python-developer | 12 |
| CODEREVIEW-013 | tech-lead | 6 |
| TESTCASE-013 | qa-engineer | 8 |
| TESTEXEC-013 | qa-engineer | 8 |
| DEVOPS-013 | devops-engineer | 3 |
| **Total** | | **59** |

The story fits within one sprint (previous 7-operation story was 33h; this 23-operation story scales proportionally with the catalog). No split into additional stories is required.

## Risks

Duplicate billable or mutating effects under at-least-once retries; large content downloads; SDK schema drift; the absence of trainer cursors; packaged-policy drift; and shared ACL classification changes.
