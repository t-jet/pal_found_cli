---
id: QUESTION-136
type: question
title: Test PyPI trusted publisher still not effective (invalid-publisher persists)
status: Closed
addressed_to: project-owner
created: 2026-09-28
updated: 2026-09-28
priority: High
assignee: devops-engineer
reporter: devops-engineer
---

# QUESTION-136: Test PyPI trusted publisher still not effective (invalid-publisher persists)

## Description

# QUESTION-136: Test PyPI trusted publisher still not effective (invalid-publisher persists)

## Context

DEVOPS-026 (DEV-STORY-026) publishes `pal_found_cli` to Test PyPI / PyPI via OIDC trusted publishing. After the owner confirmed (QUESTION-133, comment 20260928-102441-project-manager) that a pending trusted publisher was registered on both pypi.org and test.pypi.org for repo `t-jet/pal_found_cli_tool`, workflow `publish.yml`, environment `release`, the publish workflow was re-run three times. The Test PyPI publish step STILL fails with `invalid-publisher`.

## Evidence (latest run 36394972164, 2026-09-28 08:02:42Z, tag v0.1.2 @ 9da6790)

```
##[error]Trusted publishing exchange failure:
Token request failed: the server refused the request for the following reasons:
* `invalid-publisher`: valid token, but no corresponding publisher (Publisher with matching claims was not found)

* `sub`: `repo:t-jet@8374961/pal_found_cli_tool@1330967631:environment:release`
* `repository`: `t-jet/pal_found_cli_tool`
* `repository_owner`: `t-jet`
* `repository_owner_id`: `8374961`
* `job_workflow_ref`: `t-jet/pal_found_cli_tool/.github/workflows/publish.yml@refs/tags/v0.1.2`
* `ref`: `refs/tags/v0.1.2`
```

Runs observed with the same failure after the owner's registration claim:
- 36363807512 attempt 2 (07:40:57Z) — rerun-failed-jobs
- 36394268790 (07:55:27Z) — fresh tag push with fetch-depth: 0 fix
- 36394972164 (08:02:42Z) — fresh tag push with _version.py untracked fix (builds pal_found_cli-0.1.2 correctly)

Public index probes at 10:50 local (08:50Z): test.pypi.org and pypi.org both return 404 for `pal_found_cli` — nothing has been published.

## What the owner side needs to check

1. Confirm the trusted publisher was registered on test.pypi.org (NOT only pypi.org). The failing step is "Publish to Test PyPI" — the production PyPI step never runs because Test PyPI gates first.
2. Confirm the registered workflow filename is exactly `publish.yml` and the environment name is exactly `release` (case-sensitive, claim uses `environment:release`).
3. Confirm the publisher is registered for the future project name `pal_found_cli` (pending publisher), on the account that will receive the OIDC exchange.
4. If registered, verify the registration exists by signing in to test.pypi.org -> Account settings -> Publishing. A pending publisher is active on first use for a NEW project; no initial upload is required to "activate" it.
5. Confirm whether test.pypi.org may need the publisher registered separately from pypi.org (they are separate accounts/indices; the owner said both were configured, but the exchange still fails).

## Required outcome

Once the Test PyPI publisher registration is verifiably live, DevOps will re-run the publish workflow on tag v0.1.2 (build now produces pal_found_cli-0.1.2 correctly) and complete DEVOPS-026.

Prior status of parent DEVOPS-026: In Progress.

## Acceptance Criteria

- [ ] Test PyPI trusted publisher for `pal_found_cli` verified as registered and active on test.pypi.org
- [ ] (If needed) Production PyPI publisher registered so the final publish step can succeed
- [ ] DevOps re-runs the publish workflow and the Test PyPI OIDC exchange succeeds

## Related Documentation

- DEVOPS-026 diagnosis comment 20260928-034751-devops-engineer (original invalid-publisher root cause)
- QUESTION-133 (owner confirmation of publisher registration)

## Notes

The repo-side version derivation bug (tracked _version.py causing dirty-state bumps) was fixed by DevOps on 2026-09-28 (commits 0981471, 9da6790); the release job now builds pal_found_cli-0.1.2 exactly. Only the publisher registration remains.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
