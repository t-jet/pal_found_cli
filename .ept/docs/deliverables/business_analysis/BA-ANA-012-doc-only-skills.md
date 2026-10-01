# Business Analysis — BA-ANA-012

## Skills Use the CLI Interface Only (Doc-Only Skill Model)

| Field | Value |
| --- | --- |
| **Document ID** | BA-ANA-012 |
| **Feature** | FEATURE-011 |
| **Status** | Resolved — pending Project Owner approval (In Progress→Resolved 2026-09-30) |
| **Date** | 2026-09-30 |
| **Author** | Business Analyst |
| **Requirement source** | Project Owner change request 2026-09-30 (FEATURE-011) |

---

## 1. Business Case

Each Foundry skill in the `pal_found_cli_skills` repository currently carries a
separate Python script under a `scripts/` folder. For 16 of the skills that
script is a thin launcher; for datasets and ontologies it is a full copy of the
command implementation. This design conflicts with how skills are meant to be
used. Agents load a skill through its `SKILL.md` file and execute its
instructions, but the current `SKILL.md` files tell the agent to run
`python pal_found_<namespace>_cli.py ...`. That requires a user or agent to
know where Python lives, how to reach the launcher, and how the script finds the
packaged CLI. It also duplicates command logic inside the skills repository for
datasets and ontologies.

The Project Owner requirement is that skills stop containing separate Python
scripts. Any command implementation must live in the tool
(`pal_found_cli_tool`), and skills must only talk to the packaged commands
(`pal-found-*`). A skill therefore becomes documentation only: a `SKILL.md`
that describes what the skill does and how to invoke the matching installed
command, with no executable code in the skill folder.

This is a cross-cutting change to the delivered skill-content model. It follows
the rename decision in BA-ANA-010 (ND-010-03 confirmed the `pal-found-`
command prefix) and extends the documentation-centric direction of FEATURE-008
and FEATURE-009. Because every skill changes in the same way, the change is
decided at analysis stage so the design and implementation build the doc-only
model from the start.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-011-01 | Every namespace skill under `.agents/skills/pal-found-*` MUST contain no separate Python script in the skills repository. |
| BR-011-02 | Each skill MUST consist of a single `SKILL.md` file that documents the skill's purpose and the operations it covers. |
| BR-011-03 | Each `SKILL.md` MUST invoke commands through the installed `pal-found-*` interface, never through a `python ..._cli.py` invocation. |
| BR-011-04 | Any command implementation required by the skills MUST live in the tool (`pal_found_cli_tool`) and be exposed through its console commands. |
| BR-011-05 | Using a skill MUST NOT require Python knowledge; the agent calls the installed command by name only. |
| BR-011-06 | Existing datasets and ontologies command behavior MUST be preserved by the tool's own implementations when the skill copies are removed. |
| BR-011-07 | A new Epic MUST group the implementation of this doc-only skill model under an end-to-end scenario (created at design start per FEATURE-011 decision). |
| BR-011-08 | Every skill's `SKILL.md` MUST state that installing the `pal_found_cli` package is required to make the skill work, and MUST include a one-line install example per package manager: conda (`conda install -c t-jet pal_found_cli`), PyPI/pip (`pip install pal_found_cli`), and uv (`uv pip install pal_found_cli` or `uv tool install pal_found_cli`). |

## 3. Affected Skill Inventory

The skills repository distributes 19 folders under `.agents/skills/`; 18 are
namespace skills with a `scripts/` folder and one (`pal-found`) is already a
documentation-only knowledge skill. The 18 namespace skills are:

| # | Skill folder | Script present | Script kind | Invocation today |
| --- | --- | --- | --- | --- |
| 1 | pal-found-admin | `scripts/pal_found_admin_cli.py` (26 lines) | Thin wrapper | `python pal_found_admin_cli.py ...` |
| 2 | pal-found-aip-agents | script (10 lines) | Thin wrapper | `python pal_found_aip_agents_cli.py ...` |
| 3 | pal-found-audit | script (26 lines) | Thin wrapper | `python pal_found_audit_cli.py log-file ...` |
| 4 | pal-found-checkpoints | script (10 lines) | Thin wrapper | `python pal_found_checkpoints_cli.py ...` |
| 5 | pal-found-connectivity | script (10 lines) | Thin wrapper | `python pal_found_connectivity_cli.py ...` |
| 6 | pal-found-data-health | script (10 lines) | Thin wrapper | `python pal_found_data_health_cli.py ...` |
| 7 | pal-found-datasets | `scripts/pal_found_datasets_cli.py` (467 lines) | Standalone duplicate | `python pal_found_datasets_cli.py ...` |
| 8 | pal-found-filesystem | script (26 lines) | Thin wrapper | `python pal_found_filesystem_cli.py ...` |
| 9 | pal-found-functions | script (26 lines) | Thin wrapper | `python pal_found_functions_cli.py ...` |
| 10 | pal-found-language-models | script (10 lines) | Thin wrapper | `python pal_found_language_models_cli.py ...` |
| 11 | pal-found-media-sets | script (10 lines) | Thin wrapper | `python pal_found_media_sets_cli.py ...` |
| 12 | pal-found-models | script (10 lines) | Thin wrapper | `python pal_found_models_cli.py ...` |
| 13 | pal-found-ontologies | `scripts/pal_found_ontologies_cli.py` (442 lines) | Standalone duplicate | `python pal_found_ontologies_cli.py ...` |
| 14 | pal-found-orchestration | script (10 lines) | Thin wrapper | `python pal_found_orchestration_cli.py ...` |
| 15 | pal-found-sql-queries | script (10 lines) | Thin wrapper | `python pal_found_sql_queries_cli.py ...` |
| 16 | pal-found-streams | script (10 lines) | Thin wrapper | `python pal_found_streams_cli.py ...` |
| 17 | pal-found-third-party-applications | script (10 lines) | Thin wrapper | `python pal_found_third_party_applications_cli.py ...` |
| 18 | pal-found-widgets | script (10 lines) | Thin wrapper | `python pal_found_widgets_cli.py ...` |

## 4. Impact Analysis

### 4.1 Skills become documentation only (16 thin wrappers)

Sixteen skills already delegate to the tool: their launcher scripts import the
packaged module and call its entry point. Removing the scripts means these
skills lose nothing. The `SKILL.md` usage text is the only part that must
change, from `python pal_found_<ns>_cli.py` to `pal-found-<ns>`. The agent
keeps access to every operation because the command is installed with the tool.

### 4.2 Datasets and ontologies standalone implementations migrate to the tool

Datasets and ontologies are the exception. Their skill folders hold full copies
of the command implementation (467 and 442 lines) rather than thin wrappers.
The tool already owns canonical implementations of both: `pal-found-datasets`
(670 lines) and `pal-found-ontologies` (1162 lines) are the installed console
commands, and both are verified supersets of the skill copies
(no identical SHA256; tool implementation is larger and more complete). The
skill copies are therefore stale duplicates. Migrating to the doc-only model
removes the duplicates and leaves the tool copies as the single source of the
command behavior. The tool command surface already covers the same operations
that the skill copies exposed, so no net-new tool command is required.

### 4.3 Users need no Python knowledge

Today a skill user must resolve the launcher script path and run it with Python.
Under the doc-only model the agent runs `pal-found-<ns> <operation> ...` as an
installed command. No Python module path, launcher location, or interpreter
knowledge is needed.

### 4.4 `SKILL.md` invocation text must be updated

Every `SKILL.md` that currently instructs `python pal_found_*_cli.py ...` must
be updated to the `pal-found-*` command. The affected files are the 18
namespace skills under `.agents/skills/pal-found-*` (the `pal-found` knowledge
skill has no command invocations).

### 4.5 Package install is a prerequisite for every skill

A doc-only skill references installed `pal-found-*` commands, so the
`pal_found_cli` package must be installed before any skill can be used.
Install is a one-time, environment-level step performed with a package manager
and applies to every namespace skill equally. Each `SKILL.md` states this
prerequisite and includes a short one-line install example for the three
supported managers:

- conda: `conda install -c t-jet pal_found_cli`
- PyPI/pip: `pip install pal_found_cli`
- uv: `uv pip install pal_found_cli` (or `uv tool install pal_found_cli`)

These commands match the published package (`pal_found_cli` on PyPI, t-jet
conda channel) and propagate unchanged into the design and skill documentation.

## 5. Proposed Doc-Only Skill Model

| Aspect | Current model | Proposed doc-only model |
| --- | --- | --- |
| Skill content | `SKILL.md` + `scripts/*.py` | `SKILL.md` only |
| Command implementation | In skill repo (launcher or duplicate) and in tool | In tool only (`pal_found_cli_tool`) |
| Skill invocation | `python ..._cli.py <op>` | `pal-found-<ns> <op>` |
| Python knowledge | Required (path + interpreter) | Not required |
| Single source of behavior | Split (skill + tool copies) | Tool only |
| Skill distribution copy | Copies scripts + docs | Copies docs only |

## 6. Acceptance Criteria

- AC-011-01: Given any namespace skill under `.agents/skills/pal-found-*`, when the skill is inspected, then the skill contains no Python script and no `scripts/` directory.
- AC-011-02: Given a namespace skill, when its `SKILL.md` is read, then every command example invokes a `pal-found-*` command and no example uses `python ..._cli.py`.
- AC-011-03: Given a user who does not know Python, when they use a namespace skill, then they invoke the documented `pal-found-*` command by name and succeed without any Python setup.
- AC-011-04: Given the datasets skill, when the skill copy of the command is removed, then all datasets operations remain available through `pal-found-datasets` with unchanged behavior.
- AC-011-05: Given the ontologies skill, when the skill copy of the command is removed, then all ontologies operations remain available through `pal-found-ontologies` with unchanged behavior.
- AC-011-06: Given the skills repository, when it is cloned and distributed, then every delivered skill consists solely of documentation that references the installed tool commands.
- AC-011-07: Given an existing customer of the installed tool, when the doc-only model ships, then all 18 `pal-found-*` commands remain installed and callable without change.
- AC-011-08: Given any namespace skill's `SKILL.md`, when it is read, then it states that installing the `pal_found_cli` package is required and includes one-line install examples for conda, PyPI (pip), and uv.

## 7. Impact on End-to-End Business Processes

| Process | Impact |
| --- | --- |
| Skill distribution | Skills distribute as documentation only; copy instructions no longer carry executable scripts. |
| Agent usage | Agents call installed `pal-found-*` commands directly instead of launching Python scripts. |
| Onboarding | Onboarding no longer requires telling users how to reach or run a launcher script; a tool install provides the commands. |
| Datasets and ontologies | Command behavior is sourced solely from the tool; skill copies are removed, removing duplication risk. |
| Tool release | The tool remains the distribution point for all command implementations; skill updates and tool releases decouple (skills reference commands, not code). |
| Documentation | DESIGN/QA/devops deliverables that referenced the launcher pattern must be updated to the doc-only model. |

## 8. Changes in Access Restrictions

- No user authentication, credentials, or permission changes result from FEATURE-011.
- The access-control model (ADR-007) applies unchanged to the installed commands.
- Only the location of executable code changes: from skill folders to the tool package.

## 9. Assumptions and Risks

| Type | Item |
| --- | --- |
| Assumption | Tool install is a prerequisite for doc-only skills to be usable; skills alone no longer contain executable commands. |
| Assumption | Datasets and ontologies tool implementations cover the full operation set the skill copies exposed (verified superset by size; behavior parity confirmed in QA). |
| Assumption | A new Epic is warranted to group the doc-only skill implementation (per FEATURE-011 analysis decision). |
| Risk | A user loads a doc-only skill without the tool installed and finds the commands unavailable. |
| Mitigation | Each `SKILL.md` states the install prerequisite with one-line conda/pip/uv examples (BR-011-08, AC-011-08); onboarding documents repeat it. |
| Risk | A skills-embedded `SKILL.md` retains a `python ..._cli.py` example after the change. |
| Mitigation | Acceptance criteria AC-011-02 sweeps all 18 namespace `SKILL.md` files for stale invocations. |

## 10. Request Rate Changes

No change to Foundry request volumes results from FEATURE-011. Command usage
patterns stay the same; only the invocation path changes. Distribution and
onboarding traffic may change marginally as skills ship smaller (documentation
only) while the tool carries the command implementations.

## 11. Data Size Changes

No change to stored datasets or transfer volumes results from FEATURE-011.
The skills repository shrinks because executable copies of the datasets and
ontologies commands are removed.

## 12. Related Documents

- `.ept/docs/document_index.md` — Project documentation index (updated 2026-09-30).
- SRS-001 — Skill packaging requirements (FR-SKILL-1..5), documented at
  `.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md`.
- BA-ANA-010 — Confirmed `pal-found-` command prefix (ND-010-03).
- SA-ANA-012 — Architecture analysis for removing scripts from skills and
  migrating datasets/ontologies to the tool.
- DEV-027 — Cross-repository reference register for skill distribution paths.
