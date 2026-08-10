# QA Engineer Improvement Memory

## Improvement: verify per-command surface details, not just totals

Condition:
- When cross-validating a test-case deliverable against the real implementation (or when authoring inventory rows against a DESIGN doc), and the total operation count matches but per-resource breakdowns or per-command flags are inherited from a stale design note (e.g. TESTCASE-016 said "Dataset 1, Stream 7, Subscriber 7" while OP_SPECS expose Dataset 1, Stream 8, Subscriber 6; TESTCASE-015 listed `--output` on `execute-ontology` though only `get-results` registers it)

Action:
- Do verify per-resource operation counts and each command's required/optional flag set directly against the actual `OP_SPECS`/parser (import probe or reading the CLI source), and cross-check fixture bounds (e.g. binary publish cap 16 MiB, `--max-records` defaults) against the implementation constants — not just the aggregate catalog size. Update the deliverable (inventory rows, scope, STR/SQL-TC case text, evidence mappings to real test names) whenever the implemented surface differs. Verified TESTCASE-015/016 (2026-08-10): totals (5 and 15) matched but the 7/7 streams split and the execute-ontology `--output` flag were both wrong and were corrected before the approval handoff.

## Improvement: memory first

Condition:
- When starting any qa-engineer task

Action:
- Do read self-improvement skill and qa-engineer memory in first single-purpose tool call before any user update, batching, workflow read, ticket read, repo scan, or AGENTS skill-index read. If outer role-load rule applies first, make that role read tool-only and single-purpose, then immediately do memory-only read.

## Improvement: nested first-action conflict

Condition:
- When outer instructions require loading the qa-engineer role file before anything, and that role file requires memory-first behavior

Action:
- Do make first assistant action a tool-only, single-file read of `.ept/agents/qa-engineer.md`, despite the general preference to send commentary before tools. Then immediately read only self-improvement skill and qa-engineer memory in one single-purpose tool call before any user-facing commentary. After that succeeds, read AGENTS prep, skill index, workflow, and other task context in later calls. Don't send commentary before either required read completes, don't batch skill index, workflow, ticket, repo, git, docs, tests, or other task context into either first-step read, and if this order is missed, recover by loading memory at once, stating the protocol gap, and keeping later tracker access constrained to the required helper path.

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

## Improvement: tracker forbidden by user

Condition:
- When qa workflow requires ticket operations but the user explicitly forbids tracker operations

Action:
- Do perform only the requested local review or analysis, state that formal workflow sign-off is blocked by the no-tracker constraint, and don't call ticket-helper, tracker CLI, or tracker files.

## Improvement: verify reachability before waiving DoD

Condition:
- When a prior comment claims a runtime DoD criterion (e.g. "Application logs attached", "capture stderr/stdout") cannot be met because "no log/output was produced" or "path is unreachable"

Action:
- Do execute the documented reproduction steps yourself (or write a minimal repro) and capture stdout/stderr before accepting the waiver; only document unprovability with a runnable snippet after a failed execution attempt. Don't waive based solely on a prior agent's claim.

## Improvement: question-block auto-transition not automatic

Condition:
- When creating a QUESTION sub-task under a parent to request external review/approval, expecting workflow rule #5 "Question sub-tasks block the parent" + the `child_blocker_created` (AT-4) automatic transition to move the parent to Blocked

Action:
- Do NOT rely on auto-transition. After creating the QUESTION, explicitly (a) set assignee to creator before New -> Open if helper creation leaves assignee blank, (b) create the `Question` link sibling for structural parity with prior QUESTIONs, (c) create the `Blocks` link to model the blocking relationship, (d) document blocker ID + prior status as a comment per the parent's `Blocked` status instructions, and (e) manually transition the parent to Blocked. When the QUESTION reaches terminal status, remove the Blocks link and rely on `all_blockers_cleared` (AT-5) to restore prior status. Don't assume AT-4 fires on link creation.

## Improvement: don't trust brief-supplied ticket ids

Condition:
- When a user brief cites a specific sibling/related ticket id (e.g. "the TESTCASE under same DEV-STORY is TESTCASE-002")

Action:
- Do verify the cited id against the parent's actual children via `list --parent <parent>` before relying on it; briefs can mis-number siblings (TESTCASE-002 was DEV-STORY-001's, the real sibling of TESTEXEC-001 was TESTCASE-001). Don't open the wrong test-case spec or scope-creep into another story.

## Improvement: classify failures outside pytest before filing

Condition:
- When pytest tests FAIL and a captured stderr/stdout fixture reads empty while the `Captured stderr call` shows the expected bytes (typical of `logging.StreamHandler(sys.stderr)` + pytest FDCapture interaction), or when a test calls an API with parameter/return shapes that don't match the impl

Action:
- Do run a small standalone Python repro (NOT under pytest) before classifying — swap streams / call the documented signature manually and observe. If the product emits correctly in isolation, classify as test-harness or stale-test-spec defect (BUG-SUB), NOT a product defect; embed the standalone repro evidence in the execution comment. Don't file a product BUG-SUB without an isolated failing repro, and don't waive a runtime DoD claim from a prior agent without reproducing.

## Improvement: rate-limit retry is transient

Condition:
- When a ticket-helper subagent call returns "Rate limit exceeded" / "ChatRateLimited" (code 1302)

Action:
- Do NOT abort or escalate. Re-issue the same single-purpose helper call as the immediate next tool turn (brief pause via the surrounding turn); the platform rate limit is transient and the retry succeeded on the first re-issue this session. Don't switch to a different transport or skip the operation.

## Improvement: bug_subtask Blocks link does not auto-block parent

Condition:
- When a `bug_subtask` child with a `Blocks` link is created under a parent, expecting `child_blocker_created` (AT-4) to move the parent to Blocked

Action:
- Do NOT assume the parent auto-blocks. AT-4's `child_filter` is `types: [question]`, so a `bug_subtask` Blocks link does NOT fire it. The parent stays in its current status; the open BUG-SUB only blocks the parent's LATER transition via its own DoD ("All BUG-SUB sub-tasks Closed"). If you need the parent visibly Blocked, create a QUESTION sub-task instead, or manually transition the parent.

## Improvement: QUESTION approval-request auto-blocks parent via AT-4

Condition:
- When creating a QUESTION sub-task (e.g. tech-lead approval request) under a TESTCASE parent to satisfy the reviewer-approval gate

Action:
- Do create the QUESTION, set assignee to creator before New -> Open, create the Question link, then the Blocks link; AT-4 `child_blocker_created` fires on the Blocks-link creation and auto-transitions the parent to Blocked (no manual parent transition needed). Document blocker ID + prior status in a parent comment. Confirmed TESTCASE-017/018 (2026-08-10): QUESTION-040/041, links LINK-00597/00598/00599/00600, both parents auto-Blocked. On approval, tech-lead must post approval, close the QUESTION, remove the Blocks link, and manually restore the parent (AT-5/AT-6 do not reliably auto-restore).

## Improvement: testcase Open -> In Progress needs implementation-existence gate

Condition:

- When advancing a `testcase` from `Open` to `In Progress` (or starting test design work), the `Open` status DoD includes `MANDATORY VERIFICATION: Implementation exists and is accessible` and a `CORRECTIVE ACTION IF IMPLEMENTATION DOES NOT EXIST` clause (file a BUG for phantom completion)

Action:

- Do NOT rely on DEV/UNITTEST `Closed`/`Resolved` status alone. Before `Open -> In Progress`, verify real runnable code exists in the repo (grep the component file path from DESIGN-XXX, import-check the symbol, or run a smoke pytest). If status claims done but no code is present, file a `bug` ticket for phantom implementation and block TESTCASE on it instead of designing tests against vaporware.
- When implementation genuinely does not exist yet (DEV/UNITTEST still New, no phantom-completion claim), do NOT attempt the transition using a narrative activation-gate comment as evidence: the mandatory gate requires runnable code, and the helper/validator will reject it (verified TESTCASE-013/014, 2026-08-09; TESTCASE-015/016, 2026-08-10). Keep the ticket in `Open`, document the gate honestly in an activation-gate comment, author the design deliverable against the approved DESIGN doc plus the vendored SDK contract (verify the real method signatures and paths from the vendored SDK source, e.g. sql_queries SqlQuery 5 methods with get_results ARROW_TABLE mode; streams Dataset/Stream/Subscriber 15 methods), and re-verify the gate when real code lands (TESTCASE-012 precedent: stayed Open until real commit + UNITTEST Closed + DEV Resolved). The New->Open transition remains valid in parallel-design mode; only Open->In Progress waits on runnable code.

## Improvement: grooming QA review is not sign-off

Condition:

- When asked to confirm QA grooming review or readiness for a DEV-STORY before implementation exists

Action:

- Do answer only scope understanding, reviewed evidence, planned test coverage, risks, and QA actions before unblock. Don't claim QA sign-off, execute TESTCASE/TESTEXEC transitions, or require runnable implementation unless the request is for test design/execution status work.

## Improvement: dirty deliverable diff attribution

Condition:

- When editing a file that was already dirty before QA work began

Action:

- Do report only the scoped edits made by this QA pass as your changes, and call out that the file also contained pre-existing edits. Don't imply the whole `git diff` for that file was produced by this task.

## Improvement: separate validation universes

Condition:

- When QA evidence includes results from a committed archive and a local workspace with extra untracked tests

Action:

- Do report counts separately with exact source context. Don't merge archive and workspace pass counts into one implied suite.

## Improvement: create blocker link before blocked status

Condition:

- When moving a ticket to `Blocked` because a workflow DoD gate is unmet

Action:

- Do create or identify the active blocker ticket/link first, record blocker ID plus prior status in a comment, then transition the parent to `Blocked`. Don't leave a ticket in `Blocked` without a `Blocks` link.

## Improvement: resource registry path drift

Condition:

- When qa workflow says to consult `.ept/docs/resources/available_resources.md` but that path is missing

Action:

- Do use `.ept/docs/document_index.md` to find the current resource registry path, then read that file before choosing the addressed role for a QUESTION. Don't treat the stale path as a blocker if the indexed resource file exists.

## Improvement: design-only testcase with tracker forbidden

Condition:

- When user explicitly asks for QA test-case deliverable based on approved DESIGN docs, forbids tracker operations, and implementation files are absent

Action:

- Do produce scoped test-case design against the DESIGN source, list implementation files as execution preconditions, report tracker/approval workflow as blocked for manager follow-up, and don't create bug/question tickets or read tracker internals.

## Improvement: re-validate pre-warned known failures per HEAD

Condition:

- When repo/agent memory or a prior TESTEXEC cites a "known pre-existing failure" bucket for the test suite

Action:

- Do re-run the full suite on the current HEAD before assuming those failures still occur, and update the memory note with the revalidation result (HEAD + date + counts). Don't pre-warn, exclude tests, or run a reduced suite based on stale failure notes, since the tree may have since fixed them (2026-07-29 TESTEXEC-009: the LogSetup/stale-retry bucket was gone, 850/850 clean).

## Improvement: label interrupted QA evidence

Condition:
- When manager requests immediate QA return before planned regression execution finishes

Action:
- Do separate independently executed results from developer-supplied evidence in verdict and tracker comment. Don't imply unrun suites were independently verified.

## Improvement: classify offline build isolation errors

Condition:
- When an offline packaging test fails while pip tries to install build dependencies before product code runs

Action:
- Do reproduce the build outside pytest, then rerun with explicit `--no-build-isolation` and temporary local build tooling. Treat the first result as an environment setup error unless the corrected offline build still fails. For pip's negative boolean environment option, use `PIP_NO_BUILD_ISOLATION=false`; value `1` leaves isolation enabled.

## Improvement: testcase In Progress -> Resolved has two extra gates

Condition:
- When advancing a `testcase` from `In Progress` to `Resolved` after test-case authoring

Action:
- Do NOT rely on the case-set comment alone. The tracker validator enforces two additional mandatory DoD criteria before allowing the transition: (1) an explicit reviewer approval comment from the reviewer role (e.g. `tech-lead` posting "Tech lead approval" with "Approval gate for TESTEXEC-XXX: PASS" on the TESTCASE ticket, per the TESTCASE-012 sibling pattern), and (2) `time_spent_hours` populated in the subtask frontmatter. When approval is missing, create a `question` sub-task under the TESTCASE addressed to the reviewer, wire Question + Blocks links, let AT-4 block the parent, and wait for the reviewer to approve; do NOT self-approve as QA. Verified TESTCASE-013/014 (2026-08-09): the transition was rejected by the helper until both gates were met.

## Improvement: AT-6 unblock does not fire after manual link removal

Condition:
- When resolving a blocking `question` sub-task (closing it) and the Blocks link to the parent is removed before the question's status update

Action:
- Do NOT expect the AT-6 automatic transition (`this_ticket_reaches_status` -> `linked_ticket_target_status: prior_status`) to restore the parent from `Blocked`. If the Blocks link is already gone when the question reaches Resolved/Closed, the rule has nothing to act on. Instead, manually transition the parent `Blocked -> prior_status` (documented in a comment) once the blocker is terminal and the Blocks link is removed. Verified TESTCASE-013/014 (2026-08-09): tech-lead closed the approval questions and manually restored both parents to In Progress because the auto-unblock did not fire.

## Improvement: tracker helper cwd drift with parallel agents

Condition:
- When dispatching tracker operations to the ticket-helper subagent while other agents (e.g. devops-engineer) share the same terminal and change the working directory to a temp folder, causing tracker CLI "ticket not found" validation errors

Action:
- Do instruct the ticket-helper to chain `Set-Location <project-root>` (and confirm `Get-Location`) inside EVERY tracker command invocation, and use the absolute path to `tracker_cli.py` when cwd cannot be guaranteed. Verify ticket existence (`get`) before any write; when a helper reports phantom missing tickets or contradictory parent statuses, suspect cwd drift rather than actual tracker state. Verified TESTEXEC-013/014 (2026-08-10): first helper call failed with "TESTEXEC-013 not found" + "DEV-STORY-013 in Analysis" because cwd was `T:\tmp\foundry-devops013-014-20260810\candidate`; re-issue with per-command `Set-Location` succeeded immediately.

## Improvement: comment create requires --subject

Condition:
- When asking ticket-helper to create a tracker comment with only a Markdown body (`--text`) and no `--subject`

Action:
- Do ALWAYS pass `--subject '<short summary>'` together with the body — `comment create` enforces `--subject required=True` at the parser level and aborts (exit 5, no command run) without it; the helper refuses to invent a subject. Verified TESTEXEC-015/016 closure comments (2026-08-10): first close requests aborted at validation; re-issue with a subject succeeded.

## Improvement: subagent EXIT:0 may be cwd-guard echo, verify with post-write get

Condition:
- When a ticket-helper subagent reports a status transition succeeded with "EXIT:0" but the ticket still shows the prior status on a later `get`

Action:
- Do NOT trust the echoed "EXIT:0" as proof of a persisted status transition — it can come from the chained `Set-Location`/`Get-Location` guard instead of the `update --status` command. Run a post-write `get <ticket>` to confirm the persisted status before declaring success, and re-issue the transition if the status is unchanged. Verified TESTEXEC-015 (2026-08-10): first "Closed" attempt actually left the ticket Resolved; the second pass (post-write get confirmed) persisted Closed.

## Improvement: live-style CLI probes need valid 5-segment RIDs

Condition:
- When running live-style CLI probes against a namespace (e.g. connectivity) using the TESTCASE test-data RID fixtures, and the SDK rejects the input with a pydantic `ValidationError` mapped to exit 1 instead of the expected network/config error (exit 6/9)

Action:
- Do use a valid 5-segment RID (`ri.<app>.<instance>.<type>.<rid>`, e.g. `ri.connectivity.main.test.conn`) for live-style probes; the installed SDK (1.102.0) enforces a stricter RID pattern than 4-segment fixtures like `ri.connection.main.test-conn`. Verify the actual exception via `_serialize_error` instrumentation (wraps the module function, prints type/str/frames) before classifying: a `pydantic_core.ValidationError` from the SDK means input validation correctly exits 1 (ADR-001), NOT a product defect; document the 4-segment fixture as a test-data doc artifact. Verified TESTEXEC-017 (2026-08-10): after fixing the RID, the creds-present probe produced the expected ConnectionError retries with exit 6 and the scrubbed probe exit 9.

## Improvement: capture exit codes without truncating pipelines

Condition:
- When capturing CLI probe evidence and piping through `Select-Object -First N` or similar truncation before reading `$LASTEXITCODE`

Action:
- Do capture the exit code on a separate, non-truncated invocation (e.g. redirect stdout/stderr to $null with `2>$null | Out-Null` and read `$LASTEXITCODE`, or capture output to a variable first). Truncating the pipeline can mask the CLI's real exit code (E9 probe showed exit 0 where the actual path exits 6). Verified TESTEXEC-017 (2026-08-10).

## Improvement: sequence testexec transitions in order (Open -> In Progress -> Resolved -> Closed)

Condition:
- When advancing a `testexec` ticket and requesting a status jump (e.g. Open -> Resolved) instead of the configured chain

Action:
- Do plan and request the full allowed chain explicitly: `Open -> In Progress -> Resolved -> Closed`; the tracker validator rejects jumps (Open->Resolved not allowed; the helper preflight aborts cleanly). Prepare each transition's DoD evidence before requesting it (Open->In Progress: implementation exists + plan comment + TESTCASE/DEV/UNITTEST/CODEREVIEW terminal; In Progress->Resolved: per-case evidence + time reported; Resolved->Closed: no active is-blocked-by links). Also single-quote multi-word status values (`--status 'In Progress'`) — unquoted, PowerShell splits them and the CLI errors "unrecognized arguments". Verified TESTEXEC-017/018 (2026-08-10).
