# QA self-improvement memory

## Improvement: independent review must check submodule push + parent gitlink separately

Condition:

- When independently reviewing a QA batch where the deliverable lives in a git submodule (e.g., pal_found_cli_skills) and QA validated the submodule worktree HEAD

Action:

- Do treat "worktree content validated by QA" and "submodule integrated for deploy" as two separate facts: verify worktree HEAD content (git ls-tree, SKILL.md scans, pytest) AND separately verify (a) the parent repo gitlink (`git ls-tree HEAD <sub>` vs worktree `rev-parse HEAD`, `git submodule status` `+` prefix = uncommitted), and (b) whether the submodule commits are pushed (`git status -sb` ahead N, `git rev-parse origin/main`).
- Do NOT assume QA's validated HEAD is deployable; report uncommitted parent pin + unpushed submodule commits as a deployment-blocking ISSUE even when QA closure is fully correct.

## Improvement: question batch resolution workflow

Condition:

- When QA resolves QUESTION tickets after Project Owner answers, batch mode (14 tickets)

Action:

- Do resolve each against owner answer comment (author project-manager, dated answer); log a `Resolved` comment citing the owner comment ID; transition via `update <id> --status Resolved --author qa-engineer`.
- Do verify the final status of every ticket via `get` before reporting.
- Do flag owner-declined/skipped test cases (e.g., PUB-TC-006/007/020) and publishing anomalies in the resolution comment as separate concerns; never block question resolution on them.

## Improvement: TESTCASE closure after unblocking

Condition:

- When QA closes TESTCASE sub-tasks whose prerequisite questions are Closed (skill-distribution stories, e.g. TESTCASE-030/031/032)

Action:

- Do read each linked QUESTION owner/comments (question answer) and the parent DEV-STORY AC plus design docs before authoring scenarios.
- Do author Gherkin Given/When/Then cases as a deliverable under `.ept/docs/deliverables/qa/` named `TESTCASE-XXX-test-cases.md`, register it in `document_index.md`, and post plan + test-case comments on the ticket.
- Do close via Open -> In Progress -> Resolved -> Closed; set `--field time_spent_hours=N` before In Progress->Resolved; confirm no active is-blocked-by links before Resolved->Closed.
- Do NOT publish chat/transcript JSONL; keep evidence local only.

## Improvement: owner-scoped credential absent in QA env

Condition:

- When a TESTEXEC run needs authenticated GitHub ops (tag/release/asset create, collaborator read, branch-protection read) that the owner authorized but the QA env has no credential (GITHUB_TOKEN/GH_TOKEN NOTSET, no gh CLI, no token file, git credential.helper disabled; REST 401 on collaborators and branches/main/protection)

Action:

- Do NOT fabricate credentials or evidence; never claim authenticated cases pass. Verify env absence explicitly (env vars, gh, token file, git config) and capture the 401 REST responses as evidence.
- Do create one QUESTION sub-task to project-owner offering two options: (a) provision an owner-scoped credential, or (b) decline the authed cases like owner-declined mutation cases (006/007/020); add Blocks link + Question link; parent auto-Blocked.
- Do log executable anonymous cases as PASS with fresh evidence, mark declined cases owner-declined/skipped, mark authed cases BLOCKED(cred-absent), and record blocker comment with blocker ID + prior status before ending.

## Improvement: provided credential may still lack admin-read scope

Condition:

- When QA resumes an authed TESTEXEC case (e.g., PUB-TC-012 branch-protection detail) after the owner provisioned a credential, but the token is fine-grained/limited (X-OAuth-Scopes empty; /repos/{repo}/branches readable, yet /branches/main/protection -> 403 and GraphQL branchProtectionRules -> "Resource not accessible by personal access token")

Action:

- Do verify scope honestly: probe /user, /repos/{repo}, collaborators (which may PASS), then branch-protection detail endpoints; capture 403/404/GraphQL denial as evidence.
- Do classify the case PARTIAL (not PASS) when the required policy detail is unreadable; never claim the full case passed on partial flag data.
- Do raise a new QUESTION to the owner (blocks parent) offering: (1) admin-read-scope credential, or (2) explicit acceptance of partial evidence as owner-accepted PARTIAL; keep TESTEXEC Blocked until owner decides — do not close with a non-passing non-declined case.

## Improvement: interrupted tracker comment POSTing

Condition:

- When `comment create` output shows an interrupt (`^C`) after posting, then a retry is issued

Action:

- Do re-`get` the comment list before retrying; if the first comment already posted, update the retry comment to mark it superseded/duplicate instead of leaving two similar blocker records.

## Improvement: doc-only skills QA evidence workflow (FEATURE-011 stories)

Condition:

- When QA executes TESTCASE/TESTEXEC for doc-only skill conversion stories where the repo change is pure documentation/removal (no runtime behavior to run)

Action:

- Do verify with git-tree evidence first: `git ls-tree -r HEAD --name-only .agents/skills` proves no .py/scripts/ remains; confirm deletion history with `git log --all --diff-filter=D --name-only --pretty=format:%h %s -- <glob>`.
- Do scan SKILL.md content with exact-string checks (conda `-c t-jet`, pip, uv lines; stale-ref regex `python\s+[\w/._\-]*_cli\.py`), and verify tool-side op counts from the installed CLI `--help` strings (authoritative) plus parser dumps, not just docs.
- Do run the unit-test suite at HEAD as the authoritative test check (16 passed) and save evidence JSON to `.ept/tmp/` for durable linkage in comments.
- Do advance TESTEXEC New→Open→In Progress→Resolved→Closed only after posting per-case PASS/FAIL matrix with evidence file paths; then confirm the parent DEV-STORY auto-advanced QA→Deployment (AT-1) — do not force the story transition.

## Improvement: semantic coverage for offline skill guidance

Condition:

- When QA plans coverage for Foundry skills that explain CLI operation meaning to offline agents

Action:

- Do compare every documented operation and input with a pinned installed CLI parser/dispatch inventory in both directions, and check copied local links without network access.
- Do require source-backed human review of Foundry effects, parameter meaning, result interpretation, and failure uncertainty; parser and heading checks alone cannot prove semantics.
- Do use safe mock or recorded-response agent exercises across each namespace, including pagination, permission failure, pending results, and timeout uncertainty.
- Do label a reader result provisional when the skill-only boundary and public-network denial were described but not enforced; retain the formal TESTEXEC gate until approved cases, isolated inputs, and observed outputs are recorded.
- Do record sorted file-hash manifest for each isolated reader snapshot and keep an independent reader's files separate when earlier evidence has unclear provenance; distinguish cooperative in-process network denial from an OS sandbox.
- Do refresh signed record, CLI, and SDK hashes only after reviewing current source diffs and related defect retests; a stale hash on corrected code is a prompt to recheck the verdict, not proof the old failure remains.
- Do run the offline gate on both the source tree and a freshly copied skill bundle after concurrent edits; report any unrelated namespace failure separately from the reviewed ticket.

## Improvement: verify a CI-fix BUG independently at Resolved

Condition:

- When QA verifies a `bug` ticket whose fix is a committed CI/dependency-policy change and the DevOps comment claims a green run

Action:

- Do verify three independent layers, not the comment: (1) repo artifact — `git ls-tree -r HEAD` + `git show --stat <commit>` + `git show HEAD:<file>` confirm the file is committed at HEAD with the claimed content (reason + expiry) and that the branch is pushed (`git status -sb` clean); (2) gate integrity — grep the workflow for `|| true`/`continue-on-error`/inline `--ignore` and read the exact run lines; (3) live CI — query the GitHub run for the HEAD sha and record the workflow `conclusion` plus per-job `conclusion`, then read the scan step log for the policy-file line and the vulnerability count.
- Do independently re-check the remediation premise (e.g., PyPI JSON API for latest release and scanner `requires_dist`) to confirm no fixed release exists before accepting a time-bound suppression as acceptable.
- Do post one Markdown verification comment with the run/job table, AC check table, and DoD checklist; then `update <id> --status Closed --field resolution=Done`.
- Do NOT trust claimed run/job IDs — re-derive them from the HEAD sha; a claim about a run that does not match the commit under review is not evidence.

## Improvement: independent repro of comment-id allocation must account for auto comments

Condition:

- When writing an independent repro or test for tracker comment-id uniqueness under a frozen same-second clock (e.g. BUG-005 same-second writes), reusing the ticket create author for the manual comments.

Action:

- Do isolate the manual-comment author from the create author (create the ticket under a different author) OR explicitly account for the create-time auto comment consuming the base id, before asserting that the first manual comment has the unsuffixed base id; otherwise a correct fix reads as a failure and wastes a cycle.
- Don't gate an aggregate check on a shared failures list; count the per-item PASS results in a local counter so earlier unrelated failures do not cascade into a false aggregate failure.

## Improvement: offline-skill TESTCASE design batch closure pattern

Condition:

- When designin and closing TESTCASE sub-tasks for offline skill/content stories (e.g. DEV-STORY-041..055) that each have a paired TESTEXEC and comments-only output is required

Action:

- Do post one combined "readiness, plan and test cases" comment per ticket (scope + docs reviewed + plan + preconditions + Gherkin cases TC-NNN-01..N plus NEG cases + expected outputs + DoD checklist), then advance New->Open->In Progress->Resolved (`--field time_spent_hours=untracked`)->Closed, posting a short "Resolved to Closed check" comment that cites the plan-comment id, the single parent Contains link id, and "no Blocks / no QUESTION".
- Do derive cases from the frozen per-namespace register `pal_found_cli_skills/tests/test_offline_skill_gate.py` (FROZEN_OPERATIONS) plus the story scope split, and ground each case in real `references/*.md` filenames.
- Don't create deliverable files when the user says record work as comments only; the `testcase` type stores cases as comments, not files.

## Improvement: tracker --text multiline from PowerShell

Condition:

- When posting long multi-line Markdown as `comment create --text` from PowerShell on Windows

Action:

- Do write the whole body inside one single-quoted PowerShell string using literal `\n` (backslash-n) as the line separator for the CLI to decode; verify once with `comment get` that newlines rendered.
- Don't include literal apostrophes, `$`, or stray backslashes in the body (use "does not" instead of the contraction).
- Don't treat the `^C` echoed after a tracker command as failure: re-`get` the ticket to confirm the status, since the transition often succeeded.
- Don't chain tracker operations with `;`; run one documented CLI command per invocation.

## Improvement: cross-namespace SDK mock shapes

Condition:

- When one QA probe compares paginated or HTTP error behavior across Ontology, Admin, and Filesystem collectors

Action:

- Do model each namespace's actual page envelope (`data` for Ontology, `items` for Admin/Filesystem) and attach HTTP status at `exception.response.status_code`; inspect extraction helpers before interpreting a mock failure as a defect.
- Do assert envelope exit code and returned process code together, including generic TypeError and OSError errno branches.

## Improvement: semantic review hashes during concurrent doc edits

Condition:

- When several agents edit different skill namespaces while QA signs source-hashed operation rows

Action:

- Do recalculate each owned row from current record body, CLI file, and SDK file; verify all three hashes and exact line locators before reporting a namespace result.
- Do report owned namespace results separately if aggregate register generation stops on another namespace's stale hash; ask that namespace owner to refresh it after edits settle.
- Don't treat a clean local review as a passing 351-row aggregate gate or feature sign-off.

## Improvement: Windows tracker races need repeated mixed-process QA

Condition:

- When verifying tracker fixes that replace shared CSV or YAML files while ticket and link processes run concurrently

Action:

- Do repeat mixed ticket/link subprocess tests on fresh isolated fixtures; check child exits, unique IDs, retained rows, and follow-on IDs through CLI.
- Do run full tracker suite after focused PASS; one clean race run can miss Windows read failures.
- Do inspect both writer and reader paths: atomic replace needs bounded PermissionError retry, while in-place CSV truncation can expose header-only data.
- Do test persistent read denial returns bounded file-error exit 4, then keep parent defect open until every linked regression passes.

## Improvement: serialize tracker writes

Condition:

- When creating tracker links or comments while agents share tracker state

Action:

- Do run one tracker mutation at a time, then check returned ID with `link list` or `comment list`; coordinate write windows with other agents. Concurrent link creation can return same link ID for distinct links.

## Improvement: isolated candidate imports

Condition:

- When QA tests a release candidate beside an installed editable checkout of the same Python package

Action:

- Do put candidate `src` first on `sys.path` or `PYTHONPATH` before the first test run, print imported package `__file__`, and assert the path points into the candidate before counting test results.
- Do compare candidate commit and clean status with the advertised remote ref; report parent gitlink and release tag separately.

## Improvement: SDK model semantic review beyond hashes

Condition:

- When reviewing generated local SDK model pages against a frozen SDK source, especially name-only docstrings or localized summaries

Action:

- Do compare each symbol's full source description, exact definition, field names and wire aliases, linked types, and consuming operations; record per-symbol meaning verdict and page/source hashes. Do not approve from counts or hashes alone.
- Do treat a copied SDK description that conflicts with field use as a local meaning defect, then retest the corrected page at an immutable candidate commit and verify the affected-page diff before carrying other verdicts forward.

## Improvement: verify real semantic ledgers before release

Condition:

- When a feature has source and semantic review ledgers plus passing structural tests

Action:

- Do count real accepted, pending and failed rows, verify every recorded content hash against the candidate, and check that final tests consume the real ledgers. Don't treat tests of synthetic guard inputs as proof that the candidate passed its acceptance gate.

## Improvement: stream fixtures need real framing

Condition:

- When reviewing SDK methods that return SSE context managers or binary streams

Action:

- Do use fake transport responses with actual declared content type and framed payload, then exercise ordinary and wrapper lifetime, typed events, error events, and finite budgets. Don't accept a raw-response JSON decode fixture as proof of SSE behavior.
- Do distinguish a decoded-event byte budget and between-event deadline from a hard wire-byte or stalled-event bound; report the remaining limit explicitly.

## Improvement: source review and formal QA stay separate

Condition:

- When an independent source reviewer runs diagnostic fixtures before TESTCASE and TESTEXEC close

Action:

- Do record per-ID semantic verdict, reviewer, source and asset hashes in review evidence; keep formal QA status pending and QA agent unset until approved test design and execution meet their workflow DoD.
- Do label fixture outcomes diagnostic and verify TESTCASE and TESTEXEC statuses through tracker CLI before claiming QA acceptance.

## Improvement: verify preview per operation

Condition:

- When SDK fixtures omit `preview=true` for beta endpoints

Action:

- Do confirm each endpoint's requirement in its official API reference before marking omission FAIL. Mark comparable but unverified endpoints UNCERTAIN and state inference. A passing mock that expects no preview does not prove a live request works.

## Improvement: check server bounds against frozen SDK text

Condition:
- When a frozen SDK docstring describes a request list or batch limit

Action:
- Do compare current official endpoint bounds, empty input errors, and duplicate handling with the local contract. Use a mock transport to see whether the SDK validates or forwards boundary inputs. Record version uncertainty where needed; don't treat a passing success fixture as boundary coverage.

## Improvement: tracker snapshot branches need live ID recapture check

Condition:
- When QA reviews a tracker data branch while agents keep writing to the live tracker

Action:
- Do compare ticket counts, recent comments, and new link IDs through the documented CLI in both branch and live checkout before calling the branch merge ready. A branch can be internally consistent while a later live link reuses an ID assigned by the branch repair.

## Improvement: exercise a fix from its own commit tree

Condition:

- When QA verifies a bug fix that lives on a feature branch while the workspace worktree stays on main

Action:

- Do extract the reviewed SHA (`git archive <sha> | tar -x -C .ept/tmp/<dir>`) and prepend its `src` to `PYTHONPATH`, then prove resolution by printing the imported module path; never trust a suite run against the worktree import. Use `python -B` so stale bytecode cannot mask edits. Explain an extraction-only failure (for example `git check-ignore` tests over `git archive`) by re-running that file in the real repository instead of filing a defect.

## Improvement: discharge outbound Blocks links at bug closure

Condition:

- When QA closes a bug that still holds outbound `Blocks` links to dependent stories

Action:

- Do remove the link IDs owned by the fixed bug once the fix is verified, keep every `RelatesTo`, and leave other bugs' `Blocks` links to the same story alone. Record the instruction clause, the dependent acceptance criteria and any sibling closure precedent in one comment, then re-check each dependent's Blocked flag and report it. Do not treat a fix awaiting merge to main as a reason to keep the ticket open.

## Improvement: verify a doc/skill fix hash at the DEPLOYABLE pin, not a branch snapshot

Condition:

- When QA verifies a bug whose fix is a doc/skill page and the developer quotes a page SHA256 plus an accepted whole-page report

Action:

- Do compute the page hash at the deployable pin (parent `git ls-tree HEAD pal_found_cli_skills` for the gitlink, then skills `git rev-parse HEAD` + sha256 the page), and compare to the quoted hash; match only counts when the quoted hash equals the page hash at that pin.
- Do prove the fix commit is merged with `git merge-base --is-ancestor <fixcommit> <skillsHEAD>` (exit 1 = unmerged) and `git grep <required-string> <skillsHEAD> -- .agents` (0 matches = fix absent).
- Don't accept a hash that matches only an unmerged branch worktree (e.g. `.ept/tmp/feature015_integration` or `origin/feature015/*`); a merge can regress HEAD back to the original broken hash, so re-hash HEAD after any merge before closing.
- Do treat "hash matches an unmerged branch snapshot" as a failed verification: keep the outbound `Blocks` link, leave status Resolved, and escalate via a QUESTION to the fix owner.

## Improvement: QUESTION auto-block needs a Blocks link, not just the Question link

Condition:

- When QA raises a QUESTION sub-task and expects the parent to auto-block (AT-4)

Action:

- Do create BOTH links from the question to the parent: `Question` (Asks About) AND `Blocks`; only the `Blocks` link triggers `child_blocker_created`, saving `prior_status` and moving the parent to Blocked.
- Don't assume the parent blocks on question creation or on the Question link alone; verify with `get` that the parent shows Blocked and the restored `prior_status`.

## Improvement: tracker `^C` echo after a mutation is display noise

Condition:

- When a tracker `create`/`update` prints `^C` and returns no YAML

Action:

- Do re-run `get` (or `list --parent <id>`) exactly once to confirm the mutation landed before retrying; the operation usually succeeded. Don't create a duplicate ticket or comment on the next attempt.
