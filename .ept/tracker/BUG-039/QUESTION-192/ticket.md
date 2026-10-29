---
id: QUESTION-192
type: question
title: Clarify shared timeout precedence and total attempt bounds while preserving approved defaults
status: Closed
addressed_to: architect
created: 2026-10-20
updated: 2026-10-20
priority: High
assignee: architect
reporter: project-manager
time_spent_hours: 0.25
---

# QUESTION-192: Clarify shared timeout precedence and total attempt bounds while preserving approved defaults

## Description

## Decision requested
Reconcile shared timeout/count semantics for BUG-039 and BUG-040 before implementation. Keep approved DEV-STORY-008 AC-5 default four total calls; this question requests implementation interpretation and edge cases, not permission to waive that AC.

## Evidence
Tool0963: filesystem CLI:598 passes --timeout or ConfigLoader.timeout_s to SDK request_timeout; :599 constructs RetryHandler() using env directly. RetryHandler:345-347 does not apply ADR-002 range1..3600; :440 loops range(max_retries+1). ConfigLoader:280-289 clamps env timeout. SRS FR-ASYNC-3 requires wait_for, which exists. Closed BUG-SUB-001/QUESTION-023 concern absent wrapper and are not reopened. TESTCASE-003:62 explicitly names --timeout precedence. SRS:422 says maximum retry attempts and OI-3 says4 attempts, while DEV-STORY-008:72 says4 total. Default current code makes5 calls.

## Bounded questions
1. Confirm --timeout precedence for both SDK request_timeout and outer wait_for, including streams-specific configuration, valid bounds and invalid/nonpositive CLI/environment inputs. If layers intentionally differ, cite approved requirement and define observable operation behavior.
2. Confirm canonical MAX_ATTEMPTS denotes total calls, default4, consistent with DEV-STORY-008; define minimum/zero/negative/invalid inputs and max_retries backward compatibility without silently changing public semantics. Identify any approved later decision that supersedes cited AC.

## Acceptance criteria
Architect records precise configuration precedence, range and count rules, cites governing requirements and resolves conflicting wording. Tech Lead can derive positive/adverse regression oracles from decision. BA verifies original accepted business AC remains preserved; requirement change needs its owning approval workflow. No code, release waiver or invented platform evidence requested.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
