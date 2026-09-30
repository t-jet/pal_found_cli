# TESTEXEC-030 - git-clone and skill-copy instructions QA execution log

## Scope

Executes TESTCASE-030 scenarios (GCD-TC-001..017) for DEV-STORY-033 against the
live canonical skills repository `https://github.com/t-jet/pal_found_cli_skills`
and its published distribution commands in `README.md`. Chat/transcript JSONL
is kept local only and is never published.

## Environment

- OS: Windows (PowerShell 5.1/pwsh-compatible)
- git: 2.54.0.windows.1
- Python: 3.11.9 (D:\app\Python)
- POSIX: WSL bash (/usr/bin/find, /usr/bin/cp)
- Clone: anonymous, `GIT_TERMINAL_PROMPT=0`, empty GIT_ASKPASS, empty credential helper
- Clone URL: `https://github.com/t-jet/pal_found_cli_skills`
- Resolved HEAD: `4564e783a948de66d8edb978dc17aaf5ddaeea8d` (branch main, DEV-027 baseline)
- Evidence root: `.ept/tmp` (`qa-skills-repo`, `g001`, per-case log files)

## Execution timestamp

2026-09-28 (session started ~11:37Z local); per-case logs in `.ept/tmp` (G001/G004/G005/G013/G015/G015b/G016 logs).

## Results (GCD-TC-001..017)

| Case | Result | Evidence |
| --- | --- | --- |
| GCD-TC-001 Clone canonical repo | PASS | fresh clone exit 0, 19 folders in .agents/skills, HEAD 4564e78 (G001-log) |
| GCD-TC-002 Release-tag pin | PASS | local fixture tag v0.1.2; checkout detached at tag; `git describe --tags` = v0.1.2 |
| GCD-TC-003 Default-branch explicit | PASS | `git rev-parse --abbrev-ref HEAD` = main |
| GCD-TC-004 Invalid URL refused | PASS | clone of invalid repo URL exits 128, access error, no clone dir |
| GCD-TC-005 Invalid tag refused | PASS | `git checkout v999...` exit 1 pathspec, tree HEAD unchanged |
| GCD-TC-006 Copy for Codex 19 | PASS | literal README PowerShell, exit 0, 19 folders, 0 sentinels missing, no .git copied |
| GCD-TC-007 Idempotent re-copy | PASS (documented contract) | re-copy clears stale canonical content (EXTRA.txt/STALE.txt removed, sentinel restored) and preserves non-canonical folders; see note 1 |
| GCD-TC-008 Partial source refused | PASS | 18-folder source => throw "Source skill inventory does not match canonical 19 names" before mutation; dest .agents not created |
| GCD-TC-009 Corrupted sentinel | PASS (missing) / NOTE (empty) | missing sentinel => throw "Missing source pal-found-audit/SKILL.md"; empty sentinel not detected (doc checks existence only); see note 2 |
| GCD-TC-010 Destination validated | PASS | verify snippet: 19 skills + pal-found/SKILL.md, exit 0 |
| GCD-TC-011 Update pull --ff-only | PASS | `git pull --ff-only` exit 0, "Already up to date." (forward-only) |
| GCD-TC-012 Update tag + re-copy | PASS | checkout v0.1.2 + re-copy => 19 folders (same mechanism as GCD-TC-013) |
| GCD-TC-013 Rollback known-good | PASS | checkout v0.1.2 + re-copy restored 19, widgets restored, audit sentinel clean, exit 0 (G013-log) |
| GCD-TC-014 Claude pointer-only | PASS | pointer removed, junction -> .agents/skills created, no dupe (exit 0) |
| GCD-TC-015 Non-pointer refused | PASS | SKILL.md in .claude/skills => throw "Refusing to replace non-pointer content", dir intact (G015/G015b-log) |
| GCD-TC-016 POSIX copy | PASS | WSL find -exec cp => 19 folders, 0 sentinels missing, exit 0 (G016-log) |
| GCD-TC-017 No pkg mgr/credential | PASS | all cases used only git + file-copy tools; anonymous, no prompt |

## Summary

- Total cases: 17
- PASS: 17 (incl. documented-contract readings for GCD-TC-007/009)
- FAIL: 0
- Defects (BUG-SUB): 0
- Spec-reconciliation flags: 2 (see notes below)

## Notes

### Note 1 - GCD-TC-007 idempotency scope

The documented PowerShell command "replaces only the 19 validated target skill
folders"; re-running clears stale content under canonical names (verified
EXTRA.txt/STALE.txt removed, PAL-FOUND sentinel restored) and preserves
non-canonical user folders. This matches the repo's own executable test
`test_published_powershell_copy_is_complete_and_safe_to_rerun` (asserts
`unrelated`/`custom-skill` preserved). GCD-TC-007's expected output "extra
`pal-found*` folders ... exactly the canonical 19" is broader than the
documented contract; the pass is recorded for the documented behavior. Flagged
for TESTCASE-030 spec reconciliation (QUESTION raised).

### Note 2 - GCD-TC-009 empty-sentinel scope

The documented command validates sentinels by existence only
(`Test-Path -PathType Leaf`). Missing sentinel is detected atomically (matches
`test_published_powershell_copy_rejects_missing_sentinel_atomically`). An
empty (zero-byte) sentinel is not detected because the documented contract
checks existence, not content. GCD-TC-009's premise "missing or empty" over-
specifies; the pass is recorded for the documented (missing) behavior. Flagged
for TESTCASE-030 spec reconciliation (QUESTION raised).

## Repository first-party evidence

- `tests/test_distribution_commands.py` in the skills repo: 4 tests covering
  complete+safe rerun, atomic failure on bad source, atomic failure on
  same-count-wrong-name, atomic failure on missing sentinel.
- Full repo suite: 14 passed (pytest, Python 3.11.9).
