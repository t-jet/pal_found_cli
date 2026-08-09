---
id: DEV-STORY-013
type: dev_story
title: foundry-models skill (23 operations)
status: Analysis
feature_request: FEATURE-001
epic: EPIC-005
created: 2026-04-13
updated: 2026-08-09
priority: High
assignee: architect
reporter: architect
release_notes: Adds the foundry-models CLI and Claude skill with 23 Foundry SDK v2 operations for models, versions, experiments, live inference, Model Studio, runs, and trainers. Includes exact nested dispatch, four cursor-paged reads, bounded streamed persistence for three experiment-content downloads, 12-permitted/11-blocked metadata-only policy, write controls for launch and promotion, B3 tracing, safe retries, structured output, and privacy-safe errors and logs.
---

# DEV-STORY-013: foundry-models skill (23 operations)

## Description

Implement the complete supported public `foundry_sdk.v2.models` CLI surface as `foundry-models` and a matching Claude skill. The contract contains exactly 23 commands across live deployments, models, versions, experiments, experiment content, Model Studio, config versions, runs, and trainers. It uses the SDK's public nested clients and excludes preview and internal parameters.

Every command supports the shared `--timeout`, `--format`, and `--pretty` options. JSON-shaped inputs are parsed and validated before the client is created. Optional SDK arguments are omitted when the user does not provide them. The client factory and `invocation_scope` use `include_attribution=False`; this namespace must not add attribution configuration.

### Authoritative command catalog

| # | CLI command | SDK dispatch | Inputs | HTTP and result |
|---:|---|---|---|---|
| 1 | `live-deployment transform-json` | `client.models.LiveDeployment.transform_json` | Required `live_deployment_rid`, `--input-json` object | `POST /v2/models/liveDeployments/{liveDeploymentRid}/transformJson`; `TransformLiveDeploymentResponse` |
| 2 | `model create` | `client.models.Model.create` | Required `--name`, `--parent-folder-rid` | `POST /v2/models`; `Model` |
| 3 | `model get` | `client.models.Model.get` | Required `model_rid` | `GET /v2/models/{modelRid}`; `Model` |
| 4 | `model promote-version` | `client.models.Model.promote_version` | Required `model_rid`, `--source-model-version-rid` | `POST /v2/models/{modelRid}/promoteVersion`; `ModelVersion` |
| 5 | `model-version create` | `client.models.Model.Version.create` | Required `model_rid`, `--backing-repositories-json` string array, `--conda-requirements-json` string array, `--model-api-json` object, `--model-files-json` object | `POST /v2/models/{modelRid}/versions`; `ModelVersion` |
| 6 | `model-version get` | `client.models.Model.Version.get` | Required `model_rid`, `model_version_rid` | `GET /v2/models/{modelRid}/versions/{modelVersionRid}`; `ModelVersion` |
| 7 | `model-version list` | `client.models.Model.Version.list` | Required `model_rid`; optional `--page-size`, `--page-token`, `--all`, `--max-pages` | `GET /v2/models/{modelRid}/versions`; `ResourceIterator[ModelVersion]` |
| 8 | `experiment get` | `client.models.Model.Experiment.get` | Required `model_rid`, `experiment_rid` | `GET /v2/models/{modelRid}/experiments/{experimentRid}`; `Experiment` |
| 9 | `experiment search` | `client.models.Model.Experiment.search` | Required `model_rid`; optional `--order-by-json` object, `--where-json` object, `--page-size`, `--page-token`, `--all`, `--max-pages` | `POST /v2/models/{modelRid}/experiments/search`; `SearchExperimentsResponse` |
| 10 | `experiment-series json` | `client.models.Model.Experiment.Series.json` | Required `model_rid`, `experiment_rid`, `experiment_series_name`; optional `--offset`, `--page-size` | `GET /v2/models/{modelRid}/experiments/{experimentRid}/series/{experimentSeriesName}/json`; `Series` |
| 11 | `experiment-series parquet` | `client.models.Model.Experiment.Series.parquet` | Required `model_rid`, `experiment_rid`, `experiment_series_name`, `--output` | `GET /v2/models/{modelRid}/experiments/{experimentRid}/series/{experimentSeriesName}/parquet`; streamed `TableResponse` |
| 12 | `experiment-artifact-table json` | `client.models.Model.Experiment.ArtifactTable.with_streaming_response.json` | Required `model_rid`, `experiment_rid`, `experiment_artifact_table_name`, `--output`; optional `--offset`, `--page-size` | `GET /v2/models/{modelRid}/experiments/{experimentRid}/artifactTables/{experimentArtifactTableName}/json`; streamed bytes |
| 13 | `experiment-artifact-table parquet` | `client.models.Model.Experiment.ArtifactTable.with_streaming_response.parquet` | Required `model_rid`, `experiment_rid`, `experiment_artifact_table_name`, `--output` | `GET /v2/models/{modelRid}/experiments/{experimentRid}/artifactTables/{experimentArtifactTableName}/parquet`; streamed `TableResponse` |
| 14 | `model-studio create` | `client.models.ModelStudio.create` | Required `--name`, `--parent-folder-rid` | `POST /v2/models/modelStudios`; `ModelStudio` |
| 15 | `model-studio get` | `client.models.ModelStudio.get` | Required `model_studio_rid` | `GET /v2/models/modelStudios/{modelStudioRid}`; `ModelStudio` |
| 16 | `model-studio launch` | `client.models.ModelStudio.launch` | Required `model_studio_rid` | `POST /v2/models/modelStudios/{modelStudioRid}/launch`; `ModelStudioRun` |
| 17 | `model-studio-config-version create` | `client.models.ModelStudio.ConfigVersion.create` | Required `model_studio_rid`, `--name`, `--resources-json` object, `--trainer-id`, `--worker-config-json` object; optional `--changelog` | `POST /v2/models/modelStudios/{modelStudioRid}/configVersions`; `ModelStudioConfigVersion` |
| 18 | `model-studio-config-version get` | `client.models.ModelStudio.ConfigVersion.get` | Required `model_studio_rid`, `model_studio_config_version_version` | `GET /v2/models/modelStudios/{modelStudioRid}/configVersions/{modelStudioConfigVersionVersion}`; `ModelStudioConfigVersion` |
| 19 | `model-studio-config-version latest` | `client.models.ModelStudio.ConfigVersion.latest` | Required `model_studio_rid` | `GET /v2/models/modelStudios/{modelStudioRid}/configVersions/latest`; optional `ModelStudioConfigVersion` |
| 20 | `model-studio-config-version list` | `client.models.ModelStudio.ConfigVersion.list` | Required `model_studio_rid`; optional `--page-size`, `--page-token`, `--all`, `--max-pages` | `GET /v2/models/modelStudios/{modelStudioRid}/configVersions`; `ResourceIterator[ModelStudioConfigVersion]` |
| 21 | `model-studio-run list` | `client.models.ModelStudio.Run.list` | Required `model_studio_rid`; optional `--config-version`, `--page-size`, `--page-token`, `--all`, `--max-pages` | `GET /v2/models/modelStudios/{modelStudioRid}/runs`; `ResourceIterator[ModelStudioRun]` |
| 22 | `model-studio-trainer get` | `client.models.ModelStudio.Trainer.get` | Required `model_studio_trainer_trainer_id`; optional `--version` | `GET /v2/models/modelStudioTrainers/{modelStudioTrainerTrainerId}`; `ModelStudioTrainer` |
| 23 | `model-studio-trainer list` | `client.models.ModelStudio.Trainer.list` | No operation-specific inputs | `GET /v2/models/modelStudioTrainers`; `ListModelStudioTrainersResponse` |

The four cursor-paged commands are `experiment search`, `model-version list`, `model-studio-config-version list`, and `model-studio-run list`. They use `PaginationHelper`, accept the SDK page size and page token, fetch at most 40 actual pages in batch mode, and retain retry state only for the current page. The `offset` and `page_size` parameters on series JSON and artifact-table JSON are service-side slicing controls, not client pagination. Trainer list has no SDK cursor and must not expose invented pagination.

The three file-producing commands are series parquet and artifact-table JSON and parquet. They acquire a streaming SDK response, pass it to `BinaryDownloadHandler` before opening the destination, write atomically, emit the standard metadata envelope, and close the response on success or failure. Access control runs before any client construction or filesystem effect.

### Access and runtime policy

The write set is `transform_json`, every `create`, `promote_version`, and Model Studio `launch`. Shared `AccessControlGuard` write classification must be corrected so launch and promotion cannot inherit read behavior. Experiment search is a semantic read despite using POST. Read-only mode blocks the complete write set unless a canonical override permits it.

Metadata-only policy is fail closed. It permits exactly 12 operations: experiment get/search; model get; Model Studio config-version get/latest/list; Model Studio run list; Model Studio trainer get/list; and model-version get/list. It blocks the remaining 11 operations, including all file downloads and inference or mutation commands. Namespace and exact-operation controls are evaluated before the client and before any output file is touched.

Use SDK-native B3 tracing through `invocation_scope` and restore context after success and failure. Retry only the ADR-approved transient conditions, preserve local cursor state, and disclose at-least-once behavior because retrying create, launch, promotion, or inference can duplicate work or cost. Structured results and errors follow shared output contracts; logs, errors, and tracebacks must not expose credentials, request bodies, model inputs, experiment content, or downloaded bytes.

### Components and dependencies

- Add `src/foundry_cli/models/` with the command catalog, parser, dispatch, JSON validators, paging and download integration, and packaged metadata-only policy.
- Add the Claude skill and launcher for `foundry-models`.
- Add focused unit and integration test modules and update `pyproject.toml` for the console entry point, package data, and quality-tool scope.
- Reuse `AccessControlGuard`, `PaginationHelper`, `RetryHandler`, `OutputFormatter`, `ErrorHandler`, `LoggingManager`, `FoundryClientFactory`, `invocation_scope`, and `BinaryDownloadHandler`.
- Depend on the approved document index, SRS FR-AUTH/OUT/ASYNC/ERR/TRACE/ACL/SKILL and NFRs, SAD namespace and EPIC-005 cross-cuts, DESIGN-005/010/011/012, canonical environment reference, metadata allow-list, ADR-001/002/004/005/006/007, and the vendored `foundry_sdk/v2/models/` leaf files.

### Boundaries and risks

Scope is Foundry SDK v2 with UserToken authentication. It excludes OAuth, v1 APIs, private SDK members, session state, uploads, custom schemas, attribution, W3C propagation, unsupported pagination, preview flags, raw response flags, and a user-facing stream mode. Risks are duplicate billable or mutating effects under at-least-once retries, large content downloads, SDK schema drift, the absence of trainer cursors, packaged-policy drift, and shared ACL classification changes.

## Acceptance Criteria

1. The CLI, launcher, registry, and Claude skill expose exactly the 23 cataloged commands, use the stated public nested SDK clients and HTTP routes, forward required values, and omit every absent optional SDK argument; no fake discovery, preview, internal, raw, or stream command is present.
2. Every structured flag validates its documented JSON shape before client creation; invalid JSON or a wrong top-level shape exits 1 through the standard error envelope without echoing sensitive content.
3. Exactly four commands use cursor pagination, preserving SDK page size/token semantics, supporting bounded batch traversal through at most 40 actual pages, and keeping retry state local to the page being fetched.
4. Series JSON and artifact-table JSON forward `offset` and `page_size` once as service slicing parameters and never route them through `PaginationHelper`; trainer list exposes no pagination flags.
5. Series parquet plus artifact-table JSON and parquet use streaming SDK access and `BinaryDownloadHandler` before opening a file, with atomic persistence, metadata envelopes, bounded memory behavior, and response closure on every path.
6. `AccessControlGuard` runs before filesystem and client effects; read-only mode blocks transform, every create, promotion, and launch while experiment search remains a semantic read.
7. Shared ACL write verbs include Model Studio launch and model promotion, with regression coverage proving narrower overrides cannot accidentally downgrade their write classification.
8. Metadata-only mode permits exactly the documented 12 reads and blocks the other 11 operations, fails closed for missing or malformed packaged policy, and is covered by exact 12/11 tests.
9. Client creation and invocation scope always use `include_attribution=False`; no attribution environment handling is added, and surrounding attribution state is unchanged after success or failure.
10. SDK-native B3 tracing is applied to every command and the prior tracing context is restored after success and failure.
11. Retries follow ADR-004, preserve cursor-local state, do not retry validation, authorization, or permanent errors, and document at-least-once duplicate and cost risk for inference, creates, promotion, and launch.
12. JSON and binary metadata output follow the shared stdout/stderr/exit-code contracts, including serialization for SDK models, optional latest results, lists, and structured errors.
13. Credentials, JSON request bodies, inference inputs, experiment content, downloaded bytes, and server payloads are absent from logs, errors, and tracebacks, including failure and retry paths.
14. Clean wheel and editable installs expose the console command and Claude launcher from an empty working directory, include the packaged metadata policy, and preserve existing entry points.
15. Tests cover Python 3.11 and 3.12, exact signatures and routes, parsing, dispatch, pagination, streaming, ACL, tracing, retries, output, privacy, imports, and packaging; Ruff, mypy, Bandit, and the repository test suite pass with at least 80% coverage on the new namespace.

## Related Documentation

- `.ept/docs/document_index.md`
- `.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md`
- `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md`
- `.ept/docs/deliverables/architecture/DESIGN-005-common-components.md`
- `.ept/docs/deliverables/architecture/DESIGN-010-foundry-datasets-cli.md`
- `.ept/docs/deliverables/architecture/DESIGN-011-aip-agents-cli.md`
- `.ept/docs/deliverables/architecture/DESIGN-012-language-models-cli.md`
- `.ept/docs/deliverables/architecture/canonical-env-var-reference.md`
- `.ept/docs/deliverables/architecture/metadata-allow-list.md`
- ADR-001, ADR-002, ADR-004, ADR-005, ADR-006, and ADR-007 as indexed in the document index
- `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/models/`

## Technical Artifacts

- `src/foundry_cli/models/` package, CLI, and metadata-only policy
- Claude skill and launcher
- Focused unit and integration tests
- `pyproject.toml` console entry, package data, and quality configuration

## Notes

The customer task, approved requirements and architecture documents, and vendored SDK sources independently confirm the 23-operation count and contract. Primary sources agree, and there are no open questions or missing resources.
