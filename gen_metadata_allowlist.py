"""Generate metadata allow-list for Tier-3 (METADATA_ONLY) access control."""
import os, re

BASE = r'.ept\docs\customer_input\foundry-platform-python\foundry_sdk\v2'
PREFIX = "FOUNDRY_AGENTIC_CLI_"

# Collect all operations
operations = []
for ns in sorted(os.listdir(BASE)):
    ns_path = os.path.join(BASE, ns)
    if not os.path.isdir(ns_path) or ns.startswith('_'):
        continue
    for fname in sorted(os.listdir(ns_path)):
        if not fname.endswith('.py') or fname.startswith('_') or fname in ('models.py', 'errors.py'):
            continue
        cls = fname[:-3]
        content = open(os.path.join(ns_path, fname)).read()
        methods = re.findall(r'^    def ([a-z][a-z0-9_]+)\(', content, re.MULTILINE)
        unique_methods = list(dict.fromkeys(methods))
        for m in unique_methods:
            operations.append((ns, cls, m))

# Classification: True = metadata-permitted, False = blocked in Tier-3
# Default is False (deny by default per SRS §4.3)
METADATA_PERMITTED = {
    # =========================================================
    # ADMIN namespace
    # =========================================================
    ("admin", "authentication_provider", "get"): True,
    ("admin", "authentication_provider", "list"): True,
    ("admin", "authentication_provider", "preregister_group"): False,  # write
    ("admin", "authentication_provider", "preregister_user"): False,   # write
    ("admin", "cbac_banner", "get"): True,
    ("admin", "cbac_marking_restrictions", "get"): True,
    ("admin", "enrollment", "get"): True,
    ("admin", "enrollment", "get_current"): True,
    ("admin", "enrollment_role_assignment", "add"): False,   # write
    ("admin", "enrollment_role_assignment", "list"): True,
    ("admin", "enrollment_role_assignment", "remove"): False, # write
    ("admin", "group", "create"): False,
    ("admin", "group", "delete"): False,
    ("admin", "group", "get"): True,
    ("admin", "group", "get_batch"): True,
    ("admin", "group", "list"): True,
    ("admin", "group", "list_current"): True,
    ("admin", "group", "replace"): False,
    ("admin", "group", "search"): True,
    ("admin", "group_member", "add"): False,
    ("admin", "group_member", "list"): True,
    ("admin", "group_member", "remove"): False,
    ("admin", "group_membership", "list"): True,
    ("admin", "group_membership_expiration_policy", "get"): True,
    ("admin", "group_membership_expiration_policy", "replace"): False,
    ("admin", "group_provider_info", "get"): True,
    ("admin", "group_provider_info", "replace"): False,
    ("admin", "host", "list"): True,
    ("admin", "marking", "create"): False,
    ("admin", "marking", "get"): True,
    ("admin", "marking", "get_batch"): True,
    ("admin", "marking", "list"): True,
    ("admin", "marking", "replace"): False,
    ("admin", "marking_category", "create"): False,
    ("admin", "marking_category", "get"): True,
    ("admin", "marking_category", "list"): True,
    ("admin", "marking_category", "replace"): False,
    ("admin", "marking_member", "add"): False,
    ("admin", "marking_member", "list"): True,
    ("admin", "marking_member", "remove"): False,
    ("admin", "marking_role_assignment", "add"): False,
    ("admin", "marking_role_assignment", "list"): True,
    ("admin", "marking_role_assignment", "remove"): False,
    ("admin", "organization", "create"): False,
    ("admin", "organization", "get"): True,
    ("admin", "organization", "list_available_roles"): True,
    ("admin", "organization", "replace"): False,
    ("admin", "organization_guest_member", "add"): False,
    ("admin", "organization_guest_member", "list"): True,
    ("admin", "organization_guest_member", "remove"): False,
    ("admin", "organization_role_assignment", "add"): False,
    ("admin", "organization_role_assignment", "list"): True,
    ("admin", "organization_role_assignment", "remove"): False,
    ("admin", "role", "get"): True,
    ("admin", "role", "get_batch"): True,
    ("admin", "user", "delete"): False,
    ("admin", "user", "get"): True,
    ("admin", "user", "get_batch"): True,
    ("admin", "user", "get_current"): True,
    ("admin", "user", "get_markings"): True,
    ("admin", "user", "list"): True,
    ("admin", "user", "profile_picture"): False,   # binary content
    ("admin", "user", "revoke_all_tokens"): False,
    ("admin", "user", "search"): True,
    ("admin", "user_provider_info", "get"): True,
    ("admin", "user_provider_info", "replace"): False,

    # =========================================================
    # AIP_AGENTS namespace
    # =========================================================
    ("aip_agents", "agent", "all_sessions"): False,   # session data, not structural metadata
    ("aip_agents", "agent", "get"): True,
    ("aip_agents", "agent_version", "get"): True,
    ("aip_agents", "agent_version", "list"): True,
    ("aip_agents", "content", "get"): False,          # content data
    ("aip_agents", "session", "blocking_continue"): False,  # execution
    ("aip_agents", "session", "cancel"): False,       # write
    ("aip_agents", "session", "create"): False,       # write
    ("aip_agents", "session", "delete"): False,       # write
    ("aip_agents", "session", "get"): True,
    ("aip_agents", "session", "list"): True,
    ("aip_agents", "session", "rag_context"): False,  # data retrieval
    ("aip_agents", "session", "streaming_continue"): False,  # execution
    ("aip_agents", "session", "update_title"): False,  # write
    ("aip_agents", "session_trace", "get"): True,

    # =========================================================
    # AUDIT namespace
    # =========================================================
    ("audit", "log_file", "content"): False,   # binary log content
    ("audit", "log_file", "list"): True,       # log file descriptors

    # =========================================================
    # CHECKPOINTS namespace
    # =========================================================
    ("checkpoints", "record", "get"): True,
    ("checkpoints", "record", "get_batch"): True,
    ("checkpoints", "record", "search"): True,

    # =========================================================
    # CONNECTIVITY namespace
    # =========================================================
    ("connectivity", "connection", "create"): False,
    ("connectivity", "connection", "get"): True,
    ("connectivity", "connection", "get_configuration"): True,
    ("connectivity", "connection", "get_configuration_batch"): True,
    ("connectivity", "connection", "update_export_settings"): False,
    ("connectivity", "connection", "update_secrets"): False,
    ("connectivity", "connection", "upload_custom_jdbc_drivers"): False,
    ("connectivity", "file_import", "create"): False,
    ("connectivity", "file_import", "delete"): False,
    ("connectivity", "file_import", "execute"): False,  # execution
    ("connectivity", "file_import", "get"): True,
    ("connectivity", "file_import", "list"): True,
    ("connectivity", "file_import", "replace"): False,
    ("connectivity", "table_import", "create"): False,
    ("connectivity", "table_import", "delete"): False,
    ("connectivity", "table_import", "execute"): False,  # execution
    ("connectivity", "table_import", "get"): True,
    ("connectivity", "table_import", "list"): True,
    ("connectivity", "table_import", "replace"): False,
    ("connectivity", "virtual_table", "create"): False,

    # =========================================================
    # DATA_HEALTH namespace
    # =========================================================
    ("data_health", "check", "create"): False,
    ("data_health", "check", "delete"): False,
    ("data_health", "check", "get"): True,
    ("data_health", "check", "replace"): False,
    ("data_health", "check_report", "get"): True,
    ("data_health", "check_report", "get_latest"): True,

    # =========================================================
    # DATASETS namespace
    # =========================================================
    ("datasets", "branch", "create"): False,
    ("datasets", "branch", "delete"): False,
    ("datasets", "branch", "get"): True,
    ("datasets", "branch", "list"): True,
    ("datasets", "branch", "transactions"): True,     # list of transaction metadata
    ("datasets", "dataset", "create"): False,
    ("datasets", "dataset", "get"): True,
    ("datasets", "dataset", "get_health_check_reports"): True,
    ("datasets", "dataset", "get_health_checks"): True,
    ("datasets", "dataset", "get_schedules"): True,
    ("datasets", "dataset", "get_schema"): True,
    ("datasets", "dataset", "get_schema_batch"): True,
    ("datasets", "dataset", "jobs"): True,            # job descriptors (metadata)
    ("datasets", "dataset", "put_schema"): False,
    ("datasets", "dataset", "read_table"): False,     # data content
    ("datasets", "dataset", "transactions"): True,    # transaction metadata
    ("datasets", "file", "content"): False,           # binary file content
    ("datasets", "file", "delete"): False,
    ("datasets", "file", "get"): True,
    ("datasets", "file", "list"): True,
    ("datasets", "file", "upload"): False,
    ("datasets", "transaction", "abort"): False,
    ("datasets", "transaction", "build"): False,      # execution
    ("datasets", "transaction", "commit"): False,
    ("datasets", "transaction", "create"): False,
    ("datasets", "transaction", "get"): True,
    ("datasets", "transaction", "job"): True,         # job descriptor
    ("datasets", "view", "add_backing_datasets"): False,
    ("datasets", "view", "add_primary_key"): False,
    ("datasets", "view", "create"): False,
    ("datasets", "view", "get"): True,
    ("datasets", "view", "remove_backing_datasets"): False,
    ("datasets", "view", "replace_backing_datasets"): False,

    # =========================================================
    # FILESYSTEM namespace
    # =========================================================
    ("filesystem", "folder", "children"): True,
    ("filesystem", "folder", "create"): False,
    ("filesystem", "folder", "get"): True,
    ("filesystem", "folder", "get_batch"): True,
    ("filesystem", "folder", "replace"): False,
    ("filesystem", "project", "add_organizations"): False,
    ("filesystem", "project", "create"): False,
    ("filesystem", "project", "create_from_template"): False,
    ("filesystem", "project", "get"): True,
    ("filesystem", "project", "organizations"): True,
    ("filesystem", "project", "remove_organizations"): False,
    ("filesystem", "project", "replace"): False,
    ("filesystem", "resource", "add_markings"): False,
    ("filesystem", "resource", "delete"): False,
    ("filesystem", "resource", "get"): True,
    ("filesystem", "resource", "get_access_requirements"): True,
    ("filesystem", "resource", "get_batch"): True,
    ("filesystem", "resource", "get_by_path"): True,
    ("filesystem", "resource", "get_by_path_batch"): True,
    ("filesystem", "resource", "markings"): True,
    ("filesystem", "resource", "permanently_delete"): False,
    ("filesystem", "resource", "remove_markings"): False,
    ("filesystem", "resource", "restore"): False,
    ("filesystem", "resource_role", "add"): False,
    ("filesystem", "resource_role", "list"): True,
    ("filesystem", "resource_role", "remove"): False,
    ("filesystem", "space", "create"): False,
    ("filesystem", "space", "delete"): False,
    ("filesystem", "space", "get"): True,
    ("filesystem", "space", "list"): True,
    ("filesystem", "space", "replace"): False,

    # =========================================================
    # FUNCTIONS namespace
    # =========================================================
    ("functions", "query", "execute"): False,          # execution/data
    ("functions", "query", "get"): True,
    ("functions", "query", "get_by_rid"): True,
    ("functions", "query", "get_by_rid_batch"): True,
    ("functions", "query", "streaming_execute"): False, # execution
    ("functions", "value_type", "get"): True,
    ("functions", "version_id", "get"): True,

    # =========================================================
    # GEO namespace (0 public methods — no entries)
    # =========================================================

    # =========================================================
    # LANGUAGE_MODELS namespace
    # =========================================================
    ("language_models", "anthropic_model", "messages"): False,  # execution
    ("language_models", "open_ai_model", "embeddings"): False,   # execution

    # =========================================================
    # MEDIA_SETS namespace
    # =========================================================
    ("media_sets", "media_set", "abort"): False,
    ("media_sets", "media_set", "calculate"): False,      # execution
    ("media_sets", "media_set", "clear"): False,
    ("media_sets", "media_set", "commit"): False,
    ("media_sets", "media_set", "create"): False,
    ("media_sets", "media_set", "get"): True,
    ("media_sets", "media_set", "get_result"): False,     # data content (computation result)
    ("media_sets", "media_set", "get_rid_by_path"): True,
    ("media_sets", "media_set", "get_status"): True,     # operational status descriptor
    ("media_sets", "media_set", "info"): True,
    ("media_sets", "media_set", "metadata"): True,
    ("media_sets", "media_set", "read"): False,           # binary content
    ("media_sets", "media_set", "read_original"): False,  # binary content
    ("media_sets", "media_set", "reference"): False,      # creates reference (write)
    ("media_sets", "media_set", "register"): False,
    ("media_sets", "media_set", "retrieve"): False,       # data retrieval
    ("media_sets", "media_set", "transform"): False,      # execution
    ("media_sets", "media_set", "upload"): False,
    ("media_sets", "media_set", "upload_media"): False,

    # =========================================================
    # MODELS namespace
    # =========================================================
    ("models", "experiment", "get"): True,
    ("models", "experiment", "search"): True,
    ("models", "experiment_artifact_table", "json"): False,    # data content
    ("models", "experiment_artifact_table", "parquet"): False,  # data content
    ("models", "experiment_series", "json"): False,            # data content
    ("models", "experiment_series", "parquet"): False,         # data content
    ("models", "live_deployment", "transform_json"): False,    # execution
    ("models", "model", "create"): False,
    ("models", "model", "get"): True,
    ("models", "model", "promote_version"): False,             # write
    ("models", "model_studio", "create"): False,
    ("models", "model_studio", "get"): True,
    ("models", "model_studio", "launch"): False,               # execution
    ("models", "model_studio_config_version", "create"): False,
    ("models", "model_studio_config_version", "get"): True,
    ("models", "model_studio_config_version", "latest"): True,
    ("models", "model_studio_config_version", "list"): True,
    ("models", "model_studio_run", "list"): True,
    ("models", "model_studio_trainer", "get"): True,
    ("models", "model_studio_trainer", "list"): True,
    ("models", "model_version", "create"): False,
    ("models", "model_version", "get"): True,
    ("models", "model_version", "list"): True,

    # =========================================================
    # ONTOLOGIES namespace
    # =========================================================
    ("ontologies", "action", "apply"): False,              # write/execution
    ("ontologies", "action", "apply_batch"): False,
    ("ontologies", "action", "apply_with_overrides"): False,
    ("ontologies", "action_type", "get"): True,
    ("ontologies", "action_type", "get_by_rid"): True,
    ("ontologies", "action_type", "get_by_rid_batch"): True,
    ("ontologies", "action_type", "list"): True,
    ("ontologies", "action_type_full_metadata", "get"): True,
    ("ontologies", "action_type_full_metadata", "list"): True,
    ("ontologies", "attachment", "get"): True,             # attachment descriptor (not content)
    ("ontologies", "attachment", "read"): False,           # binary content
    ("ontologies", "attachment", "upload"): False,
    ("ontologies", "attachment", "upload_with_rid"): False,
    ("ontologies", "attachment_property", "get_attachment"): True,     # descriptor
    ("ontologies", "attachment_property", "get_attachment_by_rid"): True,
    ("ontologies", "attachment_property", "read_attachment"): False,   # binary content
    ("ontologies", "attachment_property", "read_attachment_by_rid"): False,
    ("ontologies", "cipher_text_property", "decrypt"): False,  # data content
    ("ontologies", "geotemporal_series_property", "get_geotemporal_series_latest_value"): False,
    ("ontologies", "geotemporal_series_property", "stream_geotemporal_series_historic_values"): False,
    ("ontologies", "linked_object", "get_linked_object"): False,     # object instances (data)
    ("ontologies", "linked_object", "list_linked_objects"): False,   # object instances (data)
    ("ontologies", "media_reference_property", "get_media_content"): False,  # binary content
    ("ontologies", "media_reference_property", "get_media_metadata"): True,  # metadata descriptor
    ("ontologies", "media_reference_property", "upload"): False,
    ("ontologies", "object_type", "get"): True,
    ("ontologies", "object_type", "get_by_rid_batch"): True,
    ("ontologies", "object_type", "get_edits_history"): False,      # data history (object instances)
    ("ontologies", "object_type", "get_full_metadata"): True,
    ("ontologies", "object_type", "get_outgoing_link_type"): True,
    ("ontologies", "object_type", "list"): True,
    ("ontologies", "object_type", "list_outgoing_link_types"): True,
    ("ontologies", "ontology", "get"): True,
    ("ontologies", "ontology", "get_full_metadata"): True,
    ("ontologies", "ontology", "list"): True,
    ("ontologies", "ontology", "load_metadata"): True,
    ("ontologies", "ontology_interface", "aggregate"): False,        # data computation
    ("ontologies", "ontology_interface", "get"): True,
    ("ontologies", "ontology_interface", "get_outgoing_interface_link_type"): True,
    ("ontologies", "ontology_interface", "list"): True,
    ("ontologies", "ontology_interface", "list_interface_linked_objects"): False,  # object instances
    ("ontologies", "ontology_interface", "list_objects_for_interface"): False,     # object instances
    ("ontologies", "ontology_interface", "list_outgoing_interface_link_types"): True,
    ("ontologies", "ontology_interface", "search"): False,           # data search
    ("ontologies", "ontology_object", "aggregate"): False,
    ("ontologies", "ontology_object", "count"): False,               # data count
    ("ontologies", "ontology_object", "get"): False,                 # object instance data
    ("ontologies", "ontology_object", "list"): False,                # object instances
    ("ontologies", "ontology_object", "search"): False,
    ("ontologies", "ontology_object_set", "aggregate"): False,
    ("ontologies", "ontology_object_set", "create_temporary"): False,
    ("ontologies", "ontology_object_set", "get"): False,             # object set data
    ("ontologies", "ontology_object_set", "load"): False,
    ("ontologies", "ontology_object_set", "load_links"): False,
    ("ontologies", "ontology_object_set", "load_multiple_object_types"): False,
    ("ontologies", "ontology_object_set", "load_objects_or_interfaces"): False,
    ("ontologies", "ontology_transaction", "post_edits"): False,
    ("ontologies", "ontology_value_type", "get"): True,
    ("ontologies", "ontology_value_type", "list"): True,
    ("ontologies", "query", "execute"): False,
    ("ontologies", "query_type", "get"): True,
    ("ontologies", "query_type", "list"): True,
    ("ontologies", "time_series_property_v2", "get_first_point"): False,
    ("ontologies", "time_series_property_v2", "get_last_point"): False,
    ("ontologies", "time_series_property_v2", "stream_points"): False,
    ("ontologies", "time_series_value_bank_property", "get_latest_value"): False,
    ("ontologies", "time_series_value_bank_property", "stream_values"): False,

    # =========================================================
    # ORCHESTRATION namespace
    # =========================================================
    ("orchestration", "build", "cancel"): False,
    ("orchestration", "build", "create"): False,
    ("orchestration", "build", "get"): True,
    ("orchestration", "build", "get_batch"): True,
    ("orchestration", "build", "jobs"): True,
    ("orchestration", "build", "search"): True,
    ("orchestration", "job", "get"): True,
    ("orchestration", "job", "get_batch"): True,
    ("orchestration", "schedule", "create"): False,
    ("orchestration", "schedule", "delete"): False,
    ("orchestration", "schedule", "get"): True,
    ("orchestration", "schedule", "get_affected_resources"): True,
    ("orchestration", "schedule", "get_batch"): True,
    ("orchestration", "schedule", "pause"): False,
    ("orchestration", "schedule", "replace"): False,
    ("orchestration", "schedule", "run"): False,       # execution
    ("orchestration", "schedule", "runs"): True,       # run history metadata
    ("orchestration", "schedule", "unpause"): False,
    ("orchestration", "schedule_version", "get"): True,
    ("orchestration", "schedule_version", "schedule"): True,

    # =========================================================
    # SQL_QUERIES namespace
    # =========================================================
    ("sql_queries", "sql_query", "cancel"): False,
    ("sql_queries", "sql_query", "execute"): False,     # execution
    ("sql_queries", "sql_query", "execute_ontology"): False,
    ("sql_queries", "sql_query", "get_results"): False, # data content
    ("sql_queries", "sql_query", "get_status"): True,   # status descriptor

    # =========================================================
    # STREAMS namespace
    # =========================================================
    ("streams", "dataset", "create"): False,
    ("streams", "stream", "create"): False,
    ("streams", "stream", "get"): True,
    ("streams", "stream", "get_end_offsets"): True,   # positional metadata
    ("streams", "stream", "get_records"): False,      # data content
    ("streams", "stream", "publish_binary_record"): False,
    ("streams", "stream", "publish_record"): False,
    ("streams", "stream", "publish_records"): False,
    ("streams", "stream", "reset"): False,
    ("streams", "subscriber", "commit_offsets"): False,
    ("streams", "subscriber", "create"): False,
    ("streams", "subscriber", "delete"): False,
    ("streams", "subscriber", "get_read_position"): True,  # positional metadata
    ("streams", "subscriber", "read_records"): False,  # data content
    ("streams", "subscriber", "reset_offsets"): False,

    # =========================================================
    # THIRD_PARTY_APPLICATIONS namespace
    # =========================================================
    ("third_party_applications", "third_party_application", "get"): True,
    ("third_party_applications", "version", "delete"): False,
    ("third_party_applications", "version", "get"): True,
    ("third_party_applications", "version", "list"): True,
    ("third_party_applications", "version", "upload"): False,
    ("third_party_applications", "version", "upload_snapshot"): False,
    ("third_party_applications", "website", "deploy"): False,
    ("third_party_applications", "website", "get"): True,
    ("third_party_applications", "website", "undeploy"): False,

    # =========================================================
    # WIDGETS namespace
    # =========================================================
    ("widgets", "dev_mode_settings", "disable"): False,
    ("widgets", "dev_mode_settings", "enable"): False,
    ("widgets", "dev_mode_settings", "get"): True,
    ("widgets", "dev_mode_settings", "pause"): False,
    ("widgets", "dev_mode_settings", "set_widget_set"): False,
    ("widgets", "dev_mode_settings", "set_widget_set_by_id"): False,
    ("widgets", "release", "delete"): False,
    ("widgets", "release", "get"): True,
    ("widgets", "release", "list"): True,
    ("widgets", "repository", "get"): True,
    ("widgets", "repository", "publish"): False,
    ("widgets", "widget_set", "get"): True,
}

# Count statistics
permitted = sum(1 for v in METADATA_PERMITTED.values() if v)
blocked = sum(1 for v in METADATA_PERMITTED.values() if not v)
unclassified = [op for op in operations if op not in METADATA_PERMITTED]

# Generate output markdown with embedded .env-format block
lines = []
lines.append("# Metadata Allow-List — Tier-3 (METADATA_ONLY) Access Control")
lines.append("")
lines.append("| Field | Value |")
lines.append("|---|---|")
lines.append("| **Document ID** | META-ALLOW-001 |")
lines.append("| **Version** | 1.0.0 |")
lines.append("| **Date** | 2026-04-13 |")
lines.append("| **Author** | Solution Architect |")
lines.append(f"| **Total operations** | {len(operations)} |")
lines.append(f"| **Tier-3 permitted** | {permitted} |")
lines.append(f"| **Tier-3 blocked** | {blocked} |")
lines.append(f"| **Unclassified (defaults to blocked)** | {len(unclassified)} |")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## Overview")
lines.append("")
lines.append("This document classifies every SDK v2 operation for Tier-3 (Metadata-Only) access control.")
lines.append("")
lines.append("**Policy:** Default-deny. Operations not explicitly listed as `true` are blocked in Tier-3.")
lines.append("")
lines.append("**Variable format:** `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_METADATA=true`")
lines.append("")
lines.append("**Review cycle:** Must be reviewed and updated on every `foundry-platform-python` minor release.")
lines.append("")
lines.append("### Classification Criteria")
lines.append("")
lines.append("| Category | Tier-3 Permitted? | Rationale |")
lines.append("|---|---|---|")
lines.append("| Resource descriptors (`get`, `list`) | **Yes** | Structural metadata; needed for navigation |")
lines.append("| Schema / stats (`get_schema`, `get_health_checks`) | **Yes** | Data quality metadata |")
lines.append("| Status descriptors (`get_status`, `runs`) | **Yes** | Operational state metadata |")
lines.append("| Positional metadata (`get_end_offsets`, `get_read_position`) | **Yes** | Stream position metadata |")
lines.append("| File/table content (`read_table`, `file.content`) | **No** | Data content |")
lines.append("| Binary content (`attachment.read`, `media.read`) | **No** | Binary data |")
lines.append("| Function/query execution (`execute`, `apply`) | **No** | Computation/execution |")
lines.append("| Language model calls (`messages`, `embeddings`) | **No** | AI execution |")
lines.append("| AIP session execution (`blocking_continue`) | **No** | AI execution |")
lines.append("| Write operations (`create`, `delete`, `replace`, etc.) | **No** | Write operations |")
lines.append("| Unclassified | **No** | Deny by default |")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## Classification Table")
lines.append("")

current_ns = None
for ns, cls, method in operations:
    if ns != current_ns:
        lines.append(f"### Namespace: `{ns}`")
        lines.append("")
        lines.append("| SDK Path | Tier-3 Status | Reason |")
        lines.append("|---|---|---|")
        current_ns = ns
    
    key = (ns, cls, method)
    if key in METADATA_PERMITTED:
        permitted_val = METADATA_PERMITTED[key]
        status = "PERMITTED" if permitted_val else "BLOCKED"
    else:
        permitted_val = False
        status = "BLOCKED (unclassified)"
    
    lines.append(f"| `{ns}.{cls}.{method}` | {status} | |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## .env-Format Allow-List (Permitted Operations Only)")
lines.append("")
lines.append("Copy the block below into your `.env` file or reference it in your configuration.")
lines.append("Only `true` entries are listed; all others are blocked by default.")
lines.append("")
lines.append("```dotenv")
lines.append(f"# Foundry CLI Metadata Allow-List — {permitted} permitted operations")
lines.append(f"# Generated: 2026-04-13 | Review on every foundry-platform-python minor release")
lines.append(f"# Default: blocked. Only listed operations are permitted in Tier-3 (METADATA_ONLY=true).")
lines.append("")

PREFIX = "FOUNDRY_AGENTIC_CLI_"
current_ns = None
for ns, cls, method in operations:
    key = (ns, cls, method)
    if METADATA_PERMITTED.get(key, False):
        if ns != current_ns:
            if current_ns is not None:
                lines.append("")
            lines.append(f"# --- {ns.upper()} ---")
            current_ns = ns
        var_name = f"{PREFIX}{ns.upper()}_{cls.upper()}_{method.upper()}_METADATA"
        lines.append(f"{var_name}=true")

lines.append("```")
lines.append("")
lines.append("---")
lines.append(f"*META-ALLOW-001 v1.0.0 — Generated 2026-04-13 — Foundry CLI Agentic Toolset*")

print('\n'.join(lines))
