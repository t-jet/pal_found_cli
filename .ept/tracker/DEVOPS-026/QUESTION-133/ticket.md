---
id: QUESTION-133
type: question
title: Register Test PyPI trusted publisher for pal_found_cli (OIDC invalid-publisher)
status: Closed
addressed_to: project-owner
created: 2026-09-28
updated: 2026-09-28
priority: High
assignee: devops-engineer
reporter: devops-engineer
---

# QUESTION-133: Register Test PyPI trusted publisher for pal_found_cli (OIDC invalid-publisher)

## Description

# Register Test PyPI trusted publisher for pal_found_cli

## Context

DEVOPS-026 (DEV-STORY-026) is publishing `pal_found_cli` to PyPI/Test PyPI via OIDC trusted publishing. The root cause of the "workflow ran but no results on PyPI" issue has been diagnosed from the actual workflow logs (run 36363162512, 2026-09-28):

1. The publish workflow never fired because no `v*` tag was pushed (tags `0.1.0/0.1.1/0.1.2` existed only locally). A release tag `v0.1.2` was pushed, which correctly triggered the workflow.
2. The workflow then failed at the "Publish to Test PyPI" step with:

```
Trusted publishing exchange failure:
Token request failed: the server refused the request for the following reasons:
* `invalid-publisher`: valid token, but no corresponding publisher (Publisher with matching claims was not found)
sub: repo:t-jet@8374961/pal_found_cli_tool@1330967631:environment:release
job_workflow_ref: t-jet/pal_found_cli_tool/.github/workflows/publish.yml@refs/tags/v0.1.2
```

This means the OIDC token was issued correctly, but **no trusted publisher is registered on Test PyPI** matching the project `pal_found_cli`.

## Owner action requested

Register a **pending trusted publisher** on test.pypi.org (account: the PyPI account associated with the owner) for the future project `pal_found_cli` with EXACTLY these claims (asset publisher / GitHub Actions):

- GitHub repository owner: `t-jet`
- GitHub repository: `pal_found_cli_tool`
- Workflow file name: `publish.yml`
- Environment name: `release`

The same publisher should also be registered on PyPI (production) so the final publish step succeeds after Test PyPI verification.

## Required verification

Confirm the publisher names match the exact claim (especially `environment: release`) so the OIDC exchange succeeds. Without this owner action, the AI agent cannot complete the PyPI publication (test.pypi.org/pypi.org account-side configuration).

Prior status of parent DEVOPS-026: In Progress.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
