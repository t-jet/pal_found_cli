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
