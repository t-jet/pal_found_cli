# Tech Lead — Improvement Memory

## Improvement: verify TESTCASE deliverable line anchors against the committed skill before approval

Condition:
- When approving a TESTCASE set whose content-accuracy cases cite specific line ranges of a static documentation skill (e.g. `.claude/skills/foundry/SKILL.md`), and the deliverable was authored against the working tree or an earlier blob

Action:
- Do verify every cited line anchor against the committed blob (`git rev-parse --short HEAD` + line counts + heading/table grep) before approving; section-level anchors matched exactly but inner-table/paragraph anchors drifted 1-8 lines in ~10 of 24 cases (KNW-TC-002 cited L12-37 vs actual L14-38; KNW-TC-003 L43-63 vs actual L44-65; KNW-TC-005 widgets row L60 vs actual L63; KNW-TC-010 datasets block L77 vs actual L85; KNW-TC-014 READONLY prose L151 vs actual L158). Also cross-check expected-value counts in the Test data table against the actual artifact (KNW-TC-002 title says "22 concept rows", actual 23). Content assertions were all accurate — classify as P3 non-blocking with an executor note ("treat anchors as approximate, verify content within the named section"), and keep the approval gate PASS unless a case references non-existent content.

## Improvement: verify skill deliverable presence before approving namespace CLIs

Condition:
- When reviewing a DEV sub-task for a new namespaced CLI/skill, and the DESIGN component breakdown lists "Claude skill and launcher for {namespace}"

Action:
- Do `git ls-tree -r --name-only {commit}` and grep for `.claude/skills/{namespace}/` before approving; prior namespace commits (62c269f connectivity/media-sets, 0c88063 sql_queries/streams) always ship SKILL.md + thin launcher in the DEV commit. Missing skill dir = P1 deliverable gap → Correction, even when the CLI code itself is fully approved. Cite DESIGN component-breakdown + story title + precedent commit as evidence. Also verify `pyproject.toml` package-data covers the metadata-allow-list.md and ruff E402 scope for the new namespace.

## Improvement: separate review-request test-count claims from actual count

Condition:
- When the reviewer reads a DEV review-request comment claiming a test count (e.g. "27 tests")

Action:
- Do count `def test_*` occurrences in the test file before citing the count; developer comments can misreport counts (this batch: checkpoints claimed 27, actual 25; data-health claimed 25, actual 27). Classify as P3 cosmetic, cite the actual count.

## Improvement: note SDK plain-int alias args as server-side-boundary only

Condition:
- When reviewing a CLI whose DESIGN says an int option has documented bounds (e.g. `--limit` "default 10, maximum 100") but the SDK model is a plain `int` alias (no Annotated bounds) and the CLI applies only `type=int`

Action:
- Do record the bound gap as P3 non-blocking follow-up (server enforces; graceful exit 1 via BadRequestError→exit 1), and state both the CLI-level and SDK-level verification evidence in the review comment. Do not make it a Correction unless the missing bound skips validation before side effects.

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
- Do ignore child-level `Blocked=Yes` flags when validating a parent story for closure: a closed child (e.g. CODEREVIEW-013) can still show `Blocked=Yes` because its own inbound `Blocks` link (e.g. DEV-013 → CODEREVIEW-013 LINK-00490) targets the child, not the story. Run `link list <child-id>` to confirm the link's target is the child itself; it does not block the parent. Parent closure only requires no `Blocks`/`Question`/`DependsOn` links on the story.
- Do EXPECT to manually restore the parent after a QUESTION approval gate: AT-5/AT-6 do NOT auto-restore the Blocked parent even when the question reaches terminal status AND its Blocks link is removed (confirmed four batches: TESTCASE-013/014, TESTCASE-015/016, TESTCASE-017/018). Sequence: post approval + Answer comments → transition question to Closed → remove the Blocks link (keep the Question link) → transition the parent Blocked→prior status. Do not wait for the automatic rules.
- Do verify which of the two QUESTION→parent links is the actual `Blocks` row before removal: the user/brief may label the wrong link ID (this batch: brief called LINK-00597/00599 "Blocks", but recon proved LINK-00598/00600 were Blocks and 00597/00599 were Question). Trust `link list` output, not the brief's link labels.

## Improvement: probe SDK kwarg names against real installed signatures before approval

Condition:
- When reviewing a namespace CLI whose OP_SPECS arg names are expected to map 1:1 to SDK kwargs, and the mock-driven unit tests pass

Action:
- Do `inspect.signature` every op with structured/JSON args against the INSTALLED SDK (not the vendored docs) and run a small runtime probe with valid-shaped inputs through the real SDK wrapper; a mock test asserting the wrong kwarg (e.g. `filters=` instead of SDK-required `file_import_filters=`) passes while the real call fails at validation. This batch caught a P1 (connectivity file_import create/replace can NEVER succeed — `ValidationError: file_import_filters Missing required keyword only argument`) only via the runtime probe; the vendored DESIGN table also carried the wrong arg name. Also probe pydantic `validate_call` extra-arg behavior before calling an extra flag a defect: `maybe_ignore_preview` strips unknown `preview` kwargs with only a UserWarning, and `validate_call` default is `extra='ignore'` — both downgrade what looks like a runtime error to a doc-only mismatch (P3).
- Do also check the SDK's per-op explicit `attribution` kwarg against the global `ATTRIBUTION_VAR` context header (http_client applies `attribution` header to ALL requests from the context var); an unreferenced per-op kwarg is usually P3 cosmetic when the context-var path satisfies the requirement.
- Do probe nested resource clients that are `cached_property` mounts by importing the resource module directly (`foundry_sdk.v2.widgets.release.AsyncReleaseClient`), NOT via `AsyncWidgetSetClient.Release.<method>` — the attribute is a `cached_property` object, so `inspect.signature`/`getattr` on it fails (`AttributeError: cached_property object has no attribute`). Discover the mount via `inspect.getsource` of the parent client's `__init__`/`cached_property`, and check `dir()` on the *module* (client classes live in per-resource modules, not exposed as top-level package attrs). (Batch 25: verified Release.delete/get/list this way; also confirmed instance-only attrs mean `dir(AsyncWidgetsClient)` prints nothing.)
- Do write runtime ACL probe scripts using the EXACT documented CLI flag surface (required kwargs as `--flag`, positionals positional, `-json` suffix for JSON args). A probe that passes a required kwarg positionally (e.g. `settings` JSON as positional on `set-widget-set-by-id`) fails with exit 1 at input validation BEFORE the ACL decision, masking the write-block (exit 8) you are trying to prove. Assert exit 8 for writes and ACL-pass (config/network error) for reads in the same probe run.

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
- Do verify four concrete code facts BEFORE writing the determination comment and keep version unchanged only if all hold: (1) pyproject [project.scripts] appends the new entry point without removing/renaming any prior one; (2) the new CLI imports only `common.*` shared infra (consume-only) and imports nothing from sibling namespace CLIs; (3) shared-infra diffs are purely additive (e.g. a new verb appended to the `_WRITE_VERBS` frozenset plus a regression test) with no existing symbol removed, renamed, or re-behaved; (4) a test asserts the operation-count contract (`len(cli.OP_SPECS) == N`). Absent any Incompatible API change, no major bump is required (SemVer additive). Cite each fact inline in the closure comment so the determination is falsifiable, not boilerplate.
- Do count OP_SPECS entries by AST-walking the `OP_SPECS: tuple[OperationSpec, ...]` AnnAssign and counting its `_op(...)` Call elements (resource/operation are the first two literal args). Naive tuple-element/regex counting over-counts nested per-op argument tuples (probe returned 6/35 instead of 5/15 in DEV-STORY-015/016 closure). Read the catalog's definition style before probing.
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

## Improvement: verify the in-flight correction landed before approving gated cases

Condition:
- When approving a TESTCASE set whose launcher/packaging cases are conditioned on an in-flight CODEREVIEW P1 correction (e.g. a missing `.claude/skills/<ns>/` skill deliverable), and the mission brief says the correction "has landed"

Action:
- Do `git log --oneline -3` + `git ls-tree -r --name-only HEAD -- .claude/skills/<ns>` + `git status --porcelain` first; confirm the skill dir is committed at the named HEAD before declaring the launcher cases valid and unconditional. Also verify the correction actually shipped with the expected contract (SKILL.md present, launcher thin/reexports packaged interfaces) rather than accepting the brief's claim. This approval gate (TESTCASE-019/020) confirmed f63a12c contains both skills and rechecked the deliverable's source-baseline note (which still said "in flight") was stale relative to HEAD — no correction to the deliverable was needed because the cases' precondition text is satisfied.

## Improvement: verify JSON-suffixed CLI inputs against SDK scalar aliases

Condition:
- When grooming a generated-SDK CLI design that names an option `--*-json` or assigns it an object/list shape

Action:
- Do inspect the authoritative SDK model alias and validate a representative value before approval; block readiness when the design requires an object but the SDK contract is scalar, because DEV and UNITTEST would otherwise encode incompatible behavior.

## Improvement: verify catalog required/optional marking against installed SDK signatures

Condition:

- When reviewing a namespace CLI whose OP_SPECS marks SDK arguments optional/required, or when a design table and vendored SDK source disagree with the installed SDK

Action:

- Do probe the installed SDK with `inspect.signature` (`required` marker / `Parameter.empty`) for every catalog entry carrying JSON or structured args; treat `required=True` in the installed SDK as authoritative even when DESIGN and vendored docs both list the arg optional (this review caught `build.search.where` mis-marked optional — runtime degrades gracefully to exit 1 via pydantic `ValidationError`, but the spec contract is wrong).
- Do classify spec-only mis-statements with graceful runtime failure as non-blocking follow-up (recorded on the review comment, not a Correction); reserve Correction for behavior that produces wrong exit codes, leaks secrets, or skips ACL. If the mis-statement changes exit-code class or skips validation before side effects, then it is blocking.

## Improvement: close review chains in block-removal-first order

Condition:

- When closing an approved CODEREVIEW whose paired DEV sub-task sits in Resolved with a bidirectional Blocks pair

Action:

- Do order the closure chain: (1) remove only the inbound `CODEREVIEW -> DEV` Blocks link, (2) close the CODEREVIEW, (3) `link list` the DEV to confirm no is-blocked-by rows remain, (4) close the DEV (Resolved→Closed DoD = "not blocked"). Preserve the outbound DEV→CODEREVIEW Blocks row and all RelatesTo links; both chains (013/014) closed cleanly with this order, re-confirmed for 015/016.

## Improvement: rule out FOUNDRY env leakage before calling test failures defects

Condition:

- When an independent review test run fails with exit-code/ACL mismatches (e.g. writes returning exit 8 instead of 0) that contradict the developer's reported pass

Action:

- Do run `Get-ChildItem Env:FOUNDRY_AGENTIC_CLI_*` (or `env | grep FOUNDRY`) before suspecting the code; a leaked `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` or `..._READONLY=true` in the shell makes the ACL correctly block every write op. Clear the leaked var and re-run — 16 of 16 failures were environmental (ACL defense working as designed), not defects. Document the leaked-var root cause in the review evidence comment so the reviewer's due diligence is falsifiable.

- Do re-confirm the same order for 017: link remove LINK-00577 (CODEREVIEW-017 -> DEV-017) exit 0, CODEREVIEW-017 Corrected -> Closed, link list DEV-017 showed only the outbound LINK-00576 Blocks row left, DEV-017 Resolved -> Closed exit 0. Note: the fix itself was verified in the working tree (uncommitted, HEAD 62c269f); flag commit-at-next-checkpoint in the approval comment, not as a blocking finding.
- Do re-confirm for 019/020 (2026-08-10, commit f63a12c): link remove LINK-00619 (019) and LINK-00638 (020) exit 0; CODEREVIEW-019/020 Corrected -> Closed with resolution=Done after posting the re-review evidence comment first (Closed DoD requires "re-review findings documented as a comment"); link list DEV-019/020 then showed only the outbound Blocks rows (LINK-00618/00637); DEV-019/020 Resolved -> Closed exit 0. Full regression re-verified independently at 1276 passed before approval.

## Improvement: resolve title-vs-evidence mismatch at closure via documented corrected surface

Condition:

- When closing a dev_story whose title/description contradicts downstream verified evidence (e.g. DEV-STORY-017 title says "15 operations", comments and release_notes and CODEREVIEW/DEVOPS probes establish 20)

Action:

- Do close on the verified evidence: confirm the corrected surface was independently cross-checked (architect three-source count, CODEREVIEW SDK-probe approval, DEVOPS installed-wheel probe), then state the corrected number and the mismatch explicitly in the closure evidence comment. Do not reopen the story or block closure for a stale title. (DEV-STORY-017/018 closed Resolved -> Closed 2026-08-10 with resolution=Done, closure comments 20260810-144913-tech-lead on both.)

## Improvement: verify documentation-skill reviews with the authored check scripts, not only the review-request claims

Condition:

- When reviewing a documentation-only DEV deliverable (e.g. the `foundry/` knowledge skill) whose review-request comment cites pre-review facts (file size, lint status, operation counts, N/N check results), and a verification script exists in the repo (e.g. `misc_dos/verify_skill_023.py`)

Action:

- Do re-run the author's own check scripts and an independent AST count against the committed blob (not the working tree) before approving; confirm `git diff HEAD -- <skill dir>` is empty so the review targets the same content UNITTEST-023 verified. This batch: `misc_dos/verify_skill_023.py` re-ran 46 checks / 0 failures and `misc_dos/count_ops_023.py` independently confirmed 351 implemented ops — both matched the review-request claims, so CODEREVIEW-023 approved with full independence. For content that cross-references ADRs (auth/ACL/TOON/exit codes), read each cited ADR file directly instead of trusting the skill's paraphrase — confirmed ADR-006/007/004/001/002/005 match Section 4/5/6/7 wording exactly. (Batch 29: CODEREVIEW-023 closed 20260811-044953-tech-lead, DEV-023 closed 20260811-045630.)

## Improvement: close duplicate QUESTION tickets via New→Duplicated with a RelatesTo link and evidence comment

Condition:

- When a QUESTION ticket (New, unassigned) is determined to be a duplicate of an already-answered QUESTION (same parent scope, same evidence base, all proposed options covered by the prior answer)

Action:

- Do verify duplicate-ness from ticket bodies (not just titles): same parent ticket, same reporter finding, same SDK evidence, and the prior answer resolving all listed options; post an evidence comment documenting the duplicate determination and the authoritative prior answer (e.g. QUESTION-043 answer 20260811-004954-tech-lead); create a `RelatesTo` link from the duplicate to the original (link id reported by the CLI — this batch LINK-00698); then transition `New → Duplicated` (allowed per question type-info, terminal). No Blocks link exists and no unblock is needed when the parent is already Closed (DEV-022 was Closed, resolution Done) — do not fabricate a blocking relationship. Leave the assignee unset rather than force-assigning when the ticket was never assigned. (Batch 29: QUESTION-042 closed Duplicated 2026-08-11, evidence comment 20260811-044947-tech-lead.)

## Improvement: answer SDK-drift QUESTIONS by re-probing installed AND vendored surfaces

Condition:

- When a QUESTION asks for a decision on a catalog whose DESIGN count conflicts with the installed SDK (schema drift), and the design was validated against an older vendored snapshot

Action:

- Do probe BOTH the installed SDK (`inspect.signature` on every resource client mounted by the namespace `_client.py`) and the vendored snapshot (list files + class methods) before deciding; resolve nested clients via the `cached_property` mount pattern and check `with_raw_response`/`ResourceIterator` return protocols for paged ops. Then correct the operation count to the authoritative installed surface per the established pattern (streams 17→15, connectivity 15→20, data-health 4→6, widgets 12→8) and record the corrected count on the blocked DEV and UNITTEST tickets so implementers don't trust the stale DESIGN count. Exclude newly-introduced SDK resources (e.g. DevModeSettingsV2) absent from the design as out-of-scope — that is a future story. (Batch 23: QUESTION-043 answered 20260811-004954, closed, LINK-00677/00678 removed, DEV-022/UNITTEST-022 stayed New with 8-op comments 20260811-005030/005035.)

## Improvement: remember question-type transition path and resolution-field absence

Condition:

- When closing a `question` ticket through In Progress (e.g. answering an addressed decision), or when setting resolution on terminal transition

Action:

- Do transition `New → Open → In Progress → Resolved → Closed` for questions; a direct `New → In Progress` is a ValidationError (only Open/Blocked/Canceled/Rejected/Duplicated allowed from New). Do NOT pass `--resolution` on question tickets — `resolution` is NOT in the question type's optional_fields (Batch 23 confirmed); plain `--status Closed` suffices. Note the question type has no `New → Blocked` transition either — blockers are recorded via Blocks link + comment only.

## Improvement: close dev_story Resolved tickets with evidence comment first, resolution field, preserved child Blocks links

Condition:

- When closing a `dev_story` from Resolved whose Resolved instructions say "Set resolution (Done/Canceled)" and "IF blocker link exists AND blocker resolved THEN remove the blocking link", and whose child CODEREVIEW sub-task shows `Blocked=Yes` from a preserved DEV→CODEREVIEW Blocks link

Action:

- Do run `workflow transitions dev_story Resolved` and `type-info dev_story` first (Closed must be allowed; `resolution` must be in optional_fields), then post the closure evidence comment with the `--author` role explicit, then `update --field resolution=Done`, then transition to `Closed`, and finally `get` the story to confirm persisted `Closed` + `resolution=Done`. Verify story-level link list has no Blocks/DependsOn/Question entries before closing; do NOT remove the child-level DEV→CODEREVIEW Blocks links (LINK-00656/00675 for 021/022) — those target children whose sources are Closed and are preserved by established pattern (013→022 closures); the child `Blocked=Yes` flag is a terminal-status artifact, not an open blocker. State the catalog correction (e.g. widgets 12→8 via QUESTION-043) explicitly in the closure evidence comment when title/release_notes are stale. (2026-08-11: DEV-STORY-021/022 closed Resolved→Closed, resolution=Done, evidence comments 20260811-043421/043435-tech-lead, both transitions exit 0, 19 links each unchanged.)

## Improvement: close feature Resolved tickets by verifying child QUESTION answers and blocking-link absence before resolution

Condition:

- When closing a `feature` ticket in `Resolved` (auto-entered when all linked DEV-STORYs reach terminal), whose Resolved instructions require reviewing linked QUESTION answers, setting resolution, checking blockers, and transitioning to Closed

Action:

- Do enumerate ALL children and links first via ticket-helper: `list --type dev_story --parent <feature>` (expect N/Closed), `list --type question --parent <feature>` (expect all terminal), and `link list <feature>` (expect only Contains/ParentChild to stories, FeatureContains to EPICs, and inbound RelatesTo — no Blocks/DependsOn/Question rows). Retrieve every QUESTION child's answer comment (subject + body) and incorporate the decisions into the closure evidence comment BEFORE transitioning. Sequence: post closure-evidence comment (author explicit) → `update --field resolution=Done` → `update --status Closed` → final `get` to confirm persisted `Closed` + `resolution=Done`. The tracker exposes no `transition` subcommand — status changes go through `update <id> --status <status>`. Feature type's `optional_fields` includes `resolution` (unlike `question` type). (2026-08-11: FEATURE-001 closed Resolved→Closed, resolution=Done, evidence comment 20260811-093056-tech-lead; 23/23 stories Closed, 5/5 QUESTIONS Closed, 55 links no blockers; answer comments QUESTION-001..005 incorporated verbatim.)
