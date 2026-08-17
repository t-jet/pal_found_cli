# Palantir Foundry CLI design repository

This repository holds requirements, architecture, delivery records, and the
agent workflow used to design and manage the Palantir Foundry CLI project.
Runtime source and distributable skills live in separate repositories.

## Repository map

| Repository | Ownership |
| --- | --- |
| [pal_found_cli](https://github.com/t-jet/pal_found_cli) | Design documents, tracker data, agent definitions, and orchestration material |
| [pal_found_cli_tool](https://github.com/t-jet/pal_found_cli_tool) | Python package, tests, build configuration, and release workflows |
| [pal_found_cli_skills](https://github.com/t-jet/pal_found_cli_skills) | Canonical `.agents/skills` distribution and validation workflow |

The tool and skills repositories are registered as submodules so a recursive
clone can reproduce the reviewed cross-repository state.

```bash
git clone --recurse-submodules https://github.com/t-jet/pal_found_cli.git
```

## Design navigation

Start with the [documentation index](.ept/docs/document_index.md). The
[repository split manifest](.ept/docs/deliverables/development/DEV-024-repository-split-manifest.md)
records content ownership, migration history, and verification evidence. The
[reference register](.ept/docs/deliverables/development/DEV-027-reference-register.md)
defines stable links between repositories.

Install and usage instructions belong to the
[tool repository](https://github.com/t-jet/pal_found_cli_tool). Skill onboarding
belongs to the
[skills repository](https://github.com/t-jet/pal_found_cli_skills).
