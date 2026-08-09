---
id: QUESTION-027
type: question
title: Confirm session token, trace propagation, and unknown-size truncation contracts
status: Closed
addressed_to: architect
created: 2026-07-27
updated: 2026-07-27
priority: High
assignee: architect
reporter: tech-lead
time_spent_hours: 1
---

# QUESTION-027: Confirm session token, trace propagation, and unknown-size truncation contracts

## Description

## Description

Confirm three contracts that cannot be settled from installed SDK behavior and current requirements alone.

## Research Done

1. Installed SDK Session has no session_token field.
2. SDK TRACE_ID_VAR, SPAN_ID_VAR, and SAMPLED_VAR emit B3 X-B3-* headers only, while requirements mention W3C and B3.
3. For unknown Content-Length, exact actual size cannot be reported without draining an unbounded stream.

## Decisions Requested

1. Session token: choose a nullable compatibility field (recommended), remove the field, or identify an alternate source.
2. Trace propagation: choose SDK-native B3 for this story (recommended), or require explicit traceparent integration.
3. Unknown-size truncation: approve actual_size as unknown with observed_size greater than the configured limit (recommended), or require draining the stream.

## Acceptance Criteria

- [ ] Architect records one decision for each contract with rationale.
- [ ] Decisions are precise enough to unblock DESIGN-005 and downstream implementation/tests.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
