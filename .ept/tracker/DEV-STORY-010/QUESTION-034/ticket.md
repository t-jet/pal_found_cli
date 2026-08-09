---
id: QUESTION-034
type: question
title: Clarify outbound B3/W3C propagation scope for DEV-STORY-010
status: Closed
addressed_to: architect
created: 2026-07-30
updated: 2026-08-01
priority: High
assignee: architect
reporter: architect
time_spent_hours: 0.15
---

# QUESTION-034: Clarify outbound B3/W3C propagation scope for DEV-STORY-010

## Description

# Question

Should DEV-STORY-010 require TracingProvider to inject and forward B3/W3C headers on outbound Foundry SDK calls, as required by SRS FR-TRACE-3 and DESIGN-005, or is tracing limited to structured-log correlation? If tracing is limited to logs, please approve that scope exception.

## Context

Ticket Technical Scope names TracingProvider; AC-9 currently associates B3/W3C headers with NDJSON stderr logs; Analysis comments/release_notes do not define outbound propagation.

## Research Done

Reviewed DEV-STORY-010 Technical Scope, AC-9, Analysis evidence comments, release_notes, SRS FR-TRACE-3, and DESIGN-005. The ticket names TracingProvider and B3/W3C headers but does not unambiguously state whether headers are injected and forwarded on outbound Foundry SDK calls.

## Answer

DEV-STORY-010 must propagate outbound SDK-native B3; tracing is not log-only. Enter `AsyncClientFactory.invocation_scope(cfg)` before constructing `AsyncFoundryClient` and keep the scope active through all retry attempts. Every outbound request must carry `X-B3-TraceId`, `X-B3-SpanId`, and `X-B3-Sampled`, and retries must reuse the same B3 context. Restore prior SDK context values when the invocation completes or fails. W3C `traceparent` and `tracestate` are out of scope. Replace AC-9 with B3-only requirements and add transport-level header tests. No scope exception is approved or required.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
