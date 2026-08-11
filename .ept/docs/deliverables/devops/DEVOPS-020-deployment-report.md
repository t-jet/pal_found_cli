# DEVOPS-020 - Foundry Data Health packaging and deployment report

## Result

| Field | Value |
|---|---|
| Story | DEV-STORY-020 |
| Task | DEVOPS-020 |
| Result | READY |
| Candidate commit | `f63a12c` (feat(checkpoints,data_health) `b0df380` + fix(checkpoints,data_health) CODEREVIEW-019/020 `f63a12c`) |
| Rollback commit | `d1f1ff6` (intermediary commit, parent of candidate; no checkpoints/data_health code) |
| Verification window | 2026-08-10 Europe/Sofia |
| Host | Windows, PowerShell, Python 3.11.9 and Python 3.12.0 |
| Target | Isolated local package environments only |
| External deployment | Not performed |
| Foundry calls | Not performed |
| Package publication | Not performed |
| Temporary path | `T:\tmp\foundry-devops019-020-20260810` |
| Time spent | 1.0 hours |

Candidate `f63a12c` is ready for release as a Python package plus matching Claude skill bundle. Clean-archive build (sdist + wheel per PEP 517), wheel and editable installation, console entry-point smoke tests, packaged metadata policy verification (3 PERMITTED / 3 BLOCKED for data-health), Python 3.11/3.12 gates, security gates, and rehearsed rollback all passed. No live credential, Foundry environment, cloud resource, registry, or shared-worktree package was changed.

## Candidate and baseline

The candidate came from a clean `git archive` of commit `f63a12c`, which contains both the Checkpoints and Data Health namespace implementations (DEV-019/DEV-020 share base commit `b0df380`) plus the CODEREVIEW-019/020 corrective fix committing the Claude skills and thin launchers and `--limit` validation. The rollback baseline is the parent commit `d1f1ff6`, which has no `data_health/` package, no `foundry-data-health` entry point, and no corresponding Claude skill directory.

| Archive | Files |
|---|---|
| Candidate `f63a12c` | 3,476 |
| Rollback `d1f1ff6` | 3,460 |

Clean candidate and rollback archives contained no `.git` directory and no unrelated files from the dirty shared worktree. DESIGN-020 and TESTCASE-020 supplied the verification contracts; documentation outside the candidate commit was not copied into its package source.

## Build artifacts

Python 3.11.9 built the candidate with `python -m build` in an isolated build environment after upgrading `pip`, `setuptools`, and `wheel`.

| Artifact | Size | SHA-256 | Result |
|---|---:|---|---|
| `foundry_cli-0.1.0-py3-none-any.whl` | 143,828 | `2AF7EC5B9A16A522F2F3DE49F4730F59B6E884789BD9145874B7BDCD9FB0B132` | PASS |
| `foundry_cli-0.1.0.tar.gz` | 200,152 | `D68744479938D5FB2B21D33F6133F340D46E6597C037A109867416551A170EE0` | PASS |

Twine accepted both artifacts (`PASSED`). Wheel inspection confirmed these required files:

```text
foundry_cli/checkpoints/__init__.py
foundry_cli/checkpoints/metadata-allow-list.md
foundry_cli/checkpoints/scripts/__init__.py
foundry_cli/checkpoints/scripts/foundry_checkpoints_cli.py
foundry_cli/data_health/__init__.py
foundry_cli/data_health/metadata-allow-list.md
foundry_cli/data_health/scripts/__init__.py
foundry_cli/data_health/scripts/foundry_data_health_cli.py
```

Wheel inspection found no `tests/`, `.claude/`, `.ept/`, `.github/`, `.env`, private-key, or certificate file. The Claude skill remains a separate repository asset, matching the established launcher pattern (DEVOPS-010/011/012/013/014/015/016/017/018).

## Entry points and policy

Installed wheel metadata exposed the two new commands and retained every console script from the rollback baseline. All 16 console entry points were present in `entry_points.txt`, including:

```text
foundry-checkpoints = foundry_cli.checkpoints.scripts.foundry_checkpoints_cli:console_main
foundry-data-health = foundry_cli.data_health.scripts.foundry_data_health_cli:console_main
```

The installed Checkpoints policy has exactly 3 `PERMITTED` and 0 `BLOCKED` rows. The installed Data Health policy has exactly 3 `PERMITTED` and 3 `BLOCKED` rows. Both match the candidate source byte-for-byte (installed=302B vs src=302B identical=True for checkpoints; 518B identical=True for data_health).

## Installation and smoke checks

The wheel used a fresh Python 3.11.9 environment. The editable install used a fresh Python 3.11.9 environment. Both used normal dependency resolution and passed `python -m pip check`. Smoke checks ran from empty directories with `PYTHONPATH` and all inherited `FOUNDRY*` variables unset.

| Check | Wheel | Editable |
|---|---:|---:|
| `foundry-checkpoints --help` | Exit 0 | Exit 0 |
| `foundry-data-health --help` | Exit 0 | Exit 0 |
| Checkpoints route help (`record --help`, `record search --help`) | Exit 0 | Covered |
| Data Health route help (`check --help`, `check-report get-latest --help`) | Exit 0 | Covered |
| Retained commands (admin, aip-agents, audit, connectivity, datasets, filesystem, functions, language-models, media-sets, models, ontologies, orchestration, sql-queries, streams) | Exit 0 each | Covered |
| Package imports (`foundry_cli.checkpoints`, `foundry_cli.data_health`) | PASS | PASS |
| Empty working directory after checks | Yes | Yes |

Package import probes confirmed 3 Checkpoints operations and 6 Data Health operations in the OP_SPECS catalogs, with `record search` the only paginated operation. The smoke directory contained only the test `.env` file during ACL checks; no `.foundry-data` directory or stray artifacts were created by the CLI itself.

## ACL policy verification (metadata-only tier)

With `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` and a dummy credential `.env`, write operations were blocked before client creation with exit code 8 (AccessControlError):

| Command | Exit | Result |
|---|---:|---|
| `foundry-data-health check create --config-json {jobStatus config}` | 8 | BLOCKED: metadata-only mode active |
| `foundry-data-health check replace <rid> --config-json {jobStatus config}` | 8 | BLOCKED: metadata-only mode active |
| `foundry-data-health check delete <rid>` | 8 | BLOCKED: metadata-only mode active |

PERMITTED metadata operations (`foundry-data-health check get <rid>`, `check-report get-latest <rid> --limit 5`, `foundry-checkpoints record get <rid>`, and `record search --where-json {"filter":{"type":"eq","field":"recordRid","value":...}}`) passed the ACL gate and proceeded to network retries (ConnectionError against the dummy hostname, exit 6), proving the allowed paths are not blocked by the policy. All ACL checks executed from the installed site-packages policy files.

## Quality, compatibility, and security

Checks ran against the clean candidate archive, not the shared worktree. Both interpreters used isolated virtual environments with complete `.[dev]` dependency installation.

| Command | Result |
|---|---|
| Python 3.11.9 full pytest with branch coverage | 1276 passed in 54.14 s; 86.55% (gate >=80% met) |
| Python 3.12.0 full pytest with branch coverage | 1276 passed in 44.19 s; 86.55% (gate >=80% met) |
| Focused checkpoints + data_health + ACL suites (3.11) | 131 passed in 0.58 s |
| Namespace branch coverage (3.11) | checkpoints 88%, data_health 90% (both above 80%) |
| `python -m ruff check src tests .claude/skills/foundry-checkpoints .claude/skills/foundry-data-health` | Exit 0; all checks passed |
| `python -m mypy src` | Exit 0; no issues in 63 source files |
| `python -m bandit -r src --severity-level high` | Exit 0; zero findings at every severity |
| `python -m safety check --full-report` | Exit 0; zero known vulnerabilities |
| `python -m pip check` | Exit 0 for wheel, editable, and restored candidate |

`ruff check .` is not the project gate. CI defines `ruff check src/ tests/`; this task adds the two new Claude skill directories because they contain the launchers. Running Ruff over `.` would also scan vendored SDK sources and separate tracker/skill tooling under `.ept/`, which are outside this product change.

## Configuration and deployment impact

Relative to rollback baseline, packaging changes add the two console entry points, packaged policy files, namespace-specific Ruff ignores, modules, tests, Claude skills, and shared ACL write-verb additions. They do not change:

- runtime or development dependency declarations;
- `.env.example` or environment-variable names;
- GitHub Actions workflows or release permissions;
- infrastructure, secrets, or secret-store configuration;
- retained console entry-point mappings.

Runtime requirements remain `foundry-platform-sdk>=1.0.0`, `python-dotenv>=1.0.0`, and `requests>=2.31.0`. Live environment validation was intentionally omitted because this task verifies packaging and prohibits external Foundry access.

## Rollback rehearsal

The rollback wheel came from a clean archive of `d1f1ff6`.

| Item | Value |
|---|---|
| Rollback wheel | `foundry_cli-0.1.0-py3-none-any.whl` |
| Size | 131,238 bytes |
| SHA-256 | `41AC0F356E383D896DB1513E6A4F1840D113B1A5C34EDDF564D97DD19637CB76` |
| Twine check | PASS |
| Candidate restoration | Verified after rollback |

Rehearsal steps and results:

1. Force-installed the candidate wheel into the isolated rollback environment. Exit 0; 16 launchers present.
2. Force-installed the rollback wheel into the same environment with `--no-deps`. Exit 0.
3. Confirmed `foundry-checkpoints.exe` and `foundry-data-health.exe` were absent, and `foundry_cli.checkpoints` / `foundry_cli.data_health` had no import specification.
4. Confirmed all retained commands (datasets, streams, admin) still returned help with exit 0.
5. Reinstalled the candidate wheel with `--no-deps`. Exit 0.
6. Confirmed `foundry-checkpoints --help` and `foundry-data-health --help` returned exit 0, imports of both namespaces succeeded, and `pip check` exited 0.

Operational rollback must install the recorded baseline wheel and restore its matching skill bundle. Candidate recovery must reinstall the recorded candidate wheel and its matching skill directory. Deleting source files is not the rollback procedure.

## Temporary files

Verification archives, build trees, virtual environments, user sites, and artifacts remain under `T:\tmp\foundry-devops019-020-20260810` for reproduction. They contain public dependencies and generated build/test files, not credentials or Foundry data. No broad cleanup was attempted.

## Final status

DEVOPS-020 is READY. Candidate `f63a12c` is production-ready for controlled package and Claude skill bundle release. Publication and live deployment remain separate authorized actions. Deployment activates after the parent story DEV-STORY-020 passes QA (TESTEXEC-020).
