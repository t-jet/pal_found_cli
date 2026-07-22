# Architect Improvement Memory

## Improvement History

## Improvement: tracker CLI comment syntax

Condition:
- When adding a comment via `.ept/skills/tracking-system/tracker/tracker_cli.py`

Action:
- Do use the `comment create` subcommand (not `comment <ticket_id>`); required flags are `--subject` and `--text`. The `update` command uses `--status`/`--author`, but comments need the nested `create` verb. For long markdown bodies, write to a temp file and pass `--text "$(cat file)"` to avoid shell-escaping issues, then delete the temp file.

## Improvement: exhaust all ADRs before claiming a requirement is absent

Condition:
- When deciding an AC-vs-implementation conflict and justifying the decision with "the requirement is not in any upstream contract"

Action:
- Do grep/read ALL relevant ADRs (not just the SRS and the directly-named ADR) for the keyword before making the absence claim. ADRs cross-reference each other and a decision clause in a sibling ADR (e.g. ADR-005 §Consequences) can mandate the very behavior under dispute. List the ADRs actually consulted in the decision comment so the reviewer can verify coverage.

## Improvement: post a visible correction when a prior decision was wrong

Condition:
- When a prior decision comment is discovered to be based on incomplete research after the ticket has already transitioned to Resolved (and the workflow forbids reopening)

Action:
- Do post a new comment titled "CORRECTION: supersedes prior decision" that explicitly names the prior comment ID, states what was wrong, cites the missed evidence, and gives the revised decision. Do not silently leave the wrong decision standing and do not edit/hide the prior comment — transparency lets the requester and implementer trace the reasoning.

## Improvement: memory read before any user-facing update

Condition:
- When starting any architect task or user request

Action:
- Do read `.ept/skills/self-improvement/SKILL.md` and `.ept/self-improvement/architect.md` as the first action and first tool call before any acknowledgement, progress update, planning, skill announcement, or repository read.

## Improvement: ticket tracker boundary

Condition:
- When gathering ticket context under a workflow that requires `ticket-helper` or tracking-system CLI use

Action:
- Don't use `rg`, `Get-Content`, or other filesystem reads against `.ept/tracker`; use only the allowed ticket interface for ticket state, links, comments, and workflow data. If `ticket-helper` is required but no subagent tool is exposed, say the limitation before using the documented tracking CLI as the only available ticket interface.

## Improvement: tracker storage exclusion when searching helper docs

Condition:
- When searching repository docs for ticket-helper or workflow instructions and direct tracker storage access is forbidden

Action:
- Do use exact ripgrep excludes with no stray spaces, for example `rg "ticket-helper" .ept -g "!.ept/tracker/**"`. Don't trust a malformed glob like `-g '! .ept/tracker/**'`, because it can list tracker files and break the ticket-helper-only rule.

## Improvement: no callable ticket-helper tool

Condition:
- When workflow requires `ticket-helper` subagent but host exposes no callable subagent tool

Action:
- Do state tool gap, read `.ept/agents/ticket-helper.md`, then use only documented tracker CLI commands through that protocol; don't read or write `.ept/tracker` files directly.

## Improvement: serialize tracker writes

Condition:
- When creating or updating tracker links, comments, or ticket fields through the tracker CLI

Action:
- Do run write operations sequentially and verify the resulting ticket/link state after batches; don't parallelize tracker writes because ID allocation can race and silently drop or overwrite intended links.

## Improvement: consult the workflow transition map before any status change

Condition:
- When a ticket update, auto-transition rule, or stakeholder instruction requires moving a ticket to a new status (including cases where an auto-transition rule like AT-x 'should have fired' but did not)

Action:
- Do call `tracker_cli.py get workflow transitions <type> <current_status>` (via ticket-helper) and only transition to a status in the returned allowed list. If the rule's intended target is not reachable, do NOT force an invalid transition; instead document the rule-handler / transition-map gap in a comment on the affected ticket, escalate to `workflow-mgr`, and leave the ticket in a non-terminal status. Cite the verbatim transition-map output as the refusal evidence so the reviewer can verify.
