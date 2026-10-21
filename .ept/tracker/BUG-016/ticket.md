---
id: BUG-016
type: bug
title: Ontology skill records contain incorrect input and result guidance
status: Closed
affected_version: pal_found_cli_skills-worktree
created: 2026-10-12
updated: 2026-10-14
priority: Medium
resolution: Done
assignee: project-manager
reporter: qa-engineer
component: ontologies
---

# BUG-016: Ontology skill records contain incorrect input and result guidance

## Description

# Ontology operation records contain incorrect input and result guidance

## Scope

Independent review of 67 `pal-found-ontologies` records against the CLI operation specs and the local Foundry SDK source found these errors in `pal_found_cli_skills/.agents/skills/pal-found-ontologies/references/`.

### Inputs and examples

- `ontology_interface.search`: the example passes `[]` for `augmented_interface_property_types`, `augmented_properties`, and `augmented_shared_property_types`. The SDK requires dictionaries. Use `{}` or valid maps.
- `time_series_property_v2.stream_points`: the record says `--format` selects `JSON` or `ARROW`; the CLI exposes `--stream-format` for that argument. Change the record; keep global output `--format json|toon|auto` distinct.
- `object_type.get_edits_history`: describe `--object-primary-key` as a JSON mapping from property API name to typed value, and add a valid example after BUG-013 fixes CLI decoding.
- `media_reference_property.upload`: remove claims that `--content-type` and `--content-length` set request headers. The CLI ignores these global flags for this operation, and the SDK upload method accepts neither.

### Selectors and preconditions

- `action_type.get`, `.get_by_rid`, `.get_by_rid_batch`: replace shared claim that API name and RID are interchangeable with each method's actual selector.
- `object_type.get`, `.get_by_rid_batch`, `.get_edits_history`, `.get_full_metadata`, `.get_outgoing_link_type`, `.list`, `.list_outgoing_link_types`: replace copied API name/RID/outgoing-link precondition with each method's actual inputs and access requirement.
- `ontology.list`: remove requirement for a requested ontology; this command takes no identifier.

### Results and failures

- `linked_object.get_linked_object`: a missing link raises `LinkedObjectNotFound`; remove suggestion of an empty successful object.
- `ontology_object.get`: remove search/filter JSON and empty-search guidance; this command takes a primary key and returns one object or an error.
- `ontology_interface.get`, `.get_outgoing_interface_link_type`: remove empty-success explanation based on implementing objects; these return nonoptional metadata models. `ontology_interface.list`, `.list_outgoing_interface_link_types` list metadata, so explain empty metadata lists rather than implementing-object matches.
- `attachment_property.get_attachment`, `.get_attachment_by_rid`, `media_reference_property.get_media_metadata`, `geotemporal_series_property.get_geotemporal_series_latest_value`, `time_series_property_v2.get_first_point`, `.get_last_point`, `time_series_value_bank_property.get_latest_value`: remove partial byte-stream failure text from metadata/value operations.
- `action_type.list`, `object_type.list`, `.list_outgoing_link_types`, `ontology.list`, `ontology_value_type.list`, `query_type.list`: remove generic invalid-filter failure text where no filter argument exists. Describe applicable branch, selector, or permission errors.

## Expected

Each record's input shape, runnable example, preconditions, result, and failure text matches the CLI and local SDK. Recheck corrected records independently, with source hashes in `maintainer/feature012-semantic-reviews/pal-found-ontologies.json`.

## Evidence

- CLI: `pal_found_cli_tool/src/pal_found_cli/ontologies/scripts/pal_found_ontologies_cli.py` (`OP_SPECS`, parser, `_invoke`).
- SDK: `.ept/docs/customer_input/foundry-platform-python/foundry_sdk/v2/ontologies/` and `v2/core/models.py`.
- Parser probe: `--format ARROW` exits 2; `--stream-format ARROW` parses.
- Independent source review: `pal_found_cli_skills/maintainer/feature012-semantic-reviews/pal-found-ontologies.json`.

Related: FEATURE-012, WORK-005, BUG-013.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
