# DEVOPS-013 - Foundry Models packaging and deployment report

## Result

| Field | Value |
|---|---|
| Story | DEV-STORY-013 |
| Task | DEVOPS-013 |
| Result | READY |
| Candidate commit | `bd13955feat(models,orchestration): add foundry-models and foundry-orchestration CLIs (DEV-013/DEV-014)` (short `bd13955`) |
| Rollback commit | `9f777fc` (parent of candidate; no models/orchestration code) |
| Verification window | 2026-08-10 00:40-00:57 Europe/Sofia |
| Host | Windows, PowerShell, Python 3.11.9 and Python 3.12.9 (uv-managed) |
| Target | Isolated local package environments only |
| External deployment | Not performed |
| Foundry calls | Not performed |
| Package publication | Not performed |
| Temporary path | `T:\tmp\foundry-devops013-014-20260810` |
| Time spent | 1.0 hours |

Candidate `bd13955` is ready for release as a Python package plus matching Claude skill bundle. Clean-archive build (sdist + wheel per PEP 517), wheel and editable installation, entry-point smoke tests, packaged metadata policy verification, Python 3.11/3.12 gates, security gates, and rehearsed rollback all passed. No live credential, Foundry environment, cloud resource, registry, or shared-worktree package was changed.

## Candidate and baseline

The candidate came from a clean `git archive` of commit `bd13955`, which contains both the Models and Orchestration namespace implementations (DEV-013/DEV-014 share one commit). The rollback baseline is the parent commit `9f777fc`, which has no `models/` or `orchestration/` package, no `foundry-models`/`foundry-orchestration` entry points, and no corresponding Claude skill directories.

| Archive | Files |
|---|---|
| Candidate `bd13955` | 2,794 |
| Rollback `9f777fc` | 2,780 |

Clean candidate and rollback archives contained no `.git` directory and no unrelated files from the dirty shared worktree. DESIGN-013 and TESTCASE-013 supplied the verification contracts; documentation outside the candidate commit was not copied into its package source.

## Build artifacts

Python 3.11.9 built the candidate with `python -m build` in an isolated build environment after upgrading `pip`, `setuptools`, and `wheel`.

| Artifact | Size | SHA-256 | Result |
|---|---:|---|---|
| `foundry_cli-0.1.0-py3-none-any.whl` | 102,587 | `0bfee4b5e3cfda154d841499e56d4a6d86c160b4ca5a0552c2a2f0eb7095fee1` | PASS |
| `foundry_cli-0.1.0.tar.gz` | 152,730 | `f4cc351e822b37186359a372a94eec71b6490bee9c0423660676445618202c16` | PASS |

Twine 7.0.0 accepted both artifacts (`PASSED`). Wheel inspection confirmed these required files:

```text
foundry_cli/models/__init__.py
foundry_cli/models/metadata-allow-list.md
foundry_cli/models/scripts/__init__.py
foundry_cli/models/scripts/foundry_models_cli.py
foundry_cli/orchestration/__init__.py
foundry_cli/orchestration/metadata-allow-list.md
foundry_cli/orchestration/scripts/__init__.py
foundry_cli/orchestration/scripts/foundry_orchestration_cli.py
```

Wheel inspection found no `tests/`, `.claude/`, `.ept/`, `.github/`, `.env`, private-key, or certificate file. The Claude skill remains a separate repository asset, matching the established launcher pattern (DEVOPS-010/011/012).

## Entry points and policy

Installed wheel metadata exposed the new commands and retained every console script from the rollback baseline:

```text
foundry-models = foundry_cli.models.scripts.foundry_models_cli:console_main
foundry-orchestration = foundry_cli.orchestration.scripts.foundry_orchestration_cli:console_main
foundry-admin = foundry_cli.admin.scripts.foundry_admin_cli:console_main
foundry-aip-agents = foundry_cli.aip_agents.scripts.foundry_aip_agents_cli:console_main
foundry-audit = foundry_cli.audit.scripts.foundry_audit_cli:console_main
foundry-datasets = foundry_cli.datasets.scripts.foundry_datasets_cli:main
foundry-filesystem = foundry_cli.filesystem.scripts.foundry_filesystem_cli:console_main
foundry-functions = foundry_cli.functions.scripts.foundry_functions_cli:console_main
foundry-language-models = foundry_cli.language_models.scripts.foundry_language_models_cli:console_main
foundry-ontologies = foundry_cli.ontologies.scripts.foundry_ontologies_cli:console_main
```

The installed Models policy has exactly 12 `PERMITTED` and 11 `BLOCKED` rows. The installed Orchestration policy has exactly 12 `PERMITTED` and 8 `BLOCKED` rows. Both match the canonical `.ept/docs/deliverables/architecture/metadata-allow-list.md`.

## Installation and smoke checks

The wheel used a fresh Python 3.11.9 environment. The editable install used a fresh Python 3.11.9 environment. Both used normal dependency resolution and passed `python -m pip check`. Smoke checks ran from empty directories with `PYTHONPATH` and all inherited `FOUNDRY*` variables unset.

| Check | Wheel | Editable |
|---|---:|---:|
| `foundry-models --help` | Exit 0 | Exit 0 |
| `foundry-orchestration --help` | Exit 0 | Exit 0 |
| Models route help (`model get --help`) | Exit 0 | Covered |
| Orchestration route help (`build search --help`) | Exit 0 | Covered |
| Claude launcher help (both namespaces) | Exit 0 | Covered |
| Retained commands (admin, aip-agents, audit, datasets, filesystem, functions, language-models, ontologies) | Exit 0 each | Exit 0 each |
| Package imports (`foundry_cli.models`, `foundry_cli.orchestration`) | PASS | PASS |
| Empty working directory after checks | Yes | Yes |

Package import probes confirmed 23 Models operations and 20 Orchestration operations in the OP_SPECS catalogs. The smoke directory contained only the test `.env` file; no `.foundry-data` directory or stray artifacts were created by the CLI itself.

## ACL policy verification (metadata-only tier)

With `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` and a dummy credential `.env`, write operations were blocked before client creation with exit code 8 (AccessControlError):

| Command | Exit | Result |
|---|---:|---|
| `foundry-models model create --name X --parent-folder-rid Y` | 8 | BLOCKED: metadata-only mode active |
| `foundry-orchestration build cancel <rid>` | 8 | BLOCKED: metadata-only mode active |

A PERMITTED metadata operation (`foundry-models model get <rid>`) passed the ACL gate and proceeded to network retries (ConnectionError against the dummy hostname, exit 6), proving the allowed path is not blocked by the policy. Invalid input (`foundry-models model get` with no positional) returned exit 1 (UserInputError). All ACL checks executed from the installed site-packages policy file.

## Quality, compatibility, and security

Checks ran against the clean candidate archive, not the shared worktree. Both interpreters used isolated virtual environments with complete `.[dev]` dependency installation.

| Command | Result |
|---|---|
| Python 3.11.9 full pytest with branch coverage | 1089 passed in 49.12 s; 85.47% (gate >=80% met) |
| Python 3.12.9 full pytest with branch coverage | 1089 passed in 47.18 s; 85.47% (gate >=80% met) |
| Targeted models + orchestration suites (3.11) | 65 passed in 1.53 s |
| `python -m ruff check src tests .claude/skills/foundry-models .claude/skills/foundry-orchestration` | Exit 0; all checks passed |
| `python -m mypy src` | Exit 0; no issues in 45 source files |
| `python -m bandit -r src --severity-level high` | Exit 0; 8,945 lines; zero findings at every severity |
| `python -m safety check --full-report` | Exit 0; 68 packages; zero known vulnerabilities, zero ignored |
| `python -m pip check` | Exit 0 for wheel, editable, and restored candidate |

Namespace branch coverage on 3.11: `foundry_models_cli.py` 89%, `foundry_orchestration_cli.py` 91%, both above the 80% gate. On Python 3.12, the legacy Audit nested-venv packaging test (`test_wheel_and_editable_installs_work_from_arbitrary_cwd_without_pythonpath`) initially failed because the nested `--system-site-packages` venv reads the base interpreter's site, not the parent venv's. After provisioning `python-dotenv` and `requests` into a task-local `PYTHONUSERBASE` for the base 3.12 interpreter (the same CI-equivalent bootstrap used in DEVOPS-011/012), the test passed and the full suite was green. This is a test-harness environment artifact, not a product defect.

`ruff check .` is not the project gate. CI defines `ruff check src/ tests/`; DEVOPS-012 added the Language Models Claude skill directory, and this task adds the two new Claude skill directories because they contain the launchers. Running Ruff over `.` would also scan vendored SDK sources and separate tracker/skill tooling under `.ept/`, which are outside this product change.

## Configuration and deployment impact

Relative to rollback baseline, packaging changes add the two console entry points, packaged policy files, namespace-specific Ruff ignores, modules, tests, Claude skills, and shared ACL write-verb changes. They do not change:

- runtime or development dependency declarations;
- `.env.example` or environment-variable names;
- GitHub Actions workflows or release permissions;
- infrastructure, secrets, or secret-store configuration;
- retained console entry-point mappings.

Runtime requirements remain `foundry-platform-sdk>=1.0.0`, `python-dotenv>=1.0.0`, and `requests>=2.31.0`. Live environment validation was intentionally omitted because this task verifies packaging and prohibits external Foundry access.

## Rollback rehearsal

The rollback wheel came from a clean archive of `9f777fc`.

| Item | Value |
|---|---|
| Rollback wheel | `foundry_cli-0.1.0-py3-none-any.whl` |
| Size | 87,422 bytes |
| SHA-256 | `9e1890f67477b92c5c535fb224b05352868f70fcbcf7b5637dd454f772f60f57` |
| Twine check | PASS |
| Rollback window | 2026-08-10 00:55:30-00:55:45 Europe/Sofia |
| Candidate restoration | 2026-08-10 00:55:50 Europe/Sofia |

Rehearsal steps and results:

1. Force-installed the rollback wheel into the isolated candidate environment with `--no-deps`. Exit 0.
2. Confirmed `foundry-models.exe` and `foundry-orchestration.exe` were absent, and `foundry_cli.models` / `foundry_cli.orchestration` had no import specification.
3. Confirmed all six retained commands (audit, datasets, filesystem, ontologies, language-models, aip-agents) still returned help with exit 0.
4. Reinstalled the candidate wheel with `--no-deps`. Exit 0.
5. Confirmed `foundry-models --help` and `foundry-orchestration --help` returned exit 0, all retained command help checks passed, and `pip check` exited 0.

Operational rollback must install the recorded baseline wheel and restore its matching skill bundle. Candidate recovery must reinstall the recorded candidate wheel and its matching skill directory. Deleting source files is not the rollback procedure.

## Temporary files

Verification archives, build trees, virtual environments, user sites, and artifacts remain under `T:\tmp\foundry-devops013-014-20260810` for reproduction. They contain public dependencies and generated build/test files, not credentials or Foundry data. No broad cleanup was attempted.

## Final status

DEVOPS-013 is READY. Candidate `bd13955` is production-ready for controlled package and Claude skill bundle release. Publication and live deployment remain separate authorized actions. Deployment activates after the parent story DEV-STORY-013 passes QA (TESTEXEC-013).
