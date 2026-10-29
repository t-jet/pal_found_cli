---
id: BUG-SUB-021
type: bug_subtask
title: REST guide paging example repeats token without request bound
status: Closed
created: 2026-10-05
updated: 2026-10-05
priority: Medium
assignee: python-developer
reporter: qa-engineer
estimated_hours: 1
time_spent_hours: 0.5
---

# BUG-SUB-021: REST guide paging example repeats token without request bound

## Description

## Reproduction
Extract first Python fenced example from pal_found_cli_skills/.agents/skills/pal-found-dev/references/rest-api.md. Set required environment variables and monkeypatch requests.get to return data=[] and nextPageToken=repeat on every call, raising RuntimeError after four responses. Execute the exact snippet. It makes five requests with page tokens [None, repeat, repeat, repeat, repeat] until the test safety stop.

## Expected
REST-TC-04 requires malformed or repeating page tokens and empty pages not to loop forever. Example must bound request count and/or detect repeated tokens while preserving normal pagination.

## Actual
Loop bounds only seen object count. Empty repeated-token pages never increment seen and never end.

## Environment
Windows PowerShell, Python 3, requests, local workspace 2026-10-05; mocked HTTP only; no credentials or live write. Found during TESTEXEC-059.

## Fix
Add explicit request bound or repeated-token detection, document client work limit, and test normal and malformed sequences. Severity Medium; affected local revision 45bc51d plus uncommitted FEATURE-013 work.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
