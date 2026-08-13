# Architecture Analysis — SA-ANA-004

## Publish foundry_cli_tool to PyPI for pip Installation

| Field | Value |
| --- | --- |
| **Document ID** | SA-ANA-004 |
| **Feature** | FEATURE-004 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Solution Architect |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Affected Services and Interfaces

| Asset | Current state | Target state |
| --- | --- | --- |
| Distribution name in pyproject.toml | `foundry-cli` | `foundry_cli_tool` |
| Import package | `foundry_cli` | unchanged |
| Console entry points (18 `foundry-*`) | present | unchanged |
| publish.yml GitHub Actions workflow | tag-triggered, twine, `PYPI_API_TOKEN` | tag-triggered; OIDC trusted publishing preferred |
| PyPI project page | absent | present, README-based description |
| Release tags | internal | pushed to public repo (FEATURE-002) |

The distribution name on PyPI is independent of the import package name and of
the console entry point names. Renaming the distribution to `foundry_cli_tool`
does not change `import foundry_cli` or any installed command.

## 2. Architecture Approach

Publish the tool through the standard PyPI flow driven by git tags. The existing
publish.yml workflow builds the sdist and wheel with setuptools, validates them
with twine, and uploads to PyPI. Two changes are required:

- Rename the distribution in `pyproject.toml` from `foundry-cli` to
  `foundry_cli_tool` so `pip install foundry_cli_tool` works (BR-003-01).
- Replace the long-lived `PYPI_API_TOKEN` secret with PyPI trusted publishing
  (OIDC) where the workflow obtains a short-lived token via `id-token: write`.
  This removes the token leak risk called out in BA-ANA-003.

A first release is staged on Test PyPI, verified with a clean-venv install, then
promoted to PyPI (AC-003-04).

## 3. Technology Stack

- PyPI (production) and Test PyPI (staging)
- setuptools PEP 517 build (existing)
- twine for artifact validation and upload
- GitHub Actions publish workflow (existing, hardened)
- Python 3.11+ (existing requirement)

No new runtime dependencies.

## 4. General Implementation Approach

1. Rename the distribution to `foundry_cli_tool` in `pyproject.toml`; verify the
   built sdist and wheel carry the new name.
2. Update publish.yml to use trusted publishing (OIDC) and a `v*` tag trigger;
   keep twine validation.
3. Create the PyPI project page and confirm the README renders as the long
   description (AC-003-05).
4. Publish a first release: build, twine check, upload to Test PyPI, install into
   a clean venv, smoke-run entry points, then promote to PyPI (AC-003-01, AC-003-02).
5. Verify `pip install --upgrade foundry_cli_tool` delivers new versions on the
   next tag (AC-003-03).

## 5. General Migration Approach

- Phase 1 (rename): distribution rename with build verification.
- Phase 2 (stage): Test PyPI upload and clean-install verification.
- Phase 3 (release): tag-triggered publish to PyPI; document the release in the
  design repo.
- Phase 4 (harden): switch to OIDC trusted publishing and revoke the token.

## 6. Risks and Constraints

| Item | Risk | Mitigation |
| --- | --- | --- |
| Broken release | Users install a non-working version | Clean-venv verification before stable announcement |
| Token leak | Malicious release published by an attacker | OIDC trusted publishing; scoped permissions |
| Name conflict | `foundry_cli_tool` already taken on PyPI | Reserve the name early; fall back documented with PO |
| Version drift | PyPI and conda releases diverge | Single source of truth: the git tag (see SA-ANA-005) |

## 7. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-004 (Analysis) |
| Epic | EPIC-010 |
| BA sub-task | BA-ANA-003 |
| SA sub-task | SA-ANA-004 |
| BA deliverable | BA-ANA-003-business-analysis.md |
| Requirement source | PO architecture-change request 2026-08-11 |
