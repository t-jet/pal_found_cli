# Agent refactoring task

## Objective

The objective of this task is to refactor agent composition so context is cache-friendly, all centrally available skills are included before an agent starts work, and shared skill updates do not require repetitive edits to individual agent definitions.

Use one central skills repository and a composition tool that renders complete agent contexts from agent-specific instructions and harness parameters.

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

Model selection is fixed by harness: Copilot inherits the exact model from the HR Copilot agent definition; Claude always uses `inherit`; Codex always uses `gpt-5.6`. Models are not agent-source parameters.

## Design

### Scope and ownership

Introduce one repository-owned agent composer that reads declarative source files and writes complete harness definitions. The composer is the only component allowed to render skills into generated agent definitions. Authors maintain shared skills and concise, agent-specific source files; generated definitions are build outputs and must not be manually edited.

The current thin-loader approach in `.ept/resources/agent_definition_template.md` is incompatible with the target behavior because it references a separate authoritative file instead of placing the complete context in each harness definition. Retire that approach for generated agents. The existing templates may remain only during migration, until every generated definition is rendered by the composer.

### Source layout

Use the following layout, where `<agent-name>` is lowercase kebab-case:

```text
.ept/resources/
  skills/<skill-name>/SKILL.md             # inline skill source
  agent_sources/<agent-name>/
    parameters.yaml                        # identity, headers, and agent-specific prompt
.ept/skills/<skill-name>/SKILL.md          # referenced skill source
.ept/tools/compose_agents.py               # composer CLI
```

`parameters.yaml` is the canonical per-agent contract. It contains the agent identity, shared header fields, each harness's supported header fields, and agent-specific instructions. Skill selection and output selection are repository policy, not agent configuration. The composer constructs every harness header from this one file and rejects unsupported, missing, or inconsistent field values.

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

Models are deliberately absent from `parameters.yaml` and are chosen by fixed repository policy. The composer extracts the Copilot model from the HR Copilot agent definition, writes `inherit` for every Claude definition, and writes `gpt-5.6` for every Codex definition. A missing or ambiguous HR Copilot model is a generation error. Claude and Codex generation does not read HR model metadata.

The composer discovers every `SKILL.md` under `.ept/skills` as a referenced skill and every `SKILL.md` under `.ept/resources/skills` as an inline skill. It rejects missing skill roots, invalid YAML front matter, a missing `name` or `description`, duplicate parsed skill names within or across the roots, and any discovered path that escapes its approved root. Individual agents cannot opt out of a centrally available skill.

The `agent_instructions` field is appended verbatim after the skills block. This keeps the shared skills cacheable and prevents agent-specific content from leaking into shared skill definitions.

### Rendering algorithm

For every agent and each mandatory harness, the composer:

1. Reads and validates `parameters.yaml`, including the shared and harness-specific header schema.
2. Discovers referenced and inline skills from their separate roots.
3. Parses each `SKILL.md` YAML front matter and separates the Markdown body from metadata.
4. Builds exactly one `<skills>` block using the required introduction without modifications.
5. Emits referenced skills first, alphabetically by parsed skill `name`, with `<file>` paths relative to the repository root.
6. Emits inline skills next, alphabetically by parsed skill `name`, with the full Markdown body inside `<instructions>`.
7. Constructs the appropriate harness header from the shared and harness-specific YAML fields, then concatenates it with the rendered skills block and `agent_instructions`.

The renderer must preserve skill bodies byte-for-byte apart from normalizing line endings to the repository convention. It must not recursively expand referenced skills. This gives agents immediate visibility of the skills intended for the initial context while retaining file-backed skills that must be read at task start.

Model selection is resolved independently of agent source files. The composer reads only the HR Copilot agent definition and writes its exact model setting to each generated Copilot definition. It writes Claude's `model: inherit` and Codex's `model = "gpt-5.6"` as fixed values. A missing or ambiguous HR Copilot model is a generation error.

### Outputs and generated-file policy

Render complete definitions to the repository's existing harness locations:

| Harness | Generated definition |
| --- | --- |
| Copilot | `.github/agents/<agent-name>.agent.md` |
| Claude | `.claude/agents/<agent-name>.md` |
| Codex | `.codex/agents/<agent-name>.toml` |

Each output contains its harness-specific metadata followed by the same rendered skills and agent-specific instructions. The shared context must therefore be identical across outputs after removing the header section. Add a generated-file marker that identifies the source directory and composer command; this supports repository hygiene checks without placing a second source of truth in the output.

Copilot, Claude, and Codex are mandatory outputs for every discovered agent source. The composer always constructs all three and fails the entire invocation if any required YAML header field, required HR Copilot model value, or destination cannot be resolved. There is no per-agent output list, filtering option, separate header file, or partial-generation mode.

### Composer interface

Provide a Python CLI because the repository already uses Python tooling:

```text
python .ept/tools/compose_agents.py --agent architect
python .ept/tools/compose_agents.py --all
python .ept/tools/compose_agents.py --all --check
```

`--agent` renders one source directory to all three mandatory harness outputs. `--all` discovers every directory below `.ept/resources/agent_sources` and renders each to all three outputs. `--check` performs the same render in memory and fails when a generated file is missing or differs, without writing any file. Normal execution writes only changed output files and reports the affected paths. Exit code `0` means all requested definitions are valid and current; any schema, discovery, parse, or drift failure is non-zero.

### Validation strategy

Unit tests cover exhaustive skill discovery, metadata parsing, source-root restrictions, ordering, rendering of both skill kinds, duplicate detection, YAML header-schema validation, mandatory three-output generation, exact shared-context equality across harnesses, HR Copilot model inheritance, fixed Claude model inheritance, and the fixed Codex `gpt-5.6` model. Fixture tests use multiple skills from both roots so the exact discovery and ordering behavior is reviewable.

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
- Each generated Copilot agent inherits the model configured for the HR Copilot agent; every Claude agent uses `inherit`; every Codex agent uses `gpt-5.6`.
- Generation fails rather than producing a partial result when any of the three mandatory harness headers or output paths is unavailable, or when the HR Copilot model cannot be resolved.
- `--all --check` detects stale, missing, or manually changed generated output and is enforced in automated tests.
- The HR agent can create a new role-based agent by adding source files and invoking the composer, without selecting skills or harness outputs or manually composing harness definitions.
