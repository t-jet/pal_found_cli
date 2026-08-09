---
id: DEV-006
type: development
title: Implement foundry-ontologies skill (67 operations)
status: Closed
created: 2026-07-28
updated: 2026-07-28
priority: Critical
assignee: python-developer
reporter: architect
estimated_hours: 24
time_spent_hours: 6.0
---

# DEV-006: Implement foundry-ontologies skill (67 operations)

## Description

Implement the foundry-ontologies skill package and CLI using established namespace patterns and common components. Scope is all 67 canonical ontology operations.

## Acceptance Criteria

- [ ] Exposes all 67 canonical ontology operations through the CLI and skill docs.
- [ ] Implements binary handling for attachment.read, attachment.upload, attachment.upload_with_rid, attachment-property reads, media_reference_property.get_media_content, media_reference_property.upload, and geotemporal/time-series stream operations.
- [ ] Handles pagination consistently for list/search/query operations.
- [ ] Enforces ACL, read-only, and metadata-only behavior for guarded operations.
- [ ] Applies retry behavior through the shared retry layer where supported.
- [ ] Serializes errors consistently through shared error handling.
- [ ] Supports JSON and TOON output modes.
- [ ] Uses B3-only tracing and does not advertise W3C trace propagation.
- [ ] Avoids unrelated namespace changes.

## Related Documentation

See parent story and linked design notes.

## Notes

Acceptance criteria replaced during manager grooming readiness update.
