---
id: QUESTION-138
type: question
title: Production PyPI trusted publisher still not effective (invalid-publisher on pypi.org)
status: Closed
addressed_to: project-owner
created: 2026-09-28
updated: 2026-09-30
priority: High
assignee: devops-engineer
reporter: devops-engineer
---

# QUESTION-138: Production PyPI trusted publisher still not effective (invalid-publisher on pypi.org)

## Context

DEVOPS-026 (DEV-STORY-026) publishes `pal_found_cli` to Test PyPI / PyPI via OIDC trusted publishing. Following the resolution of QUESTION-136 (owner corrected the Test PyPI trusted publisher workflow filename from `workflow.yml` to `publish.yml`), DevOps re-ran the publish workflow on tag v0.1.2 (run 36399172205, commit 832a0c5, 2026-09-28 08:44Z).

RESULT: **Test PyPI publish SUCCEEDED** (package pal_found_cli 0.1.2 verified on test.pypi.org) and the staged-release verification passed (clean venv install + `pal-found-datasets --help`). The production PyPI publish step (step 9) STILL fails with `invalid-publisher`.

## Evidence (run 36399172205, step 9 "Publish verified release to PyPI", 2026-09-28 08:45:11Z)

```
##[error]Trusted publishing exchange failure:
Token request failed: the server refused the request for the following reasons:
* `invalid-publisher`: valid token, but no corresponding publisher (Publisher with matching claims was not found)

* `sub`: `repo:t-jet@8374961/pal_found_cli_tool@1330967631:environment:release`
* `repository`: `t-jet/pal_found_cli_tool`
* `repository_owner`: `t-jet`
* `repository_owner_id`: `8374961`
* `workflow_ref`: `t-jet/pal_found_cli_tool/.github/workflows/publish.yml@refs/tags/v0.1.2`
* `job_workflow_ref`: `t-jet/pal_found_cli_tool/.github/workflows/publish.yml@refs/tags/v0.1.2`
* `ref`: `refs/tags/v0.1.2`
* `environment`: `release`
```

## What was verified working (repo side, all fixed by DevOps)

- Version derivation fixed (commits 0981471, 9da6790): release job builds pal_found_cli-0.1.2 exactly.
- Publish action upgraded v1.9.0 -> v1.14.2 (commit 832a0c5): fixes Metadata-Version 2.4 rejection that masked the publisher issue on the previous attempt.
- Tag v0.1.2 moved to 832a0c5; fresh publish run fired and completed: Build SUCCESS, twine check SUCCESS, **Publish to Test PyPI SUCCESS**, Verify staged release SUCCESS, Publish verified release to PyPI FAILED (invalid-publisher).
- Public probe 2026-09-28 08:47Z: test.pypi.org returns pal-found-cli 0.1.2 (wheel + sdist uploaded 08:44:57Z/08:44:58Z). pypi.org still 404.

## What the owner side needs to check (pypi.org ONLY — test.pypi.org is now working)

1. Confirm the trusted publisher is registered on **pypi.org** (production), NOT only test.pypi.org. The failing step is now the FINAL production step; Test PyPI gates successfully.
2. Confirm the production registration uses workflow file **`publish.yml`** (the previous root cause was that it was registered as `workflow.yml`). The claim now renders `job_workflow_ref: t-jet/pal_found_cli_tool/.github/workflows/publish.yml@refs/tags/v0.1.2`.
3. Confirm the registered project name is `pal_found_cli` (normalized on the index as `pal-found-cli`), on the account that receives the OIDC exchange.
4. Verify via pypi.org -> Account settings -> Publishing that the publisher row shows repo `t-jet/pal_found_cli_tool`, workflow file `publish.yml`, environment `release`, project `pal_found_cli`.

## Required outcome

Once the production PyPI publisher registration is verifiably live, DevOps will re-run the publish workflow on tag v0.1.2 (Test PyPI staging + verification already pass; only the final production step remains) and complete DEVOPS-026.

Prior status of parent DEVOPS-026: In Progress.

## Acceptance Criteria

- [ ] Production pypi.org trusted publisher for `pal_found_cli` verified as registered and active (workflow publish.yml, env release)
- [ ] DevOps re-runs the publish workflow and the production PyPI OIDC exchange succeeds
- [ ] pal_found_cli 0.1.2 visible on pypi.org

## Related Documentation

- QUESTION-136 (owner corrected Test PyPI publisher workflow filename to publish.yml; closed)
- DEVOPS-026 evidence comment 20260928-034751-devops-engineer
- Run log evidence: publish run 36399172205

## Notes

Repo-side work for DEVOPS-026 is complete and validated: version fix, action upgrade, Test PyPI publication verified end-to-end. Only the production pypi.org publisher registration remains.
