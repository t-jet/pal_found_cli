# WORK-007 historical isolated skills candidate

Date: 2026-10-14. Candidate: `.ept/tmp/feature012_skills_candidate/pal_found_cli_skills`.

This record preserves the earlier `41a72d632715fe05b380d2a0bc4e97504f523e26` candidate. The final parent release branch pins skills `3bbf551eef30290799d7b790d5244adb694ec66c`; see the [release pin verification](WORK-007-release-pin-plan.md). File hashes below apply to this earlier candidate only.

The candidate starts at advertised skills `origin/main` commit `bb26037813cda6dab5f51c03af9a0b08162a5f7e`. It contains 62 selected skill files, 18 independent namespace reviews, the semantic audit register and script, and one matching documentation test update. Commit `41a72d632715fe05b380d2a0bc4e97504f523e26` has tree `5989d93e7990cf5f517643fefbb870df899c8c31`. The [exact 83-file manifest](WORK-007-skills-candidate-manifest.json) records each path and SHA-256; its own SHA-256 is `5b88c387dc9d94167ccab35282f7fd3d93e8786226fae06f7d4fcd33d7c81572`.

The selection leaves local FEATURE-015 REST and development-guide edits out of `pal-found-dev`, along with its tests, fixtures, and maintainer ledgers. It also leaves the local Data Health configuration guide and its link from `01-check-report.md` out. The candidate keeps the reachable base versions of those files. No live worktree file was changed.

| Check on isolated candidate | Result |
| --- | --- |
| `python pal_found_cli_skills/scripts/feature012_semantic_audit.py` | 351/351 source checks and 351/351 signed semantic decisions pass |
| `python -m pytest -q tests` in candidate skills repo | 33 passed |
| `python -m pytest -q tests/test_offline_skill_gate.py` on copied bundle | 9 passed, including local links and 300-line limit |
| Complete copy of 20 skill folders | 108 files; every source/copy SHA-256 matches |
| Markdown leaf size | 108 files; maximum 207 lines in `pal-found-connectivity/references/02-imports.md` |
| `git diff --cached --check` | Exit 0 |

Copied guidance and installed CLI help support three offline reader checks: a dataset file list with an empty page and a token requires another page; a Build start response requires `build get` or `build jobs` before claiming completion; and a new Data Health check with no report has unknown health until evaluation. Help confirms `file list --page-token`, `build create --target-json` and `--fallback-branches-json`, and `check-report get-latest --limit`. No tenant call was made.

The audit used the current paired CLI files and prepared SDK through local directory junctions. Its row hashes freeze the 18 CLI modules checked, while its revision field records the CLI's `HEAD` (`bfdee7388ce2a8b2d592f17f1ba1d6f10a0424aa`), which does not include dirty CLI fixes. The candidate's 33 tests are its full suite; the 607-test live suite includes FEATURE-015 work deliberately excluded here.

At this snapshot, GitHub advertised `refs/heads/release/feature-012-offline-qa` at `41a72d632715fe05b380d2a0bc4e97504f523e26`, while `refs/heads/main` was `bb26037813cda6dab5f51c03af9a0b08162a5f7e`. Both were verified with `git ls-remote https://github.com/t-jet/pal_found_cli_skills.git` after the push. Later parent pinning and recursive-clone results are recorded in the release pin verification.
