Subject: Correction: automatic unblock did not fire for DEVOPS-037/038/046
Created: 2026-10-12T02:32:42
Updated: 2026-10-12T02:32:42
---
## Correction (python-developer)

This question is Closed, but the three devops tickets did **not** return to
their prior status (`New`) as an automatic effect of the closure. Observed
state after `QUESTION-188 -> Closed` (exit 0):

- `DEVOPS-037`: still `Blocked`; `LINK-01900 QUESTION-188 -> DEVOPS-037 Blocks`
  still present.
- `DEVOPS-038`: still `Blocked`; `LINK-01902 QUESTION-188 -> DEVOPS-038 Blocks`
  still present.
- `DEVOPS-046`: still `Blocked`; `LINK-01904 QUESTION-188 -> DEVOPS-046 Blocks`
  still present, plus a second live blocker `QUESTION-189` (addressed to
  tech-lead, status `New`).

The devops automatic rule AT-6 (`this_ticket_reaches_status`, source statuses
Resolved/Canceled/Closed, link_role source, linked_ticket_target_status
`prior_status`) resolves the target status through the devops ticket's saved
`prior_status`. The tickets were moved to `Blocked` by a manual
`update --status Blocked`, so no `prior_status` value is persisted and the
rule has no target to restore; AT-5 (`all_blockers_cleared`) is only evaluated
when the devops ticket itself is next mutated.

Net effect: the content and gate fix is complete, but clearing the block is an
explicit step in the `Blocked` instructions owned by the devops-engineer
(remove each terminal blocker's `Blocks` link, then return the ticket to
`New`). `DEVOPS-046` also remains blocked on `QUESTION-189` independently of
this question.

No devops ticket was modified here.
