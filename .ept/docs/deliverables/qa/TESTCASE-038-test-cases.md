# TESTCASE-038 — QA Test Cases: Doc-Only Skill Conversion

| Field | Value |
| --- | --- |
| **Test Case ID** | TESTCASE-038 |
| **Parent Story** | DEV-STORY-038 (FEATURE-011) |
| **Scope** | Convert the 16 thin-wrapper namespace skills to documentation-only |
| **Author** | QA Engineer |
| **Date** | 2026-10-01 |
| **Based on** | BA-DES-012, SA-DES-011, BA-ANA-012, SA-ANA-012, AC-D-012-01/02/03, BR-D-012-07 / AC-D-012-09 |
| **Target** | `pal_found_cli_skills` submodule at HEAD `7b1b99f` |

## 1. Scope

Verifies that the 16 thin-wrapper skills under `.agents/skills/pal-found-*`
(admin, aip-agents, audit, checkpoints, connectivity, data-health,
filesystem, functions, language-models, media-sets, models, orchestration,
sql-queries, streams, third-party-applications, widgets) are converted to
documentation-only: no `scripts/` directory, no Python code, every command
example invokes an installed `pal-found-*` command, and each `SKILL.md`
states the `pal_found_cli` install prerequisite with conda/pip/uv examples.

## 2. Preconditions

- `pal_found_cli_skills` submodule checked out at HEAD `7b1b99f`.
- Git working tree clean (`git status --porcelain` empty).
- Tool package `pal_found_cli` installed in the active venv with all 18
  `pal-found-*` console commands.

## 3. Test Scenarios

### DCS-TC-001 (AC-D-012-01): No Python script remains in any of the 16 skills

- **Given** the 16 namespace skills in `.agents/skills/pal-found-*`,
- **When** I inspect the git tree and the on-disk folders,
- **Then** no `.py` file and no `scripts/` directory exists in any of the 16
  skill folders, and `git status` is clean.

### DCS-TC-002 (AC-D-012-02): Every command example invokes `pal-found-*`

- **Given** each of the 16 converted skills,
- **When** I read its `SKILL.md`,
- **Then** every command example invokes a `pal-found-*` command by name and
  no example uses `python ..._cli.py`.

### DCS-TC-003 (AC-D-012-03 / BR-D-012-04): Skill is usable without Python knowledge

- **Given** a user who does not know Python,
- **When** they follow the skill,
- **Then** they invoke the documented `pal-found-<ns>` command by name and
  succeed without any Python setup, launcher path, or interpreter step.

### DCS-TC-004 (BR-D-012-07 / AC-D-012-09): Install-requirement block present in all 16 skills

- **Given** each of the 16 skills' `SKILL.md`,
- **When** I read it,
- **Then** it states that installing the `pal_found_cli` package is required
  and includes one-line install examples for conda (`conda install -c t-jet
  pal_found_cli`), pip (`pip install pal_found_cli`), and uv (`uv tool
  install pal_found_cli`).

## 4. Edge Cases

- **Edge-1:** Skill folder that still contains a `scripts/` directory or any
  `.py` launcher → must be flagged as FAIL (negative case DCS-TC-NEG-001).
- **Edge-2:** A `SKILL.md` with even one stale `python ..._cli.py` example
  among otherwise-correct `pal-found-*` examples → must be flagged as FAIL
  (negative case DCS-TC-NEG-002).
- **Edge-3:** A skill missing any one of the three install lines can cause the
  container to FAIL AC-D-012-09 scanning (negative case DCS-TC-NEG-003).

## 5. Negative Cases

### DCS-TC-NEG-001

- **Given** a skill that still ships a `scripts/` directory or Python launcher,
- **When** [probe inserts a fake `scripts/x.py`],
- **Then** the case reports FAIL (simulated; covered by the positive
  no-scripts scan which found zero).

### DCS-TC-NEG-002

- **Given** a `SKILL.md` containing a `python ..._cli.py` reference,
- **When** the stale-reference regex is applied,
- **Then** the case reports FAIL.

### DCS-TC-NEG-003

- **Given** a `SKILL.md` missing an install example for conda, pip, or uv,
- **When** the install-requirement scan is applied,
- **Then** the case reports FAIL.

## 6. Expected Outputs

- Positive scans produce counts only: 0 `.py`, 0 `scripts/` under the 16 skill
  folders; every `SKILL.md` has `pal-found-*` present and no stale `python
  ..._cli.py`.
- Install-requirement scan: `conda/pip/uv = true` for all 16 skills.
- Unit-test suite (skills repo): 16 passed at HEAD `7b1b99f`.

## 7. Test Data

- Skills path: `.agents/skills/pal-found-*` (16 namespace folders).
- Stale-ref pattern: `python\s+[\w/._\-]*_cli\.py`.
- Install regexes: `conda install -c t-jet pal_found_cli`,
  `pip install pal_found_cli`, `uv tool install pal_found_cli` / `uv pip
  install pal_found_cli`.
