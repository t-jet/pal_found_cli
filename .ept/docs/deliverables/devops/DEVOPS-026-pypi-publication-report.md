# DEVOPS-026 — PyPI publication and environment setup report

Ticket: DEVOPS-026 (DEV-STORY-026)
Environment: PyPI (production) + Test PyPI (staging), OIDC trusted publishing
Deployment type: CI/CD automated build + staged publish via GitHub Actions publish workflow on tag `v0.1.2`
Date: 2026-09-28 (initial) / 2026-09-30 (completed)
Author: devops-engineer
Status: COMPLETE — pal_found_cli 0.1.2 published to production PyPI and verified (2026-09-30)

## Owner decisions

- QUESTION-133 (Closed): owner confirmed pending trusted publishers registered on pypi.org and test.pypi.org for repo `t-jet/pal_found_cli_tool`, workflow `publish.yml`, environment `release`.
- QUESTION-136 (Closed, 2026-09-28): root cause identified — the registered publisher used workflow file `workflow.yml`, but the actual workflow is `publish.yml` (OIDC claim `job_workflow_ref t-jet/pal_found_cli_tool/.github/workflows/publish.yml`). Owner corrected the registration to `publish.yml` on test.pypi.org (and pypi.org). Comment 20260928-113334-project-manager.
- QUESTION-138 (In Progress, 2026-09-28): production pypi.org exchange still fails with `invalid-publisher` after the Test PyPI fix; owner-side action required (see below).

## Repo-side fixes applied (DevOps, all owner-authorized publication actions)

1. **Version derivation bug fixed** (commits `0981471`, `9da6790`): untracked `src/pal_found_cli/_version.py` + `.gitignore` entry; the release job now builds `pal_found_cli-0.1.2` exactly (previously a tracked version file caused dirty-state bumps).
2. **Publish action upgraded** `pypa/gh-action-pypi-publish` v1.9.0 → v1.14.2 (commit `832a0c5`, SHA `dc37677b2e1c63e2034f94d8a5b11f265b73ba33`): v1.9.0's bundled twine rejected Metadata-Version 2.4 wheels (`InvalidDistribution: Metadata is missing required fields: Name, Version`) after setuptools 84 began emitting 2.4 metadata; this masked the publisher check on the previous attempt.
3. Tag `v0.1.2` moved to `832a0c5` and force-pushed; fresh publish run fired (run `36399172205`).

## Deployment steps (run 36399172205, 2026-09-28 08:44Z, tag v0.1.2 @ 832a0c5)

### 1. Pre-deployment check

- Publish workflow (`pal_found_cli_tool/.github/workflows/publish.yml`) exists with release + conda jobs; tag-triggered on `v*`.
- Release tag `v0.1.2` on remote at the publish commit; version derivation verified (builds `pal_found_cli-0.1.2`).
- All 18 `pal-found-*` entry points defined in `[project.scripts]`.

### 2. Environment validation

- OIDC trusted publishing configured (`permissions: id-token: write`, environment `release`).
- Owner-side publisher registrations: test.pypi.org corrected to `publish.yml` (effective); pypi.org registration pending/incorrect (blocker, QUESTION-138).

### 3. Deployment execution

| Step | Result |
| :--- | :--- |
| Build package (`python -m build`) | SUCCESS — `pal_found_cli-0.1.2.tar.gz` + `pal_found_cli-0.1.2-py3-none-any.whl` |
| Check package metadata (`twine check dist/*`) | SUCCESS (PASSED) |
| Publish to Test PyPI | SUCCESS — uploaded 2026-09-28 08:44:57Z (wheel) / 08:44:58Z (sdist) |
| Verify staged release in clean environment | SUCCESS — clean venv install from test.pypi.org + `pal-found-datasets --help` |
| Publish verified release to PyPI | FAILED 08:45:11Z — `invalid-publisher` (owner-side pypi.org registration) |
| Build and optionally publish conda package | SUCCESS — consistent with DEVOPS-027 (already closed) |

### 4. Smoke test

- Test PyPI public probe (2026-09-28 08:47Z): `https://test.pypi.org/pypi/pal_found_cli/json` returns name `pal-found-cli` (normalized), latest `0.1.2`, releases `['0.1.2']`, both files present:
  - `pal_found_cli-0.1.2-py3-none-any.whl` (uploaded 08:44:57Z)
  - `pal_found_cli-0.1.2.tar.gz` (uploaded 08:44:58Z)
- Clean-environment staged release verification (CI step): install `pal_found_cli==0.1.2` from test.pypi.org + `pal-found-datasets --help` → SUCCESS.
- Production pypi.org probe: HTTP 404 (package not present — expected, publish step blocked).

### 5. Documentation

- This report registers the deployment evidence.
- Blocker and deployment progress documented on DEVOPS-026 (comment 20260928-114947-devops-engineer).
- QUESTION-138 created for the production PyPI publisher (comment 20260928-114910-devops-engineer).

### 6. Rollback

Rollback for the published Test PyPI artifacts is not required (Test PyPI is a staging index; `pal_found_cli` is a new project on it). For production: no artifacts were uploaded to pypi.org, so no rollback is needed. The movable tag `v0.1.2` remains the rollback baseline; re-running the workflow on the same tag is idempotent (Test PyPI `skip_existing: false` would need a bump or skip flag only for re-uploads, which do not apply here since production never received the package).

## Owner-side blocker (QUESTION-138)

Production pypi.org trusted publisher for project `pal_found_cli` (normalized `pal-found-cli`), repo `t-jet/pal_found_cli_tool`, workflow file `publish.yml`, environment `release` is not registered/active. Evidence (step 9, run 36399172205, 08:45:11Z):

```text
* `invalid-publisher`: valid token, but no corresponding publisher
* `sub`: `repo:t-jet@8374961/pal_found_cli_tool@1330967631:environment:release`
* `job_workflow_ref`: `t-jet/pal_found_cli_tool/.github/workflows/publish.yml@refs/tags/v0.1.2`
* `ref`: `refs/tags/v0.1.2`
* `environment`: `release`
```

## Acceptance criteria status

- [x] CI/CD publish pipeline configured (lint/type-check/test/security-scan/build/publish in place; publish tag-triggered only)
- [x] Trusted publishing used; no secrets embedded in source or artifacts
- [x] Documentation of prerequisites, publish steps, verification, rollback, and external permission blockers
- [x] Test PyPI target environment validated and package published (durable evidence above)
- [x] Production PyPI publication — COMPLETED 2026-09-30 (see below)

## Production PyPI publication — completion (2026-09-30)

### Repo-side fixes applied (commit `db9ae68`, tag `v0.1.2` moved to it)

1. **Version shadowing fixed** — `tag.strict = true` + `tag.prefix = "v"` in `[tool.setuptools_scm]` (`pyproject.toml`). Root cause: the `qa-verify-20260929` tag shared commit `832a0c5` with `v0.1.2`; with setuptools-scm default (`tag.strict = false`) the date tag was parsed as version `20260929` and shadowed the release tag, so run 36634536438 built and staged `pal_found_cli-20260929` instead of `0.1.2`.
2. **Test PyPI attestation collision fixed** — `attestations: false` on the Test PyPI staging step in `publish.yml`. Root cause: `pypa/gh-action-pypi-publish` v1.14.2 defaults `attestations: true`; the staging step wrote `*.publish.attestation` files into `dist/`, and the production step then failed with "already have publish attestations" before upload. Attestations now bind only to the final production publish (OIDC).
3. **Staging re-run idempotency fixed** — `skip-existing: true` on the Test PyPI step. The identical `0.1.2` filenames were already staged by run 36399172205; a plain re-upload returned 400 "File already exists". The production step keeps `skip-existing: false` so a production duplicate fails loudly.

### Deployment steps (run 36681617309, 2026-09-30 07:04Z, tag v0.1.2 @ db9ae68, <https://github.com/t-jet/pal_found_cli_tool/actions/runs/36681617309>)

| Step | Result |
| :--- | :--- |
| Build package (`python -m build`) | SUCCESS — `pal_found_cli-0.1.2.tar.gz` + `pal_found_cli-0.1.2-py3-none-any.whl` (version now 0.1.2, not 20260929) |
| Check package metadata (`twine check dist/*`) | SUCCESS (PASSED) |
| Publish to Test PyPI | SUCCESS — existing 0.1.2 files skipped (`skip-existing`), verified staged |
| Verify staged release in clean environment | SUCCESS — clean venv install + `pal-found-datasets --help` |
| Publish verified release to PyPI | SUCCESS — OIDC exchange OK; attestations generated; uploads 200 OK |
| Build and optionally publish conda package | SUCCESS |

### Smoke test (production, 2026-09-30)

- Production pypi.org probe `https://pypi.org/pypi/pal_found_cli/json` (07:07Z): name `pal-found-cli`, latest `0.1.2`, releases `['0.1.2']`:
  - `pal_found_cli-0.1.2-py3-none-any.whl` (uploaded 2026-09-30T07:04:58Z, <https://files.pythonhosted.org/packages/e3/10/5d991fbb9e635d7e7b88ccc7c2dcc6190fe130226e8be5376890f7b458b3/pal_found_cli-0.1.2-py3-none-any.whl>)
  - `pal_found_cli-0.1.2.tar.gz` (uploaded 2026-09-30T07:04:59Z)
- Clean-env install smoke (`.ept/tmp/de026-clean-env`, Python 3.11, production PyPI only): `pip install pal_found_cli==0.1.2` → SUCCESS; `importlib.metadata.version('pal_found_cli')` = `0.1.2`; all 18 `pal-found-*` launchers present; `pal-found-datasets --help` exit 0; `pal-found-admin --help` exit 0.

### Rollback

- Production PyPI: versioned release `0.1.2`; rollback = yank `0.1.2` on pypi.org (documented). No prior production release to regress to.
- Tag `v0.1.2` remains the reproducible build baseline (`db9ae68`).

## Related tickets

- DEVOPS-026 (In Progress/Closed), DEV-STORY-026
- QUESTION-133, QUESTION-136 (closed), QUESTION-138 (closed)
- DEVOPS-027 (conda, closed) — conda publication independent of PyPI, already successful
