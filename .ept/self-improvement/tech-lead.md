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

## Improvement: ground backward-compat closure claim on additive-skill evidence checklist

Condition:
- When a DEV-STORY closure DoD asks "backward compatibility guaranteed OR new major version increased" for a NEW namespaced skill/CLI added to an existing multi-namespace CLI repo

Action:
- Do verify four concrete code facts BEFORE writing the determination comment and keep version unchanged only if all hold: (1) pyproject [project.scripts] appends the new entry point without removing/renaming any prior one; (2) the new CLI imports only `common.*` shared infra (consume-only) and imports nothing from sibling namespace CLIs; (3) no `common.*` module was modified; (4) a test asserts the operation-count contract (e.g. `len(OP_SPECS) == 66`). Absent any Incompatible API change, no major bump is required (SemVer additive). Cite each fact inline in the closure comment so the determination is falsifiable, not boilerplate.
- Don't rubber-stamp "additive and backward-compatible" from the ticket title alone — reviewers can't tell a real review from a templated one.

## Improvement: prefer best-effort optional imports for SDK exception mapping

Condition:
- When mapping third-party SDK exception types to project exit codes and the SDK may not be installed in every environment (CI, unit tests, lightweight runners)

Action:
- Do wrap the SDK import in try/except inside a registration helper that returns a base mapping plus SDK additions; document HTTP status classification as the primary fallback so reviewers understand the layered design.

## Improvement: obey nested preflight ordering

Condition:
- When repo or developer instructions require loading a role file before work, and that role file may contain stricter preflight rules

Action:
- Do read the required role file as a single-purpose first command. Do not batch it with AGENTS skill-index reads, repo scans, or other setup. If it reveals a stricter memory preflight, immediately read only the memory skill and memory file before any user-facing update, skill-index read, workflow/ticket read, parallel batch, or task analysis. If the first action already violated this, state the slip briefly, stop all task-context reads, load the missing memory preflight alone or in a memory-only pair, then continue from the strictest remaining gate.

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
- Do delegate retrieval, workflow checks, link changes, field/body updates, comments, status transitions, and final verification to `ticket-helper` in one bounded task; ask helper to report before/after status, exact tracker actions, link ids/types, changed fields, evidence comments, transition result, blockers, and file paths. Don't run tracker commands or inspect tracker internals locally.
- Do provide an explicit `time_spent_hours` value before asking `ticket-helper` to resolve subtask tickets whose DoD requires time reporting; don't make the helper stop and ask/infer time after approval evidence is already recorded.

## Improvement: close design tickets with explicit evidence gaps covered

Condition:
- When closing a DESIGN ticket after manager verification flags missing DoD evidence

Action:
- Do add concise tracker comments for each named evidence gap before closing: document-index impact (updated or no update needed with reason), responsible-person mapping from available resources and child assignees, active blocker check, and terminal transition result.

## Improvement: stop when required ticket-helper cannot spawn

Condition:
- When a ticket workflow explicitly requires `ticket-helper` subagent-only access and subagent spawning fails because the agent thread limit is reached

Action:
- Do reuse an existing completed/open `ticket-helper` with `send_input` when one is available, or resume a prior closed `ticket-helper` only if needed; if fresh spawn, reuse, and resume all fail, report blocked with exact failures and unchanged tracker state. Don't bypass the user constraint by reading tracker files or running tracker commands locally.

## Improvement: treat vague child AC as readiness blocker

Condition:
- When checking Grooming -> Development readiness and DoD requires child subtasks ready with criteria covering named scope or edge constraints

Action:
- Do compare each child task's concrete AC against every named scope item; block readiness when AC says generic or representative coverage where full coverage is required, even if ticket description has broader intent.

## Improvement: separate commit review from dirty workspace fixes

Condition:
- When re-review asks about a named correction commit and workspace has uncommitted changes touching same files

Action:
- Do verify findings against committed blobs first. If imports, tests, lint, or type checks can pass because of untracked/unstaged files, run clean archive/worktree validation of the named commit before approving. Report current-workspace results as contaminated when later local files change outcome; don't approve commit-only review based on unstaged or untracked fixes.

## Improvement: make iterator tests consume stream

Condition:
- When review checks iterator handling for streaming, binary download, or SDK pagination paths

Action:
- Do verify the real SDK return protocol first (`inspect.signature`, awaitable check, `__aiter__`, cursor attrs), then use a test double that consumes the iterator with the same protocol as production; don't accept dict/page-envelope mocks or wrapper-call assertions when production returns an async iterator because they can hide broken async iteration and pagination metadata.
- Do verify the public streamed-response surface before designing header propagation. If no public headers accessor exists, pass `None` to bounded-download metadata inputs and test unknown-length probing; don't reach through private fields such as `response._response`.

## Improvement: keep review commands shell-native

Condition:
- When environment detection says PowerShell or Windows and review needs git diff, line extraction, temp validation, or file comparison

Action:
- Do use PowerShell-native constructs such as `ForEach-Object`, temp files, or separate `git show` reads; don't use POSIX process substitution or shell syntax that PowerShell rejects.
- Do delimit interpolated variable names before colons (`${path}:...`) and test smart punctuation through Unicode code points; don't place curly apostrophes inside single-quoted PowerShell regex strings.

## Improvement: package verified scope without reopening discovery

Condition:
- When manager supplies architect-verified scope and asks for a bounded readiness package without tracker access

Action:
- Do reuse supplied evidence, verify only missing implementation contracts such as exact SDK signatures, and return title, description, catalog, acceptance criteria, paths, risks, and transition evidence in one response. Don't reopen broad architecture discovery or mutate tracker/repo deliverables.

## Improvement: test packaged ACL policy outside repository cwd

Condition:
- When a namespace CLI depends on metadata allow-list files or other policy assets loaded by relative path

Action:
- Do test metadata-only decisions from an empty working directory against the installed or archived package. Verify every required policy asset is packaged and resolved independently of repository cwd; don't accept a repo-root test that passes only because `.ept/docs` exists nearby.

## Improvement: probe parser failures through console boundary

Condition:
- When reviewing a CLI whose requirements say every error must use a structured stdout envelope

Action:
- Do run missing-command, missing-positional, invalid-choice, and invalid-type probes through the real console boundary. Assert JSON on stdout and the required exit code; don't rely on happy-path parser unit tests because `argparse` can exit before application error handling.

## Improvement: classify local destructive commands in ACL design

Condition:
- When a namespace adds a local-only command that mutates files or persisted state, such as `session purge`

Action:
- Do verify the command's verb is classified as a write by `AccessControlGuard`, include it in namespace and operation policy keys, and test read-only and metadata-only denial before filesystem mutation. Don't assume SDK operation catalogs cover local commands.

## Improvement: verify JSON-suffixed CLI inputs against SDK scalar aliases

Condition:
- When grooming a generated-SDK CLI design that names an option `--*-json` or assigns it an object/list shape

Action:
- Do inspect the authoritative SDK model alias and validate a representative value before approval; block readiness when the design requires an object but the SDK contract is scalar, because DEV and UNITTEST would otherwise encode incompatible behavior.
