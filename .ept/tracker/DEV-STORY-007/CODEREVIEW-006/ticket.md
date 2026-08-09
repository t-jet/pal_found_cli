---
id: CODEREVIEW-006
type: codereview
title: Code review foundry-ontologies implementation
status: Closed
created: 2026-07-28
updated: 2026-07-28
priority: Critical
assignee: tech-lead
reporter: architect
estimated_hours: 6
---

# CODEREVIEW-006: Code review foundry-ontologies implementation

## Description

Review DEV-006 output for maintainability, SDK usage, security, access controls, error handling, tests, and trace behavior. Review scope is all 67 canonical ontology operations.

## Acceptance Criteria

- [ ] Review verifies all 67 canonical ontology operations are implemented and documented.
- [ ] Review verifies binary handling for attachment.read, attachment.upload, attachment.upload_with_rid, attachment-property reads, media_reference_property.get_media_content, media_reference_property.upload, and geotemporal/time-series stream operations.
- [ ] Review verifies pagination behavior for list/search/query operations.
- [ ] Review verifies ACL, read-only, and metadata-only behavior.
- [ ] Review verifies retry behavior and retry-disabled behavior.
- [ ] Review verifies error serialization for expected SDK and CLI failures.
- [ ] Review verifies JSON and TOON output modes.
- [ ] Review verifies B3-only tracing and flags any W3C trace propagation claims as incorrect.
- [ ] Review findings cite specific files and line numbers before approval.
- [ ] DEV-006 is not accepted until critical and high severity issues are resolved.

## Related Documentation

See parent story, DEV-006, and linked design notes.

## Notes

Acceptance criteria replaced during manager grooming readiness update.
