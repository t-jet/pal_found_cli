---
id: UNITTEST-006
type: unittest
title: Unit test foundry-ontologies skill (67 operations)
status: Closed
created: 2026-07-28
updated: 2026-07-28
priority: Critical
assignee: python-developer
reporter: architect
estimated_hours: 16
time_spent_hours: 3.0
---

# UNITTEST-006: Unit test foundry-ontologies skill (67 operations)

## Description

Add unit tests for parser, operation dispatch, environment flags, guards, formatting, error paths, pagination, binary handling, and tracing for the foundry-ontologies skill. Scope is all 67 canonical ontology operations.

## Acceptance Criteria

- [ ] Tests cover all 67 canonical ontology operations.
- [ ] Tests cover binary handling for attachment.read, attachment.upload, attachment.upload_with_rid, attachment-property reads, media_reference_property.get_media_content, media_reference_property.upload, and geotemporal/time-series stream operations.
- [ ] Tests cover pagination behavior for list/search/query operations.
- [ ] Tests cover ACL, read-only, and metadata-only behavior.
- [ ] Tests cover retry behavior and retry-disabled paths.
- [ ] Tests cover error serialization for expected SDK and CLI failures.
- [ ] Tests cover JSON and TOON output modes.
- [ ] Tests assert B3-only tracing behavior and do not expect W3C trace propagation.
- [ ] Coverage meets project threshold and new-code expectations.

## Related Documentation

See parent story and linked design notes.

## Notes

Acceptance criteria replaced during manager grooming readiness update.
