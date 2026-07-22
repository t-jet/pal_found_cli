# Tech Lead — Improvement Memory

## Improvement: verify reviewer ADR claims against code before fixing

Condition:
- When addressing a code-review finding that cites an ADR (e.g. "ADR-004 says errors go to stderr")

Action:
- Do read the cited ADR section directly before applying the fix; reviewers occasionally cite the wrong ADR number or invert the rule, and blindly matching their wording propagates the error.

## Improvement: flip tests asserting the bug when fixing correctness findings

Condition:
- When a code-review finding flags a correctness bug (e.g. wrong stream, wrong exit code) and the existing unit test asserts the buggy behaviour

Action:
- Do update the test in the same commit so it asserts the ADR-correct behaviour; do not leave the test enforcing the bug and creating a regression trap for the next reviewer.

## Improvement: verify blocking link exists before trying to remove it, and trust AT-5 for terminal-source blocks

Condition:
- When closing a ticket whose DoD says "remove the blocking link" or "no active is-blocked-by links", OR when advancing a ticket that is blocked by another ticket nearing a terminal status

Action:
- Do `link list` on the source AND target tickets before assuming a `Blocks` link exists; in this repo link topology is inconsistent (some codereviews only carry `ParentChild`, others carry `DEV Blocks CODEREVIEW`). Only remove a link that is actually a blocking relationship; if none exists, note "no blocking link present" and skip the removal step.
- Do NOT expect the `Blocks` link record to be deleted when the source ticket reaches a terminal status — AT-5 clears blocks *semantically* (the link row stays). Verify "not blocked" by attempting the transition, not by re-running `link list` and looking for the row to vanish.

## Improvement: verify epic auto-transition premises by enumerating all same-link siblings

Condition:
- When asked to verify whether an EPIC auto-transition (In Progress → Resolved) should fire after a DEV-STORY closure, especially when the request asserts the closed story was "the last one"

Action:
- Do `link list` the EPIC and `get` every DEV-STORY linked via EpicLink BEFORE predicting the cascade; the rule fires only when ALL linked DEV-STORYs are terminal, not when the most-recently-closed one is. Treat a user-supplied "all siblings done" premise as falsifiable — this task found 3 of 4 siblings (QA/Grooming/New) still non-terminal despite the premise.
- Don't manually transition the EPIC to manufacture the expected state; report the actual sibling-status matrix and let the auto-rule condition fail loud.

## Improvement: prefer best-effort optional imports for SDK exception mapping

Condition:
- When mapping third-party SDK exception types to project exit codes and the SDK may not be installed in every environment (CI, unit tests, lightweight runners)

Action:
- Do wrap the SDK import in try/except inside a registration helper that returns a base mapping plus SDK additions; document HTTP status classification as the primary fallback so reviewers understand the layered design.

## Improvement: obey nested preflight ordering

Condition:
- When agent instructions require loading role instructions and those role instructions contain a stricter first-action memory read

Action:
- Do read the stricter memory skill and memory file immediately after discovering the nested rule and before any user-facing update; don't batch other repo, workflow, ticket, or task reads with that memory preflight.

## Improvement: honor tracker-forbidden review mode

Condition:
- When tech-lead workflow requires ticket-helper/tracker steps but user explicitly forbids tracker operations

Action:
- Do state tracker gate is skipped due user constraint, then perform bounded repo/doc review only; don't create, search, update, comment, link, or transition tickets.

## Improvement: stop tracker integrity repair when helper has no approved write path

Condition:
- When tracker metadata is malformed and the user forbids direct tracker file access, while `ticket-helper` reports that documented CLI commands validate before they can repair the malformed record

Action:
- Do make one narrow follow-up asking `ticket-helper` for any approved data-integrity repair path; if it still reports none, stop and report blocked with exact failed command, exit code, unchanged tickets/comments/files, and verification not run.

## Improvement: keep ticket-helper as sole executor for constrained ticket workflows

Condition:
- When user explicitly requires `ticket-helper` for all ticket data and operations, especially for close/unblock/restore workflows

Action:
- Do delegate retrieval, workflow checks, link changes, comments, status transitions, and final verification to `ticket-helper` in one bounded task; don't run tracker commands or inspect tracker internals locally.
