---
id: BUG-043
type: bug
title: Functions streaming-execute decodes SDK SSE context manager before opening HTTP stream
status: Closed
affected_version: 2feb1fed64406ddc987d036ce7ae667d3bd11d9d
created: 2026-10-21
updated: 2026-10-21
priority: High
resolution: Done
assignee: python-developer
reporter: qa-engineer
component: functions-cli
fix_version: ddfab5d13bd01a1f244a4446cd10764c9091f65a
---

# BUG-043: Functions streaming-execute decodes SDK SSE context manager before opening HTTP stream

## Description

## Observed defect
Functions query streaming-execute is unusable with the frozen SDK 1.101.0 at tool revision 2feb1fed64406ddc987d036ce7ae667d3bd11d9d. The real SDK method returns AsyncSseContextManager. The CLI treats that object as decoded byte content and raises AttributeError before opening the HTTP stream. Root reports the CLI maps this failure to exit 9.

## Reproduction and evidence
Independent reviewer /root/remaining_admin_audit_pages recorded .ept/tmp/feature015_functions_probe_results.json. Invoke pal-found-functions query streaming-execute exampleQuery --parameters '{"limit":10}' with synthetic configuration, permitted local access controls and actual SDK request capture. The probe records actual_return_class=AsyncSseContextManager, requests_before_decode=0 and AttributeError: 'AsyncSseContextManager' object has no attribute 'decode'. Correct manual SDK context consumption subsequently captures POST /api/v2/functions/queries/exampleQuery/streamingExecute, Accept text/event-stream, parameters body and typed data/error events. That later capture is not evidence that the broken CLI reached HTTP transport. No live Foundry tenant or production mutation was used.
Frozen SDK query.py SHA256 5242d695ca2cc7ae2ea0afccc814bece3f3d77bea98a5c11beb53ec2e4dedcde matches the REST review oracle.

## Root cause and expected behavior
src/pal_found_cli/functions/scripts/pal_found_functions_cli.py _invoke returns the context manager unchanged because _resolve_result handles awaitables only. main calls result.decode("utf-8") on that manager. Expected: correctly open, consume and close the SDK asynchronous SSE context, preserve supported data/error event content and established CLI error/timeout/access-control contracts. The current bytes assumption prevents every otherwise permitted streaming-execute invocation from consuming its response.

## Requirements and ownership
DEV-STORY-008 AC-1 exposes streaming_execute, AC-5 requires retry/timeout/error handling, and AC-8 requires correct SDK dispatch and deterministic exit behavior. DEV-STORY-070 requires preserved CLI operations and explicitly blocks integration acceptance on essential FEATURE-012 CLI defects. BA-DES-015 BD-015-09/11/12 governs affected guidance acceptance. Relate archived FEATURE-012 ownership and original DEV-STORY-008 without reopening or editing them; block DEV-STORY-070 acceptance until the corrected tool and affected guide are independently reviewed.

## Evidence boundary
Prior DEV-STORY-085 request serialization PASS and frozen REST contract evidence remain scoped to request construction. They did not prove real SSE response consumption or whole-page CLI acceptance. This newly confirmed SDK-return-contract defect is separate from BUG-021 attribution handling and BUG-036 through BUG-042 shared fixes. No historical formal TESTCASE/TESTEXEC-085 result is reopened or recast as failed execution.

## Acceptance criteria
- Consume the real SDK AsyncSseContextManager, enter and close its context, and preserve ordered supported data/error events without decoding the manager as bytes.
- Independent mocked-transport tests reproduce failing 2feb behavior and prove corrected end-to-end CLI response consumption with actual SDK SSE types; verify empty stream, multiple events, data/error content and resource closure.
- Preserve access checks before execution, attribution, timeout/cancellation, established failure mapping and non-streaming operations; document any bounded retry behavior without duplicating emitted events.
- Record exact corrected source, code review and independent QA, retest affected Functions guidance, and pass required CI before resolving the bug.

## Current work
Implementation is assigned to python-developer; /root/ci_parser_annotation_fix is preparing the source and tests. Fix and independent acceptance are pending. No completion claim.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
