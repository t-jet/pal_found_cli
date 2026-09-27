# Agent Composer

`compose_agents.py` renders complete agent definitions for Copilot, Claude, and Codex from one centralized agent source. It discovers every shared skill, constructs the common skills context, and writes the harness-specific definition files.

Run commands from the repository root:

```powershell
python .ept/tools/compose_agents.py --help
python .ept/tools/compose_agents.py --agent architect
python .ept/tools/compose_agents.py --all
python .ept/tools/compose_agents.py --all --check
```

`--agent NAME` regenerates all three definitions for one source.
`--all` regenerates every defined source in `.ept/resources/agent_sources`; use it after a shared skill or the skills introduction changes.
`--check` makes no changes and exits nonzero when an output is missing or stale.
`--migrate-existing` creates a source from legacy `.ept/agents/<name>.md` and Copilot files.
`--format-sources` rewrites selected source files with a readable YAML literal block for `agent_instructions`.

## Prepare An Agent Source

Create `.ept/resources/agent_sources/<agent-name>/parameters.yaml`. The directory name and the `name` value must match and use lowercase kebab-case. The source must contain every required harness mapping, even when `codex` is empty:

```yaml
name: example-agent
description: Brief description of the agent.
copilot:
  tools: [read, search]
  user_invocable: true
claude:
  tools: [Read, Grep, Edit]
  permission_mode: bypassPermissions
codex: {}
agent_instructions: |-
  Agent-specific instructions belong here.
```

Then generate and validate the definitions:

```powershell
python .ept/tools/compose_agents.py --agent example-agent
python .ept/tools/compose_agents.py --agent example-agent --check
```

Do not edit generated files directly. Update `parameters.yaml`, a shared skill under `.ept/resources/skills` or `.ept/skills`, [agent-models.yaml](../resources/agent_sources/agent-models.yaml), or [skills_introduction.txt](skills_introduction.txt), then regenerate the affected agents. The complete output set is written to `.github/agents`, `.claude/agents`, and `.codex/agents`.

## Harness Models

[agent-models.yaml](../resources/agent_sources/agent-models.yaml) supplies the model for every generated definition of each harness. It must contain exactly the three non-empty string values shown below:

```yaml
copilot: local-llama-model
claude: inherit
codex: gpt-5.6
```

Models are repository-wide policy rather than per-agent configuration. Change this file and run `python .ept/tools/compose_agents.py --all` to regenerate every affected definition. The composer rejects missing, duplicate, unknown, or invalid model entries.

## Skills Introduction

[skills_introduction.txt](skills_introduction.txt) is the exact shared preamble placed at the start of every generated `<skills>` block. Keeping it separate from the Python implementation lets prompt maintainers update the common instruction without changing composer code. The utility reads this file at render time; generation fails with a clear error if it is unavailable.
