# TESTCASE-031 - harness discovery and onboarding QA test cases

## Scope

These cases verify DEV-STORY-030: that each supported agent harness discovers
all 19 skills from the canonical `.agents/skills` tree, that non-native
harnesses have exact onboarding steps, and that no skill content survives only
under the legacy `.claude/skills` location after migration.

The two supported harnesses are Codex (native discovery of `.agents/skills`)
and Claude Code (configured junction/symlink from `.claude/skills` to the
canonical tree). The canonical distribution source for live discovery is
`https://github.com/t-jet/pal_found_cli_skills` (DEV-027 and Project Owner,
QUESTION-124).

Operations covered:

- Canonical skill inventory (19 folders) under `.agents/skills`.
- Native discovery (Codex), configured discovery (Claude junction/symlink),
  and manual/onboarding discovery paths.
- Legacy `.claude/skills` check (must be empty except the pointer or be
  removed).
- Negative cases: missing skill, wrong path, stale legacy content.

The suite verifies a harness's skill listing before and after the copy or
onboarding step, using a throwaway workspace under `.ept/tmp`. It does not
modify the public repository or a real harness session.

## Source baseline and traceability

- [BA-DES-007](../business_design/BA-DES-007-business-design.md):
  BR-D-007-01..06 and AC-D-007-01..05.
- [SA-DES-006](../architecture/SA-DES-006-technical-design.md): per-harness
  discovery and wiring.
- [DEV-037 rename migration](../development/DEV-037-rename-migration.md):
  19 `pal-found*` folders, Claude link pointer, legacy pointer-only directory.
- [DEV-027 reference register](../development/DEV-027-reference-register.md):
  canonical skills URL and production commit `4564e783a948de66d8edb978dc17aaf5ddaeea8d`.
- Project Owner decision (QUESTION-124, comment `20260928-022923-project-manager`):
  QA may reference the public skills repository as the reachable distribution
  source; default branch reference acceptable.

## Preconditions

- Git 2.40+, PowerShell 5.1+ or POSIX `sh`, and the relevant harness CLI
  (Codex or Claude Code) available in the test environment, or a harness
  launcher stub that reads the same skill directory listing.
- A fresh clone under `.ept/tmp`, and a throwaway workspace under `.ept/tmp`
  used as the harness working directory.
- A canonical 19-name manifest derived from the skills README inventory.
- Record OS, harness name and version, clone URL, resolved HEAD, exit code,
  and skill-listing output for every case.

## Test data

| Data | Value |
| --- | --- |
| Canonical skills URL | `https://github.com/t-jet/pal_found_cli_skills` |
| Baseline commit | `4564e783a948de66d8edb978dc17aaf5ddaeea8d` |
| Expected skill count | 19 (`pal-found` + 18 namespace skills) |
| Native discovery path | workspace `.agents/skills` |
| Configured path (Claude) | workspace `.claude/skills` junction/symlink to `.agents/skills` |
| Legacy pointer | `.claude/skills/README.md` only (or removed) |
| Wrong path fixture | a sibling directory (for example `.claude/not-skills`) |
| Missing skill fixture | a clone with one `pal-found*` folder removed |

## Test scenarios

### HDN-TC-001 - Canonical inventory is exactly 19 under .agents/skills (positive)

- Given a fresh canonical clone,
  when a user lists the directories under `.agents/skills`,
  then exactly 19 `pal-found*` folders are present, including `pal-found` and
  18 namespace skills.

### HDN-TC-002 - Codex native discovery (positive)

- Given a workspace whose `.agents/skills` holds the canonical 19 folders,
  when a new Codex session lists its available skills,
  then `pal-found` and at least one namespace skill (for example
  `pal-found-datasets`) are listed.

### HDN-TC-003 - Claude configured discovery via junction/symlink (positive)

- Given a workspace whose `.claude/skills` is the documented link to
  `.agents/skills`,
  when a new Claude Code session lists its available skills,
  then `pal-found` and at least one namespace skill are listed.

### HDN-TC-004 - Discovery works after a fresh clone/install (positive / boundary)

- Given a clean workspace with no prior skills and a fresh clone,
  when the user runs the documented copy and starts a new harness session,
  then all 19 skills are discovered.

### HDN-TC-005 - Manual onboarding path is documented exactly (positive / manual)

- Given a harness that does not scan `.agents/skills`,
  when the user follows the documented manual target path,
  then the harness loads all 19 skills and the target path is recorded.

### HDN-TC-006 - Missing skill is not presented to the harness (negative)

- Given a workspace where one `pal-found*` folder is missing,
  when a harness session lists skills,
  then the missing skill is absent and the remaining 18 are listed.

### HDN-TC-007 - Wrong path yields no skills (negative / path)

- Given skills copied to a non-standard location (for example `.claude/not-skills`)
  with no pointer or link,
  when a harness session lists skills,
  then it finds none and the onboarding instructions name the correct target
  path.

### HDN-TC-008 - Stale legacy content is rejected or reduced to a pointer (negative / stale-legacy)

- Given a workspace whose `.claude/skills` retains skill content beyond the
  single `README.md` pointer,
  when a user runs the documented onboarding check,
  then the check flags the non-pointer content and does not silently overwrite
  it.

### HDN-TC-009 - Legacy location holds no skill content only (positive / legacy)

- Given a completed migration and verified discovery,
  when a user inspects `.claude/skills`,
  then it contains only the migration pointer or is removed, and no `SKILL.md`
  exists there that does not also exist under `.agents/skills`.

### HDN-TC-010 - Skill listing names use the pal-found names (positive / naming)

- Given any harness that discovers the skills,
  when a session lists them,
  then every listed name starts with `pal-found` and no `foundry-` name
  appears.

### HDN-TC-011 - Cross-harness single copy stays canonical (positive / boundary)

- Given one canonical `.agents/skills` tree,
  when both Codex (native) and Claude (linked) load skills,
  then both load the same 19 folders and no duplicate skill copy exists.

### HDN-TC-012 - Empty canonical tree yields empty listing (negative / boundary)

- Given a workspace whose `.agents/skills` has zero skill folders,
  when a harness session lists skills,
  then it reports no skills and points to the onboarding instructions.

## Expected outputs

- Positive discovery cases report the full 19-name `pal-found*` set.
- Negative cases either absent the targeted skill or report no skills with a
  reference to onboarding instructions.
- Legacy `.claude/skills` never holds authoritative skill content.
- All listed skill names use the `pal-found` prefix.

## Evidence for TESTEXEC

Record OS, harness name and version, session skill-listing output before and
after the step, the copy or link command, exit code, and a directory listing
of `.agents/skills` and `.claude/skills`. Evidence stays under `.ept/tmp`;
chat/transcript JSONL is never published.

## Open risks

- Harness CLIs may be unavailable in the test environment; a launcher stub
  that reads the same directory listing is an acceptable substitute and is
  recorded in the evidence.
- Junction/symlink behavior differs across platforms and is captured per case.
