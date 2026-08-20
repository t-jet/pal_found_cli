---
id: BUG-SUB-016
type: bug_subtask
title: PowerShell skill-copy instructions silently copy zero folders
status: Closed
created: 2026-08-17
updated: 2026-08-17
priority: High
assignee: python-developer
reporter: python-developer
time_spent_hours: 0.62
---

# BUG-SUB-016: PowerShell skill-copy instructions silently copy zero folders

## Description

## Description

The public skills README at commit b961b2186ad2c8c98f67ab98d708beff6c944281, lines 41-52, documents a PowerShell skill-copy flow that exits successfully but copies no skill folders. The command enumerates the repository root instead of .agents/skills and uses a POSIX-style backslash continuation that is not valid for this PowerShell flow.

## Steps to reproduce

1. Clone the public skills repository without credentials and check out b961b2186ad2c8c98f67ab98d708beff6c944281.
2. Change directory to the repository root as documented.
3. Run the literal PowerShell command from README lines 41-52.
4. Count copied skill folders in the documented destination.

## Expected behavior

The documented Windows flow copies all 19 skill folders, or stops with a clear error before reporting success.

## Actual behavior

The command exits successfully and copies 0 folders. A corrected control that enumerates .agents/skills copies 19 folders.

## Environment

Windows NT 10.0.26200; PowerShell 7.6.5; Git 2.54; public skills commit b961b2186ad2c8c98f67ab98d708beff6c944281. QA window: 2026-08-17 15:02:48-15:13:40 +03:00.

## Acceptance criteria

- [ ] Correct the documented PowerShell command and related distribution documentation.
- [ ] Add an executable regression test proving the literal Windows flow copies 19 skill folders and fails loudly on an invalid source.
- [ ] Keep the documented target paths consistent with the supported harnesses.
- [ ] Run the focused documentation/distribution checks and record results.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
