# Architecture Analysis — SA-ANA-005

## Publish foundry_cli_tool to a Conda Channel

| Field | Value |
| --- | --- |
| **Document ID** | SA-ANA-005 |
| **Feature** | FEATURE-005 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Solution Architect |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Affected Services and Interfaces

| Asset | Current state | Target state |
| --- | --- | --- |
| Conda channel (anaconda.org or conda-forge) | absent | present and public |
| Conda recipe (`meta.yaml`) | absent | generated and versioned |
| GitHub Actions CI | builds wheel only | also builds and uploads the conda package |
| Git tags | source of truth for releases | shared by PyPI and conda publication |
| README | pip install instructions | adds conda install instructions |

The package is pure Python with runtime dependencies already available on conda
channels (`foundry-platform-sdk`, `python-dotenv`, `requests`), so a standard
recipe covers it.

## 2. Architecture Approach

Two channel options:

- **Option A: own channel on anaconda.org.** Build the package with
  `conda-build`, upload with `anaconda-client`, and document the channel in the
  README. Full control over the channel, no external review process.
- **Option B: conda-forge feedstock.** Generate a recipe with grayskull and
  maintain a feedstock that conda-forge builds and serves. Highest visibility,
  but a public review process and stricter maintenance rules.

Recommended: start with Option A for control and speed, keep Option B as a
follow-up if the community channel is wanted. Either way, the git tag stays the
single source of truth so conda and PyPI releases cannot drift (BR-005-03,
AC-005-03).

## 3. Technology Stack

- conda-build for package building
- grayskull for recipe generation
- anaconda-client for channel upload
- anaconda.org channel (Option A) or conda-forge feedstock (Option B)
- GitHub Actions CI to build on tag and on main

No changes to the Python runtime or packaging internals.

## 4. General Implementation Approach

1. Generate the recipe with grayskull from `pyproject.toml`; review `meta.yaml`
   for correct version source (git tag) and dependencies.
2. Build locally with `conda-build` and verify the package installs into a clean
   conda environment (AC-005-01, AC-005-02).
3. Add a GitHub Actions job that builds and uploads on tag pushes
   (AC-005-03).
4. Upload to the channel; verify the channel page describes the tool and
   installation (AC-005-05).
5. Confirm a user without channel access gets a clear failure message
   (AC-005-04) by testing against a channel without permissions.

## 5. General Migration Approach

- Phase 1 (recipe): generate and validate the recipe.
- Phase 2 (channel): create the channel and upload the first build.
- Phase 3 (automate): wire the build and upload into CI on tags.
- Phase 4 (sync): document that every release updates PyPI (SA-ANA-004) and the
  conda channel from the same tag.

## 6. Risks and Constraints

| Item | Risk | Mitigation |
| --- | --- | --- |
| Version drift | conda and PyPI releases diverge | Both built from the same git tag |
| Broken release | users install a non-working conda package | Clean-env install check before announcing |
| Dependency availability | a dependency missing on conda | Verify all runtime deps exist on the target channel |
| Channel choice | anaconda.org vs conda-forge direction not decided | Recommendation: own channel first, feedstock later |

## 7. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-005 (Analysis) |
| Epic | EPIC-010 |
| BA sub-task | BA-ANA-005 |
| SA sub-task | SA-ANA-005 |
| BA deliverable | BA-ANA-005-business-analysis.md |
| Requirement source | PO architecture-change request 2026-08-11 |
