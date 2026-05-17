---
id: DESIGN-001
type: design
title: 'DEV-STORY-002: Technical Design — RetryHandler, ErrorSerializer, OutputFormatter,
  LogSetup'
status: New
created: 2026-05-17
updated: 2026-05-17
priority: Critical
assignee: tech-lead
reporter: tech-lead
---

# DESIGN-001: DEV-STORY-002: Technical Design — RetryHandler, ErrorSerializer, OutputFormatter, LogSetup

## Description

Technical design for four components in foundry_cli_common.py:
1. RetryHandler: Exponential backoff with jitter for HTTP 429/503, configurable via RETRY_* env vars, asyncio.wait_for timeout
2. ErrorSerializer: Maps SDK exceptions to exit codes 0-9 per ADR-001, JSON error envelopes to stdout
3. OutputFormatter: Format auto-selection (ADR-004), JSON/TOON dispatch, metadata to stderr
4. LogSetup: NDJSON logging configuration to stderr (ADR-005), log level from env var

Deliverables:
- Complete class/function signatures with type annotations
- Exception mapping table for ErrorSerializer
- Integration points with components from DEV-STORY-001
- Test case specifications for all components
- Performance benchmarks (error serialization <5ms, format selection <10ms, log setup <10ms)


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
