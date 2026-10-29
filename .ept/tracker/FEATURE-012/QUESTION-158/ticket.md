---
id: QUESTION-158
type: question
title: Allow analysis counterpart to be Resolved or Closed
status: Closed
addressed_to: project-owner
created: 2026-10-03
updated: 2026-10-03
priority: Medium
assignee: project-manager
reporter: project-manager
time_spent_hours: 0.1
---

# Correct the analysis closure status gate

## Question

The revised SA-ANA closure Definition of Done requires the related BA-ANA ticket to be in the Resolved status. BA-ANA-013 met that condition when both analyses were Resolved, and then closed under its revised rule. BA-ANA-013 is now Closed, so SA-ANA-013 cannot satisfy the current wording. Please change both BA-ANA and SA-ANA closure gates to accept a counterpart in Resolved or Closed (or explicitly state that having reached Resolved satisfies the gate), and align their Resolved-state instructions. Then confirm the correction so SA-ANA-013 can close.

## Research Done

The current `get SA-ANA-013` output requires BA-ANA in Resolved status, while `get BA-ANA-013` shows Closed. The revised `get BA-ANA-013` gate allowed its closure while SA-ANA-013 was Resolved. The tracker CLI has no workflow-edit command; its `workflow` command only inspects types, statuses, and transitions. QUESTION-157 was canceled after the first correction; this remaining serial-state conflict became visible after BA closure.

## Acceptance criteria

The Project Owner confirms wording that permits SA-ANA-013 to close when BA-ANA-013 is Closed, with all approvals remaining required.
