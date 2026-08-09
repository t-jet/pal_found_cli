---
id: DEV-STORY-003
type: dev_story
title: Implement AccessControlGuard, PaginationHelper
status: Closed
feature_request: FEATURE-001
epic: EPIC-001
created: 2026-04-13
updated: 2026-07-26
priority: Critical
resolution: Done
assignee: architect
reporter: architect
story_points: 8
release_notes: 'AccessControlGuard and PaginationHelper shared infrastructure: enforce SRS/SAD access-control
  precedence, metadata-only/read-only tiers, metadata allow-list behavior, pagination
  controls, page-token metadata, and batched page aggregation for namespace skills.'
---

# DEV-STORY-003: Implement AccessControlGuard, PaginationHelper

## Description

AccessControlGuard and PaginationHelper shared infrastructure completed for namespace skills. AccessControlGuard implements the SRS/SAD access-control precedence model, read-only and metadata-only tiers, operation-level override behavior, metadata allow-list handling, and structured AccessControlError output. PaginationHelper implements first-page defaults, page-token metadata, batch page aggregation, and configured page-size limits.

## Acceptance Criteria

### AccessControlGuard (FR-ACL: Three-Tier Access Model)

- [x] Implements the 8-step precedence model from SRS-001 FR-ACL-5: ENABLED check (op -> namespace), READONLY override (op -> namespace), global READONLY, METADATA_ONLY override (namespace), global METADATA_ONLY, default full access. First matching rule wins.
- [x] Enforces three access tiers per SRS-001 FR-ACL-1: full, read-only, and metadata-only.
- [x] Read-only tier blocks write operations and permits read operations.
- [x] Metadata-only tier blocks data content reads and writes, allowing metadata reads only.
- [x] METADATA_ONLY implies READONLY, so writes are blocked.
- [x] Metadata allow-list uses deny-by-default behavior for unclassified operations.
- [x] Raises AccessControlError with exit code 8 and structured JSON error envelope on blocked operations.
- [x] Supports per-operation READONLY independence from namespace-level controls.
- [x] Acceptance test covers the SRS FR-ACL-5 per-operation write override example.

### PaginationHelper (FR-PAG: Pagination)

- [x] Exposes page-size, page-token, and batch-pages parser behavior for paginated operations.
- [x] Defaults to first-page behavior and configured default page size.
- [x] Emits next page token metadata to stderr using the ADR-005 metadata separator.
- [x] Retrieves and aggregates up to the configured batch page limit.
- [x] Enforces max batch pages from configuration.
- [x] Coordinates with OutputFormatter for page aggregation.

### Non-Functional

- [x] Components implemented as typed Python classes in shared common infrastructure.
- [x] Unit and focused verification coverage passed above the required threshold.
- [x] Integration tests exercise access-control precedence and pagination behavior.

## Related Documentation

- .ept/docs/deliverables/architecture/SAD-001-foundry-cli.md
- .ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md
- .ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md
- .ept/docs/deliverables/architecture/adr/ADR-005-log-format.md
- .ept/docs/deliverables/architecture/adr/ADR-007-operation-level-readonly.md
- .ept/docs/deliverables/architecture/canonical-env-var-reference.md
- .ept/docs/deliverables/architecture/metadata-allow-list.md
- tests/test_access_control_guard.py
- tests/test_pagination_helper.py

## Notes

Deployment readiness verified: all DEV-STORY-003 child tickets are Closed; no DEVOPS child exists; QA children are Closed; deployment validation evidence is recorded; no unresolved defects are listed under the story.
