---
id: QUESTION-135
type: question
title: ANACONDA_API_TOKEN lacks api:write scope for conda channel upload
status: Duplicated
addressed_to: project-owner
created: 2026-09-28
updated: 2026-09-28
priority: Medium
assignee: devops-engineer
reporter: devops-engineer
---

# QUESTION-135: ANACONDA_API_TOKEN lacks api:write scope for conda channel upload

## Description

# ANACONDA_API_TOKEN requires api:write scope for channel upload

## Context

DEVOPS-027 (DEV-STORY-028) automates conda publication via GitHub Actions. The workflow (publish.yml conda job) now builds the package successfully (pal_found_cli-0.1.2-py_0.conda), but the upload step fails:

```
Unauthorized: ('Authentication token does not have the sufficient scope to perform this action expected: api:write', 401)
```

This confirms the `ANACONDA_API_TOKEN` secret in t-jet/pal_found_cli_tool exists (owner confirmed in QUESTION-120 comment 20260928-022219-project-manager) but does NOT have the `api:write` scope required to upload packages to the channel.

## Owner action requested

Regenerate the anaconda.org API token with the `api:write` scope (and `api:read` for verification), and update the `ANACONDA_API_TOKEN` secret in the t-jet/pal_found_cli_tool GitHub repository settings. The upload target channel is the owner's username `t-jet` (personal channel).

## Required verification

After the token is updated, the agent will re-run the publish workflow on tag v0.1.2; the conda build already passes, so only the upload step remains to be verified on anaconda.org.

Prior status of parent DEVOPS-027: In Progress.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
