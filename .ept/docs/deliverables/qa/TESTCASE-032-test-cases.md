# TESTCASE-032 - canonical skill-tree migration QA test cases

## Scope

These cases verify DEV-STORY-031: the migration and rename of the 19 skills
into the standard `.agents/skills` tree with confirmed `pal-found` naming,
updated frontmatter and launcher names, updated internal references, a
rollback-safe legacy transition, and no change to CLI behavior or data.

The canonical tree to verify is `https://github.com/t-jet/pal_found_cli_skills`
at the `.agents/skills` layout (DEV-027 and Project Owner, QUESTION-126). The
mapped names follow the rename table from SA-DES-010 / ND-010-01..04
(`foundry-` to `pal-found-`).

Operations covered:

- Fresh clone of the canonical skills repository.
- Final `.agents/skills` layout (19 folders).
- Old-path (`.claude/skills`) transition to a pointer or removal.
- Name, frontmatter, launcher-name, and cross-reference checks.
- Negative cases: missing, duplicate, and stale folders.

The suite reads the public repository and validates the tree structure and
file content under throwaway checkouts under `.ept/tmp`; it does not mutate
the repository or any harness.

## Source baseline and traceability

- [BA-DES-007](../business_design/BA-DES-007-business-design.md):
  BR-D-007-01..06 and AC-D-007-01..05.
- [SA-DES-006](../architecture/SA-DES-006-technical-design.md): standard-folder
  migration, renames, discovery, legacy cleanup.
- [SA-DES-010](../architecture/SA-DES-010-technical-design.md) and
  [BA-DES-011](../business_design/BA-DES-011-business-design.md): confirmed
  rename mapping ND-010-01..04 (`pal_found_` / `pal-found-`).
- [DEV-037 rename migration](../development/DEV-037-rename-migration.md):
  19 `pal-found*` folders, launcher names, legacy pointer.
- [DEV-027 reference register](../development/DEV-027-reference-register.md):
  canonical skills URL and production commit `4564e783a948de66d8edb978dc17aaf5ddaeea8d`.
- Project Owner decision (QUESTION-126, comment `20260928-023149-project-manager`):
  QA may clone the skills repository; the migrated `.agents/skills` layout with
  19 skill folders is present.

## Preconditions

- Git 2.40+; Python 3.11+ for frontmatter parsing and the inventory tests.
- Fresh clone via `git clone https://github.com/t-jet/pal_found_cli_skills`
  with anonymous git (`GIT_TERMINAL_PROMPT=0`, empty credential helper).
- A throwaway checkout under `.ept/tmp` for migration fixtures (old-path,
  missing, duplicate, stale folders).
- Record OS, git version, clone URL, resolved HEAD, exit code, and file
  listings for every case.

## Test data

| Data | Value |
| --- | --- |
| Canonical skills URL | `https://github.com/t-jet/pal_found_cli_skills` |
| Baseline commit | `4564e783a948de66d8edb978dc17aaf5ddaeea8d` |
| Expected skill count | 19 (`pal-found` + 18 namespace skills) |
| Final tree | `.agents/skills/pal-found*` (19 folders) |
| Legacy path | `.claude/skills` (pointer-only `README.md`, or removed) |
| Rename mapping | `foundry-x` becomes `pal-found-x`; `foundry/` becomes `pal-found` |
| Reference tokens | `pal_found_*` module names; `pal-found-*` command names |

## Test scenarios

### SMT-TC-001 - Fresh clone yields the final 19-folder layout (positive)

- Given a fresh clone of the canonical skills repository,
  when a user lists `.agents/skills`,
  then exactly 19 `pal-found*` folders are present with one `SKILL.md` each.

### SMT-TC-002 - Final layout matches the rename mapping (positive / naming)

- Given the confirmed rename map ND-010-01..04,
  when each `.agents/skills` folder and its `SKILL.md` frontmatter are checked,
  then every name starts with `pal-found` and no `foundry-` folder or
  `foundry` skill name remains.

### SMT-TC-003 - Frontmatter uses the final names (positive)

- Given each skill's `SKILL.md` frontmatter,
  when the `name` field is parsed,
  then it equals the folder name and starts with `pal-found`.

### SMT-TC-004 - Launcher names use the final command names (positive)

- Given each skill's launcher references,
  when the documented `pal-found-*` command names are checked,
  then launchers reference `pal_found_*_cli.py` modules and `pal-found-*`
  commands, with no `foundry-` command names.

### SMT-TC-005 - Cross-references resolve within the canonical tree (positive / references)

- Given the final tree,
  when relative links and cross-skill references are gathered,
  then each resolves to an existing path in `.agents/skills` (or the skills
  repository) and none targets a legacy `foundry-` path.

### SMT-TC-006 - README cites the final names (positive)

- Given the repository README (and, for the pal_found_cli repo, AGENTS.md),
  when distribution and naming references are scanned,
  then they cite `pal_found_cli_skills`, `.agents/skills`, and `pal-found`
  names, with no `foundry_cli_skills` or `foundry-` operational names.

  Scope note (QUESTION-137 reconciliation): per the DEV-024 repository-split
  manifest, AGENTS.md belongs to pal_found_cli, not pal_found_cli_skills; the
  skills repo canonically contains `.agents/skills/`, `tests/`,
  `.github/workflows/`, and `pyproject.toml`. The AGENTS.md clause is therefore
  conditioned on the pal_found_cli repo only.

### SMT-TC-007 - Legacy path is pointer-only or removed (positive / legacy)

- Given a completed migration,
  when a user inspects `.claude/skills`,
  then it contains only the migration-pointer `README.md` or does not exist,
  and it holds no `SKILL.md` authoritative content.

### SMT-TC-008 - Old-path transition is read-only until verified (boundary / legacy)

- Given a workspace during migration whose legacy `.claude/skills` holds the
  previous tree,
  when discovery has not yet passed,
  then the legacy content is preserved read-only and the canonical tree can be
  rolled back from the last known-good state.

### SMT-TC-009 - No CLI behavior, operations, or data change (positive / boundary)

- Given the renamed skill launchers,
  when the operation catalog referenced by each skill is compared to the
  implemented CLI surface,
  then operations, exit codes, and data semantics are unchanged from the
  pre-rename baseline.

### SMT-TC-010 - Missing folder is reported (negative)

- Given a `.agents/skills` tree with one expected `pal-found*` folder removed,
  when the inventory check runs,
  then it reports the missing name and the count is 18.

### SMT-TC-011 - Duplicate folder is reported (negative)

- Given a `.agents/skills` tree containing two folders with the same
  `pal-found-x` name,
  when the inventory check runs,
  then it reports the duplicate and does not treat it as canonical.

### SMT-TC-012 - Stale legacy folder is reported (negative / stale)

- Given a workspace whose legacy `.claude/skills` still holds a migrated skill
  `SKILL.md` (not just the pointer),
  when the legacy check runs,
  then it flags the stale content so it is not mistaken for the canonical copy.

### SMT-TC-013 - Rollback restores the last known-good tree (boundary / rollback)

- Given a bad migration at a later tag,
  when a user checks out the last known-good commit and restores `.agents/skills`,
  then the 19 canonical folders are restored and `git diff` against the
  known-good tree shows no unexpected change.

### SMT-TC-014 - Inventory validation is atomic (positive / boundary)

- Given the canonical inventory check,
  when a source tree is missing or mismatched,
  then the check throws before any destination mutation, leaving the
  destination unchanged (validated atomically).

## Expected outputs

- Positive cases confirm the canonical 19-folder `.agents/skills` tree with
  `pal-found` names, matching frontmatter, launcher and reference tokens, and
  a pointer-only or absent legacy location.
- Negative cases (missing, duplicate, stale) report the anomaly and never
  mutate a destination.
- No CLI behavior or data change is observed.
- Rollback reproduces the last known-good tree.

## Evidence for TESTEXEC

Record OS, git version, clone URL, resolved HEAD, exit code, directory
listings of `.agents/skills` and `.claude/skills`, parsed frontmatter names,
launcher and reference grep output, and diff output for rollback cases.
Evidence stays under `.ept/tmp`; chat/transcript JSONL is never published.

## Open risks

- Live HEAD may drift from the pinned DEV-027 baseline; the 19-name manifest
  is asserted against the README inventory, not a hard-coded SHA.
- Legacy-pointer and rollback behavior differ across platforms and is captured
  per case.
