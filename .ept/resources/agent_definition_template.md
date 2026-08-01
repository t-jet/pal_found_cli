# Role-based agent creation instructions

Use these instructions only for role-based agents that own work such as analysis, architecture, implementation, testing, delivery, or governance.

Do not use them for service, utility, protocol, or tool-wrapper agents. Those agents need definitions designed for their service contract and are outside this template's scope.

## Files to create

Create four files for each role-based agent:

```text
.ept/agents/<agent-name>.md
.claude/agents/<agent-name>.md
.codex/agents/<agent-name>.toml
.github/agents/<agent-name>.agent.md
```

The `.ept/agents` file is the sole source of role instructions. The other three files are platform-specific loaders. They contain metadata, platform tool configuration where supported, and a reference to the `.ept/agents` file. They must not duplicate its contents.

## Create the authoritative role content

Use [.ept/resources/agent_content_template.md](agent_content_template.md) as the literal source for `.ept/agents/<agent-name>.md`.

Copy the entire template. Preserve every instruction, heading, XML tag, section, line order, and fixed phrase. Do not add, remove, reorder, summarize, or rewrite fixed content. Replace only the placeholders listed below.

| Placeholder | Required replacement |
| --- | --- |
| `{{agent_type}}` | Role title or agent type |
| `{{agent_specialization}}` | Role-specific scope and specialization |
| `{{agent_skills_experience_and_enterprise_standards_following}}` | Skills, experience, and standards required by the role |
| `{{agent_name}}` | Lowercase kebab-case agent name used in filenames and improvement-memory path |
| `{{tracker_assignee}}` | Exact assignee value used by the tracking system |
| `{{deliverables_code_scripts_tasks_and_work_products_quality_standards_by_deliverable_type}}` | Role-specific quality standards, grouped by deliverable or work-product type |

### Placeholder guidance

`{{agent_type}}` identifies the professional role. Use a short title that fits between "sophisticated" and "agent" in the opening sentence. Include the expertise qualifier when needed, for example `expert AI Solution Architect` or `expert AI QA Engineer`. Do not describe responsibilities here.

`{{agent_specialization}}` states the role's primary domain, delivery context, and governing body of practice. Keep it to one compact phrase. It must complete the sentence after "specializing in". A suitable value names both the work and its quality context, for example `enterprise-grade distributed systems, applying established architecture and security standards`. Do not repeat the role title or list individual skills.

`{{agent_skills_experience_and_enterprise_standards_following}}` defines what the role can do and the standards it applies. Start with a comma-separated list that follows "expert in" grammatically. Cover:

- core technical or analytical competencies;
- review, risk, and collaboration responsibilities;
- expected quality attributes such as security, scalability, maintainability, or testability;
- named standards, methods, or industry practices the role must follow.

This replacement may contain additional complete sentences when a list alone cannot define the role. State observable capabilities, not personality traits or promotional claims. Because the template supplies the final period, omit a trailing period from the replacement.

`{{agent_name}}` is the stable machine identifier. Use lowercase kebab-case, such as `solution-architect` or `qa-engineer`. The same value must be used in the `.ept/agents` filename, improvement-memory filename, and all three platform-loader filenames. Do not use a display name, spaces, underscores, or a tracker label here.

`{{tracker_assignee}}` is the exact assignee token accepted by the tracking system. Obtain it from the role registry or tracker configuration. It may differ from `{{agent_name}}`, so do not derive or normalize it. Insert only the token, without quotes, backticks, or explanatory text.

`{{deliverables_code_scripts_tasks_and_work_products_quality_standards_by_deliverable_type}}` contains the role's enforceable quality rules. Write valid XML fragments inside the existing `<Deliverable_Quality_Standards>` wrapper. Add one descriptive child element per deliverable or work-product type:

```xml
<Design_Documents>
Define required sections, traceability, diagrams, decisions, assumptions, constraints, and implementation guidance.
</Design_Documents>
<Reviews>
Define review criteria, mandatory checks, evidence, severity rules, and the form of actionable feedback.
</Reviews>
```

Name child elements after outputs the role owns, such as specifications, designs, code changes, test cases, reviews, deployment work, or governance decisions. Inside each element, specify:

- required contents and formats;
- standards and checks to apply;
- edge cases, risks, and constraints to cover;
- evidence or traceability required before handoff;
- concrete acceptance conditions where applicable.

Use directive language such as `include`, `verify`, `record`, `check`, and `provide`. Do not add another `<Deliverable_Quality_Standards>` wrapper, unrelated workflow rules, or platform tool instructions.

Replacement text may span multiple lines where the placeholder represents a section body. Keep replacement text inside the placeholder's existing section. Do not create new top-level sections or change tag names.

The completed file must contain no unresolved placeholder tokens.

## Create the Claude Code loader

Create `.claude/agents/<agent-name>.md`:

```markdown
---
name: <display-name>
description: <role scope and invocation guidance>
tools: <Claude Code tool list>
permissionMode: bypassPermissions
model: inherit
---

## Instructions

Load and strictly follow all instructions in [.ept/agents/<agent-name>.md](.ept/agents/<agent-name>.md) before doing anything else. That file is the authoritative definition of your role, workflow, tool-use rules, and standards.
```

Use Claude Code tool names. Select the smallest set that covers the role:

| Capability | Claude Code tools |
| --- | --- |
| Read and search files | `Read`, `Glob`, `Grep` |
| Create or change files | `Write`, `Edit` |
| Run commands | `Bash` |
| Delegate to subagents | `Agent` |
| Research external sources | `WebFetch`, `WebSearch` |
| Use MCP integrations | `mcp_*` or required named MCP tools |

The role's workflow requires `Agent` when it must call `ticket-helper` or another subagent. Do not grant unrelated tools.

## Create the Codex loader

Create `.codex/agents/<agent-name>.toml`:

```toml
name = "<display-name>"
description = "<concise role scope and invocation guidance>"
developer_instructions = """
## Instructions

Load and strictly follow all instructions in .ept/agents/<agent-name>.md before doing anything else. That file is the authoritative definition of your role, workflow, tool-use rules, and standards.
"""
```

Do not add `tools`, `permissionMode`, `model`, or `user-invocable`. Codex supplies agent categories and tools through its runtime configuration. The TOML file only registers the role and points it to the authoritative instructions.

## Create the GitHub Copilot loader

Create `.github/agents/<agent-name>.agent.md`:

```markdown
---
name: <display-name>
description: <role scope and invocation guidance>
tools: <Copilot tool list>
model: local-llama-model
user-invocable: true
---

## Instructions

Load and strictly follow all instructions in [.ept/agents/<agent-name>.md](.ept/agents/<agent-name>.md) before doing anything else. That file is the authoritative definition of your role, workflow, tool-use rules, and standards.
```

Use Copilot and VS Code tool identifiers. Build the tool list from the role's responsibilities:

| Capability | Copilot tools |
| --- | --- |
| Read files and inspect output | `read/readFile`, `read/problems`, `read/terminalSelection`, `read/terminalLastCommand`, `read/viewImage` |
| Search the workspace | `search/codebase`, `search/fileSearch`, `search/listDirectory`, `search/textSearch`, `search/changes` |
| Create or change files | `edit/createDirectory`, `edit/createFile`, `edit/editFiles`, `edit/rename` |
| Run and manage commands | `execute/runInTerminal`, `execute/getTerminalOutput`, `execute/awaitTerminal`, `execute/killTerminal`, `execute/createAndRunTask` |
| Inspect test failures | `execute/testFailure` |
| Delegate to subagents | `agent/runSubagent` |
| Use workspace memory | `vscode/memory` |
| Research external sources | `web/fetch`, `web/githubRepo` |
| Manage multi-step work | `todo` |

Add Python, language-service, browser, diagram, notebook, or extension tools only when the role requires them. Use exact identifiers installed in the target Copilot environment. Do not use Claude Code tool names in this file.

The role's workflow requires `agent/runSubagent` when it must call `ticket-helper` or another subagent.

## Names and descriptions

Use one lowercase kebab-case `<agent-name>` for all filenames and template paths. Use one display name consistently across platform loaders.

Descriptions are discovery metadata. State the role, its responsibilities, and requests that should invoke it. Description length may differ by platform, but scope must remain consistent.

## Creation procedure

1. Confirm the new agent is role-based. Stop if it is a service, utility, protocol, or tool-wrapper agent.
2. Choose `<agent-name>`, display name, tracker assignee, responsibilities, specialization, standards, and quality requirements.
3. Copy `.ept/resources/agent_content_template.md` to `.ept/agents/<agent-name>.md`.
4. Replace only the six documented placeholders. Preserve all other content literally.
5. Create the Claude loader and select Claude Code tools for the role.
6. Create the Codex loader without platform tool fields.
7. Create the Copilot loader and select Copilot tools for the role.
8. Confirm all three loaders reference `.ept/agents/<agent-name>.md`.
9. Create `.ept/self-improvement/<agent-name>.md` if the memory file does not exist.
10. Update role registries or resource documentation required by the repository.
11. Run the validation checklist.

## Validation checklist

- [ ] Agent is role-based, not a service, utility, protocol, or tool-wrapper agent.
- [ ] `.ept/agents/<agent-name>.md` is a complete copy of `agent_content_template.md` with only documented placeholders replaced.
- [ ] No fixed instruction, heading, XML tag, section, or line order changed.
- [ ] No unresolved placeholder tokens remain.
- [ ] Tracker assignee is valid for the role.
- [ ] Improvement-memory path uses the same `<agent-name>` as the files.
- [ ] Role-specific standards are inside `<Deliverable_Quality_Standards>`.
- [ ] Platform loaders contain metadata and the authoritative-file reference only.
- [ ] Claude loader uses Claude Code tools.
- [ ] Codex loader contains no platform tool list.
- [ ] Copilot loader uses role-specific Copilot tool identifiers.
- [ ] All loaders reference the same `.ept/agents/<agent-name>.md` path.
- [ ] Filename stem and display name are consistent across platforms.

## Final rule

Change role wording only through placeholders in `agent_content_template.md`. Keep all shared instructions and structure literal. Treat Claude Code, Codex, and GitHub Copilot loaders as separate platform adapters with different metadata and tool models.
