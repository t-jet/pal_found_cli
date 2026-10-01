# TESTCASE-039 — QA Test Cases: Datasets/Ontologies Migration to Tool

| Field | Value |
| --- | --- |
| **Test Case ID** | TESTCASE-039 |
| **Parent Story** | DEV-STORY-039 (FEATURE-011) |
| **Scope** | Migrate datasets and ontologies command implementations to the tool; remove stale skill copies |
| **Author** | QA Engineer |
| **Date** | 2026-10-01 |
| **Based on** | BA-DES-012, SA-DES-011, AC-D-012-04/05/07, BR-D-012-05/03 |
| **Target** | `pal_found_cli_skills` submodule at HEAD `7b1b99f`; `pal_found_cli_tool` |

## 1. Scope

Verifies that the standalone datasets and ontologies command copies
(`scripts/pal_found_datasets_cli.py`, `scripts/pal_found_ontologies_cli.py`)
are removed from the skills repository, that the tool's `pal-found-datasets`
(33 ops) and `pal-found-ontologies` (67 ops) remain callable with unchanged
behavior, that both SKILL.md files are doc-only, and that all 18
`pal-found-*` commands remain installed.

## 2. Preconditions

- `pal_found_cli_skills` submodule at HEAD `7b1b99f`; `pal_found_cli_tool` at
  HEAD `ba2f011`.
- Tool package installed in the active venv.
- 18 console entry points present (`pal-found-datasets`, `pal-found-ontologies`
  among them).

## 3. Test Scenarios

### DMO-TC-001 (AC-D-012-04): Datasets skill copy removed, operations via tool

- **Given** the datasets skill,
- **When** I inspect the skills repo and the git history,
- **Then** the standalone `pal_found_datasets_cli.py` copy is removed, the
  `pal-found-datasets` command is callable, and all datasets operations remain
  available with unchanged behavior.

### DMO-TC-002 (AC-D-012-05): Ontologies skill copy removed, operations via tool

- **Given** the ontologies skill,
- **When** I inspect the skills repo and the git history,
- **Then** the standalone `pal_found_ontologies_cli.py` copy is removed, the
  `pal-found-ontologies` command is callable, and all ontologies operations
  remain available with unchanged behavior.

### DMO-TC-003 (SA-DES-011 4.1 / BR-D-012-05): Operation parity 33/67

- **Given** the tool's installed `pal-found-datasets` and `pal-found-ontologies`
  commands,
- **When** I enumerate their operation catalogs,
- **Then** datasets exposes 33 operations across 5 resource clients and
  ontologies exposes 67 operations, matching the design and the documented
  operation sets.

### DMO-TC-004 (AC-D-012-07): All 18 `pal-found-*` commands remain installed

- **Given** an existing customer of the installed tool,
- **When** the doc-only migration ships,
- **Then** all 18 `pal-found-*` commands remain installed and callable without
  change (no command added, renamed, or removed).

### DMO-TC-005 (AC-D-012-02): Datasets/ontologies SKILL.md are doc-only

- **Given** the `pal-found-datasets` and `pal-found-ontologies` SKILL.md files,
- **When** each is read,
- **Then** both are documentation-only: every command example invokes the tool
  command by name, no `python ..._cli.py` remains, and the install-requirement
  block (conda/pip/uv) is present.

## 4. Edge Cases

- **Edge-1:** A stale `pal_found_datasets_cli.py` or `pal_found_ontologies_cli.py`
  still present in the skills tree → FAIL (DMO-TC-NEG-001).
- **Edge-2:** A missing operation in the tool catalog relative to the
  documented skill set → FAIL (DMO-TC-NEG-002).
- **Edge-3:** Fewer than 18 entry points installed → FAIL (DMO-TC-NEG-003).

## 5. Negative Cases

### DMO-TC-NEG-001

- **Given** the git tree still contains a datasets or ontologies `_cli.py` copy,
- **When** `git ls-tree` is run,
- **Then** the case reports FAIL (positive scan found zero).

### DMO-TC-NEG-002

- **Given** the tool catalog drops an operation the skills document,
- **When** operation counts are compared,
- **Then** the case reports FAIL.

### DMO-TC-NEG-003

- **Given** fewer than 18 `pal-found-*` entry points,
- **When** `pyproject.toml` scripts are enumerated,
- **Then** the case reports FAIL.

## 6. Expected Outputs

- `git log --diff-filter=D -- *_datasets_cli.py *_ontologies_cli.py` shows both
  files deleted (commit `7e75991`).
- `pal-found-datasets --help`: "Foundry Datasets CLI - 33 operations across 5
  resource clients".
- `pal-found-ontologies --help`: "Foundry Ontologies CLI - 67 operations".
- `pyproject.toml` scripts: 18 entry points.

## 7. Test Data

- Skills path: `.agents/skills/pal-found-datasets/SKILL.md`,
  `.agents/skills/pal-found-ontologies/SKILL.md`.
- Tool path: `pal_found_cli_tool` (HEAD `ba2f011`).
- Reference operation sets: datasets 33 (dataset 11, branch 5, file 5,
  transaction 6, view 6); ontologies 67 (per SA-DES-011 catalogue).
