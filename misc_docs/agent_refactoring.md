# Agent refactoring task

## Objective

The objective of this task is to make agent composition cache-friendly and centrally managed: every generated agent receives all available skills before work starts, and shared skill, model, or prompt-introduction updates can be applied without repetitive edits to individual definitions.

Use central skill and model configuration with a composition tool that renders complete agent contexts from agent-specific instructions and harness parameters.

## Current behavior

Currently, agents rely on instructions that reference skills such as `workflow` or `self-improvement`; the agent must discover and load the required secondary instructions during execution. Harness definitions are maintained separately, which makes shared updates repetitive.

Some agents are created by the HR agent. This workflow remains supported, but HR creates an agent source and invokes the composer instead of manually modifying generated definitions.

## Target behavior

Each generated agent must contain a complete context assembled from central skills, the agent's instructions, and harness-specific header parameters. Central skill changes are reflected in every agent after regeneration without per-agent skill-body edits.

The HR agent creates `.ept/resources/agent_sources/<agent-name>/parameters.yaml` with the agent name, shared metadata, supported harness parameters, and agent-specific instructions. It does not select skills, models, or output harnesses, and it does not edit generated files. The same name is rendered for every harness.

The composer always generates Copilot, Claude, and Codex definitions. Every `SKILL.md` in `.ept/resources/skills` is rendered inline, while every `SKILL.md` in `.ept/skills` is rendered as a repository-relative file reference. No agent source may opt out of a discovered skill.

Skills should be included into agent's context using the following structure:

```xml
<skills>
Skills provide specialized capabilities, domain knowledge, and refined workflows for producing high-quality outputs.
Each skill can be provided as an inline instructions in the `<skill>` sections below or as a reference to the file. Skills provided inline have a `<instructions>` section with the skill's instructions. Skills provided as a reference have a `<file>` section with the path to the skill's instructions file relative to the root of the project repository.
Multiple skills can be combined when a task requires different capabilities.
BLOCKING REQUIREMENT: When one or more skills provided as a reference to the file applies to the user's request, you MUST load and read the SKILL.md file IMMEDIATELY as your first action for all applied skills, BEFORE generating any other response or taking any other action on the task. Use appropriate file reading tool to load the relevant skill(s).
NEVER just mention or reference a skill in your response without actually reading its content first. If a skill is relevant, load it before proceeding.
How to determine if a skill applies:
1. Review the available skills and match their descriptions against current task requirements.
2. If a skill's description indicates that it is relevant to the task, load that skill immediately.
3. When multiple skills apply (e.g., following project workflow to design architecture documentation with flowcharts), load all relevant skills.
Examples:
- "Proceed with ticket execution according to instructions for the ticket type" -> Read the workflow skill by reading the workflow skill FIRST, then proceed
- "author the SAD using C4 views" -> Read the workflow, architecture, documentation and diagramming skills FIRST, then proceed
- "Implement end-to-end tests using Playwright" -> Load and read the playwright skill FIRST, then proceed

Available skills:
<skill>
<name>playwright</name>
<description>Battle-tested Playwright patterns for E2E, API, component, visual, accessibility, and security testing. Covers locators, fixtures, POM, network mocking, auth flows, debugging, CI/CD (GitHub Actions, GitLab, CircleCI, Azure, Jenkins), framework recipes (React, Next.js, Vue, Angular), and migration guides from Cypress/Selenium. TypeScript and JavaScript.
</description>
<file>.ept/skills/playwright/SKILL.md</file>
</skill>
<skill>
<name>workflow</name>
<description>Provides instructions to AI agents on organizing development work, moving features through project stages, selecting and linking the correct ticket types, and respecting role responsibilities at each stage.
</description>
<instructions>

# Workflow Skill — Project Development Process

## Purpose

This skill guides AI agents on how to organize development work, move features through project stages, select and link the correct ticket types, and respect role responsibilities at each stage.

---

## Mandatory ticket handling instructions

- Tickets should not be transitioned from one status to another if the transition has a Definition of Done (DoD) and that DoD is not met.
...
</instructions>
</skill>
</skills>
```

The introduction part of the skills section should be provided exactly as in the example above.
Skills that contain a file reference should be placed first and then followed by skills that contain inline content.
Inside each category skills should be sorted alphabetically by skill name.

To produce a part of the prompt that contains the skills section, each skill should be converted from the SKILL.md file into the `<skill>` structure as shown above. The name should be taken from the `name` field in the SKILL.md file, the description should be taken from the `description` field in the SKILL.md file, and the content should be taken from the body of the SKILL.md file.

Each generated agent prompt must be composed of the following sections:

1. harness-specific header cotaining the agent's name, model, tools and other harness-specific configurations
2. skills section containing all required skills for the agent
3. agent-specific instructions section containing the agent's prompt

Model selection is centralized in `.ept/resources/agent_sources/agent-models.yaml`. The required `copilot`, `claude`, and `codex` entries apply to every generated agent; models are not per-agent source parameters.

## Design

### Scope and ownership

Introduce one repository-owned agent composer that reads declarative source files and writes complete harness definitions. The composer is the only component allowed to render skills into generated agent definitions. Authors maintain shared skills and concise, agent-specific source files; generated definitions are build outputs and must not be manually edited.

The role-based creation templates guide authors to place the complete role content in `parameters.yaml` under `agent_instructions`, while the composer renders the complete context into each harness definition. Templates must not direct authors to create legacy `.ept/agents` files or harness-specific loaders.

### Source layout

Use the following layout, where `<agent-name>` is lowercase kebab-case:

```text
.ept/resources/
  skills/<skill-name>/SKILL.md             # inline skill source
  agent_sources/agent-models.yaml          # model for each output harness
  agent_sources/<agent-name>/
    parameters.yaml                        # identity, headers, and agent-specific prompt
.ept/skills/<skill-name>/SKILL.md          # referenced skill source
.ept/tools/compose_agents.py               # composer CLI
.ept/tools/skills_introduction.txt         # shared skills-block introduction
```

`parameters.yaml` is the canonical per-agent contract. It contains the agent identity, shared header fields, each harness's supported header fields, and agent-specific instructions. `agent-models.yaml` is the canonical harness-model contract and must contain exactly the non-empty string entries `copilot`, `claude`, and `codex`. Skill selection, model selection, and output selection are repository policy, not agent configuration. The composer constructs every harness header from these central inputs and rejects unsupported, missing, or inconsistent values.

The HR agent creates or updates this source directory and invokes the composer. It does not edit generated files directly.

### Input schema

Use a small, explicit YAML schema:

```yaml
name: architect
description: Solution Architect & Business Analyst for enterprise-grade development.
copilot:
  tools:
    - read
    - search
    - edit
    - execute
    - agent
  user_invocable: true
claude:
  tools:
    - Read
    - Glob
    - Grep
    - Edit
    - Bash
    - Agent
  permission_mode: bypassPermissions
codex: {}
agent_instructions: |
  Agent-specific instructions go here.
```

The required common fields are `name`, `description`, and `agent_instructions`. `name` and `description` are written once and reused in every harness header. The required `copilot` mapping contains `tools` and `user_invocable`; the required `claude` mapping contains `tools` and `permission_mode`; and the required `codex` mapping is empty because the Codex adapter supports no per-agent header parameters. The composer rejects unknown fields in all mappings and rejects an omitted required harness mapping, even when it is empty.

Models are deliberately absent from `parameters.yaml`. The composer reads each harness model from `.ept/resources/agent_sources/agent-models.yaml` and writes it to every definition for that harness. Missing, duplicate, unknown, or non-string model entries are generation errors.

The composer discovers every `SKILL.md` under `.ept/skills` as a referenced skill and every `SKILL.md` under `.ept/resources/skills` as an inline skill. It rejects missing skill roots, invalid YAML front matter, a missing `name` or `description`, duplicate parsed skill names within or across the roots, and any discovered path that escapes its approved root. Individual agents cannot opt out of a centrally available skill.

The `agent_instructions` field is appended verbatim after the skills block. This keeps the shared skills cacheable and prevents agent-specific content from leaking into shared skill definitions.

### Rendering algorithm

For every agent and each mandatory harness, the composer:

1. Reads and validates `parameters.yaml`, including the shared and harness-specific header schema.
2. Reads and validates `agent-models.yaml`.
3. Discovers referenced and inline skills from their separate roots.
4. Parses each `SKILL.md` YAML front matter and separates the Markdown body from metadata.
5. Builds exactly one `<skills>` block using `skills_introduction.txt` without modifications.
6. Emits referenced skills first, alphabetically by parsed skill `name`, with `<file>` paths relative to the repository root.
7. Emits inline skills next, alphabetically by parsed skill `name`, with the full Markdown body inside `<instructions>`.
8. Constructs each harness header from the shared and harness-specific YAML fields plus its configured model, then concatenates it with the rendered skills block and `agent_instructions`.

The renderer must preserve skill bodies byte-for-byte apart from normalizing line endings to the repository convention. It must not recursively expand referenced skills. This gives agents immediate visibility of the skills intended for the initial context while retaining file-backed skills that must be read at task start.

Model selection is resolved independently of agent source files. The composer reads `.ept/resources/agent_sources/agent-models.yaml` and uses its `copilot`, `claude`, and `codex` values for the corresponding harness definitions. It rejects missing, duplicate, unknown, or non-string model configuration rather than generating incomplete or inconsistent definitions.

### Outputs and generated-file policy

Render complete definitions to the repository's existing harness locations:

| Harness | Generated definition |
| --- | --- |
| Copilot | `.github/agents/<agent-name>.agent.md` |
| Claude | `.claude/agents/<agent-name>.md` |
| Codex | `.codex/agents/<agent-name>.toml` |

Each output contains its harness-specific metadata followed by the same rendered skills and agent-specific instructions. The shared context must therefore be identical across outputs after removing the header section. Add a generated-file marker that identifies the source directory and composer command; this supports repository hygiene checks without placing a second source of truth in the output.

Copilot, Claude, and Codex are mandatory outputs for every discovered agent source. The composer always constructs all three and fails the entire invocation if any required YAML header field, model configuration value, or destination cannot be resolved. There is no per-agent output list, filtering option, separate header file, or partial-generation mode.

### Composer interface

Provide a Python CLI because the repository already uses Python tooling:

```text
python .ept/tools/compose_agents.py --agent architect
python .ept/tools/compose_agents.py --all
python .ept/tools/compose_agents.py --all --check
```

`--agent` renders one source directory to all three mandatory harness outputs. `--all` discovers every directory below `.ept/resources/agent_sources` and renders each to all three outputs. `--check` performs the same render in memory and fails when a generated file is missing or differs, without writing any file. Normal execution writes only changed output files and reports the affected paths. Exit code `0` means all requested definitions are valid and current; any schema, discovery, parse, or drift failure is non-zero.

### Validation strategy

Unit tests cover exhaustive skill discovery, metadata parsing, source-root restrictions, ordering, rendering of both skill kinds, duplicate detection, YAML header-schema validation, mandatory three-output generation, exact shared-context equality across harnesses, and centralized model configuration validation and rendering. Fixture tests use multiple skills from both roots so the exact discovery and ordering behavior is reviewable.

Repository-hygiene tests run `compose_agents.py --all --check`. This is the cheapest discriminating check: it proves the committed generated definitions still match their central skill and source inputs. CI must run the unit tests and this check, so a skill update that changes generated context cannot merge without regenerated outputs.

### Migration and compatibility

Migrate `architect` as a vertical slice. Move its shared and harness-specific header values into `parameters.yaml`; copy the complete existing `.ept/agents/architect.md` content verbatim into `agent_instructions`; render all three harness definitions; and validate the result. Once this succeeds, migrate `ba`, `tech-lead`, `python-developer`, `qa-engineer`, and `devops-engineer` as the first role-based batch using the same procedure. The current content of each `.ept/agents/<agent-name>.md` file is the authoritative agent-specific instruction source during migration. Service and tool-wrapper agents remain outside the role-agent templates unless a separate source schema is introduced for their contracts.

During migration, do not attempt to reconcile manual edits in generated definitions. Move intentional edits into `parameters.yaml` or the relevant skill, then regenerate. Remove obsolete loader-only templates, header files, and guidance only after no generated agent relies on them.

## Implementation plan

1. Define the YAML schema and generated-file marker in `.ept/resources/agent_sources`, documenting common header fields, required harness mappings, and repository-controlled skill discovery.
2. Implement `.ept/tools/compose_agents.py` with schema validation, exhaustive skill discovery, front-matter parsing, deterministic rendering, mandatory three-output atomic writes, and `--check` support.
3. Add focused unit and fixture tests for validation errors, common-field reuse, harness-specific header rendering, exhaustive skill discovery and ordering, mandatory output generation, per-harness model selection, and cross-harness context equality.
4. Convert the `architect` agent into the new source format by copying its current `.ept/agents/architect.md` content verbatim into `agent_instructions`, then render its Copilot, Claude, and Codex definitions as the migration slice.
5. Add the repository-hygiene test and CI command that runs `python .ept/tools/compose_agents.py --all --check`.
6. Update the HR agent instructions so agent creation requires source files plus the composer command, then migrate `ba`, `tech-lead`, `python-developer`, `qa-engineer`, and `devops-engineer` after the `architect` slice passes, copying each current `.ept/agents/<agent-name>.md` body into `agent_instructions`.
7. Remove loader-only templates and obsolete agent-creation instructions after the check passes for every generated agent.

## Acceptance criteria

- A single command produces complete Copilot, Claude, and Codex definitions for every requested agent source.
- Each agent source declares `name`, `description`, and all required harness mappings in one `parameters.yaml`; no separate harness-header source files exist.
- Shared metadata is declared once and reused in every supported harness header, while each harness mapping permits only its defined fields.
- Every generated definition contains the mandated skills introduction exactly, referenced skills before inline skills, and alphabetical ordering within each group.
- Inline skills include parsed metadata and the complete `SKILL.md` body; referenced skills use repository-relative paths only.
- Every `SKILL.md` under `.ept/skills` and `.ept/resources/skills` is included in every generated agent context using its required representation, with no per-agent skill list.
- Each migrated agent's `agent_instructions` preserves the complete pre-migration content of its `.ept/agents/<agent-name>.md` file.
- A skill change is reflected in every affected generated definition after regeneration, with no per-agent skill-body edits.
- All harness definitions for an agent have identical rendered skills and agent instructions, differing only in their allowed harness header.
- Each generated harness definition uses its model from `.ept/resources/agent_sources/agent-models.yaml`; the configuration contains exactly the non-empty string keys `copilot`, `claude`, and `codex`.
- Generation fails rather than producing a partial result when any of the three mandatory harness headers or output paths is unavailable, or when the centralized model configuration cannot be resolved.
- `--all --check` detects stale, missing, or manually changed generated output and is enforced in automated tests.
- The HR agent can create a new role-based agent by adding source files and invoking the composer, without selecting skills or harness outputs or manually composing harness definitions.

## Implementation evidence

### Delivered components

The composer is implemented at `.ept/tools/compose_agents.py`. It validates the agent-source schema, discovers all referenced skills below `.ept/skills` and inline skills below `.ept/resources/skills`, parses skill metadata, and renders one deterministic skills block per agent. It writes all three required outputs: `.github/agents/<agent-name>.agent.md`, `.claude/agents/<agent-name>.md`, and `.codex/agents/<agent-name>.toml`.

The rendered models follow the required policy: Copilot reads the model from `.github/agents/hr.agent.md`, Claude writes `model: inherit`, and Codex writes `model = "gpt-5.6"`. The command supports `--agent`, `--all`, `--check`, `--migrate-existing`, and `--format-sources`. The formatting option writes `agent_instructions` as a YAML literal block so the embedded prompt remains human-readable and directly editable.

### Migrated agents

Centralized source files exist for `architect`, `ba`, `tech-lead`, `python-developer`, `qa-engineer`, and `devops-engineer` under `.ept/resources/agent_sources`. Each source preserves the prior `.ept/agents/<agent-name>.md` body in `agent_instructions` and supplies the shared description plus Copilot and Claude header parameters. Copilot, Claude, and Codex definitions for these agents have been generated from those sources.

The HR agent instructions in `.ept/agents/hr.md` now direct agent creation through `parameters.yaml` and the composer, including the per-agent and all-agent drift checks. The repository hygiene suite invokes `compose_agents.py --all --check` so stale generated files fail validation.

### Verification record

The following commands completed successfully after implementation:

```text
.venv\Scripts\python.exe .ept\tools\compose_agents.py --all --check
.venv\Scripts\python.exe -m pytest tests\test_compose_agents.py tests\test_repository_hygiene.py -q
```

The focused test run completed with `14 passed`. The tests cover exhaustive skill discovery and ordering, both skill representations, source-schema failures, all required harness outputs, fixed model selection, literal-block source formatting, preservation of each migrated legacy instruction body, and repository drift detection.

## Review-01

### Findings

1. **Critical: generated Codex definitions are invalid TOML.** `render_codex` places the complete prompt in a basic multiline TOML string without escaping backslashes or embedded `"""` sequences. The six migrated role-agent definitions include the Windows instruction `` `\` separator `` and fail `tomllib` parsing. `--all --check` therefore reports these files as current even though Codex cannot load them.

2. **High: normal generation is not atomic.** The composer writes each generated output as it is processed. A failure while writing a later harness output, or while validating a later agent during `--all`, leaves earlier generated files updated. This conflicts with the requirement to generate the three mandatory outputs atomically.

3. **High: generated-file markers are missing.** None of the Copilot, Claude, or Codex renderers emits the required marker naming the source directory and composer command. This removes the requested traceability for generated outputs.

4. **Medium: skill-root containment is not enforced after resolving paths.** Skill discovery accepts matching `SKILL.md` files without resolving and verifying that they remain under their approved skill root. A symlink inside either skill tree can point outside the approved root and still be rendered as trusted content.

5. **Medium: agent source identity is not validated or bound to its directory.** The source schema only requires a non-empty `name`; it does not enforce lowercase kebab-case or require the source directory to use the same name. The renderer interpolates this value into output paths, so a path-like name can escape the intended harness directory.

6. **Medium: prompt bodies are not preserved verbatim.** The parser strips trailing newlines from skill bodies, and source loading strips trailing newlines from `agent_instructions`. The design requires skill bodies to be preserved byte-for-byte except for line-ending normalization, and requires instructions to be appended verbatim.

7. **Low: ambiguous HR Copilot model metadata is silently accepted.** YAML parsing collapses duplicate `model` keys, and malformed YAML falls back to regex extraction. The design requires generation to fail when the HR Copilot model is missing or ambiguous.

### Test gaps

The tests do not parse rendered Codex TOML, test atomic failure behavior, verify symlink/root containment, reject invalid source names, reject duplicate HR model keys, require generated-file markers, or verify exact trailing-newline preservation. A TOML parse test for every generated Codex definition would have exposed the critical defect.

## Fix-01

### Corrections

1. **Codex TOML is now valid for arbitrary prompt content.** `render_codex` serializes `developer_instructions` with `json.dumps`, which produces a valid TOML basic string and escapes Windows backslashes, double quotes, and newlines. The generated `.codex/agents/*.toml` definitions were regenerated, and `test_generated_codex_definitions_are_valid_toml` parses every one with `tomllib`.

2. **Generation now stages and restores output files.** `main` first composes and validates every requested agent in memory. `write_outputs` writes changed content to temporary files, replaces destinations only after all staging succeeds, and restores any destination already replaced if a later replacement fails. The regression test `test_write_outputs_restores_files_when_a_replacement_fails` simulates a second replacement failure and verifies both files retain their original contents.

3. **Every generated definition has a traceability marker.** Copilot and Claude headers now include `generated-from` and `generated-by`; Codex has an equivalent leading TOML comment. Each identifies `.ept/resources/agent_sources/<agent>/parameters.yaml` and `python .ept/tools/compose_agents.py --agent <agent>`.

4. **Resolved skill paths are constrained to their declared root.** `discover_skills` resolves every discovered `SKILL.md` and rejects a path that cannot be made relative to the resolved skill root. `test_skill_discovery_rejects_path_outside_root` uses a file symlink to an external skill and verifies rejection.

5. **Agent names are now safe and source-bound.** `load_agent_source` requires lowercase kebab-case names and requires the `parameters.yaml` parent directory name to match. This prevents a source name from controlling an output path outside the three approved harness directories. `test_agent_source_rejects_invalid_or_mismatched_name` covers rejection.

6. **Prompt endings are preserved.** Skill parsing retains the complete Markdown body after line-ending normalization, including trailing newlines; agent-source loading retains YAML-decoded `agent_instructions` unchanged. Inline skill rendering no longer adds a replacement newline before `</instructions>`. `test_skill_and_instruction_trailing_newlines_are_preserved` verifies both cases.

7. **HR model ambiguity is rejected.** YAML is loaded through `UniqueKeyLoader`, which rejects duplicate mapping keys. `copilot_model` no longer falls back to regex parsing after invalid YAML, so malformed or ambiguous HR front matter fails generation. `test_copilot_model_rejects_duplicate_model_keys` verifies duplicate `model` entries are rejected.

### Verification evidence

The following completed successfully after regenerating all six migrated agents:

```text
.venv\Scripts\python.exe -m pytest tests\test_compose_agents.py tests\test_repository_hygiene.py -q
21 passed

.venv\Scripts\python.exe .ept\tools\compose_agents.py --all --check
exit code 0
```

## Review-02

### Review findings

1. **Medium: rendered shared contexts are not byte-identical across harnesses.** `render_copilot` and `render_claude` append `\n` after `agent_instructions`, while `render_codex` places `agent_instructions` at the end of `developer_instructions` without that extra newline. Consequently, the same agent produces a different shared payload depending on harness, and the Markdown renderers do not append `agent_instructions` verbatim. This violates the required cross-harness context equality and the prompt-preservation contract.

### Test coverage gap

The suite checks preservation when parsing skills and source files, but it does not compare each rendered harness payload byte-for-byte after removing the harness header. A regression test covering an instruction body with and without a trailing newline would expose this mismatch.

## Fix-02

### Fix-02 Corrections

1. **Shared contexts are now byte-identical across all harnesses.** `shared_context` constructs the one common payload from the rendered skills block, its required separator, and `agent_instructions`. Copilot, Claude, and Codex all render that exact string. The Markdown renderers no longer append a synthetic newline after the agent instructions, so both trailing-newline and no-trailing-newline instruction bodies remain unchanged.

2. **Regression coverage compares rendered contexts directly.** `test_rendered_shared_context_is_identical_across_harnesses` extracts the Copilot and Claude header sections, parses the Codex TOML payload, and compares all three contexts byte-for-byte. It covers instruction bodies both with and without a final newline.

3. **Generated Markdown definitions were regenerated.** The six migrated agents' Copilot and Claude definitions now match the corrected shared-context payload. Existing Codex definitions already used that payload and required no changes.

### Fix-02 Verification Evidence

The following commands completed successfully after regeneration:

```text
.venv\Scripts\python.exe -m pytest tests\test_compose_agents.py tests\test_repository_hygiene.py -q
18 passed

.venv\Scripts\python.exe .ept\tools\compose_agents.py --all --check
exit code 0
```

## Review-03

### Scope

Independent pass over `.ept/tools/compose_agents.py`, `tests/test_compose_agents.py`, and `tests/test_repository_hygiene.py` after Fix-02, checking against the acceptance criteria and prior review findings. Confirmed current state by running the check command and the focused test suite; both pass with no drift.

### Findings

1. **Low: `migrate()` has an untested fallback branch.** When Copilot front matter fails `yaml.safe_load`, `migrate()` falls back to a regex scan for `name|description|tools|user-invocable` and a manual `"true"/"false"` string conversion for `user-invocable`. No test exercises this path, so a change to the regex or the boolean coercion could silently break re-migration of an agent whose existing Copilot header is not valid YAML. This is a one-time migration helper rather than the generation path itself, so the risk is limited, but it is the only remaining untested branch of meaningful complexity in the module.

2. **Low: `format_agent_source` / `--format-sources` has no direct test.** `dump_agent_source` is tested, but the file-round-trip behavior of `format_agent_source` (reading a source, rewriting it, and requiring `agent_instructions` to be present) is not. A source file missing `agent_instructions` would raise `CompositionError`, which is correct, but that error path is unverified.

3. **Informational: whole-run atomicity exceeds the stated design.** `main()` composes every requested agent into one `all_outputs` mapping before any file is touched, so a schema or discovery failure partway through `--all` cannot leave a subset of agents regenerated. The design only required atomicity per agent's three outputs; the implementation applies it across the entire batch, which is a strict improvement and introduces no new risk.

4. **No functional defects found.** The points raised in Review-01 are all verified fixed in the current source: Codex strings are produced with `json.dumps` and parse under `tomllib` (confirmed by re-reading generated `.codex/agents/*.toml`); `write_outputs` stages to temp files and rolls back on partial failure; every renderer emits `generated-from`/`generated-by` metadata; `discover_skills` resolves paths and rejects escapes from the approved root; `load_agent_source` enforces kebab-case names and directory/name binding; skill bodies and `agent_instructions` preserve trailing newlines; `copilot_model` reads through `UniqueKeyLoader` and rejects duplicate keys. Manual inspection of generated `architect.md`, `architect.agent.md`, and `architect.toml` confirms matching shared content and correct per-harness headers.

### Test coverage gap

Beyond the two low-severity items above, coverage is otherwise thorough: skill discovery/ordering, both skill representations, schema validation failures, all three mandatory outputs, fixed model policy, TOML validity, atomic write rollback, symlink containment, name validation, newline preservation, and cross-harness content equality all have direct tests. Adding tests for the `migrate()` regex fallback and for `format_agent_source`'s missing-field error would close the remaining gaps but are not required for the composer's generation correctness.

### Verification evidence

```text
.venv\Scripts\python.exe .ept\tools\compose_agents.py --all --check
exit code 0

.venv\Scripts\python.exe -m pytest tests\test_compose_agents.py tests\test_repository_hygiene.py -q
18 passed
```

## Fix-03

### Fix-03 Corrections

1. **The legacy migration fallback is now covered.** `test_migrate_falls_back_to_legacy_header_and_converts_boolean` supplies malformed legacy Copilot front matter, verifies the regex fallback extracts the description and comma-separated tools, and verifies that `user-invocable: false` is converted to a Boolean value in the generated source.

2. **Source formatting is now covered.** `test_format_agent_source_round_trips_and_requires_instructions` verifies that `format_agent_source` writes a readable YAML literal block that reloads successfully, and that a source without `agent_instructions` raises `CompositionError`.

### Fix-03 Verification Evidence

The following commands completed successfully:

```text
.venv\Scripts\python.exe -m pytest tests\test_compose_agents.py tests\test_repository_hygiene.py -q
.venv\Scripts\python.exe .ept\tools\compose_agents.py --all --check
```

## Fix-04

### Fix-04 Corrections

1. **Copilot tools now use the harness format.** `render_copilot` converts the source tool list to one comma-separated value instead of allowing YAML to render a block list. Wildcard tool references are emitted with literal single quotes, such as `'github/*'`, preventing the previous escaped triple-quote output.

2. **Codex instructions now remain readable in generated files.** `render_codex` uses a TOML multiline basic string for `developer_instructions` rather than a JSON-style single-line string. The serializer preserves the parsed prompt by escaping backslashes and embedded triple-quote delimiters as TOML requires.

3. **Generated definitions were refreshed.** The Copilot and Codex definitions for `architect`, `ba`, `devops-engineer`, `python-developer`, `qa-engineer`, and `tech-lead` were regenerated from their centralized sources.

4. **Renderer coverage now asserts both output contracts.** Focused tests verify comma-separated Copilot tools with single-quoted wildcard references, and triple-quoted Codex instructions that continue to parse back to the original prompt.

### Fix-04 Verification Evidence

The following completed successfully:

```text
.venv\Scripts\python.exe -m pytest tests\test_compose_agents.py -q -k "copilot_uses_comma or codex_uses_multiline"
2 passed, 19 deselected

.venv\Scripts\python.exe .ept\tools\compose_agents.py --all --check
exit code 0

.venv\Scripts\python.exe -c "import tomllib; from pathlib import Path; [tomllib.loads(path.read_text(encoding='utf-8')) for path in Path('.codex/agents').glob('*.toml')]; print('All Codex definitions parse as TOML.')"
All Codex definitions parse as TOML.
```

## Enhancement-01

### Composer usability and documentation

1. **Descriptive command help.** The composer now uses an explicit argument parser. `python .ept/tools/compose_agents.py --help` describes `--agent`, `--all`, `--check`, `--migrate-existing`, and `--format-sources`, including that `--all` regenerates every defined agent source. The all-agent regeneration capability already existed; it is now discoverable and documented.

2. **File-backed shared skills introduction.** The fixed `SKILLS_INTRODUCTION` Python constant was moved to `.ept/tools/skills_introduction.txt`. `render_skills()` loads the file when it builds each skills block, preserving the mandated introduction while allowing prompt-only maintenance without editing Python code. A missing or unreadable introduction file raises `CompositionError`.

3. **Tool documentation.** `.ept/tools/README.md` documents the utility's output behavior, command examples, option semantics, source-file preparation, required `parameters.yaml` schema, generated output locations, and safe regeneration workflow. It also identifies `skills_introduction.txt` as the shared prompt preamble.

4. **Focused regression coverage.** Composer tests now verify that rendering takes the introduction from the sibling text file and that generated help exposes all supported options, including full regeneration through `--all`.

### Verification note

The focused composer test execution reported `17 passed`; the full module test run additionally reported six existing failures because the legacy fixtures under `.ept/agents/*.md` are absent from this checkout. These failures occur in `test_migrated_agent_instructions_preserve_legacy_bodies` before any composer behavior introduced by this enhancement is exercised.

## Enhancement-02

### Centralized harness model configuration

1. **Models now come from `agent-models.yaml`.** The composer reads `.ept/resources/agent_sources/agent-models.yaml` for the Copilot, Claude, and Codex model values while rendering every agent. It no longer derives the Copilot model from the HR agent definition or hard-codes the Claude and Codex model values in renderer functions.

2. **Model configuration is validated.** The file must define exactly the non-empty string keys `copilot`, `claude`, and `codex`. Missing, unknown, duplicate, or invalid entries stop generation with `CompositionError` instead of producing partial definitions.

3. **Regression coverage verifies the source of truth.** Tests cover loading all three configured models, rejection of duplicate YAML keys, and rendering of each harness model from the central mapping.
