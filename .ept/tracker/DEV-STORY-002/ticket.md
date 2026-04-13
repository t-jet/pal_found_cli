---
id: DEV-STORY-002
type: dev_story
title: Implement RetryHandler, ErrorSerializer, OutputFormatter, LogSetup
status: New
feature_request: FEATURE-001
epic: EPIC-001
created: 2026-04-13
updated: 2026-04-13
priority: Critical
assignee: architect
reporter: architect
---

# DEV-STORY-002: Implement RetryHandler, ErrorSerializer, OutputFormatter, LogSetup

## Description

RetryHandler: exponential back-off with jitter; configurable max attempts via env var. ErrorSerializer: maps SDK exceptions to structured JSON error envelopes on stdout + typed exit code (ADR-001). OutputFormatter: auto-selects TOON vs JSON (ADR-004); writes to stdout. LogSetup: structured JSON logging to stderr (ADR-005).

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
