# Business Design — BA-DES-012

## Skills Use the CLI Interface Only (Doc-Only Skill Model)

| Field | Value |
| --- | --- |
| **Document ID** | BA-DES-012 |
| **Feature** | FEATURE-011 |
| **Status** | Resolved 2026-09-30 — BA design complete; held at Resolved, not yet Closed pending SA-DES-011 terminal status |
| **Date** | 2026-09-30 |
| **Author** | Business Analyst |
| **Based on** | BA-ANA-012 (Resolved), SA-ANA-012 (Resolved), EPIC-011 |
| **Requirement source** | Project Owner change request 2026-09-30 (FEATURE-011) |

---

## 1. Design Overview

The design turns every namespace skill in the `pal_found_cli_skills`
repository into documentation only. Each skill becomes a single `SKILL.md`
file that describes the skill and shows how to call the matching installed
command. No Python script, and no `scripts/` folder, stays inside a skill.
All command behavior already lives in the tool (`pal_found_cli_tool`),
exposed through its `pal-found-*` console commands, so removing the scripts
does not remove any operation.

Two skill families need different treatment. For 16 skills the script is a
thin launcher that only re-exports the tool command; deleting it loses
nothing. For datasets and ontologies the skill folder holds a full copy of
the command implementation, and the tool already carries a verified superset
(`pal-found-datasets`, `pal-found-ontologies`). Migrating to doc-only
removes those stale copies and leaves the tool as the single source of
behavior. Everything else in the design is the same for all 18 skills.

## 2. Confirmed Decisions from Analysis

| ID | Decision |
| --- | --- |
| DA-012-01 | Each skill contains only a `SKILL.md` file; no `scripts/` folder and no executable code. |
| DA-012-02 | Skills invoke the installed `pal-found-<namespace>` command by name; never a `python ..._cli.py` call. |
| DA-012-03 | Any command implementation the skills depend on lives in `pal_found_cli_tool` and is exposed via its console entry points. |
| DA-012-04 | Using a skill requires no Python knowledge: the agent runs the documented command name. |
| DA-012-05 | Datasets and ontologies keep their behavior from the tool's own implementations; the skill copies are removed as stale duplicates. |
| DA-012-06 | EPIC-011 groups the change as an end-to-end scenario. |

Source: BA-ANA-012 sections 2, 4, 5; SA-ANA-012 (migration and packaging
approach, resolves QUESTION-141).

## 3. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-D-012-01 | Each of the 18 namespace skills MUST be documentation only: a single `SKILL.md` and no Python script in the skill folder. |
| BR-D-012-02 | Every `SKILL.md` MUST instruct agents to run the matching `pal-found-*` command; no `python ..._cli.py` example may remain. |
| BR-D-012-03 | All command behavior for the skills MUST come from the installed tool and never from code stored in the skills repository. |
| BR-D-012-04 | A skill user MUST be able to use the skill without knowing Python or knowing where the tool is installed; command name suffices. |
| BR-D-012-05 | Datasets and ontologies MUST retain their current operation set through `pal-found-datasets` and `pal-found-ontologies` after the skill copies are removed. |
| BR-D-012-06 | Distribution and onboarding documentation MUST describe skills as documentation that references installed tool commands, and MUST state the tool install prerequisite. |
| BR-D-012-07 | Every skill's `SKILL.md` MUST state that installing the `pal_found_cli` package is required and MUST include a one-line install example per package manager: conda (`conda install -c t-jet pal_found_cli`), PyPI/pip (`pip install pal_found_cli`), and uv (`uv pip install pal_found_cli` or `uv tool install pal_found_cli`). Mirrors approved BR-011-08. |

## 4. Doc-Only Skill Model

| Aspect | Today | Under BA-DES-012 |
| --- | --- | --- |
| Skill content | `SKILL.md` + `scripts/*.py` | `SKILL.md` only |
| Command implementation | In skill repo (launcher or duplicate) and in tool | Tool only |
| Skill invocation | `python ..._cli.py <op>` | `pal-found-<ns> <op>` |
| Python knowledge | Required (path + interpreter) | Not required |
| Single source of behavior | Split (skill + tool copies) | Tool only |
| Skill distribution | Copies scripts and docs | Copies docs only |
| Tool install prerequisite | Implicit | Stated in every skill and onboarding doc, with one-line conda/pip/uv install examples (BR-D-012-07) |

## 5. Logical Flow (business terms)

1. The agent loads a skill through its `SKILL.md`.
2. The `SKILL.md` lists the operations the skill covers and shows each command
   as `pal-found-<namespace> <operation> ...`.
3. The agent runs the named command; the installed tool resolves it.
4. Output returns to the agent; no Python module path, launcher location, or
   interpreter is involved.
5. A user installing the tool once gets every command the skills reference.
6. A skill whose user has not installed the tool states in `SKILL.md` that
   installing `pal_found_cli` is required and gives a one-line install example
   for conda, pip, and uv (AC-D-012-09).

## 6. UI/UX (abstract)

No graphical interface is built. The user experience is:

- A user who installs the tool can run every documented command by name.
- A user reading a skill never sees Python instructions, only `pal-found-*`
  commands.
- A user browsing the skills repository sees documentation-only folders.
- A user without the tool installed is told in the skill and onboarding
  docs that the tool must be installed first, with a one-line install example
  for conda, pip, and uv.

## 7. API Specification (abstract)

| Command | Purpose | Notes |
| --- | --- | --- |
| `pal-found-<namespace>` | Runs the operations for one skill namespace | All 18 existing commands stay installed and callable |
| `pal-found-datasets` | Datasets operations | Behavior from the tool's implementation; skill copy removed |
| `pal-found-ontologies` | Ontologies operations | Behavior from the tool's implementation; skill copy removed |

No command is added, renamed, or removed. The command surface is unchanged;
only where the agent learns the command name moves (from a Python script in
the skill to the installed command).

## 8. Data and Business Structures

No business data structures change. The relevant structures are artifacts in
the repository:

| Structure | Change |
| --- | --- |
| Skill folder `.agents/skills/pal-found-<ns>/` | Keeps `SKILL.md`; drops `scripts/` |
| `SKILL.md` command examples | Rebased from `python ..._cli.py` to `pal-found-<ns>` |
| Tool package `pal_found_cli_tool` | Unchanged; already carries the command implementations |
| Distribution guide | Updated to describe doc-only skills, the tool install prerequisite, and one-line conda/pip/uv install examples |

## 9. Acceptance Criteria

- AC-D-012-01: Given any namespace skill under `.agents/skills/pal-found-*`, when the skill is inspected, then the skill contains no Python script and no `scripts/` directory.
- AC-D-012-02: Given a namespace skill, when its `SKILL.md` is read, then every command example invokes a `pal-found-*` command and no example uses `python ..._cli.py`.
- AC-D-012-03: Given a user who does not know Python, when they use a namespace skill, then they invoke the documented `pal-found-*` command by name and succeed without any Python setup.
- AC-D-012-04: Given the datasets skill, when the skill copy is removed, then all datasets operations remain available through `pal-found-datasets` with unchanged behavior.
- AC-D-012-05: Given the ontologies skill, when the skill copy is removed, then all ontologies operations remain available through `pal-found-ontologies` with unchanged behavior.
- AC-D-012-06: Given the skills repository, when it is distributed, then every delivered skill consists solely of documentation that references the installed tool commands.
- AC-D-012-07: Given an existing customer of the installed tool, when the doc-only model ships, then all 18 `pal-found-*` commands remain installed and callable without change.
- AC-D-012-08: Given the distribution and onboarding documentation, when it is read, then it states that skills are documentation-only and that the tool must be installed first.
- AC-D-012-09: Given any namespace skill's `SKILL.md`, when it is read, then it states that installing the `pal_found_cli` package is required and includes a one-line install example for conda (`conda install -c t-jet pal_found_cli`), pip (`pip install pal_found_cli`), and uv (`uv pip install pal_found_cli`). Mirrors AC-011-08.

## 10. Migration Procedure

1. Convert the 16 thin-wrapper skills: remove each `scripts/pal_found_<ns>_cli.py`, keep `SKILL.md`, rebase all command examples to `pal-found-<ns>`, and add an Installation statement with one-line conda/pip/uv examples (BR-D-012-07, AC-D-012-09).
2. Migrate datasets and ontologies: remove the stale skill copies, confirm `pal-found-datasets` and `pal-found-ontologies` cover the same operations with unchanged behavior (verified as supersets at analysis).
3. Update every skill distribution guide and onboarding document to describe doc-only skills and state the tool install prerequisite with one-line conda/pip/uv examples (BR-D-012-07).
4. Sweep all 18 `SKILL.md` files for any `python ..._cli.py` example and any script reference (AC-D-012-02).
5. Run the acceptance criteria, including behavior checks for datasets and ontologies.
6. Record evidence tied to the delivered commit and the final skill layout.

## 11. Migration Impact on Delivered Skills and Onboarding

| Area | Impact |
| --- | --- |
| Skills repository | 18 folders become documentation-only; datasets and ontologies duplicates removed; repository shrinks. |
| Agent usage | Agents call installed `pal-found-*` commands directly; no Python resolution. |
| Onboarding | No instruction to reach or run a launcher script; a single tool install supplies the commands; each skill documents the one-line conda/pip/uv install. |
| Tool release | The tool remains the distribution point for command implementations; skill updates and tool releases decouple. |
| Existing users | All 18 commands remain installed and callable after the change (BR-D-012-05, AC-D-012-07). |
| Risk | A user loads a doc-only skill without the tool installed; mitigation is the stated prerequisite and one-line conda/pip/uv examples in skill and onboarding docs (AC-D-012-08, AC-D-012-09). |

## 12. Developer Story Breakdown

The implementation splits into three stories so each can fit one sprint and
each has a clear owner:

| DEV-STORY | Scope | Assignee |
| --- | --- | --- |
| DEV-STORY-038 | Convert the 16 thin-wrapper skills to doc-only: remove `scripts/*.py`, rebase `SKILL.md` examples to `pal-found-*`, and add the `pal_found_cli` install-requirement statement with one-line conda/pip/uv examples. | python-developer |
| DEV-STORY-039 | Migrate datasets and ontologies to the tool: remove stale skill copies, verify `pal-found-datasets` and `pal-found-ontologies` behavior, add any missing coverage. | tech-lead |
| DEV-STORY-040 | Update distribution, onboarding, and evidence: doc-only skill description, tool install prerequisite with one-line conda/pip/uv examples, sweep for stale `python ..._cli.py` references, run acceptance criteria. | qa-engineer |

All three are children of FEATURE-011 and linked to EPIC-011 via EpicLink.

## 13. Requirements Traceability

| Business requirement | Dev story | Acceptance criteria |
| --- | --- | --- |
| BR-011-01 / BR-D-012-01 | DEV-STORY-038 | AC-011-01 / AC-D-012-01 |
| BR-011-03 / BR-D-012-02 | DEV-STORY-038 | AC-011-02 / AC-D-012-02 |
| BR-011-05 / BR-D-012-04 | DEV-STORY-038 | AC-011-03 / AC-D-012-03 |
| BR-011-06 / BR-D-012-05 | DEV-STORY-039 | AC-011-04 / AC-011-05 / AC-D-012-04 / AC-D-012-05 |
| BR-011-04 / BR-D-012-03 | DEV-STORY-039 | AC-D-012-07 |
| BR-011-02 / BR-D-012-06 | DEV-STORY-040 | AC-011-06 / AC-011-07 / AC-D-012-06 / AC-D-012-08 |
| BR-011-08 / BR-D-012-07 | DEV-STORY-038, DEV-STORY-040 | AC-011-08 / AC-D-012-09 |

## 14. Related Documents

- `.ept/docs/document_index.md` — Project documentation index (updated 2026-09-30).
- `BA-ANA-012-doc-only-skills.md` — Business analysis for the doc-only model.
- `SA-ANA-012` — Architecture analysis for removing scripts and migrating
  datasets/ontologies to the tool (resolves QUESTION-141).
- `EPIC-011` — End-to-end scenario for documentation-only skills.
