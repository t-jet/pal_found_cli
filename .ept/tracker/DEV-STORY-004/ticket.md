---
id: DEV-STORY-004
type: dev_story
title: Implement BinaryDownloadHandler, SessionManager, TracingProvider
status: Closed
feature_request: FEATURE-001
epic: EPIC-001
created: 2026-04-13
updated: 2026-07-28
priority: High
resolution: Done
assignee: tech-lead
reporter: architect
story_points: 13
release_notes: Adds BinaryDownloadHandler, SessionManager, and TracingProvider to the common runtime. Extends ConfigLoader and CLI/SDK integration for download limits and paths, binary output cleanup, session purge, and tracing context. Adds focused unit, integration, security, and concurrency coverage while preserving existing defaults and output compatibility; tracing remains disabled by default.
---

# DEV-STORY-004: Implement BinaryDownloadHandler, SessionManager, TracingProvider

## Description

Implement BinaryDownloadHandler, SessionManager, and TracingProvider per SRS/SAD.

## Acceptance Criteria

- [ ] Binary downloads stream without full buffering, use the configured base path and 1,572,864-byte default cap, sanitize names, stay within the UUID directory, persist exact capped bytes, return file_path/file_size/MD5/SHA256/MIME/truncated, emit a structured truncation warning, and clean partial failures.
- [ ] Session state persists as atomic JSON under the configured session path with alias containment and uniqueness, required fields, 7-day UTC expiry cleanup, idempotent purge, corruption and schema errors, no token leakage, and concurrency-safe creation.
- [ ] Tracing is disabled by default; when enabled, it generates valid non-zero W3C trace and span IDs, binds supported SDK context, preserves trace across invocation, resets context on all exits, and does not leak across concurrent or back-to-back calls.
- [ ] ConfigLoader exposes validated download path, session path, and max download bytes.
- [ ] Common exports and integration cover binary output JSON, cleanup on CLI invocation, session purge, and tracing around SDK calls.
- [ ] Focused unit, integration, security, and concurrency tests pass; the full suite and 80% coverage gate pass.

## Related Documentation

- .ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md sections FR-DL, FR-SESSION, and FR-TRACE
- .ept/docs/deliverables/architecture/SAD-001-foundry-cli.md component and sequence sections
- .ept/docs/deliverables/architecture/canonical-env-var-reference.md

## Notes

Implementation was absent at analysis. DESIGN must settle unknown content-length reporting, session alias and corruption policy, supported SDK tracing context, and retry span policy.
