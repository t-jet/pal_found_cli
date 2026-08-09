---
id: TESTCASE-010
type: testcase
title: Design Foundry Audit CLI QA cases
status: Closed
created: 2026-08-01
updated: 2026-08-01
priority: High
assignee: qa-engineer
reporter: qa-engineer
estimated_hours: 4
time_spent_hours: 0.25
---

# TESTCASE-010: Design Foundry Audit CLI QA cases

## Description

Create traceable cases from the DEV-STORY-010 acceptance criteria and DESIGN-010.

## Acceptance Criteria

- Cases cover both operations and every DESIGN-010 QA scenario.
- Every case defines inputs, expected stdout and stderr, exit code, prerequisites, and cleanup.
- Capture outbound SDK requests and assert that tracing-enabled calls contain valid `X-B3-TraceId`, `X-B3-SpanId`, and `X-B3-Sampled` headers.
- Assert that tracing-disabled calls generate no B3 headers.
- Assert that every retry attempt uses the same B3 header values.
- Assert that prior SDK context is restored after both successful and failed invocations.
- Assert that neither `traceparent` nor `tracestate` is emitted or claimed.
- Assert that ACL denial leaves prior SDK context unchanged and occurs before client or filesystem work.
- Cover the explicit 40-page cap and verify pagination counters reset before a retry.
- Cover stream failure and cancellation cleanup, including response closure and removal of unpublished temporary or partial files.
- Cover unsafe output filenames and contained-path enforcement.
- Verify success, metadata, diagnostics, and error data remain on their required stdout or stderr streams.
- Verify authentication failures and configuration failures use their separate ADR-001 exit codes and envelopes.

## Related Documentation

- `.ept/docs/deliverables/architecture/DESIGN-010-audit-cli.md`
- `DEV-STORY-010`

## Notes

QA case-design estimate: 4 hours. TESTEXEC-010 waits for approved cases.
