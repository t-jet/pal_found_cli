# DEVOPS-011 - Foundry AIP Agents packaging and deployment report

## Result

| Field | Value |
|---|---|
| Story | DEV-STORY-011 |
| Task | DEVOPS-011 |
| Result | READY |
| Candidate commit | `4bc449ccff7f6d922027b49f0f7d797d2ecb3554` |
| Rollback commit | `87d817c6f9d3329b57fadd20f3df84f93be9d570` |
| Verification window | 2026-08-09 13:26-13:33 Europe/Sofia |
| Host | Windows 11, PowerShell, Python 3.11.9 and 3.12.0 |
| Target | Isolated local package environments only |
| External deployment | Not performed |
| Foundry calls | Not performed |
| Package publication | Not performed |
| Temporary path | `T:\tmp\foundry-devops011-4bc449c-20260809-132623` |
| Time spent | 0.12 hours |

Candidate is ready for release as a Python package plus matching Claude skill bundle. Build, clean installation, package-policy, regression, security, dependency, and rollback checks passed. No live credential, Foundry environment, cloud resource, registry, or shared-worktree package was changed.

## Candidate and baseline

The candidate came from a clean `git archive` of this linear commit chain:

```text
ee2cef76222a8e1ddf3cde1fdd47ac576d03051d  feat: add AIP Agents CLI and session support
8a533fd9814ef610fd17dcda7f35747ffbaed8c8  fix: handle native Foundry SDK errors
02920aaf11ea9b9cf60467ad4bcb139159497f6d  fix: complete Foundry SDK error mapping
224ca5d13afdac27d1691207e9c0f5272b0344a8  test: add AIP Agents QA cases
4bc449ccff7f6d922027b49f0f7d797d2ecb3554  test: record AIP Agents QA execution
```

The rollback baseline is the parent of the first AIP Agents commit. Clean candidate and rollback archives contained 1,421 and 1,410 files respectively. Neither archive contained `.git` or unrelated files from the dirty shared worktree. DESIGN-011 and TESTEXEC-011 supplied the verification contracts; documentation outside the candidate commit was not copied into its package source.

## Build artifacts

Python 3.11.9 built the candidate with `python -m build` in an isolated build environment after upgrading `pip`, `setuptools`, and `wheel`.

| Artifact | Size | SHA-256 | Result |
|---|---:|---|---|
| `foundry_cli-0.1.0-py3-none-any.whl` | 71,741 bytes | `d643e160a353e9350f03bb0d1617099aefd4ef0a484afee36da1158ef13d1eae` | PASS |
| `foundry_cli-0.1.0.tar.gz` | 109,990 bytes | `e60eb763f6e7ebdcf6d403a7609ca32387d3ed6a2e349b17d83abdcc79b42ef0` | PASS |

Twine 7.0.0 accepted both artifacts. Wheel inspection confirmed these required files:

```text
foundry_cli/aip_agents/__init__.py
foundry_cli/aip_agents/metadata-allow-list.md
foundry_cli/aip_agents/scripts/__init__.py
foundry_cli/aip_agents/scripts/foundry_aip_agents_cli.py
```

Wheel inspection found no `tests/`, `.claude/`, `.ept/`, `.github/`, `.env`, private-key, or certificate file. The Claude skill remains a separate release asset.

## Entry points, policy, and installation checks

Wheel metadata exposed the new command and retained every console script from the rollback baseline:

```text
foundry-aip-agents=foundry_cli.aip_agents.scripts.foundry_aip_agents_cli:console_main
foundry-audit=foundry_cli.audit.scripts.foundry_audit_cli:console_main
foundry-datasets=foundry_cli.datasets.scripts.foundry_datasets_cli:main
foundry-filesystem=foundry_cli.filesystem.scripts.foundry_filesystem_cli:console_main
foundry-ontologies=foundry_cli.ontologies.scripts.foundry_ontologies_cli:console_main
```

Wheel and editable installs used normal dependency resolution. `pip check` passed after each install. All smoke checks ran from empty working directories with `PYTHONPATH`, `FOUNDRY_TOKEN`, and `FOUNDRY_HOSTNAME` unset. `FOUNDRY_AGENTIC_CLI_ENV_FILE` pointed to a nonexistent file.

| Check | Wheel | Editable |
|---|---:|---:|
| `foundry-aip-agents --help` | Exit 0 | Exit 0 |
| Packaged module help | Exit 0 | Covered by installed console/import checks |
| Claude launcher help | Exit 0 | Exit 0 |
| Audit, Datasets, Filesystem, and Ontologies help | Exit 0 each | Exit 0 each |
| AIP metadata policy exists | Yes, in `site-packages` | Yes, in editable source |
| Empty working directory after checks | Yes | Yes |

The installed metadata-only policy permitted exactly six of the 15 SDK operations, blocked nine, and blocked local `session purge`. Package and launcher imports exited 0 with no stdout or stderr and created no file or directory. Help paths did not require configuration or credentials.

## Quality, compatibility, and security

Checks ran against separate clean archive copies, not the shared worktree. Both interpreters used isolated virtual environments with complete `.[dev]` dependency installation. A task-local `PYTHONUSERBASE` supplied runtime dependencies to the legacy Audit test that creates a nested `--system-site-packages` environment and installs its wheel with `--no-deps`.

| Command | Result |
|---|---|
| Python 3.11.9 full pytest with branch coverage | 723 passed in 30.92 s; 84.52% |
| Python 3.12.0 full pytest with branch coverage | 723 passed in 28.54 s; 84.52% |
| `python -m ruff check src tests .claude/skills/foundry-aip-agents` | Exit 0; all checks passed |
| `python -m mypy src` | Exit 0; no issues in 30 source files |
| `python -m bandit -r src --severity-level high` | Exit 0; 6,507 lines; zero findings at every severity |
| `python -m pip check` | Exit 0; no broken requirements |
| `python -m safety check --full-report` | Exit 0; 68 packages; zero known vulnerabilities |

Safety 3.8.1 reported that `check` is deprecated but completed against its open-source database without authentication. No vulnerability was ignored. The 80% repository branch-coverage gate passed on both supported Python versions.

`ruff check .` is not the project gate. CI defines `ruff check src/ tests/`; DESIGN-011 requires established Ruff configuration; DEVOPS-010 used the same product scope. DEVOPS-011 adds the AIP Claude skill directory because it contains the new launcher. Running Ruff over `.` would also scan vendored SDK sources under `.ept/docs` and separate tracker and skill tooling under `.ept/skills`, which are outside this product change.

## Configuration and deployment impact

Relative to rollback baseline, packaging changes add the AIP console entry point, packaged policy file, namespace-specific Ruff ignore, module, tests, Claude skill, and shared error/ACL/client changes. They do not change:

- runtime or development dependency declarations;
- `.env.example` or environment-variable names;
- GitHub Actions workflows or release permissions;
- infrastructure, secrets, or secret-store configuration;
- retained console entry-point mappings.

Runtime requirements remain `foundry-platform-sdk>=1.0.0`, `python-dotenv>=1.0.0`, and `requests>=2.31.0`. Live environment validation was intentionally omitted because this task verifies packaging and prohibits external Foundry access.

## Rollback rehearsal

The rollback wheel came from a clean archive of `87d817c6f9d3329b57fadd20f3df84f93be9d570`.

| Item | Value |
|---|---|
| Rollback wheel | `foundry_cli-0.1.0-py3-none-any.whl` |
| Size | 62,942 bytes |
| SHA-256 | `d208c4185b70690edf2d1db2337855f4de4a9482b17ac663ce043b4f21d070d5` |
| Twine check | PASS |
| Rollback window | 2026-08-09 13:33:10-13:33:12 Europe/Sofia |
| Candidate restoration completed | 2026-08-09 13:33:15 Europe/Sofia |

Rehearsal steps and results:

1. Force-installed rollback wheel with `--no-deps` into isolated candidate environment. Exit 0.
2. Confirmed `foundry-aip-agents.exe` was absent, `foundry_cli.aip_agents` had no import specification, and rollback archive had no AIP Claude skill.
3. Confirmed Audit, Datasets, Filesystem, and Ontologies help commands still exited 0.
4. Reinstalled candidate wheel with `--no-deps`. Exit 0.
5. Confirmed AIP module and console returned; AIP console and Claude launcher help exited 0.
6. Confirmed all retained command help checks and `pip check` still exited 0.

Operational rollback should install the recorded baseline wheel and restore its matching skill bundle. Candidate recovery should reinstall the recorded candidate wheel and its matching AIP skill directory. Deleting source files is not the rollback procedure.

## Temporary files

Verification archives, build trees, virtual environments, user sites, and artifacts remain under `T:\tmp\foundry-devops011-4bc449c-20260809-132623` for reproduction. They contain public dependencies and generated build/test files, not credentials or Foundry data. No broad cleanup was attempted.

## Final status

DEVOPS-011 is READY. Candidate `4bc449ccff7f6d922027b49f0f7d797d2ecb3554` is production-ready for controlled package and Claude skill bundle release. Publication and live deployment remain separate authorized actions.
