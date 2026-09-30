# TESTEXEC-032 - canonical skill-tree migration QA execution log

## Scope

Executes TESTCASE-032 scenarios (SMT-TC-001..014) for DEV-STORY-031 against
the live canonical skills repository
`https://github.com/t-jet/pal_found_cli_skills` at the `.agents/skills`
layout. Chat/transcript JSONL is kept local only and is never published.

## Environment

- OS: Windows (PowerShell 5.1/pwsh-compatible); WSL bash (case-sensitive
  ext4 under /tmp) for the duplicate-folder case
- git: 2.54.0.windows.1
- Python: 3.11.9 (D:\app\Python)
- Clone: anonymous, `GIT_TERMINAL_PROMPT=0`, empty GIT_ASKPASS, empty
  credential helper
- Clone URL: `https://github.com/t-jet/pal_found_cli_skills`
- Resolved HEAD: `4564e783a948de66d8edb978dc17aaf5ddaeea8d` (branch main)
- Evidence root: `.ept/tmp` (`g001`, per-case log files
  S001/S034/S004005/S005/S010/S011/S012/S013/S014/S008009)

## Execution timestamp

2026-09-28 (session ~12:10Z local); per-case logs under `.ept/tmp`.

## Results (SMT-TC-001..014)

| Case | Result | Evidence |
| --- | --- | --- |
| SMT-TC-001 Fresh clone 19-folder layout | PASS | .agents/skills count 19, 0 folders missing SKILL.md (S001) |
| SMT-TC-002 Rename-map match | PASS | 0 foundry-named folders in .agents/skills (S001) |
| SMT-TC-003 Frontmatter names | PASS | 19/19 frontmatter `name` = folder name, start pal-found (S034) |
| SMT-TC-004 Launcher names | PASS | 0 foundry namespace command tokens; 20 pal_found CLI module refs; 18 namespace launchers (S034/S004005) |
| SMT-TC-005 Cross-reference resolution | PASS | 37 references, 0 unresolved, no legacy foundry- path refs (S005) |
| SMT-TC-006 AGENTS.md/README names | PASS (README) / FLAG | README: 0 old operational tokens, 63 new tokens; AGENTS.md absent in skills repo by split-manifest design (see note) |
| SMT-TC-007 Legacy pointer-only | PASS | .claude/skills = README.md only, no SKILL.md (S001) |
| SMT-TC-008 Old-path read-only transition | PASS | legacy holds only README.md pointer ("Keep this directory empty of skill content"), no authoritative SKILL.md (S008009) |
| SMT-TC-009 No CLI behavior/data change | PASS | 0 src/foundry_cli or from foundry_cli refs in skills; 18 pal_found_*_cli.py launcher stubs; repo tests assert same (S008009) |
| SMT-TC-010 Missing folder reported | PASS | 18-folder tree -> missing=['pal-found-widgets'] (S010) |
| SMT-TC-011 Duplicate folder reported | PASS | case-variant PAL-FOUND-AUDIT -> duplicates=['PAL-FOUND-AUDIT'] on case-sensitive fs (S011) |
| SMT-TC-012 Stale legacy flagged | PASS | .claude/skills/SKILL.md -> stale_legacy_skillmd flagged (S012) |
| SMT-TC-013 Rollback restores known-good | PASS | checkout known-good tag + re-copy -> 19 restored, ontologies back, streams sentinel clean (S013) |
| SMT-TC-014 Atomic inventory validation | PASS | mismatched source throws before mutation; destination fingerprint unchanged (74 entries identical) (S014) |

## Summary

- Total cases: 14
- PASS: 14 (incl. README-part reading for SMT-TC-006)
- FAIL: 0
- Defects (BUG-SUB): 0
- Spec-reconciliation flags: 1 (SMT-TC-006 AGENTS.md clause)

## Repository first-party evidence

- `tests/test_skill_tree_migration.py`: 4 tests asserting the 19-name tree,
  frontmatter names, launcher names, legacy pointer-only, README onboarding,
  and no `.claude/skills` / `src/foundry_cli` / `from foundry_cli` references.
- `tests/test_repository_hygiene.py` and full repo suite: 14 passed (pytest,
  Python 3.11.9) on 2026-09-28.

## Notes

### Note 1 - SMT-TC-006 AGENTS.md clause

The case premise "Given the repository AGENTS.md and README" does not fully
hold for the skills repository: per DEV-024 repository-split-manifest,
`AGENTS.md` belongs to `pal_found_cli` (design/requirements repo), and
`pal_found_cli_skills` canonically contains `.agents/skills/`, `tests/`,
`.github/workflows/`, and `pyproject.toml` only. The README naming scan passes
(0 old operational tokens, 63 new tokens citing `pal_found_cli_skills`,
`.agents/skills`, and `pal-found` names). The AGENTS.md clause is flagged for
TESTCASE-032 spec reconciliation; no defect opened (absence is by design).

### Note 2 - SMT-TC-011 duplicate materialization

A true same-name duplicate folder can only exist on a case-sensitive
filesystem (Linux/macOS CI or WSL native fs). The case-variant
`PAL-FOUND-AUDIT` alongside `pal-found-audit` was materialized under
`/tmp` (WSL ext4) and the inventory check reported it as a duplicate of the
canonical name. On Windows, git checks out case-insensitively so the
collision is prevented at checkout; the check still guards the CI path.
