# Metadata Allow-List — Tier-3 (METADATA_ONLY) Access Control

| Field | Value |
|---|---|
| **Document ID** | META-ALLOW-001 |
| **Version** | 1.0.0 |
| **Date** | 2026-04-13 |
| **Author** | Solution Architect |
| **Total operations** | 355 |
| **Tier-3 permitted** | 162 |
| **Tier-3 blocked** | 193 |
| **Unclassified (defaults to blocked)** | 0 |

---

## Overview

This document classifies every SDK v2 operation for Tier-3 (Metadata-Only) access control.

**Policy:** Default-deny. Operations not explicitly listed as `true` are blocked in Tier-3.

**Variable format:** `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_METADATA=true`

**Review cycle:** Must be reviewed and updated on every `foundry-platform-python` minor release.

### Classification Criteria

| Category | Tier-3 Permitted? | Rationale |
|---|---|---|
| Resource descriptors (`get`, `list`) | **Yes** | Structural metadata; needed for navigation |
| Schema / stats (`get_schema`, `get_health_checks`) | **Yes** | Data quality metadata |
| Status descriptors (`get_status`, `runs`) | **Yes** | Operational state metadata |
| Positional metadata (`get_end_offsets`, `get_read_position`) | **Yes** | Stream position metadata |
| File/table content (`read_table`, `file.content`) | **No** | Data content |
| Binary content (`attachment.read`, `media.read`) | **No** | Binary data |
| Function/query execution (`execute`, `apply`) | **No** | Computation/execution |
| Language model calls (`messages`, `embeddings`) | **No** | AI execution |
| AIP session execution (`blocking_continue`) | **No** | AI execution |
| Write operations (`create`, `delete`, `replace`, etc.) | **No** | Write operations |
| Unclassified | **No** | Deny by default |

---

## Classification Table

### Namespace: `admin`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `admin.authentication_provider.get` | PERMITTED | |
| `admin.authentication_provider.list` | PERMITTED | |
| `admin.authentication_provider.preregister_group` | BLOCKED | |
| `admin.authentication_provider.preregister_user` | BLOCKED | |
| `admin.cbac_banner.get` | PERMITTED | |
| `admin.cbac_marking_restrictions.get` | PERMITTED | |
| `admin.enrollment.get` | PERMITTED | |
| `admin.enrollment.get_current` | PERMITTED | |
| `admin.enrollment_role_assignment.add` | BLOCKED | |
| `admin.enrollment_role_assignment.list` | PERMITTED | |
| `admin.enrollment_role_assignment.remove` | BLOCKED | |
| `admin.group.create` | BLOCKED | |
| `admin.group.delete` | BLOCKED | |
| `admin.group.get` | PERMITTED | |
| `admin.group.get_batch` | PERMITTED | |
| `admin.group.list` | PERMITTED | |
| `admin.group.list_current` | PERMITTED | |
| `admin.group.replace` | BLOCKED | |
| `admin.group.search` | PERMITTED | |
| `admin.group_member.add` | BLOCKED | |
| `admin.group_member.list` | PERMITTED | |
| `admin.group_member.remove` | BLOCKED | |
| `admin.group_membership.list` | PERMITTED | |
| `admin.group_membership_expiration_policy.get` | PERMITTED | |
| `admin.group_membership_expiration_policy.replace` | BLOCKED | |
| `admin.group_provider_info.get` | PERMITTED | |
| `admin.group_provider_info.replace` | BLOCKED | |
| `admin.host.list` | PERMITTED | |
| `admin.marking.create` | BLOCKED | |
| `admin.marking.get` | PERMITTED | |
| `admin.marking.get_batch` | PERMITTED | |
| `admin.marking.list` | PERMITTED | |
| `admin.marking.replace` | BLOCKED | |
| `admin.marking_category.create` | BLOCKED | |
| `admin.marking_category.get` | PERMITTED | |
| `admin.marking_category.list` | PERMITTED | |
| `admin.marking_category.replace` | BLOCKED | |
| `admin.marking_member.add` | BLOCKED | |
| `admin.marking_member.list` | PERMITTED | |
| `admin.marking_member.remove` | BLOCKED | |
| `admin.marking_role_assignment.add` | BLOCKED | |
| `admin.marking_role_assignment.list` | PERMITTED | |
| `admin.marking_role_assignment.remove` | BLOCKED | |
| `admin.organization.create` | BLOCKED | |
| `admin.organization.get` | PERMITTED | |
| `admin.organization.list_available_roles` | PERMITTED | |
| `admin.organization.replace` | BLOCKED | |
| `admin.organization_guest_member.add` | BLOCKED | |
| `admin.organization_guest_member.list` | PERMITTED | |
| `admin.organization_guest_member.remove` | BLOCKED | |
| `admin.organization_role_assignment.add` | BLOCKED | |
| `admin.organization_role_assignment.list` | PERMITTED | |
| `admin.organization_role_assignment.remove` | BLOCKED | |
| `admin.role.get` | PERMITTED | |
| `admin.role.get_batch` | PERMITTED | |
| `admin.user.delete` | BLOCKED | |
| `admin.user.get` | PERMITTED | |
| `admin.user.get_batch` | PERMITTED | |
| `admin.user.get_current` | PERMITTED | |
| `admin.user.get_markings` | PERMITTED | |
| `admin.user.list` | PERMITTED | |
| `admin.user.profile_picture` | BLOCKED | |
| `admin.user.revoke_all_tokens` | BLOCKED | |
| `admin.user.search` | PERMITTED | |
| `admin.user_provider_info.get` | PERMITTED | |
| `admin.user_provider_info.replace` | BLOCKED | |
### Namespace: `aip_agents`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `aip_agents.agent.all_sessions` | BLOCKED | |
| `aip_agents.agent.get` | PERMITTED | |
| `aip_agents.agent_version.get` | PERMITTED | |
| `aip_agents.agent_version.list` | PERMITTED | |
| `aip_agents.content.get` | BLOCKED | |
| `aip_agents.session.blocking_continue` | BLOCKED | |
| `aip_agents.session.cancel` | BLOCKED | |
| `aip_agents.session.create` | BLOCKED | |
| `aip_agents.session.delete` | BLOCKED | |
| `aip_agents.session.get` | PERMITTED | |
| `aip_agents.session.list` | PERMITTED | |
| `aip_agents.session.rag_context` | BLOCKED | |
| `aip_agents.session.streaming_continue` | BLOCKED | |
| `aip_agents.session.update_title` | BLOCKED | |
| `aip_agents.session_trace.get` | PERMITTED | |
### Namespace: `audit`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `audit.log_file.content` | BLOCKED | |
| `audit.log_file.list` | PERMITTED | |
### Namespace: `checkpoints`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `checkpoints.record.get` | PERMITTED | |
| `checkpoints.record.get_batch` | PERMITTED | |
| `checkpoints.record.search` | PERMITTED | |
### Namespace: `connectivity`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `connectivity.connection.create` | BLOCKED | |
| `connectivity.connection.get` | PERMITTED | |
| `connectivity.connection.get_configuration` | PERMITTED | |
| `connectivity.connection.get_configuration_batch` | PERMITTED | |
| `connectivity.connection.update_export_settings` | BLOCKED | |
| `connectivity.connection.update_secrets` | BLOCKED | |
| `connectivity.connection.upload_custom_jdbc_drivers` | BLOCKED | |
| `connectivity.file_import.create` | BLOCKED | |
| `connectivity.file_import.delete` | BLOCKED | |
| `connectivity.file_import.execute` | BLOCKED | |
| `connectivity.file_import.get` | PERMITTED | |
| `connectivity.file_import.list` | PERMITTED | |
| `connectivity.file_import.replace` | BLOCKED | |
| `connectivity.table_import.create` | BLOCKED | |
| `connectivity.table_import.delete` | BLOCKED | |
| `connectivity.table_import.execute` | BLOCKED | |
| `connectivity.table_import.get` | PERMITTED | |
| `connectivity.table_import.list` | PERMITTED | |
| `connectivity.table_import.replace` | BLOCKED | |
| `connectivity.virtual_table.create` | BLOCKED | |
### Namespace: `data_health`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `data_health.check.create` | BLOCKED | |
| `data_health.check.delete` | BLOCKED | |
| `data_health.check.get` | PERMITTED | |
| `data_health.check.replace` | BLOCKED | |
| `data_health.check_report.get` | PERMITTED | |
| `data_health.check_report.get_latest` | PERMITTED | |
### Namespace: `datasets`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `datasets.branch.create` | BLOCKED | |
| `datasets.branch.delete` | BLOCKED | |
| `datasets.branch.get` | PERMITTED | |
| `datasets.branch.list` | PERMITTED | |
| `datasets.branch.transactions` | PERMITTED | |
| `datasets.dataset.create` | BLOCKED | |
| `datasets.dataset.get` | PERMITTED | |
| `datasets.dataset.get_health_check_reports` | PERMITTED | |
| `datasets.dataset.get_health_checks` | PERMITTED | |
| `datasets.dataset.get_schedules` | PERMITTED | |
| `datasets.dataset.get_schema` | PERMITTED | |
| `datasets.dataset.get_schema_batch` | PERMITTED | |
| `datasets.dataset.jobs` | PERMITTED | |
| `datasets.dataset.put_schema` | BLOCKED | |
| `datasets.dataset.read_table` | BLOCKED | |
| `datasets.dataset.transactions` | PERMITTED | |
| `datasets.file.content` | BLOCKED | |
| `datasets.file.delete` | BLOCKED | |
| `datasets.file.get` | PERMITTED | |
| `datasets.file.list` | PERMITTED | |
| `datasets.file.upload` | BLOCKED | |
| `datasets.transaction.abort` | BLOCKED | |
| `datasets.transaction.build` | BLOCKED | |
| `datasets.transaction.commit` | BLOCKED | |
| `datasets.transaction.create` | BLOCKED | |
| `datasets.transaction.get` | PERMITTED | |
| `datasets.transaction.job` | PERMITTED | |
| `datasets.view.add_backing_datasets` | BLOCKED | |
| `datasets.view.add_primary_key` | BLOCKED | |
| `datasets.view.create` | BLOCKED | |
| `datasets.view.get` | PERMITTED | |
| `datasets.view.remove_backing_datasets` | BLOCKED | |
| `datasets.view.replace_backing_datasets` | BLOCKED | |
### Namespace: `filesystem`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `filesystem.folder.children` | PERMITTED | |
| `filesystem.folder.create` | BLOCKED | |
| `filesystem.folder.get` | PERMITTED | |
| `filesystem.folder.get_batch` | PERMITTED | |
| `filesystem.folder.replace` | BLOCKED | |
| `filesystem.project.add_organizations` | BLOCKED | |
| `filesystem.project.create` | BLOCKED | |
| `filesystem.project.create_from_template` | BLOCKED | |
| `filesystem.project.get` | PERMITTED | |
| `filesystem.project.organizations` | PERMITTED | |
| `filesystem.project.remove_organizations` | BLOCKED | |
| `filesystem.project.replace` | BLOCKED | |
| `filesystem.resource.add_markings` | BLOCKED | |
| `filesystem.resource.delete` | BLOCKED | |
| `filesystem.resource.get` | PERMITTED | |
| `filesystem.resource.get_access_requirements` | PERMITTED | |
| `filesystem.resource.get_batch` | PERMITTED | |
| `filesystem.resource.get_by_path` | PERMITTED | |
| `filesystem.resource.get_by_path_batch` | PERMITTED | |
| `filesystem.resource.markings` | PERMITTED | |
| `filesystem.resource.permanently_delete` | BLOCKED | |
| `filesystem.resource.remove_markings` | BLOCKED | |
| `filesystem.resource.restore` | BLOCKED | |
| `filesystem.resource_role.add` | BLOCKED | |
| `filesystem.resource_role.list` | PERMITTED | |
| `filesystem.resource_role.remove` | BLOCKED | |
| `filesystem.space.create` | BLOCKED | |
| `filesystem.space.delete` | BLOCKED | |
| `filesystem.space.get` | PERMITTED | |
| `filesystem.space.list` | PERMITTED | |
| `filesystem.space.replace` | BLOCKED | |
### Namespace: `functions`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `functions.query.execute` | BLOCKED | |
| `functions.query.get` | PERMITTED | |
| `functions.query.get_by_rid` | PERMITTED | |
| `functions.query.get_by_rid_batch` | PERMITTED | |
| `functions.query.streaming_execute` | BLOCKED | |
| `functions.value_type.get` | PERMITTED | |
| `functions.version_id.get` | PERMITTED | |
### Namespace: `language_models`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `language_models.anthropic_model.messages` | BLOCKED | |
| `language_models.open_ai_model.embeddings` | BLOCKED | |
### Namespace: `media_sets`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `media_sets.media_set.abort` | BLOCKED | |
| `media_sets.media_set.calculate` | BLOCKED | |
| `media_sets.media_set.clear` | BLOCKED | |
| `media_sets.media_set.commit` | BLOCKED | |
| `media_sets.media_set.create` | BLOCKED | |
| `media_sets.media_set.get` | PERMITTED | |
| `media_sets.media_set.get_result` | BLOCKED | |
| `media_sets.media_set.get_rid_by_path` | PERMITTED | |
| `media_sets.media_set.get_status` | PERMITTED | |
| `media_sets.media_set.info` | PERMITTED | |
| `media_sets.media_set.metadata` | PERMITTED | |
| `media_sets.media_set.read` | BLOCKED | |
| `media_sets.media_set.read_original` | BLOCKED | |
| `media_sets.media_set.reference` | BLOCKED | |
| `media_sets.media_set.register` | BLOCKED | |
| `media_sets.media_set.retrieve` | BLOCKED | |
| `media_sets.media_set.transform` | BLOCKED | |
| `media_sets.media_set.upload` | BLOCKED | |
| `media_sets.media_set.upload_media` | BLOCKED | |
### Namespace: `models`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `models.experiment.get` | PERMITTED | |
| `models.experiment.search` | PERMITTED | |
| `models.experiment_artifact_table.json` | BLOCKED | |
| `models.experiment_artifact_table.parquet` | BLOCKED | |
| `models.experiment_series.json` | BLOCKED | |
| `models.experiment_series.parquet` | BLOCKED | |
| `models.live_deployment.transform_json` | BLOCKED | |
| `models.model.create` | BLOCKED | |
| `models.model.get` | PERMITTED | |
| `models.model.promote_version` | BLOCKED | |
| `models.model_studio.create` | BLOCKED | |
| `models.model_studio.get` | PERMITTED | |
| `models.model_studio.launch` | BLOCKED | |
| `models.model_studio_config_version.create` | BLOCKED | |
| `models.model_studio_config_version.get` | PERMITTED | |
| `models.model_studio_config_version.latest` | PERMITTED | |
| `models.model_studio_config_version.list` | PERMITTED | |
| `models.model_studio_run.list` | PERMITTED | |
| `models.model_studio_trainer.get` | PERMITTED | |
| `models.model_studio_trainer.list` | PERMITTED | |
| `models.model_version.create` | BLOCKED | |
| `models.model_version.get` | PERMITTED | |
| `models.model_version.list` | PERMITTED | |
### Namespace: `ontologies`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `ontologies.action.apply` | BLOCKED | |
| `ontologies.action.apply_batch` | BLOCKED | |
| `ontologies.action.apply_with_overrides` | BLOCKED | |
| `ontologies.action_type.get` | PERMITTED | |
| `ontologies.action_type.get_by_rid` | PERMITTED | |
| `ontologies.action_type.get_by_rid_batch` | PERMITTED | |
| `ontologies.action_type.list` | PERMITTED | |
| `ontologies.action_type_full_metadata.get` | PERMITTED | |
| `ontologies.action_type_full_metadata.list` | PERMITTED | |
| `ontologies.attachment.get` | PERMITTED | |
| `ontologies.attachment.read` | BLOCKED | |
| `ontologies.attachment.upload` | BLOCKED | |
| `ontologies.attachment.upload_with_rid` | BLOCKED | |
| `ontologies.attachment_property.get_attachment` | PERMITTED | |
| `ontologies.attachment_property.get_attachment_by_rid` | PERMITTED | |
| `ontologies.attachment_property.read_attachment` | BLOCKED | |
| `ontologies.attachment_property.read_attachment_by_rid` | BLOCKED | |
| `ontologies.cipher_text_property.decrypt` | BLOCKED | |
| `ontologies.geotemporal_series_property.get_geotemporal_series_latest_value` | BLOCKED | |
| `ontologies.geotemporal_series_property.stream_geotemporal_series_historic_values` | BLOCKED | |
| `ontologies.linked_object.get_linked_object` | BLOCKED | |
| `ontologies.linked_object.list_linked_objects` | BLOCKED | |
| `ontologies.media_reference_property.get_media_content` | BLOCKED | |
| `ontologies.media_reference_property.get_media_metadata` | PERMITTED | |
| `ontologies.media_reference_property.upload` | BLOCKED | |
| `ontologies.object_type.get` | PERMITTED | |
| `ontologies.object_type.get_by_rid_batch` | PERMITTED | |
| `ontologies.object_type.get_edits_history` | BLOCKED | |
| `ontologies.object_type.get_full_metadata` | PERMITTED | |
| `ontologies.object_type.get_outgoing_link_type` | PERMITTED | |
| `ontologies.object_type.list` | PERMITTED | |
| `ontologies.object_type.list_outgoing_link_types` | PERMITTED | |
| `ontologies.ontology.get` | PERMITTED | |
| `ontologies.ontology.get_full_metadata` | PERMITTED | |
| `ontologies.ontology.list` | PERMITTED | |
| `ontologies.ontology.load_metadata` | PERMITTED | |
| `ontologies.ontology_interface.aggregate` | BLOCKED | |
| `ontologies.ontology_interface.get` | PERMITTED | |
| `ontologies.ontology_interface.get_outgoing_interface_link_type` | PERMITTED | |
| `ontologies.ontology_interface.list` | PERMITTED | |
| `ontologies.ontology_interface.list_interface_linked_objects` | BLOCKED | |
| `ontologies.ontology_interface.list_objects_for_interface` | BLOCKED | |
| `ontologies.ontology_interface.list_outgoing_interface_link_types` | PERMITTED | |
| `ontologies.ontology_interface.search` | BLOCKED | |
| `ontologies.ontology_object.aggregate` | BLOCKED | |
| `ontologies.ontology_object.count` | BLOCKED | |
| `ontologies.ontology_object.get` | BLOCKED | |
| `ontologies.ontology_object.list` | BLOCKED | |
| `ontologies.ontology_object.search` | BLOCKED | |
| `ontologies.ontology_object_set.aggregate` | BLOCKED | |
| `ontologies.ontology_object_set.create_temporary` | BLOCKED | |
| `ontologies.ontology_object_set.get` | BLOCKED | |
| `ontologies.ontology_object_set.load` | BLOCKED | |
| `ontologies.ontology_object_set.load_links` | BLOCKED | |
| `ontologies.ontology_object_set.load_multiple_object_types` | BLOCKED | |
| `ontologies.ontology_object_set.load_objects_or_interfaces` | BLOCKED | |
| `ontologies.ontology_transaction.post_edits` | BLOCKED | |
| `ontologies.ontology_value_type.get` | PERMITTED | |
| `ontologies.ontology_value_type.list` | PERMITTED | |
| `ontologies.query.execute` | BLOCKED | |
| `ontologies.query_type.get` | PERMITTED | |
| `ontologies.query_type.list` | PERMITTED | |
| `ontologies.time_series_property_v2.get_first_point` | BLOCKED | |
| `ontologies.time_series_property_v2.get_last_point` | BLOCKED | |
| `ontologies.time_series_property_v2.stream_points` | BLOCKED | |
| `ontologies.time_series_value_bank_property.get_latest_value` | BLOCKED | |
| `ontologies.time_series_value_bank_property.stream_values` | BLOCKED | |
### Namespace: `orchestration`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `orchestration.build.cancel` | BLOCKED | |
| `orchestration.build.create` | BLOCKED | |
| `orchestration.build.get` | PERMITTED | |
| `orchestration.build.get_batch` | PERMITTED | |
| `orchestration.build.jobs` | PERMITTED | |
| `orchestration.build.search` | PERMITTED | |
| `orchestration.job.get` | PERMITTED | |
| `orchestration.job.get_batch` | PERMITTED | |
| `orchestration.schedule.create` | BLOCKED | |
| `orchestration.schedule.delete` | BLOCKED | |
| `orchestration.schedule.get` | PERMITTED | |
| `orchestration.schedule.get_affected_resources` | PERMITTED | |
| `orchestration.schedule.get_batch` | PERMITTED | |
| `orchestration.schedule.pause` | BLOCKED | |
| `orchestration.schedule.replace` | BLOCKED | |
| `orchestration.schedule.run` | BLOCKED | |
| `orchestration.schedule.runs` | PERMITTED | |
| `orchestration.schedule.unpause` | BLOCKED | |
| `orchestration.schedule_version.get` | PERMITTED | |
| `orchestration.schedule_version.schedule` | PERMITTED | |
### Namespace: `sql_queries`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `sql_queries.sql_query.cancel` | BLOCKED | |
| `sql_queries.sql_query.execute` | BLOCKED | |
| `sql_queries.sql_query.execute_ontology` | BLOCKED | |
| `sql_queries.sql_query.get_results` | BLOCKED | |
| `sql_queries.sql_query.get_status` | PERMITTED | |
### Namespace: `streams`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `streams.dataset.create` | BLOCKED | |
| `streams.stream.create` | BLOCKED | |
| `streams.stream.get` | PERMITTED | |
| `streams.stream.get_end_offsets` | PERMITTED | |
| `streams.stream.get_records` | BLOCKED | |
| `streams.stream.publish_binary_record` | BLOCKED | |
| `streams.stream.publish_record` | BLOCKED | |
| `streams.stream.publish_records` | BLOCKED | |
| `streams.stream.reset` | BLOCKED | |
| `streams.subscriber.commit_offsets` | BLOCKED | |
| `streams.subscriber.create` | BLOCKED | |
| `streams.subscriber.delete` | BLOCKED | |
| `streams.subscriber.get_read_position` | PERMITTED | |
| `streams.subscriber.read_records` | BLOCKED | |
| `streams.subscriber.reset_offsets` | BLOCKED | |
### Namespace: `third_party_applications`

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `third_party_applications.third_party_application.get` | PERMITTED | |
| `third_party_applications.version.delete` | BLOCKED | |
| `third_party_applications.version.get` | PERMITTED | |
| `third_party_applications.version.list` | PERMITTED | |
| `third_party_applications.version.upload` | BLOCKED | |
| `third_party_applications.version.upload_snapshot` | BLOCKED | |
| `third_party_applications.website.deploy` | BLOCKED | |
| `third_party_applications.website.get` | PERMITTED | |
| `third_party_applications.website.undeploy` | BLOCKED | |
### Namespace: `widgets`

> **Surface correction (QUESTION-043, 2026-08-11):** The installed runtime SDK
> `foundry-platform-sdk 1.102.0` exposes exactly **8** widgets operations. The rows for
> `dev_mode_settings.disable`, `dev_mode_settings.get`, `dev_mode_settings.pause`, and
> `dev_mode_settings.set_widget_set` are retained for canonical completeness but are
> **NOT implemented** in the `foundry-widgets` CLI (DEV-022). `DevModeSettingsV2` is out
> of scope. The packaged allow-list in `src/foundry_cli/widgets/metadata-allow-list.md`
> contains only the 8 implemented rows.

| SDK Path | Tier-3 Status | Reason |
|---|---|---|
| `widgets.dev_mode_settings.disable` *(not implemented)* | BLOCKED | |
| `widgets.dev_mode_settings.enable` | BLOCKED | |
| `widgets.dev_mode_settings.get` *(not implemented)* | PERMITTED | |
| `widgets.dev_mode_settings.pause` *(not implemented)* | BLOCKED | |
| `widgets.dev_mode_settings.set_widget_set` *(not implemented)* | BLOCKED | |
| `widgets.dev_mode_settings.set_widget_set_by_id` | BLOCKED | |
| `widgets.release.delete` | BLOCKED | |
| `widgets.release.get` | PERMITTED | |
| `widgets.release.list` | PERMITTED | |
| `widgets.repository.get` | PERMITTED | |
| `widgets.repository.publish` | BLOCKED | |
| `widgets.widget_set.get` | PERMITTED | |

---

## .env-Format Allow-List (Permitted Operations Only)

Copy the block below into your `.env` file or reference it in your configuration.
Only `true` entries are listed; all others are blocked by default.

```dotenv
# Foundry CLI Metadata Allow-List — 162 permitted operations
# Generated: 2026-04-13 | Review on every foundry-platform-python minor release
# Default: blocked. Only listed operations are permitted in Tier-3 (METADATA_ONLY=true).

# --- ADMIN ---
FOUNDRY_AGENTIC_CLI_ADMIN_AUTHENTICATION_PROVIDER_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_AUTHENTICATION_PROVIDER_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_CBAC_BANNER_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_CBAC_MARKING_RESTRICTIONS_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_ENROLLMENT_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_ENROLLMENT_GET_CURRENT_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_ENROLLMENT_ROLE_ASSIGNMENT_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_GROUP_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_GROUP_GET_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_GROUP_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_GROUP_LIST_CURRENT_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_GROUP_SEARCH_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_GROUP_MEMBER_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_GROUP_MEMBERSHIP_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_GROUP_MEMBERSHIP_EXPIRATION_POLICY_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_GROUP_PROVIDER_INFO_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_HOST_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_MARKING_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_MARKING_GET_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_MARKING_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_MARKING_CATEGORY_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_MARKING_CATEGORY_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_MARKING_MEMBER_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_MARKING_ROLE_ASSIGNMENT_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_ORGANIZATION_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_ORGANIZATION_LIST_AVAILABLE_ROLES_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_ORGANIZATION_GUEST_MEMBER_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_ORGANIZATION_ROLE_ASSIGNMENT_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_ROLE_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_ROLE_GET_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_USER_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_USER_GET_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_USER_GET_CURRENT_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_USER_GET_MARKINGS_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_USER_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_USER_SEARCH_METADATA=true
FOUNDRY_AGENTIC_CLI_ADMIN_USER_PROVIDER_INFO_GET_METADATA=true

# --- AIP_AGENTS ---
FOUNDRY_AGENTIC_CLI_AIP_AGENTS_AGENT_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_AIP_AGENTS_AGENT_VERSION_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_AIP_AGENTS_AGENT_VERSION_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_AIP_AGENTS_SESSION_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_AIP_AGENTS_SESSION_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_AIP_AGENTS_SESSION_TRACE_GET_METADATA=true

# --- AUDIT ---
FOUNDRY_AGENTIC_CLI_AUDIT_LOG_FILE_LIST_METADATA=true

# --- CHECKPOINTS ---
FOUNDRY_AGENTIC_CLI_CHECKPOINTS_RECORD_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_CHECKPOINTS_RECORD_GET_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_CHECKPOINTS_RECORD_SEARCH_METADATA=true

# --- CONNECTIVITY ---
FOUNDRY_AGENTIC_CLI_CONNECTIVITY_CONNECTION_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_CONNECTIVITY_CONNECTION_GET_CONFIGURATION_METADATA=true
FOUNDRY_AGENTIC_CLI_CONNECTIVITY_CONNECTION_GET_CONFIGURATION_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_CONNECTIVITY_FILE_IMPORT_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_CONNECTIVITY_FILE_IMPORT_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_CONNECTIVITY_TABLE_IMPORT_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_CONNECTIVITY_TABLE_IMPORT_LIST_METADATA=true

# --- DATA_HEALTH ---
FOUNDRY_AGENTIC_CLI_DATA_HEALTH_CHECK_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_DATA_HEALTH_CHECK_REPORT_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_DATA_HEALTH_CHECK_REPORT_GET_LATEST_METADATA=true

# --- DATASETS ---
FOUNDRY_AGENTIC_CLI_DATASETS_BRANCH_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_BRANCH_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_BRANCH_TRANSACTIONS_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_GET_HEALTH_CHECK_REPORTS_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_GET_HEALTH_CHECKS_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_GET_SCHEDULES_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_GET_SCHEMA_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_GET_SCHEMA_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_JOBS_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_TRANSACTIONS_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_FILE_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_FILE_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_TRANSACTION_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_TRANSACTION_JOB_METADATA=true
FOUNDRY_AGENTIC_CLI_DATASETS_VIEW_GET_METADATA=true

# --- FILESYSTEM ---
FOUNDRY_AGENTIC_CLI_FILESYSTEM_FOLDER_CHILDREN_METADATA=true
FOUNDRY_AGENTIC_CLI_FILESYSTEM_FOLDER_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_FILESYSTEM_FOLDER_GET_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_FILESYSTEM_PROJECT_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_FILESYSTEM_PROJECT_ORGANIZATIONS_METADATA=true
FOUNDRY_AGENTIC_CLI_FILESYSTEM_RESOURCE_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_FILESYSTEM_RESOURCE_GET_ACCESS_REQUIREMENTS_METADATA=true
FOUNDRY_AGENTIC_CLI_FILESYSTEM_RESOURCE_GET_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_FILESYSTEM_RESOURCE_GET_BY_PATH_METADATA=true
FOUNDRY_AGENTIC_CLI_FILESYSTEM_RESOURCE_GET_BY_PATH_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_FILESYSTEM_RESOURCE_MARKINGS_METADATA=true
FOUNDRY_AGENTIC_CLI_FILESYSTEM_RESOURCE_ROLE_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_FILESYSTEM_SPACE_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_FILESYSTEM_SPACE_LIST_METADATA=true

# --- FUNCTIONS ---
FOUNDRY_AGENTIC_CLI_FUNCTIONS_QUERY_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_FUNCTIONS_QUERY_GET_BY_RID_METADATA=true
FOUNDRY_AGENTIC_CLI_FUNCTIONS_QUERY_GET_BY_RID_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_FUNCTIONS_VALUE_TYPE_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_FUNCTIONS_VERSION_ID_GET_METADATA=true

# --- MEDIA_SETS ---
FOUNDRY_AGENTIC_CLI_MEDIA_SETS_MEDIA_SET_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_MEDIA_SETS_MEDIA_SET_GET_RID_BY_PATH_METADATA=true
FOUNDRY_AGENTIC_CLI_MEDIA_SETS_MEDIA_SET_GET_STATUS_METADATA=true
FOUNDRY_AGENTIC_CLI_MEDIA_SETS_MEDIA_SET_INFO_METADATA=true
FOUNDRY_AGENTIC_CLI_MEDIA_SETS_MEDIA_SET_METADATA_METADATA=true

# --- MODELS ---
FOUNDRY_AGENTIC_CLI_MODELS_EXPERIMENT_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_MODELS_EXPERIMENT_SEARCH_METADATA=true
FOUNDRY_AGENTIC_CLI_MODELS_MODEL_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_MODELS_MODEL_STUDIO_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_MODELS_MODEL_STUDIO_CONFIG_VERSION_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_MODELS_MODEL_STUDIO_CONFIG_VERSION_LATEST_METADATA=true
FOUNDRY_AGENTIC_CLI_MODELS_MODEL_STUDIO_CONFIG_VERSION_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_MODELS_MODEL_STUDIO_RUN_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_MODELS_MODEL_STUDIO_TRAINER_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_MODELS_MODEL_STUDIO_TRAINER_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_MODELS_MODEL_VERSION_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_MODELS_MODEL_VERSION_LIST_METADATA=true

# --- ONTOLOGIES ---
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ACTION_TYPE_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ACTION_TYPE_GET_BY_RID_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ACTION_TYPE_GET_BY_RID_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ACTION_TYPE_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ACTION_TYPE_FULL_METADATA_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ACTION_TYPE_FULL_METADATA_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ATTACHMENT_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ATTACHMENT_PROPERTY_GET_ATTACHMENT_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ATTACHMENT_PROPERTY_GET_ATTACHMENT_BY_RID_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_MEDIA_REFERENCE_PROPERTY_GET_MEDIA_METADATA_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_OBJECT_TYPE_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_OBJECT_TYPE_GET_BY_RID_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_OBJECT_TYPE_GET_FULL_METADATA_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_OBJECT_TYPE_GET_OUTGOING_LINK_TYPE_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_OBJECT_TYPE_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_OBJECT_TYPE_LIST_OUTGOING_LINK_TYPES_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ONTOLOGY_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ONTOLOGY_GET_FULL_METADATA_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ONTOLOGY_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ONTOLOGY_LOAD_METADATA_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ONTOLOGY_INTERFACE_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ONTOLOGY_INTERFACE_GET_OUTGOING_INTERFACE_LINK_TYPE_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ONTOLOGY_INTERFACE_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ONTOLOGY_INTERFACE_LIST_OUTGOING_INTERFACE_LINK_TYPES_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ONTOLOGY_VALUE_TYPE_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_ONTOLOGY_VALUE_TYPE_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_QUERY_TYPE_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ONTOLOGIES_QUERY_TYPE_LIST_METADATA=true

# --- ORCHESTRATION ---
FOUNDRY_AGENTIC_CLI_ORCHESTRATION_BUILD_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ORCHESTRATION_BUILD_GET_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_ORCHESTRATION_BUILD_JOBS_METADATA=true
FOUNDRY_AGENTIC_CLI_ORCHESTRATION_BUILD_SEARCH_METADATA=true
FOUNDRY_AGENTIC_CLI_ORCHESTRATION_JOB_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ORCHESTRATION_JOB_GET_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_ORCHESTRATION_SCHEDULE_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ORCHESTRATION_SCHEDULE_GET_AFFECTED_RESOURCES_METADATA=true
FOUNDRY_AGENTIC_CLI_ORCHESTRATION_SCHEDULE_GET_BATCH_METADATA=true
FOUNDRY_AGENTIC_CLI_ORCHESTRATION_SCHEDULE_RUNS_METADATA=true
FOUNDRY_AGENTIC_CLI_ORCHESTRATION_SCHEDULE_VERSION_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_ORCHESTRATION_SCHEDULE_VERSION_SCHEDULE_METADATA=true

# --- SQL_QUERIES ---
FOUNDRY_AGENTIC_CLI_SQL_QUERIES_SQL_QUERY_GET_STATUS_METADATA=true

# --- STREAMS ---
FOUNDRY_AGENTIC_CLI_STREAMS_STREAM_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_STREAMS_STREAM_GET_END_OFFSETS_METADATA=true
FOUNDRY_AGENTIC_CLI_STREAMS_SUBSCRIBER_GET_READ_POSITION_METADATA=true

# --- THIRD_PARTY_APPLICATIONS ---
FOUNDRY_AGENTIC_CLI_THIRD_PARTY_APPLICATIONS_THIRD_PARTY_APPLICATION_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_THIRD_PARTY_APPLICATIONS_VERSION_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_THIRD_PARTY_APPLICATIONS_VERSION_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_THIRD_PARTY_APPLICATIONS_WEBSITE_GET_METADATA=true

# --- WIDGETS ---
FOUNDRY_AGENTIC_CLI_WIDGETS_DEV_MODE_SETTINGS_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_WIDGETS_RELEASE_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_WIDGETS_RELEASE_LIST_METADATA=true
FOUNDRY_AGENTIC_CLI_WIDGETS_REPOSITORY_GET_METADATA=true
FOUNDRY_AGENTIC_CLI_WIDGETS_WIDGET_SET_GET_METADATA=true
```

---
*META-ALLOW-001 v1.0.0 — Generated 2026-04-13 — Foundry CLI Agentic Toolset*
