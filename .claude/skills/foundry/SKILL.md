---
name: foundry
description: Cross-cutting Palantir Foundry knowledge shared by all foundry-* CLI skills: platform concepts, the 20-namespace operation catalogue, UserTokenAuth + .env setup, the 8-step access control model, TOON vs JSON output rules, exit-code troubleshooting, and known limitations.
---

# Foundry Platform Knowledge

This skill holds the general knowledge that the `foundry-*` namespace skills share. It explains what the Foundry platform is, what the CLI exposes, how authentication and access control work, and how to interpret output and failures. For a specific namespace, read its own skill file first; this file fills in the context those files assume.

## 1. Foundry platform concepts

Palantir Foundry is a data platform that combines data management, ontology modeling, and application building. The CLI covers the API v2 surface across these concepts:

| Concept | What it is | Namespace skill(s) |
| --- | --- | --- |
| Projects and folders | Container hierarchy for organizing Foundry resources | `foundry-filesystem` |
| Datasets | Tabular data stored in branches; each branch holds transactions that build on each other | `foundry-datasets` |
| Branches and transactions | A branch is a named line of dataset history; transactions group changes (create/commit/abort) | `foundry-datasets` |
| Schemas | Column definitions applied to a dataset | `foundry-datasets` |
| Files | Named binary blobs inside a dataset | `foundry-datasets` |
| Views | Derived datasets backed by other datasets | `foundry-datasets` |
| Ontologies | Semantic layer over datasets: object types, object sets, links, action types, query types | `foundry-ontologies` |
| Object types and object sets | Object types map dataset rows to typed objects; object sets are collections of objects | `foundry-ontologies` |
| Links | Typed relationships between objects | `foundry-ontologies` |
| Functions | Server-side queries (with value types and versioning) callable from the CLI | `foundry-functions` |
| AIP agents and sessions | Agents with conversational sessions, content, and traces | `foundry-aip-agents` |
| Media sets | Stores for unstructured binary media with a transaction lifecycle | `foundry-media-sets` |
| Streams | Time-ordered record streams with subscribers and committed offsets (ADR-003 batch strategy) | `foundry-streams` |
| Models | ML models, live deployments, experiments, and Model Studio artifacts | `foundry-models` |
| Platform administration | Enrollment, groups, markings, organizations, roles, users | `foundry-admin` |
| Audit logs | Log files and bounded content downloads | `foundry-audit` |
| Checkpoints | Named records for external system state | `foundry-checkpoints` |
| Data health | Checks and check reports on data quality | `foundry-data-health` |
| Connectivity | Connections, file/table imports, virtual tables, JDBC drivers | `foundry-connectivity` |
| SQL queries | Ad-hoc SQL with Arrow result downloads | `foundry-sql-queries` |
| Language models | Anthropic messages and OpenAI embeddings inference | `foundry-language-models` |
| Third-party applications | Websites, deployments, and versioned uploads | `foundry-third-party-applications` |
| Widgets | Dev mode settings, widget-set repositories and releases | `foundry-widgets` |

## 2. Namespace overview

The SDK v2 catalogue has 20 namespaces. 18 have CLI skills; `geo` and `core` expose no public CLI-callable operations (SAD-001 AA-3). Counts below are the implemented `OP_SPECS` surfaces verified against the source; the canonical references (ENV-REF-001, META-ALLOW-001, SAD-001, SRS-001) enumerate 355 SDK operations in total.

| Namespace | CLI skill | Operations |
| --- | --- | --- |
| admin | foundry-admin | 66 |
| aip_agents | foundry-aip-agents | 15 |
| audit | foundry-audit | 2 |
| checkpoints | foundry-checkpoints | 3 |
| connectivity | foundry-connectivity | 20 |
| data_health | foundry-data-health | 6 |
| datasets | foundry-datasets | 33 |
| filesystem | foundry-filesystem | 31 |
| functions | foundry-functions | 7 |
| language_models | foundry-language-models | 2 |
| media_sets | foundry-media-sets | 19 |
| models | foundry-models | 23 |
| ontologies | foundry-ontologies | 67 |
| orchestration | foundry-orchestration | 20 |
| sql_queries | foundry-sql-queries | 5 |
| streams | foundry-streams | 15 |
| third_party_applications | foundry-third-party-applications | 9 |
| widgets | foundry-widgets | 8 |
| geo | — | 0 |
| core | — | 0 |

The implemented total is **351** operations (18 namespaces, widgets at the runtime 8-op surface). The **355** documented in ENV-REF-001, META-ALLOW-001, and SAD-001 includes 4 widgets operations from the 12-op design baseline that the installed SDK 1.102.0 does not expose (`dev-mode-settings disable/get/pause/set-widget-set`); see Section 8.

## 3. Operation catalogue

Each namespace CLI exposes operations grouped by resource client. CLI command names kebab-case the resource and operation (`foundry-datasets dataset get-schema`); SDK dispatch uses the snake_case names below. The tables list each resource client with its operations; the full argument-level detail lives in the individual `foundry-*` skill files.

**admin (66)** — `authentication_provider` get, list, preregister_group, preregister_user; `cbac_banner` get; `cbac_marking_restrictions` get; `enrollment` get, get_current; `enrollment_role_assignment` add, list, remove; `group` create, delete, get, get_batch, list, list_current, replace, search; `group_member` add, list, remove; `group_membership` list; `group_membership_expiration_policy` get, replace; `group_provider_info` get, replace; `host` list; `marking` create, get, get_batch, list, replace; `marking_category` create, get, list, replace; `marking_member` add, list, remove; `marking_role_assignment` add, list, remove; `organization` create, get, list_available_roles, replace; `organization_guest_member` add, list, remove; `organization_role_assignment` add, list, remove; `role` get, get_batch; `user` delete, get, get_batch, get_current, get_markings, list, profile_picture, revoke_all_tokens, search; `user_provider_info` get, replace.

**aip_agents (15)** — `agent` all_sessions, get; `agent_version` get, list; `content` get; `session` blocking_continue, cancel, create, delete, get, list, rag_context, streaming_continue, update_title; `session_trace` get.

**audit (2)** — `log_file` content, list.

**checkpoints (3)** — `record` get, get_batch, search.

**connectivity (20)** — `connection` create, get, get_configuration, get_configuration_batch, update_export_settings, update_secrets, upload_custom_jdbc_drivers; `file_import` create, delete, execute, get, list, replace; `table_import` create, delete, execute, get, list, replace; `virtual_table` create.

**data_health (6)** — `check` create, delete, get, replace; `check_report` get, get_latest.

**datasets (33)** — `dataset` create, get, get_health_check_reports, get_health_checks, get_schedules, get_schema, get_schema_batch, jobs, put_schema, read_table, transactions; `branch` create, delete, get, list, transactions; `file` content, delete, get, list, upload; `transaction` abort, build, commit, create, get, job; `view` add_backing_datasets, add_primary_key, create, get, remove_backing_datasets, replace_backing_datasets.

**filesystem (31)** — `folder` children, create, get, get_batch, replace; `project` add_organizations, create, create_from_template, get, organizations, remove_organizations, replace; `resource` add_markings, delete, get, get_access_requirements, get_batch, get_by_path, get_by_path_batch, markings, permanently_delete, remove_markings, restore; `resource_role` add, list, remove; `space` create, delete, get, list, replace.

**functions (7)** — `query` execute, get, get_by_rid, get_by_rid_batch, streaming_execute; `value_type` get; `version_id` get.

**language_models (2)** — `anthropic_model` messages; `open_ai_model` embeddings.

**media_sets (19)** — `media_set` abort, calculate, clear, commit, create, get, get_result, get_rid_by_path, get_status, info, metadata, read, read_original, reference, register, retrieve, transform, upload, upload_media.

**models (23)** — `experiment` get, search; `experiment_artifact_table` json, parquet; `experiment_series` json, parquet; `live_deployment` transform_json; `model` create, get, promote_version; `model_studio` create, get, launch; `model_studio_config_version` create, get, latest, list; `model_studio_run` list; `model_studio_trainer` get, list; `model_version` create, get, list.

**ontologies (67)** — `action` apply, apply_batch, apply_with_overrides; `action_type` get, get_by_rid, get_by_rid_batch, list; `action_type_full_metadata` get, list; `attachment` get, read, upload, upload_with_rid; `attachment_property` get_attachment, get_attachment_by_rid, read_attachment, read_attachment_by_rid; `cipher_text_property` decrypt; `geotemporal_series_property` get_geotemporal_series_latest_value, stream_geotemporal_series_historic_values; `linked_object` get_linked_object, list_linked_objects; `media_reference_property` get_media_content, get_media_metadata, upload; `object_type` get, get_by_rid_batch, get_edits_history, get_full_metadata, get_outgoing_link_type, list, list_outgoing_link_types; `ontology` get, get_full_metadata, list, load_metadata; `ontology_interface` aggregate, get, get_outgoing_interface_link_type, list, list_interface_linked_objects, list_objects_for_interface, list_outgoing_interface_link_types, search; `ontology_object` aggregate, count, get, list, search; `ontology_object_set` aggregate, create_temporary, get, load, load_links, load_multiple_object_types, load_objects_or_interfaces; `ontology_transaction` post_edits; `ontology_value_type` get, list; `query` execute; `query_type` get, list; `time_series_property_v2` get_first_point, get_last_point, stream_points; `time_series_value_bank_property` get_latest_value, stream_values.

**orchestration (20)** — `build` cancel, create, get, get_batch, jobs, search; `job` get, get_batch; `schedule` create, delete, get, get_affected_resources, get_batch, pause, replace, run, runs, unpause; `schedule_version` get, schedule.

**sql_queries (5)** — `sql_query` cancel, execute, execute_ontology, get_results, get_status.

**streams (15)** — `dataset` create; `stream` create, get, get_end_offsets, get_records, publish_binary_record, publish_record, publish_records, reset; `subscriber` create, commit_offsets, delete, get_read_position, read_records, reset_offsets.

**third_party_applications (9)** — `third_party_application` get; `version` delete, get, list, upload, upload_snapshot; `website` deploy, get, undeploy.

**widgets (8)** — `dev_mode_settings` enable, set_widget_set_by_id; `release` delete, get, list; `repository` get, publish; `widget_set` get.

**geo / core (0)** — SDK namespaces with no public CLI-callable operations.

## 4. Authentication setup

Every CLI needs two values before it can reach Foundry:

| Variable | Required | Purpose |
| --- | --- | --- |
| `FOUNDRY_TOKEN` | yes | Palantir bearer token. The SDK builds `UserTokenAuth` from this token alone. |
| `FOUNDRY_HOSTNAME` | yes | Foundry instance hostname, e.g. `https://foundry.example.com`. `AsyncClientFactory` consumes it when constructing the client. |

Set them in the shell, or in a `.env` file. The loader follows ADR-006 in this order:

1. **Explicit override** — if `FOUNDRY_AGENTIC_CLI_ENV_FILE` is set, load exactly that file. If it is missing, fail with exit code 9 (ConfigurationError). No fallback.
2. **Git-root `.env`** — walk up from the current directory to the first directory containing `.git`; load `.env` there. If no `.git` is found, load `.env` from the current directory.
3. **Environment variables only** — if no `.env` file exists, proceed with the shell environment. No error.

The home directory is deliberately never searched. `python-dotenv` loads with `override=False`, so variables already set in the shell take precedence over `.env` values.

Setup steps:

1. Copy `.env.example` to `.env` in the repository root.
2. Fill in `FOUNDRY_TOKEN` and `FOUNDRY_HOSTNAME`.
3. Run any read-only command, e.g. `foundry-filesystem project get --project-rid ri.project.main.project.xxx`. A successful JSON/TOON result confirms auth works.
4. Keep `.env` out of version control; the template is committed, the real file is not.

## 5. Access control configuration

Every operation passes through an access control guard before any SDK call. Decisions follow the 8-step precedence model (ADR-007):

| Step | Check | If true |
| --- | --- | --- |
| 1 | Operation `_ENABLED` | `false` → block |
| 2 | Namespace `_ENABLED` | `false` → block |
| 3 | Operation `_READONLY=false` | overrides a parent READONLY=true → permit write |
| 4 | Namespace `_READONLY` | `true` → block writes |
| 5 | Global `FOUNDRY_AGENTIC_CLI_READONLY` | `true` → block writes |
| 6 | Namespace `_METADATA_ONLY` | `true` → metadata-only policy applies |
| 7 | Global `FOUNDRY_AGENTIC_CLI_METADATA_ONLY` | `true` → metadata-only policy applies |
| 8 | Permit | default |

Control variables follow the naming patterns in ENV-REF-001:

| Scope | Pattern | Example |
| --- | --- | --- |
| Global | `FOUNDRY_AGENTIC_CLI_{KEY}` | `FOUNDRY_AGENTIC_CLI_READONLY` |
| Namespace | `FOUNDRY_AGENTIC_CLI_{NS}_{CONTROL}` | `FOUNDRY_AGENTIC_CLI_DATASETS_READONLY` |
| Operation | `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_{CONTROL}` | `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_GET_ENABLED` |

Control suffixes: `_ENABLED` (`true`/`false`), `_READONLY` (override only, `false` grants write), `_METADATA_ONLY` (`true`/`false`). Operation-level `_READONLY=true` is not supported as an independent setting (ADR-007); to block a single write operation, set its `_ENABLED=false`.

**Metadata-only mode.** Tier-3 policy is default-deny (META-ALLOW-001): only 162 of the 355 operations are permitted, 193 are blocked. The packaged per-namespace policy lives in `metadata-allow-list.md` inside each namespace source directory. A blocked operation exits with exit code 8 (`AccessControlError`) before any network call. The access control model follows SRS-001 Section 4 (FR-ACL) and ADR-007.

## 6. Output format: TOON vs JSON

`--format` accepts `json`, `toon`, or `auto`; `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT` (default `auto`) sets the same choice. Under `auto`, the rule from ADR-004 is:

- **TOON** — only when the top-level result is a list **and** every item is a dict with the identical field set.
- **JSON** — everything else: errors, single objects, empty lists, mixed-type arrays, heterogeneous-field arrays, binary download envelopes, and pagination metadata.

Data goes to stdout. Metadata (pagination, retry info) goes to stderr, preceded by the separator line `# ---metadata-start---`. TOON rendering uses `toon-python`; data is on stdout, metadata on stderr.

## 7. Troubleshooting

### Exit codes (ADR-001)

| Code | Meaning | Typical recovery |
| --- | --- | --- |
| 0 | Success | — |
| 1 | User input error (bad args, validation) | Fix the command line |
| 2 | Authentication error (missing/invalid token or hostname) | Check `FOUNDRY_TOKEN`/`FOUNDRY_HOSTNAME` |
| 3 | Permission denied (API 403) | Request access in Foundry |
| 4 | Not found (API 404) | Check RIDs/paths |
| 5 | Timeout (`asyncio.wait_for` exceeded) | Raise `FOUNDRY_AGENTIC_CLI_TIMEOUT_S` |
| 6 | Server error (API 5xx, excluding retried 503) | Retry later |
| 7 | Rate limit exhausted (HTTP 429 after retries) | Back off, reduce concurrency |
| 8 | Access control block (readonly/metadata-only/disabled) | Adjust ACL env vars |
| 9 | Configuration error (missing env var, bad `.env` path) | Fix configuration |

All failures also emit a JSON error object on stdout.

### Retries and timeouts (ADR-002)

Exponential backoff with jitter, max 4 total attempts (1 + 3 retries), per-call timeout 30 s by default (`FOUNDRY_AGENTIC_CLI_TIMEOUT_S`, range 1–3600). Streams namespace uses `FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S` (default 120 s) for long-lived record connections.

### Logs (ADR-005)

NDJSON structured logs go to stderr. Required fields: `ts`, `level`, `logger`, `msg`; context fields (`op`, `call_id`, `attempt`, `delay_ms`, `access_decision`, `http_status`) appear when relevant. `FOUNDRY_AGENTIC_CLI_LOG_LEVEL` (default `WARNING`) controls verbosity.

### Common failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| Exit 9 at startup | `FOUNDRY_TOKEN` or `FOUNDRY_HOSTNAME` missing (ConfigurationError raised before client construction); or `FOUNDRY_AGENTIC_CLI_ENV_FILE` points to a missing file | Set both variables; fix the env-file path |
| Exit 2 on a call | Token rejected by Foundry (SDK auth failure at request time) | Replace `FOUNDRY_TOKEN` with a valid token |
| Exit 8 on a write in read-only mode | `READONLY=true` active | Set operation/namespace `_READONLY=false`, or remove the global flag |
| Exit 8 in metadata-only mode | Operation blocked by allow-list | Disable metadata-only, or use a permitted operation |
| Binary download fails | Over 1.5 MiB bound (`FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES`) | Stream the content outside the CLI |
| Binary upload fails | Over 16 MiB bound | Split or transfer large media outside the CLI |
| Exit 7 under load | HTTP 429 after retries | Back off and retry later |
| Exit 1 on a `-json` flag | Invalid JSON argument | Validate the JSON locally and re-run |

## 8. Known limitations and open items

- **`geo` and `core` have no operations.** They exist in the SDK v2 catalogue but expose only error and model types (SAD-001 AA-3). No skill folders exist for them.
- **Widgets SDK drift.** DESIGN-022 documents 12 widgets operations from the vendored SDK snapshot; installed `foundry-platform-sdk` 1.102.0 exposes 8 (QUESTION-043). The runtime surface is authoritative and the CLI implements 8. `DevModeSettingsV2` is out of scope.
- **Snapshot vs installed SDK.** The vendored SDK copy under `.ept/docs/customer_input/` is version `0.0.0` (git-derived); the installed runtime is `foundry-platform-sdk 1.102.0`. Operation counts must be re-verified on every SDK minor release (ENV-REF-001 review cycle).
- **Binary size bounds.** Downloads are bounded at 1.5 MiB and uploads at 16 MiB per operation. Large media must be handled outside the CLI.
- **Preview parameters excluded.** Preview-mode SDK parameters are not part of the CLI surface.
- **Attribution scope.** `FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION` / `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS` apply only to namespaces within FR-ATTR-4 scope (media_sets currently); other namespaces set `include_attribution=False`.
