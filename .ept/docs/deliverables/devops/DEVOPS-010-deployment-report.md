# DEVOPS-010 - Foundry Audit packaging and deployment report

## Result

| Field | Value |
|---|---|
| Story | DEV-STORY-010 |
| Task | DEVOPS-010 |
| Result | READY |
| Reviewed commit | `87d817c6f9d3329b57fadd20f3df84f93be9d570` |
| Verification window | 2026-08-01 21:31-21:38 Europe/Sofia |
| Host | Windows, PowerShell, Python 3.11.9 |
| Target | Isolated local package environments only |
| External deployment | Not performed |
| Foundry calls | Not performed |
| Package publication | Not performed |
| Temporary path | `T:\tmp\foundry-devops010-87d817c6` (cleanup blocked by host policy) |
| Time spent | 0.20 hours |

Commit `87d817c6f9d3329b57fadd20f3df84f93be9d570` is ready for the package deployment stage. Build, install, help, package-policy, regression, security, and rollback checks passed. No live worktree package, release, Foundry environment, or registry was changed.

## Build artifacts

The candidate came from a clean `git archive` of the reviewed commit. Build used `python -m build` in an isolated build environment.

| Artifact | Size | SHA-256 | Result |
|---|---:|---|---|
| `foundry_cli-0.1.0-py3-none-any.whl` | 62,942 bytes | `dd99ee62051ee2bfa4d5731af76038812f99ef78aeed2da001a75ae39db75955` | PASS |
| `foundry_cli-0.1.0.tar.gz` | 99,908 bytes | `60d79d63a5aaeec18bec0b4cdf6946d23ed2229271253ecb46dd82b7d545f272` | PASS |

`python -m twine check` passed for both files. The wheel contains these Audit files:

```text
foundry_cli/audit/__init__.py
foundry_cli/audit/metadata-allow-list.md
foundry_cli/audit/scripts/__init__.py
foundry_cli/audit/scripts/foundry_audit_cli.py
```

Wheel policy inspection found no `tests/`, `.claude/`, `.ept/`, `.github/`, `.env`, key, or certificate material. The Claude skill remains a separate repository asset, matching the established launcher pattern.

## Entry points and smoke checks

Installed wheel metadata exposed the expected scripts without changing retained mappings:

```text
foundry-audit=foundry_cli.audit.scripts.foundry_audit_cli:console_main
foundry-datasets=foundry_cli.datasets.scripts.foundry_datasets_cli:main
foundry-filesystem=foundry_cli.filesystem.scripts.foundry_filesystem_cli:console_main
foundry-ontologies=foundry_cli.ontologies.scripts.foundry_ontologies_cli:console_main
```

All smoke checks ran from an empty arbitrary working directory. `FOUNDRY_AGENTIC_CLI_ENV_FILE` pointed to a nonexistent file, and `FOUNDRY_TOKEN` and `FOUNDRY_HOSTNAME` were unset. This forced help paths to prove they do not load configuration or require credentials.

| Time (Europe/Sofia) | Command | Exit | Result |
|---|---|---:|---|
| 2026-08-01 21:31 | Clean Python 3.11 wheel install | 0 | PASS |
| 2026-08-01 21:32 | `foundry-audit --help` | 0 | Listed `log-file list` and `log-file content` |
| 2026-08-01 21:32 | `foundry-audit log-file --help` | 0 | Listed exactly `list` and `content` |
| 2026-08-01 21:32 | `python -m foundry_cli.audit.scripts.foundry_audit_cli --help` and route help | 0 | PASS |
| 2026-08-01 21:32 | Claude launcher root and route help, using an absolute launcher path | 0 | PASS |
| 2026-08-01 21:32 | Retained `foundry-datasets`, `foundry-filesystem`, and `foundry-ontologies` help | 0 each | PASS |
| 2026-08-01 21:33 | Python 3.11 editable install and `foundry-audit --help` | 0 | PASS |

The arbitrary working directory remained empty. No `.foundry-data` directory appeared. Help exited during argument parsing, before configuration loading, client construction, network access, or download-path creation.

Python 3.12 was not installed on this DevOps host, so a second local editable environment was not feasible. Fresh QA evidence in [TESTEXEC-010](../qa/TESTEXEC-010-test-results.md) covers Python 3.12.0: 933 tests passed, standalone package import produced no stdout or stderr, and wheel/editable package probes passed. DevOps still performed independent wheel, editable, entry-point, launcher, arbitrary-CWD, and rollback checks on Python 3.11.9.

## Quality and security gates

Commands ran against the clean candidate archive, not the shared worktree.

| Time (Europe/Sofia) | Command | Exit | Evidence |
|---|---|---:|---|
| 2026-08-01 21:34 | `ruff check src/ tests/` | 0 | All checks passed |
| 2026-08-01 21:34 | `mypy src/` | 0 | No issues in 26 source files |
| 2026-08-01 21:34 | `pytest tests/ --cov=foundry_cli --cov-report=term-missing --cov-report=xml -q` | 0 | 668 passed; 82.46% branch coverage; 80% gate met |
| 2026-08-01 21:35 | `bandit -r src/ --severity-level high` | 0 | 5,768 lines; 0 findings at every severity |
| 2026-08-01 21:35 | `safety check --full-report` after CI-equivalent tool upgrade | 0 | 69 packages scanned; 0 vulnerabilities |
| 2026-08-01 21:31 | `python -m build` | 0 | Wheel and sdist built |
| 2026-08-01 21:31 | `python -m twine check dist/*` | 0 | Both artifacts passed |

Safety initially reported nine findings in the virtual environment's bundled `pip 24.0` and `setuptools 65.5.0`. Project CI upgrades `pip`, `setuptools`, and `wheel` before dependency installation. Repeating that documented order installed `pip 26.2`, `setuptools 83.0.0`, and `wheel 0.47.0`; the rescan returned zero vulnerabilities. No exception or ignore rule was used.

QA independently approved all 26 cases at the same reviewed commit. Its evidence records 83 targeted tests, 933 full-suite tests on Python 3.11 and 3.12, 82.66% branch coverage, and clean static, security, compilation, package, ACL, and side-effect probes.

## Configuration and deployment impact

The change from rollback baseline to candidate adds the Audit package, tests, skill, launcher, console entry, package data, and tool-specific lint/coverage settings. It does not change:

- runtime or development dependencies;
- `.env.example`, environment-variable names, or credential handling;
- GitHub Actions workflows or release permissions;
- infrastructure, cloud resources, secrets, or secret-store configuration;
- existing console entry-point mappings.

Runtime dependencies in the wheel remain `foundry-platform-sdk>=1.0.0`, `python-dotenv>=1.0.0`, and `requests>=2.31.0`. No live environment validation was needed because this task verified packaging only and prohibited external Foundry access.

## Rollback rehearsal

Rollback baseline is commit `cdf9b2a3d5e468a359471def06a80c80d73ec82a` (`tracker and ticket-helper improvements`), the last commit before Audit implementation. Its clean archive contained no Audit package or Claude Audit launcher.

| Item | Value |
|---|---|
| Rollback wheel | `foundry_cli-0.1.0-py3-none-any.whl` |
| Rollback wheel SHA-256 | `5c224a7e512df0950365e904da10c1b6bea53f19816c95bd589dcd1be2ff6fea` |
| Rehearsal window | 2026-08-01 21:33:32-21:33:36 Europe/Sofia |

Rollback procedure and evidence:

1. Force-installed the rollback wheel with `--no-deps` into the isolated candidate environment. Exit 0.
2. Confirmed `foundry_cli.audit` was absent, `foundry-audit.exe` was absent, and the rollback archive had no `.claude/skills/foundry-audit/` launcher.
3. Confirmed retained Datasets, Filesystem, and Ontologies help commands still exited 0.
4. Reinstalled the candidate wheel with `--no-deps`. Exit 0.
5. Confirmed Audit module and entry point returned, `foundry-audit --help` exited 0, and all retained commands still exited 0.

Operational release rollback should install the recorded pre-Audit artifact and restore the matching skill bundle. Source-file deletion is not the rollback mechanism.

## Temporary-file cleanup

At 2026-08-01 21:38:16 Europe/Sofia, cleanup targeted only `T:\tmp\foundry-devops010-87d817c6` after confirming that its resolved path was below `T:\tmp`. Host command policy rejected the recursive removal before execution. The isolated archives, build trees, and virtual environments remain at that exact path (20,656 entries). They contain downloaded public packages and generated test/build artifacts, not credentials or live Foundry data. No broader cleanup was attempted.

## Final status

DEVOPS-010 is READY for completion. Candidate installation and rollback are reproducible. All locally required checks passed, and fresh QA supplies the unavailable local Python 3.12 execution evidence. No external deployment or publication remains part of this task.
