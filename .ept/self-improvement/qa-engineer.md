# QA Engineer Improvement Memory

## Improvement: memory first

Condition:
- When starting any qa-engineer task

Action:
- Do read self-improvement skill and qa-engineer memory in first single-purpose tool call before any user update, batching, workflow read, ticket read, or repo scan.

## Improvement: nested first-action conflict

Condition:
- When outer instructions require loading the qa-engineer role file before anything, and that role file requires memory-first behavior

Action:
- Do make the first tool call a single file read of only `.ept/agents/qa-engineer.md`, then immediately read self-improvement skill and qa-engineer memory in one single-purpose tool call; don't batch AGENTS.md prep, skill index, workflow, ticket, repo, or commentary-adjacent context with that first role read.

## Improvement: tracker helper missing

Condition:
- When qa workflow asks for ticket-helper but no ticket-helper tool is exposed

Action:
- Do state helper unavailability, use only documented tracker CLI operations when allowed, and never read tracker storage files directly.

## Improvement: no parallel tracker writes

Condition:
- When creating or updating tracker links, comments, statuses, or fields through helper protocol

Action:
- Do run write operations one at a time and verify state after suspicious output; don't parallelize tracker writes because ID allocation can race.

## Improvement: helper write author

Condition:
- When asking ticket-helper to create comments, remove links, or update ticket status

Action:
- Do include `author: qa-engineer` in first write request so helper has required actor metadata.

## Improvement: helper blocked by agent limit

Condition:
- When ticket-helper is required by user or workflow, but subagent spawn fails because agent thread limit is reached

Action:
- Do stop ticket work, report helper blockage, and don't use tracker CLI or tracker files when user or workflow explicitly requires ticket-helper only.

## Improvement: verify reachability before waiving DoD

Condition:
- When a prior comment claims a runtime DoD criterion (e.g. "Application logs attached", "capture stderr/stdout") cannot be met because "no log/output was produced" or "path is unreachable"

Action:
- Do execute the documented reproduction steps yourself (or write a minimal repro) and capture stdout/stderr before accepting the waiver; only document unprovability with a runnable snippet after a failed execution attempt. Don't waive based solely on a prior agent's claim.

## Improvement: question-block auto-transition not automatic

Condition:
- When creating a QUESTION sub-task under a parent to request external review/approval, expecting workflow rule #5 "Question sub-tasks block the parent" + the `child_blocker_created` (AT-4) automatic transition to move the parent to Blocked

Action:
- Do NOT rely on auto-transition. After creating the QUESTION, explicitly (a) create the `Question` link sibling for structural parity with prior QUESTIONs, (b) create the `Blocks` link to model the blocking relationship, (c) document blocker ID + prior status as a comment per the parent's `Blocked` status instructions, and (d) manually transition the parent to Blocked. When the QUESTION reaches terminal status, remove the Blocks link and rely on `all_blockers_cleared` (AT-5) to restore prior status — don't assume AT-4 fires on link creation.
