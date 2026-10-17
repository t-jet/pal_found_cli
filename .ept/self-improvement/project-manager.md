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
