# TESTCASE-030 - git-clone and skill-copy distribution instructions QA test cases

## Scope

These cases verify the distribution documentation for DEV-STORY-033. The
deliverable is the README within `pal_found_cli_skills` that documents, per
supported harness, how to clone the repository, copy the 19 `pal-found*`
skill folders into the target harness, and update or roll back afterwards.

Operations covered:

- `git clone` of `https://github.com/t-jet/pal_found_cli_skills` (canonical
  URL per DEV-027 and Project Owner, QUESTION-122).
- Skill folder copy from `.agents/skills/` into the harness target folder.
- Update by `git pull` / tag checkout and re-copy.
- Verify the copied tree (19-folder inventory and `SKILL.md` sentinel).
- Onboard a non-native harness (Claude Code) without duplicating content.

The suite does not mutate the public repository, releases, tags, or harness
configuration. Positive clone and copy cases read from the live public
repository at the pinned baseline; negative cases use throwaway fixtures
under `.ept/tmp`.

## Source baseline and traceability

- [BA-DES-008](../business_design/BA-DES-008-business-design.md):
  BR-D-008-01..06 and AC-D-008-01..05.
- [SA-DES-007](../architecture/SA-DES-007-technical-design.md):
  repository-based distribution, clone-copy-update flow, per-harness target
  map, tag-based versioning.
- [DEV-037 rename migration](../development/DEV-037-rename-migration.md):
  copy of the 19 `pal-found*` folders, Claude link pointer.
- [DEV-027 reference register](../development/DEV-027-reference-register.md):
  canonical skills URL `https://github.com/t-jet/pal_found_cli_skills` and
  verified production commit `4564e783a948de66d8edb978dc17aaf5ddaeea8d`.
- Project Owner decision (QUESTION-122, comment `20260928-022644-project-manager`):
  git-clone and skill-copy documentation may reference the live canonical URL
  for anonymous clone/copy.

## Preconditions

- Git 2.40 or newer; PowerShell 5.1+ (Windows) or POSIX `sh` (Linux/macOS)
  available for the copy fixtures.
- Anonymous git: `GIT_TERMINAL_PROMPT=0`, empty `GIT_ASKPASS`, and empty
  credential helper for every git command. No token or cached credential.
- A fresh clone under `.ept/tmp` for each positive case; the target harness
  workspace also lives under `.ept/tmp` so no real workspace is touched.
- Record OS, git version, clone URL, resolved HEAD, exit code, and
  stderr/stdout for every case.
- All positive cases run against the live canonical skills repository (default
  branch). The expected 19-name manifest is taken from `pal_found_cli_skills/
  README.md` (the canonical inventory list).

## Test data

| Data | Value |
| --- | --- |
| Canonical skills URL | `https://github.com/t-jet/pal_found_cli_skills` |
| Baseline commit | `4564e783a948de66d8edb978dc17aaf5ddaeea8d` (per DEV-027; live HEAD may be newer) |
| Expected skill count | 19 (`pal-found` + 18 namespace skills) |
| Sentinel file | the `SKILL.md` file inside each skill folder |
| Invalid clone URL | `https://github.com/t-jet/pal_found_cli_no_such_repo.git` |
| Invalid tag | `v999.999.999-notthere` |
| Copy source | `<clone>\.agents\skills` (PowerShell) / `.agents/skills` (POSIX) |
| Codex target | `<workspace>\.agents\skills` |
| Claude target | `<workspace>\.claude\skills` (junction/symlink to `.agents/skills`) |

## Test scenarios

### GCD-TC-001 - Clone the canonical repository (positive)

- Given a clean environment with anonymous git and no credentials,
  when a user runs `git clone https://github.com/t-jet/pal_found_cli_skills`,
  then the command exits 0 and the clone contains `.agents/skills/` with 19
  `pal-found*` folders.

### GCD-TC-002 - Clone honors the documented release-tag pin (boundary)

- Given a user read the README "Clone" section using `git checkout` with a
  release tag,
  when a release tag exists and the user checks out that tag,
  then the tree reflects precisely that tag and `git describe --tags` matches.

### GCD-TC-003 - Default-branch clone is explicit (boundary / URL)

- Given the README states "omit the tag to use the default branch",
  when a user clones without a tag and runs `git rev-parse --abbrev-ref HEAD`,
  then the branch is the repository default (`main`).

### GCD-TC-004 - Invalid repository URL is refused (negative)

- Given an anonymous git environment,
  when a user runs `git clone https://github.com/t-jet/pal_found_cli_no_such_repo.git`,
  then the command exits non-zero, prints an access error, and creates no
  usable clone.

### GCD-TC-005 - Invalid release tag is refused (negative / version)

- Given a cloned repository,
  when a user runs `git checkout v999.999.999-notthere`,
  then git exits non-zero with `fatal: invalid reference` and the working tree
  is left on the previously checked out revision.

### GCD-TC-006 - Copy for Codex copies exactly 19 folders (positive)

- Given a fresh clone whose `.agents/skills` contains the canonical 19 names,
  when a user runs the documented PowerShell copy command into a new
  workspace `.agents/skills` directory,
  then all 19 `pal-found*` folders and their `SKILL.md` sentinels exist in the
  destination, the count is 19, and no `.git` or stray folder is copied.

### GCD-TC-007 - Copy is idempotent on an existing target (boundary)

- Given the destination `.agents/skills` already contains stale content under
  the 19 canonical `pal-found*` names,
  when a user reruns the documented copy command,
  then the stale content under those canonical names is cleared and restored to
  the current canonical files, non-canonical user folders are preserved
  untouched, and the command exits 0.

  Scope note (QUESTION-137 reconciliation): the documented command removes and
  regenerates only the 19 canonical names in its expected-name list; it does
  not enumerate or remove non-canonical `pal-found*` user folders. The
  skills-repo test `test_published_powershell_copy_is_complete_and_safe_to_
  rerun` asserts unrelated/custom skills are preserved on rerun, so the
  expected output is scoped to canonical-named content only.

### GCD-TC-008 - Copy refuses a wrong/partial source (negative)

- Given a source `.agents/skills` that is missing one `pal-found*` folder or
  has a sentinel `SKILL.md` removed,
  when a user runs the documented copy command,
  then the command throws before mutating the destination and the destination
  is unchanged (no partial copy).

### GCD-TC-009 - Copy detects a missing sentinel (negative / boundary)

- Given a source folder whose `SKILL.md` sentinel is missing,
  when a user runs the documented copy command,
  then the command fails with a message naming the affected skill's sentinel
  file and does not copy the incomplete skill.

  Scope note (QUESTION-137 reconciliation): the documented command validates
  sentinels by existence only (`Test-Path -PathType Leaf`); a missing sentinel
  fails atomically (skills-repo test
  `test_published_powershell_copy_rejects_missing_sentinel_atomically`), while
  an empty (zero-byte) sentinel is not detected because content validation is
  out of the documented contract. The empty-sentinel clause was dropped; no
  implementation change is warranted.

### GCD-TC-010 - Destination is validated after copy (positive / boundary)

- Given a successful copy into the Codex target,
  when a user runs the documented verification snippet,
  then it reports 19 skills and confirms the `pal-found` `SKILL.md` exists.

### GCD-TC-011 - Update path with pull --ff-only (positive)

- Given a cloned repository on the default branch,
  when a user runs `git pull --ff-only`,
  then the command exits 0 and the tree advances forward-only (no merge).

### GCD-TC-012 - Update by tag checkout and re-copy (positive)

- Given a repository with a newer release tag,
  when a user runs `git checkout` with that tag and re-copies the 19 folders,
  then the destination reflects the new tag inventory and the copied count is 19.

### GCD-TC-013 - Rollback by tag checkout and re-copy (boundary)

- Given the current copied tree is a bad update,
  when a user checks out the last known-good tag and re-copies,
  then the destination is restored exactly to the known-good 19-folder tree.

### GCD-TC-014 - Claude Code onboarding removes only a pointer (boundary / permission)

- Given a workspace whose `.claude/skills` contains only the migration-pointer
  `README.md`,
  when a user runs the documented Claude onboarding snippet,
  then the pointer is removed, a junction/symlink to `.agents/skills` is
  created, and no skill content is duplicated.

### GCD-TC-015 - Claude onboarding refuses non-pointer legacy content (negative)

- Given a workspace whose `.claude/skills` holds skill content beyond the
  single `README.md` pointer,
  when a user runs the documented Claude onboarding snippet,
  then the command throws "Refusing to replace non-pointer content" and leaves
  the legacy directory intact.

### GCD-TC-016 - POSIX copy matches the Windows copy contract (cross-platform)

- Given a POSIX shell environment and a fresh clone,
  when a user runs the documented `find -exec cp -R` command into a clean
  target,
  then all 19 folders and sentinels are present and the count is 19.

### GCD-TC-017 - Clone and copy need no package manager or credential (positive)

- Given an environment without any package-manager install,
  when a user performs the documented clone and copy steps,
  then only git and file-copy tools are used and no credential prompt appears.

## Expected outputs

- Positive clone/copy/update cases exit 0 and yield the canonical 19-folder
  tree with `SKILL.md` sentinels.
- Negative cases exit non-zero with the documented error text and leave target
  state unchanged.
- Verification snippets print a count of 19 for the copying into the named
  harness.
- No package installation is performed; distribution is file-based.

## Evidence for TESTEXEC

For each case record: OS, git version, PowerShell/POSIX shell version, clone
URL, resolved HEAD, exit code, stderr/stdout, and a directory listing of the
copied tree. Evidence stays under `.ept/tmp`; chat/transcript JSONL is never
published.

## Open risks

- Live repository HEAD may drift from the pinned DEV-027 baseline; tests
  assert the 19-folder manifest from the README, not a hard-coded SHA.
- Claude onboarding uses a filesystem junction/symlink; behavior may differ
  across Windows/macOS/Linux and is captured in the evidence.
