# QA Engineer Improvement Memory

## Improvement: 3.12 harness needs pytest-asyncio before async suite runs

Condition:
- When running a namespace focused suite (or full regression) on a secondary Python 3.12 interpreter provisioned via `--user --break-system-packages` PYTHONUSERBASE, and collection fails with "Unknown pytest.mark.asyncio" / "Unknown config option: asyncio_mode" / ImportError on the test module

Action:
- Do provision `pytest-asyncio` (plus pytest-cov, python-dotenv, requests, the pinned foundry-platform-sdk) into that userbase BEFORE running any async-marked suite, and set `PYTHONPATH=src` for src-layout imports; classify the resulting collection/run failures as a test-harness gap, not a product defect. Verified TESTEXEC-019/020 (2026-08-10): 3.12 focused run failed 38 tests until pytest-asyncio 1.4.0 installed; then 131 focused and 1276 full passed on 3.12.

## Improvement: wheel --no-index install fails without local SDK cache

Condition:
- When verifying a wheel/editable packaging case in a fresh venv and using `--no-index` / `PIP_NO_INDEX=1` (test-case docs say offline build with local deps), and pip fails with "Could not find a version that satisfies the requirement foundry-platform-sdk>=1.0.0 (from versions: none)"

Action:
- Do NOT treat this as a product defect. The SDK is not vendored locally, so `--no-index` cannot resolve it; install the wheel with dependency resolution (plain `pip install <wheel>`) or first provision deps into the venv, then re-run the launcher/ACL probes. Verify entry-point launchers exist after install (`Get-ChildItem venv\Scripts\foundry-*.exe`). Verified TESTEXEC-019/020 (2026-08-10): `--no-index` install failed, retry with deps succeeded and all probes passed.

## Improvement: verify per-command surface details, not just totals

Condition:
- When cross-validating a test-case deliverable against the real implementation (or when authoring inventory rows against a DESIGN doc), and the total operation count matches but per-resource breakdowns or per-command flags are inherited from a stale design note (e.g. TESTCASE-016 said "Dataset 1, Stream 7, Subscriber 7" while OP_SPECS expose Dataset 1, Stream 8, Subscriber 6; TESTCASE-015 listed `--output` on `execute-ontology` though only `get-results` registers it)

Action:
- Do verify per-resource operation counts and each command's required/optional flag set directly against the actual `OP_SPECS`/parser (import probe or reading the CLI source), and cross-check fixture bounds (e.g. binary publish cap 16 MiB, `--max-records` defaults) against the implementation constants — not just the aggregate catalog size. Update the deliverable (inventory rows, scope, STR/SQL-TC case text, evidence mappings to real test names) whenever the implemented surface differs. Verified TESTCASE-015/016 (2026-08-10): totals (5 and 15) matched but the 7/7 streams split and the execute-ontology `--output` flag were both wrong and were corrected before the approval handoff.

## Improvement: DESIGN doc can be stale against installed SDK — verify via inspect.signature

Condition:
- When authoring a TESTCASE deliverable against a DESIGN doc whose operation count was NOT yet corrected (e.g. DESIGN-022 still listed 12 widgets ops after a QUESTION-043 decision cut it to 8), or when the implementation directory does not exist yet at gate time

Action:
- Do ground the case set in the ACTUAL installed SDK surface via `inspect.signature` on the installed package (never the vendored snapshot alone), assert the stale/out-of-scope ops are ABSENT in the catalog case, note the design-amendment dependency in the deliverable, and if the Open->In Progress gate fails (no runnable code) keep the ticket in Open with a gate-status comment documenting exactly which files/entry points are missing — do not force the transition and do not file a BUG when DEV is legitimately in progress. Verified TESTCASE-022 (2026-08-11): 8-op surface confirmed against installed `foundry_sdk.v2.widgets` (enable/set_widget_set_by_id; repository get/publish; widget-set get; release delete/get/list; DevModeSettingsV2 out of scope), DESIGN-022 stale 12-op flagged, `src/foundry_cli/widgets/` absent -> TESTCASE-022 stayed Open with gate comment 20260811-022006; TESTCASE-021 gate PASSED at HEAD 74094bc (9-op OP_SPECS, 4/5 policy, 37 focused tests) -> In Progress with plan comment 20260811-021400.

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
- Do NOT rely on the case-set comment alone. The tracker validator enforces two additional mandatory DoD criteria before allowing the transition: (1) an explicit reviewer approval comment from the reviewer role (e.g. `tech-lead` posting "Tech lead approval" with "Approval gate for TESTEXEC-XXX: PASS" on the TESTCASE ticket, per the TESTCASE-012 sibling pattern), and (2) `time_spent_hours` populated in the subtask frontmatter. When approval is missing, create a `question` sub-task under the TESTCASE addressed to the reviewer, wire Question + Blocks links, let AT-4 block the parent, and wait for the reviewer to approve; do NOT self-approve as QA. Verified TESTCASE-013/014 (2026-08-09): the transition was rejected by the helper until both gates were met. Reconfirmed TESTCASE-021/022 (2026-08-11): tech-lead had posted approvals DIRECTLY on the TESTCASE tickets (20260811-025114/025117 and 025135/025140, no QUESTION sub-tasks needed); set `time_spent_hours=8` via `update --field time_spent_hours=8`, then In Progress->Resolved->Closed all succeeded with post-write get confirming each status. Resolved->Closed DoD is only "no active is-blocked-by links" — verify via link list (only Contains/ParentChild from parent) before closing.

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

## Improvement: comment bodies with literal apostrophes break PowerShell single-quoting

Condition:
- When writing a tracker comment body that contains literal apostrophes inside a PowerShell single-quoted `--text` argument (e.g. Python dict/tuple literals like `{'check': 4, 'check_report': 2}` or `('Check',)`), the single quote terminates the argument early and the CLI errors "unrecognized arguments" (exit 2) with truncated text

Action:
- Do double every literal apostrophe (`''`) inside the single-quoted `--text` string before sending, so PowerShell keeps the argument intact and the stored body matches byte-for-byte; verify with a `comment get` when fidelity matters, and check no comment was committed before retrying (the argparse failure happens before any write, so no duplicate risk). Verified TESTCASE-020 (2026-08-10): attempt 1 aborted at exit 2 on `{'check': 4, 'check_report': 2}`; attempt 2 with doubled apostrophes committed `20260810-190859-qa-engineer` byte-identical.

## Improvement: pre-existing 3.12 audit wheel flake classified as harness, not defect

Condition:
- When running the full suite on a uv-provisioned Python 3.12 and `tests/test_audit_console_wrapper.py::test_wheel_and_editable_installs_work_from_arbitrary_cwd_without_pythonpath` fails with `ModuleNotFoundError: No module named dotenv` in the installed-wheel smoke (child venv created with `--system-site-packages`)

Action:
- Do classify as a pre-existing environment-harness flake, NOT a product defect and NOT a BUG-SUB: uv-managed 3.12 interpreters (Roaming/uv cache/seeded venv) have no conventional base site-packages containing dotenv, so the child `--system-site-packages` venv cannot resolve it; the audit namespace wheel test passes on 3.11 (base interpreter has dotenv). Evidence: identical flake recorded in devops019-020 batch py312-full.log ("1 failed, 1275 passed" first, "1276 passed" on rerun). Document the flake in the execution-log note and keep focused suites + per-namespace coverage as the pass evidence on 3.12. Verified TESTEXEC-021/022 (2026-08-11): 3.11 1362 passed, 3.12 1361 passed + the single audit flake.

## Improvement: use uv seeded venv and Start-Process logs for 3.12 long suites

Condition:
- When provisioning a Python 3.12 environment for QA suites and running long full-suite pytest runs in a shared PowerShell terminal

Action:
- Do create the 3.12 venv with `uv venv --seed` (provides pip, needed by the audit wheel-build fixture; uv cache interpreters and plain `uv venv` lack pip and user-site is disabled via ENABLE_USER_SITE=False), install deps with `uv pip install --python <venv>`, set `PYTHONPATH=src`, and run long suites via `Start-Process -NoNewWindow -Wait` with separate stdout/stderr log files. The shared terminal suffers KeyboardInterrupt contamination from parallel agents; detached-with-logfile runs survive it. Also note the first wheel install into a fresh venv may silently skip console scripts — `--force-reinstall --no-deps` fixes it (harness artifact). Verified TESTEXEC-021/022 (2026-08-11).

## Improvement: verify document-index links when registering a QA deliverable

Condition:
- When registering a QA test-case deliverable in `.ept/docs/document_index.md`, or when a prior registration (DEV/DEVOPS) added a link to a repo artifact outside `.ept/docs/` (e.g. a skill under `.claude/skills/`)

Action:
- Do resolve every relative link touched in the index (and the pre-existing entries adjacent to the insertion point) with `Test-Path`/`Resolve-Path` from `.ept/docs/`; `.claude/` artifacts need `../../.claude/...`, not `skills/...`. Don't leave a broken index link behind. Verified TESTCASE-023 (2026-08-11): the DEV-023 registration had `[Foundry Knowledge Skill](skills/foundry/SKILL.md)` resolving to `.ept/docs/skills/...` (nonexistent); corrected to `../../.claude/skills/foundry/SKILL.md` and documented in the authored-evidence comment.

## Improvement: static-doc deliverables — verify counts via AST over real CLI sources

Condition:
- When designing QA test cases for a documentation/static-markdown story whose expected values are operation counts or per-namespace catalog shapes

Action:
- Do verify every count against the ACTUAL implemented source, not the DESIGN doc: an AST probe over `src/foundry_cli/*/scripts/*_cli.py` (`OP_SPECS` AnnAssign tuple of `_op(...)` calls; dispatch-style CLIs like datasets count `if operation ==` branches; tuple-of-dict-literal catalogs like language_models) reproduces the exact 18-namespace table (admin 66, ..., ontologies 67, widgets 8, total 351). Note CLI path separators on Windows glob output are backslashes (`cli.replace("\\","/")`). Cross-check the largest catalogs against test-asserted counts (e.g. `test_operation_catalog_has_67_unique_operations`). Verified TESTCASE-023 (2026-08-11): AST counts matched the skill table exactly; 351 implemented + 4 widgets design rows = 355 documented.

## Improvement: content-accuracy probes — rule out probe artifacts before filing FAIL

Condition:
- When executing static-markdown QA cases via one-off Python probes and a case initially reports FAIL (or a catalogue block parser returns 0 pairs / all-AST-missing)

Action:
- Do treat each FAIL as a suspected probe artifact first and re-verify before classifying, checking: (a) path index after `glob` on Windows — namespace is `parts[2]` of the joined relative path or `split("/")[-3]` of the absolute path, never `-4` (which collapses every file under one `foundry_cli` key); (b) skill catalogue blocks are `**ns (N)** — res op, op; ...` — segments start after an em-dash and only RESOURCE names are backtick-wrapped, so parse with `re.search` (not `re.match`) on the segment and `[a-z_0-9]+` for ops (digit-bearing names like `time_series_property_v2` fail `[a-z_]+`); (c) string-vs-int comparisons in dicts (parse int before comparing); (d) case-sensitive fix/verb checks vs the actual skill casing (e.g. "Set operation/namespace" not "set ..."); (e) row-count slices off by the separator/header line (skill concept table has 23 data rows, not the fixture's 22 — a counting artifact in the TESTCASE doc, not a skill defect). Document the artifact as a probe correction in the execution log, not as a BUG-SUB. Verified TESTEXEC-023 (2026-08-11): 4 of 4 "FAILs" in the first consolidated probe were artifacts (path index -4, str/int compare, geo-block regex, row slice); final probe 24/24 PASS, no defects.
