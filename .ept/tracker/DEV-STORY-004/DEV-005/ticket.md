---
id: DEV-005
type: development
title: Implement BinaryDownloadHandler, SessionManager, and TracingProvider
status: Closed
created: 2026-07-27
updated: 2026-07-27
priority: High
assignee: python-developer
reporter: manager
estimated_hours: 20
time_spent_hours: 20
---

# DEV-005: Implement BinaryDownloadHandler, SessionManager, and TracingProvider

## Description

Implement the three common runtime components plus required configuration and CLI/SDK integration.

## Acceptance Criteria

- [x] Binary downloads stream without full buffering, enforce configured path and cap, sanitize names, contain files under UUID directories, return required metadata, warn on truncation, and clean partial failures.
- [x] Session state uses atomic JSON persistence, contained unique aliases, required schema, UTC expiry cleanup, idempotent purge, explicit corruption errors, and concurrency-safe creation.
- [x] Tracing is off by default; enabled tracing uses valid W3C IDs, supported SDK context, invocation continuity, guaranteed reset, and no cross-call leakage.
- [x] ConfigLoader exposes validated download path, session path, and maximum download bytes.
- [x] Common exports and integration cover binary JSON output, CLI cleanup, session purge, and tracing around SDK calls.
- [x] APIs are typed, maintainable, and do not leak secrets.
- [x] Lint and mypy pass.

## Related Documentation

- .ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md
- .ept/docs/deliverables/architecture/SAD-001-foundry-cli.md
- .ept/docs/deliverables/architecture/DESIGN-005-common-components.md
