---
name: work-instructions
description: Provides instructions on how to handle work tickets, including classifying, searching, creating, referencing, and executing tasks according to defined workflows and role responsibilities.
license: Apache-2.0
metadata:
  author: t-jet
  version: "0.1.0"
---

<workflowGuidance>
<Step_0_Ticket_Gate>
This gate applies equally to user requests, assigned tickets, and self-initiated work. Skipping it is a protocol violation.

**No analysis, research, implementation, or response content may be produced until steps 1–4 below are complete.**

1. Use the tracking-system skill to search for an existing ticket matching the request.
  - If multiple matching tickets are found, choose the most relevant one based on context and priority.
2. If no ticket is found, use the tracking-system skill to create one.
3. Mandatory: use the tracking-system skill to retrieve full ticket details, read supplied instructions, understand DoD criteria for the current status, and strictly follow them.
4. Analyze previous ticket comments, linked tickets and linked documents to understand context, constraints, assumptions, decisions, and progress so far.
5. Only now proceed with the actual work.
</Step_0_Ticket_Gate>
<Acting_on_user_requests>
1. **Classify** — new feature/change → new ticket; related to existing ticket → sub-task or reference.
2. **Search** — use the tracking-system skill to search for matching tickets by keywords.
3. **Create or reference** — if found, create sub-task under it; otherwise create a root-level ticket.
4. **Load instructions** — use the tracking-system skill to retrieve ticket workflow instructions.
5. **Execute status-by-status** — apply the canonical continue and stop conditions in Ticket_execution_rules.
7. **Log all work** with provided grounding evidence in ticket comments (never in separate files).
</Acting_on_user_requests>
<Handling_assigned_tickets>
1. Use the tracking-system skill to list non-terminal tickets assigned to {{tracker_assignee}}.
2. Use the tracking-system skill to list outbound links for each ticket and filter out blocked ones.
3. Prioritize: Critical > High > Medium > Low; within same priority, oldest first.
4. For each ticket, follow steps 4–7 from “Acting on user requests” above.
5. If no specific ticket was mentioned, loop back to step 1 for the next ticket.
</Handling_assigned_tickets>
<Ticket_execution_rules>
While working on a ticket:
- Read the instructions in the instructions session returned by the tracking-system skill using get command for the current ticket.
- Advance one status at a time.
- Ensure that the DoD criteria are met before each transition.
- If DoD criteria are ambiguous or can't be met, do not transition the status; create a QUESTION sub-task per c3_No_Assumptions.
- After completing a status, add a timestamped comment documenting what was done with grounded evidence for the actions taken and decisions made.
- Continue while: you own the actual ticket status, DoD is met, not blocked, not terminal.
- Stop when: terminal status reached, next status is another role’s or blocked.
</Ticket_execution_rules>
</workflowGuidance>

<toolUseInstructions>
<constraints>
<c1_Tracking_System_Skill_Rule>
All ticket, link, comment, and workflow operations must use the tracking-system skill and its documented CLI. Before every command, validate its syntax against the skill reference; use the terminal exit code as the result; and never read or modify internal `.ept/tracker/` storage directly. If the exit code indicates failure, do not proceed with the assumed result; retry once, and if it fails again, create a QUESTION sub-task or log the error in a ticket comment.
</c1_Tracking_System_Skill_Rule>
<c2_No_Documentation_Files>
Work notes, progress, decisions, plans, summaries, and completion reports go into **ticket comments only** — never into separate files. The only files you may create are stakeholder deliverables explicitly listed in a ticket’s Acceptance Criteria and stored under `.ept/docs/deliverables/`.

All ticket comments must be written in **Markdown format** (headings, lists, code blocks, bold/italic as appropriate, strictly following markdown syntax standards).

Before creating any file, ask: *"Is this a deliverable or documentation?"* If documentation → use a ticket comment.

Allowed deliverable types: SADs, ADRs, Technical Specifications, Requirements Documents, API Documentation, Design Documents, Implementation Plans, User Guides, Deployment Guides, RFPs and RFP Responses.
</c2_No_Documentation_Files>
<c3_No_Assumptions>
When requirements, specifications, or context are unclear, create a QUESTION sub-task addressed to the appropriate role (see “Finding Responsible Persons” below). Do not guess.
</c3_No_Assumptions>
<c4_Consult_Documentation_First>
Before making decisions, consult `.ept/docs/document_index.md` and relevant linked documents. Keep that index up to date when deliverables change.
</c4_Consult_Documentation_First>
<c5_Constraint_Policy_Change_Impact>
When a ticket introduces or modifies constraints, policies, or architectural decisions:
- Update all affected documentation.
- Use the tracking-system skill to search the tracker for impacted tickets.
- For completed tickets: create remediation tickets and link them.
- For in-progress/not-started tickets: add comments or `RelatesTo` links.
</c5_Constraint_Policy_Change_Impact>
</constraints>
<Finding_Responsible_Persons>
When you need to find colleagues or the appropriate responsible person for a QUESTION sub-task, consult `.ept/resources/available_resources.md` to identify the correct person or role to address the question to.
If you cannot determine the appropriate person or role from the available resources, escalate the question to the project owner.
</Finding_Responsible_Persons>
</toolUseInstructions>
