# python-developer — improvement memory

## Improvement: circular-import when registering cross-module exception mappings

Condition:

- When adding an exception-class → exit-code (or similar) mapping inside `error_serializer` (or any low-level module) for an exception defined in a module that imports FROM that low-level module (e.g. `access_control_guard` imports `EXIT_ACCESS_CONTROL` from `error_serializer`).

Action:

- Do the import lazily inside the registration function (`_register_sdk_exceptions`) wrapped in try/except, never at module top level. This breaks the cycle because the function runs at import time only after the constants it depends on are already defined. Place the registration BEFORE any early `return mapping` in the same function so it always executes.

## Improvement: BUG-SUB-004 exit-code 8 gap pattern

Condition:

- When an exception type is documented in an exit-code taxonomy (ADR-001) with a constant (`EXIT_ACCESS_CONTROL = 8`) but `serialize()` returns the default code instead.

Action:

- Check `_EXCEPTION_TO_EXIT_CODE` map population and whether HTTP-classification fallback applies. No-HTTP-status exceptions (AccessControlError) must have an explicit map entry; the HTTP path cannot rescue them. Add a regression test that asserts BOTH the code AND the full stdout envelope (type, exit_code_name, message, call_id).

## Improvement: stdout-capture fixture is fragile for print_to_stdout=True

Condition:

- When writing an envelope test that uses the suite's `stdout_capture` autouse fixture with `print_to_stdout=True`.

Action:

- Do inline stdout capture (io.StringIO + try/finally restore) inside the test instead of relying on the shared fixture, which may be reset/ordered unpredictably across tests in the same class.

## Improvement: tests using a non-production calling convention can mask spec bugs

Condition:

- When a shared component has a canonical env-var transformation rule documented in the spec (e.g. SRS §5.2 `{NS}_{CLASS}_{OP}` kept verbatim) but existing unit tests call the component with a synthetic/humanised convention (e.g. `check("datasets", "create_dataset")` instead of `check("dataset", "create")`).

Action:

- Do align unit-test call arguments to the production calling convention that matches the env vars the tests set; don't let tests rely on internal verb-parsing heuristics to bridge the gap. When fixing a transformation bug, grep the test suite for ALL call sites of the affected method and verify each one matches its asserted env keys under the corrected code, because the old buggy behaviour may have made mismatched conventions pass by accident.

## Improvement: check isinstance(dict) before hasattr for dict-key extraction

Condition:

- When extracting a value from a response that can be either a dict or a Pydantic-style object, and the key name (e.g. "items", "next_page_token") could shadow a built-in dict method or vice versa.

Action:

- Do branch on `isinstance(response, dict)` (and `isinstance(response, list)`) BEFORE any `hasattr(response, <key>)` check, because every dict satisfies `hasattr(response, "items")` via its bound `.items()` method, returning the method object instead of the keyed value.

## Improvement: verify artifact/glob fixes against real build output, isolate with diff -w

Condition:

- When fixing a defect in a tracked config/workflow file (e.g. a publish.yml artifact glob), especially when the working tree already carries uncommitted whitespace or line-ending drift from earlier sessions.

Action:

- Do confirm the artifact format against real on-disk build evidence (e.g. `.ept/tmp/conda-channel` output) before editing, and confirm the change is content-only with `git diff -w` so pre-existing whitespace noise is not mis-attributed to your edit or accidentally broadened.

## Improvement: git diff --check flags CR at EOL when cr-at-eol not set

Condition:

- When fixing a trailing-whitespace gate failure (git diff --check) in a repo with mixed line endings (core.autocrlf=false, no .gitattributes, no cr-at-eol), where added lines end with CRLF while unchanged lines stay CRLF.

Action:

- Do strip trailing whitespace including the CR from the flagged added lines only (keep unchanged line endings intact), then re-verify with the exact gate command. Tools that append to project files (self-improvement memory appends, subagent memory updates) can re-introduce flagged lines, so re-run the strip and the gate after all such appends, as the last step.

## Improvement: hygiene test forbids `_cli.py`/`scripts/` in SKILL.md, not in references

Condition:

- When authoring doc-only skill content that splits operation detail into `references/*.md` and cites the CLI parser path (e.g. `.../scripts/pal_found_<ns>_cli.py`) as a source locator.

Action:

- Do keep parser/`scripts/` source locators OUT of `SKILL.md` (the repository-hygiene test scans only `pal-found-*/SKILL.md` for `python ..._cli.py` / `scripts/`) and place those source pins only in `references/*.md` parts, which the test does not scan.

## Improvement: batch `update --status` commands can ^C after already completing server-side

Condition:

- When running two chained tracker commands in one terminal call (e.g. `update --status Open; update --status "In Progress"`), the second can render as `^C` while the server already applied both transitions.

Action:

- Do verify actual current status with `get <id>` after a ^C in a chained batch before retrying; do not assume a failed transition. Re-running a now-invalid transition (`In Progress -> Open`) is the tell that the batch already succeeded.

## Improvement: validate CLI create arguments against SDK signature

Condition:

- When a CLI operation wraps an SDK create method and fails because a required SDK argument is absent.

Action:

- Do compare the local SDK docs and installed method signature, then test both parser requirement and exact async SDK call arguments.

## Improvement: preserve cursor semantics for SDK async iterators

Condition:

- When a CLI exposes page tokens for an SDK method returning `AsyncResourceIterator`.

Action:

- Do use the SDK's public raw-response wrapper to fetch and decode one page per request; test an empty page with continuation, the initial cursor, page bounds, and the returned next cursor across affected operations.

## Improvement: document CLI page shape, not SDK page model

Condition:
- When source-backed skill records describe paginated operations

Action:
- Do inspect CLI pagination helper and formatter before writing result guidance. State stdout item list, stderr continuation metadata, and SDK page model separately; check empty pages with a continuation token.
- Do explain each newly listed paging flag in a parameter note outside the input inventory; the offline gate requires guidance for every flag and a flag name alone does not tell readers its effect.
- Do retain SDK page fields needed to interpret records as ordered per-page stderr metadata, and test item order plus metadata order across multiple pages.

## Improvement: check resource aliases before narrowing target prose

Condition:
- When an SDK operation accepts a resource RID alias and examples show only one resource type

Action:
- Do read the alias definition and docstring, then describe all supported resource categories in behavior and input guidance. Label a narrow example as one valid case.

## Improvement: isolated SDK reader acceptance

Condition:

- When source-blind SDK reader task requires independent namespace acceptance

Action:

- Do copy owning skill into isolated snapshot, hash snapshot and prepared SDK, run public composed FoundryClient routes through denied-network fake transport, and label detached resource fixtures as smoke only.

## Improvement: inspect iterator API before rejecting page access

Condition:

- When SDK method annotation says `ResourceIterator` but guide reads `.data` or `.next_page_token`.

Action:

- Do inspect iterator class properties and page-fetch timing, then run guide call through composed client MockTransport before filing route defect. Return annotation alone insufficient.

## Improvement: measure example coverage without test files

Condition:

- When docs examples need unit coverage but hosted runtime modules unavailable.

Action:

- Do measure non-test modules with `coverage report --omit '*test*.py'`; invoke actual entry points through narrow dependency stubs and assert rows, modes, and failures. Label hosted runtime unexecuted.

## Improvement: semantic schema checks before example writes

Condition:

- When prepared-runtime example groups or sums pandas values before a dataset write.

Action:

- Do test nonnumeric input and output values against actual example code; reject wrong types before write with a check that still runs under optimized Python. Coverage percent alone cannot prove valid output schema.

## Improvement: SDK source fences versus offline reader prose

Condition:

- When generating offline API model pages from SDK definitions containing public links or placeholder comments

Action:

- Do keep exact SDK source in fenced blocks, add complete local meaning in reader prose, and record per-symbol source/page hashes with independent review pending. When a Python alias is `Any`, check pinned SDK documentation for type/encoding tables and emit source-backed valid JSON examples plus documentation hash. Do check source fidelity separately from prose tests that normalize optional attribution links.

## Improvement: root SDK mock transport must cover lazy clients

Condition:

- When testing an operation through public FoundryClient with a patched HTTP-client constructor

Action:

- Do keep constructor patch active through nested resource access and request; root client constructs resource clients lazily. Assert fake transport handled request before claiming offline success.

## Improvement: compare inventories to distributed records

Condition:

- When testing preservation of documented operation IDs against frozen baseline

Action:

- Do extract IDs from actual distributed operation headings and compare exact sorted hash; don't hash another frozen constant as the "actual" result.

## Improvement: uncertain REST write fixture

Condition:

- When offline SDK guidance handles a lost upload or commit reply

Action:

- Do mutate fake server state before raising transport timeout, reconcile through known RID and staged or branch reads, and assert exactly one mutation; never let a passing fixture hide automatic replay.

## Improvement: unmeasured ticket time

Condition:

- When subtask DoD requires time in frontmatter but actual contributor hours were not measured

Action:

- Do ask responsible lead for workflow treatment before Resolved. If approved, enter only a measured partial minimum in `time_spent_hours`, name its exact interval in a comment, and exclude unknown historical hours. Don't copy one subtask's interval to another or substitute estimate hours.

## Improvement: integer request timeout cannot certify wall deadline

Condition:

- When SDK request timeout accepts positive whole seconds and app promises a shorter elapsed-time budget.

Action:

- Do stop before call if fewer than one whole second remains; pass integer timeout no greater than remaining whole seconds; recheck clock after response before claiming complete. Preserve partial result on overrun and test slow or noncooperative transport. Don't promise hard preemption of a blocking call.

## Improvement: verify review defect against current tree before re-fixing

Condition:

- When acting on a codereview Correction where reviewer assessed an older commit and later commits landed after review.

Action:

- Do verify defect against current tree first: git status --short, diff reviewer-commit..HEAD for target files, recount from actual record headings. If already fixed, don't rewrite — cite fix commit + independent count + gate result as correction comment, then move to Corrected.

## Improvement: review-time gate count is historical not a target

Condition:

- When reviewer ACTION REQUIRED names a specific gate result (e.g. "stay 23 passed") but the suite grew since review.

Action:

- Do run the current gate, assert relevant checks pass with exit 0, report actual count and exit code as evidence; don't treat the review-time count as a target or a failure signal.

## Improvement: re-verify bug-fix artifact before advancing a QA-retested bug ticket

Condition:

- When advancing a BUG-SUB (Open -> In Progress -> Resolved -> Closed) whose fix was authored earlier and QA already posted a retest comment.

Action:

- Do independently confirm the claimed artifact exists on disk (file_search), that the cited proof file content matches the claim, and re-run the exact fixture/gate to capture a fresh exit code before writing the DoD comment; don't rely on the QA comment alone as the closure evidence.

## Improvement: bug_subtask Resolved instruction requires removing own Blocks link

Condition:

- When a BUG-SUB in Resolved still has an outbound `Blocks` link (e.g. to a TESTEXEC) and the Closed DoD says "Ticket not blocked (no active blocks links)".

Action:

- Do `link list <BUG-SUB>` to get the LINK id, `link remove <LINK-id>`, then re-run `link list` on the bug and on the blocked target to prove only the bug's own link was removed; don't remove a sibling bug's Blocks link.

## Improvement: development Resolved -> Closed batch closure

Condition:

- When closing several `development` sub-tasks from `Resolved` after their paired code reviews already closed.

Action:

- Do pre-verify the whole batch with one `list --type development` and one `list --type codereview` (both exit 0) instead of per-ticket `get`; the output already has the Blocked column, so only run `link list <DEV>` to confirm no `Blocks` link. Missing `Contains` link from the parent story is not a Closed DoD blocker. Then per ticket: post evidence comment + `update --status Closed` (one ticket at a time). Expect `update` output `allowed_transitions: [Resolved]` and `definitions_of_done: []` as the success tell.

## Improvement: drive many tracker CLI mutations from a subprocess driver

Condition:

- When advancing many tickets (e.g. a 15-ticket unittest wave) each through several `comment create` + `update --status` calls from PowerShell.

Action:

- Do write a small Python driver in `.ept/tmp` that shells out to `python .ept/tools/tracker/tracker_cli.py ...` via `subprocess` (list args, never a shell string), run the real verification first and abort with no transitions on any non-zero exit, and stop on the first failing CLI call. Don't hand-type long Markdown `--text` in PowerShell: backticks, `"` and apostrophes corrupt it (a stray backtick made a word a command and broke the argument). Keep `\n` inside the payload; it is decoded by the CLI.

## Improvement: unittest ticket blocked by a stale parent-story block

Condition:

- When a `unittest` sub-task's parent DEV-STORY is `Blocked` because its recorded blocker (BUG-SUB/DEV) is already Closed but the story was never returned to Development.

Action:

- Do create a QUESTION sub-task addressed to tech-lead, add `Blocks` + `Question` links to the unittest ticket, then move it New -> Open -> Blocked (record blocker id + prior status as a comment) and leave it blocked. Don't verify against or fabricate closure for content whose parent is still blocked. Note: the `child_blocker_created` auto-rule cannot fire from a `New` ticket (New only allows Open/Canceled/Rejected/Duplicated), so promote to Open first and then `update --status Blocked` manually.

## Improvement: doc-content unittest verification re-run

Condition:

- When a `unittest` ticket verifies authored offline skill documentation content (not executable code) and must be re-verified before Open -> In Progress -> Resolved -> Closed.

Action:

- Do run the acceptance set = `python -m pytest tests/test_offline_skill_gate.py tests/test_documented_examples.py tests/test_skill_documentation.py tests/test_repository_hygiene.py -q` with cwd set to `pal_found_cli_skills`, plus the independent probe `python .ept/tmp/verify_wave.py <namespace>`; the probe gives frozen-op reachability, one-record-per-op, example parse, <=300-line leaves, link resolution and install block per namespace. Note pytest needs the skill-folder cwd while the tracker CLI needs repo-root cwd, so run the driver with explicit per-call cwd, not a shared shell Set-Location (the shell cwd persists across terminal calls and then breaks the other tool).

## Improvement: unittest closure advances the parent story automatically

Condition:

- When closing the last `unittest` sub-task of a DEV-STORY already in Development (DEV and CODEREVIEW closed).

Action:

- Do confirm the dev_story AT-1 rule (`all_children_reach_status`, child_filter types [development, unittest, codereview], source Development, target QA) and then verify the parent actually moved to QA with `get DEV-STORY-XXX` after the close; do not attempt a manual Development -> QA transition.

## Improvement: closing a question does not auto-unblock a hand-Blocked ticket

Condition:

- When a `question` reaches Closed/Resolved and its `Blocks` links target tickets that were moved to `Blocked` by a manual `update --status Blocked` (no persisted `prior_status`).

Action:

- Do verify the target's actual status with `list`/`get` and re-read `link list <question>` before claiming "unblocked". If the `Blocks` link is still present and the target is still `Blocked`, don't report it as unblocked: the auto rule AT-6 restores `prior_status`, which is unset for a manual block, and AT-5 (`all_blockers_cleared`) only evaluates when the blocked ticket itself is next mutated. Post the observed state and note that removing the terminal blocker's `Blocks` link and returning the ticket to its prior status is the owner's explicit `Blocked`-status step.

## Improvement: fix a leak plus harden the gate with a fail-then-pass proof

Condition:

- When a defect is "content passes the current gate because the gate pattern is too narrow" (e.g. distributed skill ships `DEV-046` while the regex only forbids `FEATURE|DEV-STORY|CODEREVIEW-<n>`).

Action:

- Do three things in one pass: (1) fix the content, (2) extend the gate pattern to the whole internal-id family (bare sub-task prefixes plus longer forms) and scan the full distributed tree (`rglob("*.md")`, not just `SKILL.md`), (3) prove the gap by temporarily injecting the label and showing the new gate fails (exit 1) while the old gate still passes (exit 0), then revert and re-run green. Report all three exit codes as evidence.

## Improvement: collision suffix overlaps author alphabet

Condition:
- When filename-based IDs combine a sanitized name with a retry suffix, and suffix characters can appear in names

Action:
- Do reserve separators outside the sanitizer alphabet, mark the new ID format, and test mixed names, same-second retries, concurrent writes, and legacy references. Do not claim exact author recovery for ambiguous legacy filenames without stored metadata.

## Improvement: verify a fix commit by extracting its tree, not the working copy

Condition:

- When a bug fix already exists as a commit on an unmerged branch and you must document root cause, fix and verification without modifying code.

Action:

- Do git archive <sha> | tar -x -C .ept/tmp/<name> into a scratch tree and run probes against that tree with PYTHONPATH=src, plus the same probe against the parent commit's tree so the defect is shown present before and absent after. Never test through the working copy, which sits on main and does not contain the fix.

## Improvement: system python may lack project deps; use the venv interpreter for probes

Condition:

- When a scratch tree's test or probe run fails at import with ModuleNotFoundError for a project dependency (e.g. toon_format), or the system interpreter only has an older SDK.

Action:

- Do rerun with the workspace venv interpreter (.venv/Scripts/python.exe) which carries the full dependency set, and record the SDK version in the evidence comment. Do not report the import failure as a defect in the fix.

## Improvement: a reuse-free wire probe must supply schema-valid fixtures

Condition:

- When writing an independent CLI-to-wire probe for an SDK-calling CLI, with the intent of not reusing the branch's own test helpers.

Action:

- Do read the SDK schema or the branch fixtures for the exact request payload shape; a minimal placeholder config (e.g. {type: statusCheckConfig}) fails SDK validation, makes requests empty, and yields a false negative. Print exit code and captured stdout on the failure path so an empty capture is distinguishable from a real omission.
