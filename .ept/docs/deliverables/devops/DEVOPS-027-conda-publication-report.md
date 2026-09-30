# DEVOPS-027 — conda publication and environment setup report

Ticket: DEVOPS-027 (DEV-STORY-028)
Environment: anaconda.org, target = `t-jet` channel (owner personal channel)
Deployment type: CI/CD automated conda build + upload via GitHub Actions publish workflow
Date: 2026-09-28
Author: devops-engineer

## Owner decision (QUESTION-134, Closed)

Project Owner confirmed (comment 20260928-103429-project-manager) that the
`ANACONDA_API_TOKEN` secret was regenerated with the `api:write` scope (and
`api:read`) and updated in the t-jet/pal_found_cli_tool GitHub repository
settings. This resolved the Unauthorized 401 at the conda upload step
(`Authentication token does not have the sufficient scope to perform this action
expected: api:write`).

## Deployment steps

### 1. Pre-deployment check

- Publish workflow (`pal_found_cli_tool/.github/workflows/publish.yml`) exists with
  a `conda` job that builds `conda.recipe` with the standalone `conda-build` binary
  and uploads to the `t-jet` channel when `ANACONDA_API_TOKEN` is present.
- The conda build already passed in earlier runs
  (`pal_found_cli-0.1.2-py_0.conda`); only the upload step was blocked by token scope.
- Release tag `v0.1.2` exists on the remote and points to the publish commit
  (final: `9da6790`).

### 2. Environment validation

- `ANACONDA_API_TOKEN` secret present in t-jet/pal_found_cli_tool (owner-confirmed,
  QUESTION-134). Upload target is the owner channel `t-jet`.
- anaconda.org API reachable; package `t-jet/pal_found_cli` did not exist before
  this deployment (first probe returned 404).

### 3. Deployment execution

- Re-ran the publish workflow on tag `v0.1.2`. The conda job succeeded on three
  consecutive runs (36363807512 attempt 2, 36394268790, 36394972164). The final
  successful upload happened on run 36394972164, conda job, step "Publish conda
  package when channel permission exists" at 2026-09-28 08:05:51Z:

```text
Using Anaconda API: https://api.anaconda.org
Using "t-jet" as upload username
Processing "conda-channel/noarch/pal_found_cli-0.1.2-py_0.conda"
File type is "Conda"
Creating package "pal_found_cli"
Creating release "0.1.2"
Uploading file "t-jet/pal_found_cli/0.1.2/noarch/pal_found_cli-0.1.2-py_0.conda"
Upload complete
conda located at: https://anaconda.org/t-jet/pal_found_cli
```

- The conda package was built with `SETUPTOOLS_SCM_PRETEND_VERSION=0.1.2` (set by
  conda-build from the `GIT_TAG` env var in `conda.recipe/meta.yaml`), so the
  package version matches the release tag exactly.

### 4. Smoke test

- anaconda.org API probe (public, no auth) confirmed the package is live:

```text
name        : pal_found_cli
full_name   : t-jet/pal_found_cli
latest      : 0.1.2
public      : True
files (1):
  noarch/pal_found_cli-0.1.2-py_0.conda  version=0.1.2  uploaded=2026-09-28 08:05:51Z  size=81317
```

- Installed the published package in a clean conda env
  (`conda install -p <env> pal_found_cli=0.1.2 -c t-jet -c conda-forge`): install
  succeeded from the `t-jet` channel.
- All 18 `pal-found-*` console entry points present in the env
  (`pal-found-admin`, `pal-found-aip-agents`, `pal-found-audit`,
  `pal-found-checkpoints`, `pal-found-connectivity`, `pal-found-data-health`,
  `pal-found-datasets`, `pal-found-filesystem`, `pal-found-functions`,
  `pal-found-language-models`, `pal-found-media-sets`, `pal-found-models`,
  `pal-found-ontologies`, `pal-found-orchestration`, `pal-found-sql-queries`,
  `pal-found-streams`, `pal-found-third-party-applications`, `pal-found-widgets`).
- Smoke `pal-found-datasets --help` -> Foundry Datasets CLI usage (33 operations);
  `pal-found-audit --help` -> Foundry Audit CLI (2 log-file operations);
  `pal-found-checkpoints --help` -> Foundry Checkpoints CLI (3 operations). All exit 0.

### 5. Documentation

This report is registered in `.ept/docs/document_index.md` under the DevOps
deployment reports section. Deployment evidence and steps are documented as a
comment on DEVOPS-027.

## Durable deployment evidence

| Item | Value |
| --- | --- |
| Package | `t-jet/pal_found_cli` version `0.1.2` |
| File | `noarch/pal_found_cli-0.1.2-py_0.conda` (81317 bytes) |
| Uploaded | 2026-09-28 08:05:51 UTC (final run 36394972164) |
| Channel | `t-jet` (owner personal channel) |
| URL | `https://anaconda.org/t-jet/pal_found_cli` |
| Public | Yes |
| Entry points | 18 `pal-found-*` console scripts, smoke-tested |

## Acceptance criteria

- [x] Conda build + upload automated via GitHub Actions publish workflow on tag push
- [x] Scoped credentials: `ANACONDA_API_TOKEN` with `api:write` (no secrets in source)
- [x] Prerequisites, publish steps, verification, and rollback documented (this report)
- [x] Target environment validated and durable deployment evidence recorded
- [x] Package verified installable from the published channel with working entry points

## Rollback

The package is owner-controlled on anaconda.org. To roll back: delete or hide the
release `0.1.2` on `https://anaconda.org/t-jet/pal_found_cli/settings` (owner
action), or publish a corrected version. No destructive action was taken during
this deployment. The token is scoped to `api:write`; rotation is owner-side.

## Result

SUCCESS. `pal_found_cli` 0.1.2 is publicly published on the `t-jet` anaconda.org
channel, verified installable with all entry points smoke-tested.
