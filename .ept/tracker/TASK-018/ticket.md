---
id: TASK-018
type: task
title: Refresh FEATURE-015 combined draft and publication status
status: Closed
priority: High
assignee: project-manager
reporter: project-manager
created: 2026-11-16
updated: 2026-11-17
---

# Refresh FEATURE-015 combined draft and publication status

## Scope
Reconcile reviewed release, tracker-data and agent-configuration branches into parent draft PR 6. Preserve current main, historical repairs and unrelated live edits. Feature release acceptance remains separate.

## Acceptance criteria and deliverables
- Verify forward paired skills/tool pins, exact published source CI and preserved branch histories.
- Refresh existing .ept/docs/deliverables/qa/FEATURE-015-draft-release-status-2026-10-18.md with current remote revisions, actual QA counts and remaining workflow gates; update document_index.md where affected.
- Integrate a freshly independently verified tracker capture and published configuration notes.
- Validate changed local links, exact candidate diff and clean isolated branch; push normal history and verify remote PR/ref.
- Record commits, remote verification and limitations in ticket comments. No feature main merge or feature closure.

## References
FEATURE-015; TASK-014; TASK-016; TASK-017; DEVOPS-047; .ept/docs/document_index.md; SA-DES-014 verification-and-delivery.
