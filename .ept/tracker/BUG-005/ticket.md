---
id: BUG-005
type: bug
title: Preserve tracker comments during same-second writes
status: Open
affected_version: current-workspace-tracker
created: 2026-10-06
updated: 2026-10-06
priority: High
assignee: tech-lead
reporter: project-manager
component: tracker
---

# BUG-005: Preserve tracker comments during same-second writes

## Description

# Tracker comments overwrite evidence within the same second

## Observed defect
Tracker CLI writes by the same author on one ticket within the same second reuse a timestamp-based comment identity. A subsequent field or status update can replace the previously written substantive approval comment with an automatic update comment.

## Environment and affected version
Current workspace tracker CLI, observed 2026-10-06 in PowerShell on Windows. Exact tracker release is not declared; affected version is the current workspace implementation.

## Reproduction evidence
QUESTION-185 reviewer reported approval comment 20261006-162954-tech-lead, then updated status within the same second. CLI comment retrieval later showed only the automatic update; no durable written approval remained. QUESTION-183 exhibited the same issue and was corrected before closure. Do not reproduce destructively on approval tickets; a future fix must use an isolated tracker fixture.

## Expected behavior
Each substantive and automatic comment has a unique stable identity. Field and status writes must preserve earlier approval evidence, including when the same author performs multiple writes within one second.

## Actual behavior
Earlier comment evidence can be silently replaced. CLI exit success does not establish preservation.

## Acceptance criteria
- Distinct comment identities preserve all same-author writes made within one second.
- Existing comment references remain valid and supported CLI behavior is preserved.
- Tests cover substantive comment followed by field/status update, multiple comments, and concurrent writers against isolated storage.
- Independent QA verifies no overwrite, with durable readback evidence.

## Workaround and scope
Serialize writes with at least one second between writes to the same ticket by the same author. Read back substantive evidence after subsequent status updates. Put approval answers in ticket bodies when needed for recovery. Keep Closed archives unchanged and recover missing approval through a new QUESTION. No tracker implementation is part of FEATURE-015 design revision.

## Related tickets
FEATURE-015, QUESTION-183, QUESTION-185, QUESTION-186. QUESTION-186 records recovered durable approval.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
