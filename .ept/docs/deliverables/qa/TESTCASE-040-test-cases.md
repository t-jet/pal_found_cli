# TESTCASE-040 — QA Test Cases: Distribution, Onboarding, Evidence Update

| Field | Value |
| --- | --- |
| **Test Case ID** | TESTCASE-040 |
| **Parent Story** | DEV-STORY-040 (FEATURE-011) |
| **Scope** | Update distribution and onboarding docs for doc-only skills; state tool install prerequisite; sweep all 18 SKILL.md for stale refs; run doc-only acceptance criteria |
| **Author** | QA Engineer |
| **Date** | 2026-10-01 |
| **Based on** | BA-DES-012, SA-DES-011, AC-D-012-06/08/02/04/05, BR-D-012-06/07 |
| **Target** | `pal_found_cli_skills` submodule at HEAD `7b1b99f` |

## 1. Scope

Verifies that the distribution and onboarding documentation describes skills
as documentation-only and states the tool install prerequisite with one-line
conda/pip/uv examples, and that a sweep of all 18 namespace `SKILL.md` files
finds no stale `python ..._cli.py` reference. The behavior checks for
datasets (33) and ontologies (67) remain unchanged via the tool commands.

## 2. Preconditions

- `pal_found_cli_skills` submodule at HEAD `7b1b99f`.
- Distribution/onboarding docs (README.md) and all 18 namespace SKILL.md
  present.
- Tool commands `pal-found-datasets` / `pal-found-ontologies` callable.

## 3. Test Scenarios

### DBO-TC-001 (AC-D-012-06): Documentation-only distribution

- **Given** the skills repository,
- **When** it is distributed,
- **Then** every delivered skill folder consists solely of documentation that
  references installed tool commands (single SKILL.md; no executable code).

### DBO-TC-002 (AC-D-012-08 / BR-D-012-06): Onboarding states doc-only + tool install prerequisite

- **Given** the distribution and onboarding documentation (README.md),
- **When** it is read,
- **Then** it states that skills are documentation-only and that the tool must
  be installed first, and includes one-line conda/pip/uv install examples.

### DBO-TC-003 (BR-D-012-07 / AC-D-012-09): Tool install prerequisite in every SKILL.md

- **Given** all 18 namespace `SKILL.md` files,
- **When** each is read,
- **Then** each states that installing the `pal_found_cli` package is required
  with conda/pip/uv install examples.

### DBO-TC-004 (AC-D-012-02): No stale `python ..._cli.py` in all 18 SKILL.md

- **Given** a sweep of all 18 namespace `SKILL.md` files,
- **When** each is read,
- **Then** no `python ..._cli.py` example or script reference remains.

### DBO-TC-005 (AC-D-012-04/05): Datasets/ontologies behavior unchanged via tool

- **Given** the behavior checks,
- **When** datasets and ontologies are exercised,
- **Then** behavior is unchanged via `pal-found-datasets` (33 ops) and
  `pal-found-ontologies` (67 ops).

## 4. Edge Cases

- **Edge-1:** README or a SKILL.md missing any install example → FAIL
  (DBO-TC-NEG-001).
- **Edge-2:** A single stale `python ..._cli.py` anywhere in the 18-skill sweep
  → FAIL (DBO-TC-NEG-002).
- **Edge-3:** A skill folder that still carries executable content → FAIL
  (DBO-TC-NEG-003).

## 5. Negative Cases

### DBO-TC-NEG-001

- **Given** onboarding or a SKILL.md missing conda, pip, or uv install example,
- **When** the install-requirement scan is applied,
- **Then** the case reports FAIL.

### DBO-TC-NEG-002

- **Given** a `SKILL.md` with a `python ..._cli.py` reference,
- **When** the stale-ref sweep is applied to all 18 files,
- **Then** the case reports FAIL.

### DBO-TC-NEG-003

- **Given** a skill folder that ships executable code (`.py` or `scripts/`),
- **When** the doc-only distribution check is applied,
- **Then** the case reports FAIL.

## 6. Expected Outputs

- README.md "Install prerequisite" block states doc-only + `pal_found_cli`
  install with `conda install -c t-jet pal_found_cli`, `pip install
  pal_found_cli`, `uv tool install pal_found_cli`.
- 18 namespace SKILL.md: `install_req_full_met = true`, `stale_py_any = false`.
- Datasets/ontologies help: 33 / 67 operations.

## 7. Test Data

- Distribution/onboarding doc: `README.md`.
- Skills: all 18 `.agents/skills/pal-found-*/SKILL.md`.
- Tool behavior: `pal-found-datasets --help`, `pal-found-ontologies --help`.
