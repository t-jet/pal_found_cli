---
id: BUG-023
type: bug
title: Ontology CLI accepts missing SDK-required inputs across 18 operations
status: Closed
affected_version: pal_found_cli_tool-bfdee738-dirty
created: 2026-10-13
updated: 2026-10-14
priority: High
resolution: Done
assignee: python-developer
reporter: qa-engineer
component: ontologies
---

# Defect
CLI parser presents SDK-required inputs as optional. Omitting them parses successfully, then the SDK call raises TypeError before network. Current offline records also call these flags optional. Source inventory has 20 operations. Two attachment uploads handle required values in CLI: `_invoke` infers content_length, defaults content_type, and rejects missing filename with a clear ValueError; the remaining 18 lack equivalent validation or defaults.

# Reproduction
Windows, foundry_sdk 1.101.0, pal_found_cli_tool HEAD bfdee738 plus local edits. Run `python .ept/tmp/ontology_missing_args_probe.py`. It parses `query execute palantir myQuery`, then `_invoke` against the installed SDK signature reports `parsed=YES; sdk_call_attempts=1; error=missing a required argument: parameters`. No Foundry connection.

# Affected 18 operations and required keywords
- action.apply: parameters
- action.apply_batch: requests
- action.apply_with_overrides: overrides, request
- action_type.get_by_rid_batch: requests
- object_type.get_by_rid_batch: requests
- ontology.load_metadata: action_types, interface_types, link_types, object_types, query_types
- ontology_interface.aggregate: aggregation, group_by
- ontology_interface.search: augmented_interface_property_types, augmented_properties, augmented_shared_property_types, other_interface_types, selected_interface_property_types, selected_object_types, selected_shared_property_types
- ontology_object.aggregate: aggregation, group_by
- ontology_object.search: select
- ontology_object_set.aggregate: aggregation, group_by, object_set
- ontology_object_set.create_temporary: object_set
- ontology_object_set.load: object_set, select
- ontology_object_set.load_links: links, object_set
- ontology_object_set.load_multiple_object_types: object_set, select
- ontology_object_set.load_objects_or_interfaces: object_set, select
- ontology_transaction.post_edits: edits
- query.execute: parameters

# Expected and actual
Expected: CLI help and skill identify SDK-required inputs; incomplete commands fail before SDK invocation with exit 1 or receive documented valid defaults. Actual: parser accepts incomplete commands and SDK signature fails at call time.

# Acceptance criteria
Reconcile requiredness for all 18 operations, retain attachment upload validation/inference, and test representative JSON object/list inputs plus an empty parameter map for a query. Correct offline records and semantic review; independent QA verifies behavior and exit taxonomy.

# Test reference
TASK-006 independent 67-operation Ontology semantic audit; BUG-011/013/017 QA continuation.
