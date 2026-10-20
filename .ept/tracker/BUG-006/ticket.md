---
id: BUG-006
type: bug
title: 'Security Scan job fails: safety dependency scan reports nltk 3.10.3 path-traversal
  vulnerability'
status: Closed
affected_version: pal_found_cli_tool-main-CI-run-37427184107
created: 2026-10-11
updated: 2026-10-11
priority: High
resolution: Done
assignee: qa-engineer
reporter: project-manager
component: ci
---

# BUG-006: Security Scan job fails: safety dependency scan reports nltk 3.10.3 path-traversal vulnerability

## Description

# Security Scan job fails: safety reports path-traversal vulnerability in nltk 3.10.3

## Observed defect

The `CI` workflow in `t-jet/pal_found_cli_tool` fails at the `Security Scan` job on `main`. The `Run bandit SAST (fail on HIGH severity)` step passes. The `Run safety dependency scan` step fails with exit code 64 after reporting one vulnerability, which skips the downstream `Build Package` job.

## Environment and affected version

- Repository: `t-jet/pal_found_cli_tool`
- Workflow: `.github/workflows/ci.yml`, job `security-scan`
- Runner: `ubuntu-latest`, Python `3.11`
- Latest failing run: `37427184107` (branch `main`, created 2026-10-06T07:02:07Z)
- Failing job: `112150492418` (`Security Scan`)
- Tool version: `safety 3.8.1`

## Reproduction evidence

Step log of job `112150492418`:

```text
Found and scanned 69 packages
1 vulnerability reported
0 vulnerabilities ignored

-> Vulnerability found in nltk version 3.10.3
   Vulnerability ID: SFTY-20260902-58666
   Affected spec: <=3.10.3
   ADVISORY: ... Path Traversal due to the use of built-in `open()` on caller-controlled paths ... (TransitionParser.train, TransitionParser.parse, AveragedPerceptron.save, AveragedPerceptron.load, PerceptronTagger.save_to_json, save_maxent_params)
   CVE-2026-81726

##[error]Process completed with exit code 64.
```

`nltk` is not a declared dependency in `pal_found_cli_tool/pyproject.toml` (direct dependencies are `foundry-platform-sdk`, `python-dotenv`, `requests`; `dev` extras add pytest, mypy, ruff, bandit). It enters the scan environment transitively. The controlling package must be confirmed before a fix is chosen.

## Expected behavior

The `security-scan` job concludes success on `main` and the full `CI` workflow concludes success. Bandit keeps failing the build on HIGH-severity findings (no `|| true`). The dependency scan passes with no unremediated HIGH or CRITICAL findings, or with only reviewed, time-bound suppressions recorded in a committed policy file.

## Actual behavior

The dependency scan fails on the `nltk` advisory and the workflow stops before build. `pip install -e ".[dev]"` alone is insufficient setup; the job also runs `pip install bandit safety`, and `safety check --full-report` reports the finding against the resolved environment.

## Acceptance criteria

- The `Run safety dependency scan` step passes on `main` with no unremediated HIGH or CRITICAL findings.
- The `security-scan` job and the full `CI` workflow conclude success; `Build Package` is no longer skipped because of the scan.
- The Bandit HIGH-severity gate stays enforced.
- A vulnerable transitive dependency is upgraded or constrained to a fixed release where one exists. Any remaining suppression is a reviewed, time-bound entry in a committed policy file with a recorded reason and expiry, not an inline `--ignore` without justification.
- The fix is reversible and does not weaken the other CI jobs (lint, type-check, test).

## Fix direction

1. Confirm which direct dependency pulls `nltk` (inspect `pip install -e ".[dev]"` resolution and `pip show nltk` in the workflow environment).
2. Check whether a fixed `nltk` release exists above 3.10.3; if so, constrain the transitive dependency to the fixed floor.
3. If no fixed release exists, evaluate a documented, time-bound suppression and record it in a safety policy file, with the rationale and a follow-up to remove it.

## Related documentation

- `pal_found_cli_tool/.github/workflows/ci.yml` (job `security-scan`)
- `pal_found_cli_tool/pyproject.toml` (dependencies and `dev` extras)
- `.ept/docs/deliverables/development/DEV-026-release-verification.md`


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
