---
id: BUG-030
type: bug
title: Ontology object-set load drops SDK mapping and page fields
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

# BUG-030: Ontology object-set load drops SDK mapping and page fields

## Description

# Defect
Ontology `_invoke_paginated` normalizes SDK page envelopes to `data` and `next_page_token` only. Three object-set load operations therefore omit server fields that are not available in the CLI result or ADR-005 pagination metadata. `load_multiple_object_types` loses interface-to-object mappings needed to interpret objects scoped to interfaces.

# Affected operations and fields
- ontology_object_set.load: total_count, compute_usage, property_securities.
- ontology_object_set.load_multiple_object_types: total_count, interface_to_object_type_mappings, interface_to_object_type_mappings_v2, compute_usage, property_securities.
- ontology_object_set.load_objects_or_interfaces: total_count, transaction_id.

# Reproduction
Windows, pal_found_cli_tool HEAD bfdee738 with local Ontology pagination fix, installed foundry_sdk 1.101.0. Run `python .ept/tmp/ontology_page_fields_probe.py`. SDK-shaped mocked page for each operation has one data record plus fields above. Each `_invoke_paginated` result is `[ {"id": 1} ]`; stderr pagination helper exposes only pages_fetched, total_items and page_size. None of the server fields survives. No Foundry connection. Local SDK models in `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/ontologies/models.py` define these fields; interface mapping fields are required in the multiple-object-types response.

# Expected and actual
Expected: CLI preserves server metadata needed for result interpretation and requested compute/security/scope values, through a documented output or metadata channel, while retaining bounded pagination. Actual: metadata is silently dropped; skills state only list output. ADR-005 defines stderr separation but does not waive response fields.

# Acceptance criteria
Define a stable representation for per-page SDK fields across batches; include interface mappings, total_count, compute_usage, property_securities, and transaction_id where returned. Preserve list item order, cursor behavior and ADR-005 metadata separation. Correct three skill records and test single/multi-page output. Independent QA verifies no field loss.

# Test reference
TASK-006 Ontology semantic review; BUG-011 pagination fix QA.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
