---
id: DEV-004
type: development
title: Implement AccessControlGuard and PaginationHelper behavior
status: New
created: 2026-07-22
updated: 2026-07-22
priority: Critical
assignee: python-developer
reporter: architect
estimated_hours: 8
---

## Scope
Implement shared ACL and pagination behavior for DEV-STORY-003.

Target areas: AccessControlGuard, PaginationHelper, canonical metadata allow-list loading, and CLI integration points that need guard checks or pagination flags.

## Acceptance criteria
- Enforce ACL precedence from SRS-001 FR-ACL and ADR-007, including ENABLED=false precedence and operation or namespace READONLY=false overrides.
- Treat METADATA_ONLY=true as read-only plus content-read restriction; block writes and data content reads unless the operation is metadata-allowed.
- Raise AccessControlError with exit code 8 per ADR-001 and structured error data that identifies the blocking rule.
- Parse metadata-allow-list.md by accepting only canonical backticked SDK paths marked PERMITTED; deny unclassified operations by default.
- Ensure no SDK call or side effect happens after AccessControlGuard blocks a request.
- Add --page-size, --page-token, and --batch-pages to every paginated CLI operation.
- Aggregate up to the configured batch limit, enforce the max batch cap, propagate SDK page tokens, and emit pagination metadata to stderr after # ---metadata-start--- per ADR-005.
- Report null/no next token when the SDK has no further page.
