# Self-Improvement Memory — Project Workflow Manager

## Improvement: Handle failing GitHub check requests via BUG handoff

Condition:

- When a user reports a failing or red GitHub check, or any GitHub/CI state request

Action:

- Don't implement the fix yourself. Do: search the tracker for a matching ticket first; if none, diagnose read-only (fetch run/job/step logs via the GitHub API helper under `.ept/tmp`, never print the token); create a BUG with exact run/job IDs and step exit codes; promote it to Open; hand off to devops-engineer; independently verify the green result; then let QA verify to Closed.

## Improvement: Verify handoff agent claims independently

Condition:

- When a subagent handoff reports a success outcome that asserts an external state (CI status, published artifact, live check)

Action:

- Do re-check that external state yourself from the authoritative source (e.g. GitHub API run/job conclusions) before reporting the outcome as done. Don't repeat the agent's claim unchecked.

## Improvement: Check allowed fields before update --field

Condition:

- When closing or updating ticket with `update --field key=value` (e.g. `resolution`, `fix_version`) on type task or any other type

Action:

- Do read allowed fields from `type-info <type>` first. `resolution` is not allowed on task. Don't guess field names; use only fields listed for that type.

## Improvement: Register read-only inspection requests as task

Condition:

- When user asks for status/progress inspection or any read-only tracker reporting

Action:

- Do create a task ticket (or reuse matching one), promote to Open, record report as a comment, advance to Resolved then Closed. Don't produce the report without a ticket.

## Improvement: One-try retry after interrupted terminal command

Condition:

- When a tracker CLI command gets interrupted (Ctrl+C) or returns no output

Action:

- Do retry the exact command once and check exit code. Don't change the command or assume it succeeded.
