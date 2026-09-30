# TESTEXEC-031 - harness discovery and onboarding QA execution log

## Scope

Executes TESTCASE-031 scenarios (HDN-TC-001..012) for DEV-STORY-030 against
the live canonical skills repository
`https://github.com/t-jet/pal_found_cli_skills` and its README discovery and
onboarding instructions. Chat/transcript JSONL is kept local only and is
never published.

## Environment

- OS: Windows (PowerShell 5.1/pwsh-compatible)
- git: 2.54.0.windows.1
- Python: 3.11.9 (D:\app\Python)
- Harness launcher: local stub reading the same `.agents/skills` (Codex) and
  `.claude/skills` (Claude junction) directory listings a real session scans
  (acceptable substitute per TESTCASE-031 evidence rules).
- Clone: anonymous, `GIT_TERMINAL_PROMPT=0`, empty GIT_ASKPASS, empty
  credential helper
- Clone URL: `https://github.com/t-jet/pal_found_cli_skills`
- Resolved HEAD: `4564e783a948de66d8edb978dc17aaf5ddaeea8d` (branch main)
- Evidence root: `.ept/tmp` (`g001`, `g-fresh`, `ws-codex`, `ws-claude`,
  per-case log files H001/H002/H003/H004/H006/H007012/H008/H011)

## Execution timestamp

2026-09-28 (session ~11:50Z local); per-case logs under `.ept/tmp`.

## Results (HDN-TC-001..012)

| Case | Result | Evidence |
| --- | --- | --- |
| HDN-TC-001 Canonical 19 inventory | PASS | .agents/skills count 19, all pal-found*, includes pal-found (H001) |
| HDN-TC-002 Codex native discovery | PASS | harness stub lists pal-found + pal-found-datasets + 17 more, COUNT=19, exit 0 (H002) |
| HDN-TC-003 Claude junction discovery | PASS | junction to .agents/skills; stub lists COUNT=19, exit 0 (H003) |
| HDN-TC-004 Fresh clone/install discovery | PASS | fresh clone + copy + session lists COUNT=19, exit 0 (H004) |
| HDN-TC-005 Manual onboarding path | PASS | documented target path (workspace .agents/skills) copy verified functional via GCD-TC-006/016; fresh workspace discovered 19 |
| HDN-TC-006 Missing skill absent | PASS | 18-folder workspace lists 18; pal-found-widgets absent (H006) |
| HDN-TC-007 Wrong path yields none | PASS | skills in .claude/not-skills not found; stub NO_SKILL_PATH; onboarding names correct target (H007012) |
| HDN-TC-008 Stale legacy flagged | PASS | SKILL.md in .claude/skills -> onboarding check throws "Refusing to replace non-pointer content", content intact, no junction (H008) |
| HDN-TC-009 Legacy pointer-only | PASS | .claude/skills has only README.md pointer, no SKILL.md (H001) |
| HDN-TC-010 pal-found naming | PASS | 0 foundry-* names in .agents/skills; all pal-found (H001) |
| HDN-TC-011 Cross-harness single copy | PASS | Codex (native) and Claude (junction) both list identical 19-name set; junction is a ReparsePoint to the single canonical copy (H011 + debug) |
| HDN-TC-012 Empty tree yields none | PASS | empty .agents/skills -> stub NO_SKILLS (H007012) |

## Summary

- Total cases: 12
- PASS: 12
- FAIL: 0
- Defects (BUG-SUB): 0

## Repository first-party evidence

- Full skills repo suite: 14 passed (pytest, Python 3.11.9) on 2026-09-28.
- Discovery contract corroborated by `tests/test_repository_hygiene.py` and
  `tests/test_skill_tree_migration.py` in the skills repository.

## Notes

- HDN-TC-003 initial run returned NO_SKILLS because the fixture workspace had
  not yet been populated; after populating the canonical tree (documented
  copy) the junction discovery returned all 19. This was a precondition
  fixture gap, not a product issue; the case is recorded PASS with the
  populated-fixture evidence.
- HDN-TC-011 `no_duplicate_copy` is confirmed by the junction being a single
  ReparsePoint; listing through a junction shows the target content (19 dirs),
  which is the same single canonical copy, not a second copy.
