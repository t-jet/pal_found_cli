# TESTCASE-025 - Public GitHub repository QA test cases

## Scope

These cases cover DEV-STORY-025 and the publication of the three canonical
repositories:

- `https://github.com/t-jet/pal_found_cli`
- `https://github.com/t-jet/pal_found_cli_tool`
- `https://github.com/t-jet/pal_found_cli_skills`

The suite verifies anonymous read and clone access, contribution surfaces,
public tags and releases, restricted writes, secret safety, branch protection,
rollback, error handling, and concurrent access. It does not change repository
visibility, protection rules, issues, pull requests, tags, or releases unless
the repository owner explicitly authorizes the named case.

The current implementation baseline is root commit `240898c5`, tool commit
`370c971b`, and skills commit `34b6c404`. All three repositories are public and
anonymous reads work. None currently has a tag or release, so the positive
release-asset case needs a fixture before TESTEXEC-025 can run it.

## Source baseline and traceability

- [BA-ANA-002](../business_analysis/BA-ANA-002-business-analysis.md):
  BR-002-01..06 and AC-002-01..05.
- [SA-ANA-002](../architecture/SA-ANA-002-architecture-analysis.md): public
  GitHub hosting, anonymous verification, restricted writes, and secret review.
- [BA-DES-002](../business_design/BA-DES-002-business-design.md):
  BR-D-002-01..07 and AC-D-002-01..06.
- [SA-DES-002](../architecture/SA-DES-002-technical-design.md): GitHub REST and
  git verification, branch protection, public releases, secret safety, and
  reversible visibility.
- [DEV-025 publication checklist](../development/DEV-025-publication-checklist.md):
  per-repository publication and rollback checks.
- Split prerequisite: DEV-STORY-024, verified at root `240898c5` with tool and
  skills gitlinks pinned to the commits above.

## Preconditions

### Safe anonymous cases

- Git 2.40 or newer, Python 3.11 or newer, and HTTPS access to GitHub.
- `GIT_TERMINAL_PROMPT=0`, empty `GIT_ASKPASS`, and an empty git credential
  helper for every anonymous git command.
- No GitHub token, cookie, SSH agent, or cached credential in the test process.
- Temporary clones and evidence files live only under `.ept/tmp`.
- Record local and UTC start/end timestamps, OS, git version, Python version,
  repository URL, resolved HEAD, exit code, HTTP status, and stderr/stdout.

### Owner-controlled cases

- Written repository-owner authorization names the repositories, maintenance
  window, test account, allowed mutations, rollback steps, and recovery owner.
- A non-maintainer GitHub test account and an owner account use separate
  credential stores. Tokens are never printed or placed in command arguments.
- Before PUB-TC-011 or 012 runs, the owner supplies an approved collaborator
  roster and the expected `main` protection policy for each repository. Record
  only account roles and redacted identifiers in TESTEXEC-025.
- Branch-protection and collaborator checks use read-only API calls where
  possible.
- Visibility rollback runs only in the approved window. Record the pre-test
  visibility and protection state before any change, then restore and verify it.
- Positive release testing needs a harmless fixture tag, release, and small
  checksum-known asset. Current repositories have zero tags and zero releases.

## Test data

| Data | Value |
| --- | --- |
| Repository set | `pal_found_cli`, `pal_found_cli_tool`, `pal_found_cli_skills` |
| Root expected HEAD | `240898c5daa7ed693e969369141d66e6e5123b6f` |
| Tool expected HEAD | `370c971b4d05340d80a0dad009bc8b4c0233d345` |
| Skills expected HEAD | `34b6c404994cdcc4f97b18d2a493fff6c1d3d895` |
| Anonymous git configuration | `GIT_TERMINAL_PROMPT=0`; `GIT_ASKPASS=`; `git -c credential.helper=` |
| Clone concurrency | Five independent clones per repository, maximum 60 seconds each |
| Invalid repository | `https://github.com/t-jet/pal_found_cli_missing_test.git` |
| Release fixture | Owner-created `qa-public-access-<timestamp>` tag and release with `qa-public-access.txt` plus SHA-256 |
| Permission fixture | Owner-approved maintainer/collaborator roles per repository, with identifiers redacted in evidence |
| Protection fixture | Owner-approved required reviews, status checks, and bypass policy for `main` per repository |
| Secret patterns | GitHub PAT, AWS access-key ID, Slack token, and private-key header patterns; heuristic scan results require manual review |
| Secret scanner evidence | Scanner name, version, configuration hash, redacted report, and exit code for each repository |
| Allowed tracked environment file | `.env.example` containing placeholders only |
| Forbidden tracked files | `.env`, token files, private keys, customer exports, credential archives |

## Expected output rules

- Successful git and local validation commands return exit code 0.
- An anonymous clone or `ls-remote` against a private, missing, or invalid
  repository returns a nonzero git exit code, normally 128, without disclosing
  content.
- Successful GitHub REST reads return HTTP 200. Empty issues, pull requests,
  tags, or releases are valid empty arrays, not errors.
- Unauthenticated writes return HTTP 401, 403, or 404 and create no object.
- Rate-limited REST calls return HTTP 403 or 429 with rate-limit headers. Tests
  must not exhaust the shared production quota deliberately.
- Network interruption returns a nonzero git/curl exit code within the test
  timeout and leaves no usable partial checkout.
- Every TESTEXEC result records expected versus actual output and marks the case
  PASS, FAIL, or BLOCKED. A case requiring an absent fixture or missing owner
  authorization is BLOCKED, not skipped or assumed to pass.

## Test cases

### PUB-TC-001 - Anonymous repository metadata and README access

- Type: positive, public read.
- Traceability: AC-002-01, AC-D-002-01.
- Given no GitHub credentials, when each repository metadata endpoint, landing
  page, README, and default-branch tree are requested, then each request returns
  HTTP 200 and exposes the expected repository name, `visibility=public`,
  `private=false`, and readable content.
- Expected: three repositories pass; no login redirect or authorization header.
- Cleanup: none.

### PUB-TC-002 - Anonymous HEAD lookup

- Type: positive, git protocol.
- Traceability: AC-002-01, AC-002-02.
- Given credentials and prompts are disabled, when `git -c credential.helper=
  ls-remote --symref <url> HEAD` runs for each repository, then exit code is 0,
  HEAD targets `refs/heads/main`, and the returned hash matches the recorded
  baseline or an owner-approved later commit.
- Cleanup: none.

### PUB-TC-003 - Independent anonymous clones

- Type: positive, distribution.
- Traceability: AC-002-02, AC-D-002-02.
- Given an empty `.ept/tmp` destination, when each repository is cloned over
  HTTPS without credentials, then all three commands exit 0, produce clean
  worktrees, and check out the hashes recorded by PUB-TC-002.
- Cleanup: remove or retain the temporary directories according to the execution
  evidence policy; never write outside `.ept/tmp`.

### PUB-TC-004 - Recursive design-repository clone and gitlink integrity

- Type: positive, integration.
- Traceability: AC-002-01, AC-002-02; FEATURE-003 prerequisite.
- Given the public root repository, when it is cloned with
  `--recurse-submodules`, then the root, tool, skills, and SDK submodules clone
  without prompts. Tool and skills hashes match the root gitlinks and their
  origins use canonical `pal_found_*` URLs.
- Cleanup: temporary clone only.

### PUB-TC-005 - Issues and pull-request lists are public

- Type: positive, contribution read path.
- Traceability: AC-002-03, AC-D-002-03.
- Given no GitHub account, when the issues and pulls web pages and REST list
  endpoints are opened for each repository, then each returns HTTP 200. An empty
  list is valid. Existing public entries, if any, can be opened without login.
- Cleanup: none.

### PUB-TC-006 - External user can create an issue

- Type: positive, controlled mutation.
- Traceability: AC-002-03, AC-D-002-03.
- Given owner authorization and a non-maintainer test account, when the account
  submits a clearly marked QA issue in each repository, then GitHub creates it,
  the issue is publicly readable, and the account cannot edit repository code or
  settings.
- Expected side effect: three QA issues. Record their URLs, then close them with
  an owner-approved cleanup comment.
- Authorization: mandatory. Without it, mark BLOCKED.

### PUB-TC-007 - External user can open a pull request but cannot merge it

- Type: positive and security, controlled mutation.
- Traceability: AC-002-03, BR-D-002-03, BR-D-002-05.
- Given owner authorization, a disposable fork, and a harmless documentation
  branch, when the non-maintainer opens a pull request, then the PR is publicly
  readable and cannot be merged or bypass required checks by that account.
- Cleanup: close the PR and delete the disposable fork/branch after evidence is
  captured. Without authorization, mark BLOCKED.

### PUB-TC-008 - Public tag listing with no releases

- Type: positive boundary case.
- Traceability: AC-002-04, AC-D-002-04.
- Given the current zero-tag, zero-release state, when anonymous tag and release
  endpoints are queried, then they return HTTP 200 with empty arrays. The release
  page remains publicly readable and shows no releases rather than an auth error.
- Cleanup: none.

### PUB-TC-009 - Public release and asset download

- Type: positive, controlled fixture.
- Traceability: AC-002-04, AC-D-002-04.
- Given an owner has published the approved fixture release, when an anonymous
  user opens the tag, release, and asset URLs, then all return HTTP 200. The asset
  downloads without credentials and its SHA-256 matches the fixture record.
- Test all repositories because DEV-025 applies the checklist to each one.
- Dependency: fixture absent at authoring time. Mark BLOCKED until provided.
- Cleanup: owner deletes the fixture only if the authorization says to do so.

### PUB-TC-010 - Anonymous write is denied

- Type: negative, security.
- Traceability: BR-002-06, BR-D-002-05.
- Given an anonymous clean clone, when a harmless commit is created locally and
  `git -c credential.helper= push --dry-run origin HEAD:refs/heads/qa-denied` is
  attempted with prompts disabled, then the command returns nonzero and no remote
  ref is created.
- Expected: authentication/permission failure without repository content or
  secret disclosure.
- Cleanup: local temporary clone only.

### PUB-TC-011 - Maintainer and collaborator permissions remain restricted

- Type: security, owner-controlled read.
- Traceability: BR-002-06, BR-D-002-05, SEC-3.
- Given an owner-scoped credential supplied through a protected environment,
  when collaborator and team permissions are read for each repository, then only
  approved maintainers have push/admin access and the three permission sets are
  independently configurable.
- Authorization: owner approval required even though the operation is read-only.
  Redact account IDs and never record tokens.

### PUB-TC-012 - Main-branch protection is active

- Type: security, owner-controlled read.
- Traceability: BR-D-002-05, SA-DES-002 UC-2 and SEC-3.
- Given owner-approved read access to repository settings, when protection rules
  for `main` are retrieved, then required reviews/checks match the approved
  policy and non-maintainers cannot bypass them.
- Authorization: required. Missing settings evidence makes the case BLOCKED.

### PUB-TC-013 - Secret and private-data scan

- Type: security, positive and negative fixtures.
- Traceability: BR-D-002-06, AC-D-002-06, SEC-1.
- Given fresh clones including reachable history, when a maintained secret
  scanner and high-confidence token/private-key patterns scan every repository,
  then no confirmed credential, private key, customer data, or live `.env` file
  is found. Heuristic hits are reviewed line by line and recorded as confirmed or
  false positive. Run the history-aware scan with redaction enabled and record
  the scanner name, version, configuration hash, command, and exit code without
  copying a detected value into the evidence.
- Negative fixture: the same rules/configuration must detect a synthetic token
  during a filesystem scan of an untracked `.ept/tmp` fixture; never commit the
  fixture. Record only the rule ID and redacted location.
- Cleanup: delete the temporary synthetic fixture.

### PUB-TC-014 - Ignore rules exclude local credentials

- Type: security, negative.
- Traceability: BR-D-002-06, SEC-2.
- Given a temporary `.env` and private-key-named file in each clone, when
  `git status --ignored` and `git check-ignore` run, then local credential files
  are ignored. No real `.env`, key, token file, or credential archive is tracked.
  `.env.example` may be tracked only when it contains placeholders.
- Cleanup: remove temporary files.

### PUB-TC-015 - Missing repository and malformed URL

- Type: negative, error handling.
- Traceability: public access error experience in BA-DES-002 and SA-DES-002.
- Given a missing repository URL and a malformed HTTPS URL, when anonymous web
  and git requests run, then the web request returns 404 or a client validation
  error, git returns nonzero (normally 128), no credentials are requested, and no
  partial content is usable.
- Cleanup: temporary destination only.

### PUB-TC-016 - Network interruption and timeout

- Type: negative, resilience.
- Traceability: AVAIL-1 and publication verification reliability.
- Given a test-only unreachable proxy or blocked endpoint, when clone and REST
  commands run with a 30-second test timeout, then they fail within the bound,
  report a network error without credentials, and leave no checkout accepted as
  complete. Retrying against the normal public endpoint succeeds.
- Cleanup: clear test-only proxy variables and partial directories.

### PUB-TC-017 - Concurrent anonymous clones are consistent

- Type: concurrency and integrity.
- Traceability: BR-002-01, BR-002-02, AVAIL-1.
- Given the HEAD values from PUB-TC-002, when five anonymous clones per
  repository run concurrently, then all 15 finish within 60 seconds, exit 0, and
  resolve to the same per-repository hash. No checkout has worktree corruption.
- Cleanup: temporary clones only.

### PUB-TC-018 - REST pagination and rate-limit behavior

- Type: edge and negative.
- Traceability: SA-DES-002 GitHub REST verification surface.
- Given public list endpoints, when `per_page=1` and pagination links are used,
  then pages are readable without credentials and do not duplicate entries.
  Record `X-RateLimit-*` headers. Do not exhaust quota; if GitHub returns 403 or
  429, honor the reset/retry header and mark the environmental result accurately.
- Cleanup: none.

### PUB-TC-019 - Former repository URLs redirect safely

- Type: compatibility and error handling.
- Traceability: repository rename dependency and documented GitHub redirects.
- Given the former `foundry_cli`, `foundry_cli_tool`, and `foundry_cli_skills`
  URLs, when anonymous web and git reads run, then each either redirects to the
  canonical public repository without credential leakage or returns a clear
  not-found response documented as an expired compatibility path. Canonical URLs
  remain the only URLs used in current documentation.
- Cleanup: none.

### PUB-TC-020 - Controlled private rollback and public restoration

- Type: rollback, security, destructive external change.
- Traceability: AC-002-05, AC-D-002-05, BR-D-002-07, REV-1.
- Given explicit owner authorization, a maintenance window, recorded pre-test
  settings, and a recovery owner, when one repository is changed from public to
  private, then new anonymous metadata, web, clone, and fetch requests fail with
  404/auth denial and expose no remote content. Already cloned local data is
  expected to remain on disk and must not be mistaken for continued public
  access. When visibility is restored, anonymous reads and clones return to
  normal and protection/collaborator settings match the recorded baseline.
- Run one repository at a time. Stop and restore immediately on any unexpected
  result. Without explicit authorization, mark BLOCKED and do not simulate the
  production visibility change.

## Traceability matrix

| Requirement | Cases |
| --- | --- |
| AC-002-01 / AC-D-002-01: anonymous content read | PUB-TC-001, 002, 004, 005 |
| AC-002-02 / AC-D-002-02: anonymous clone | PUB-TC-002, 003, 004, 017 |
| AC-002-03 / AC-D-002-03: issues and pull requests | PUB-TC-005, 006, 007 |
| AC-002-04 / AC-D-002-04: tags, releases, assets | PUB-TC-008, 009, 018 |
| BR-002-04 / BR-D-002-07 and AC-002-05 / AC-D-002-05: private rollback | PUB-TC-020 |
| BR-002-06 / BR-D-002-05: restricted writes | PUB-TC-007, 010, 011, 012 |
| BR-D-002-06 / AC-D-002-06: secret safety | PUB-TC-013, 014 |
| Availability, error, compatibility, concurrency | PUB-TC-015, 016, 017, 018, 019 |

## TESTEXEC-025 dependencies

- Cases PUB-TC-001..005, 008, 010, 013..019 are safe to execute with anonymous
  or local read-only tooling. PUB-TC-010 uses `--dry-run` and must verify that no
  remote ref appeared.
- PUB-TC-006 and 007 need approved issue/PR mutations and cleanup ownership.
- PUB-TC-009 needs one public release fixture per repository. There are no tags
  or releases at this baseline.
- PUB-TC-011 and 012 need owner-approved, read-only settings evidence.
- PUB-TC-020 needs explicit authorization for a real visibility change,
  maintenance timing, and a tested restoration path. It must never run from an
  ordinary QA session.
- A Tech Lead or Architect must review and approve this specification before
  TESTEXEC-025 begins, per the QA execution gate.
