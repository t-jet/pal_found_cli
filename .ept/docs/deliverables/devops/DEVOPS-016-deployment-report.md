# DEVOPS-016 - Foundry Streams packaging and deployment report

## Result

| Field | Value |
|---|---|
| Story | DEV-STORY-016 |
| Task | DEVOPS-016 |
| Result | READY |
| Candidate commit | `0c88063` (feat(sql_queries,streams): add foundry-sql-queries and foundry-streams CLIs (DEV-015/DEV-016)) |
| Rollback commit | `bd13955` (parent of candidate; no sql_queries/streams code) |
| Verification window | 2026-08-10 Europe/Sofia |
| Host | Windows, PowerShell, Python 3.11.9 and Python 3.12.9 (uv-managed) |
| Target | Isolated local package environments only |
| External deployment | Not performed |
| Foundry calls | Not performed |
| Package publication | Not performed |
| Temporary path | `T:\tmp\foundry-devops015-016-20260810` |
| Time spent | 1.0 hours |

Candidate `0c88063` is ready for release as a Python package plus matching Claude skill bundle. Clean-archive build (sdist + wheel per PEP 517), wheel and editable installation, console entry-point smoke tests, packaged metadata policy verification (3 PERMITTED / 12 BLOCKED), Python 3.11/3.12 gates, security gates, and rehearsed rollback all passed. No live credential, Foundry environment, cloud resource, registry, or shared-worktree package was changed.

## Candidate and baseline

The candidate came from a clean `git archive` of commit `0c88063`, which contains both the SQL Queries and Streams namespace implementations (DEV-015/DEV-016 share one commit). The rollback baseline is the parent commit `bd13955`, which has no `streams/` package, no `foundry-streams` entry point, and no corresponding Claude skill directory.

| Archive | Files |
|---|---|
| Candidate `0c88063` | 2,808 |
| Rollback `bd13955` | 2,794 |

Clean candidate and rollback archives contained no `.git` directory and no unrelated files from the dirty shared worktree. DESIGN-016 and TESTCASE-016 supplied the verification contracts; documentation outside the candidate commit was not copied into its package source.

## Build artifacts

Python 3.11.9 built the candidate with `python -m build` in an isolated build environment after upgrading `pip`, `setuptools`, and `wheel`.

| Artifact | Size | SHA-256 | Result |
|---|---:|---|---|
| `foundry_cli-0.1.0-py3-none-any.whl` | 116,146 | `881be17f4d2a40f8b152e9701ae23e3305f830e9e339af08acc1a46334aad57b` | PASS |
| `foundry_cli-0.1.0.tar.gz` | 165,453 | `e112c9fba0811729ae000b542a8b6cdebbbf5323a779aa4aa147392dc8db291c` | PASS |

Twine accepted both artifacts (`PASSED`). Wheel inspection confirmed these required files:

```text
foundry_cli/sql_queries/__init__.py
foundry_cli/sql_queries/metadata-allow-list.md
foundry_cli/sql_queries/scripts/__init__.py
foundry_cli/sql_queries/scripts/foundry_sql_queries_cli.py
foundry_cli/streams/__init__.py
foundry_cli/streams/metadata-allow-list.md
foundry_cli/streams/scripts/__init__.py
foundry_cli/streams/scripts/foundry_streams_cli.py
```

Wheel inspection found no `tests/`, `.claude/`, `.ept/`, `.github/`, `.env`, private-key, or certificate file. The Claude skill remains a separate repository asset, matching the established launcher pattern (DEVOPS-010/011/012/013/014).

## Entry points and policy

Installed wheel metadata exposed the new command and retained every console script from the rollback baseline. All 12 console entry points were present in `entry_points.txt`, including:

```text
foundry-sql-queries = foundry_cli.sql_queries.scripts.foundry_sql_queries_cli:console_main
foundry-streams = foundry_cli.streams.scripts.foundry_streams_cli:console_main
```

The installed Streams policy has exactly 3 `PERMITTED` and 12 `BLOCKED` rows. The installed SQL Queries policy has exactly 1 `PERMITTED` and 4 `BLOCKED` rows. Both match the candidate source byte-for-byte (Compare-Object diff = 0 lines).

## Installation and smoke checks

The wheel used a fresh Python 3.11.9 environment. The editable install used a fresh Python 3.11.9 environment. Both used normal dependency resolution and passed `python -m pip check`. Smoke checks ran from empty directories with `PYTHONPATH` and all inherited `FOUNDRY*` variables unset.

| Check | Wheel | Editable |
|---|---:|---:|
| `foundry-streams --help` | Exit 0 | Exit 0 |
| `foundry-sql-queries --help` | Exit 0 | Exit 0 |
| Streams route help (`stream get --help`) | Exit 0 | Covered |
| SQL Queries route help (`query get-status --help`) | Exit 0 | Covered |
| Retained commands (admin, aip-agents, audit, datasets, filesystem, functions, language-models, models, ontologies, orchestration) | Exit 0 each | Covered |
| Package imports (`foundry_cli.streams`, `foundry_cli.sql_queries`) | PASS | PASS |
| Empty working directory after checks | Yes | Yes |

Package import probes confirmed 15 Streams operations and 5 SQL Queries operations in the OP_SPECS catalogs. The smoke directory contained only the test `.env` file; no `.foundry-data` directory or stray artifacts were created by the CLI itself.

## ACL policy verification (metadata-only tier)

With `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` and a dummy credential `.env`, write operations were blocked before client creation with exit code 8 (AccessControlError):

| Command | Exit | Result |
|---|---:|---|
| `foundry-streams dataset create --name d --parent-folder-rid ri.f --schema-json {}` | 8 | BLOCKED: metadata-only mode active |
| `foundry-sql-queries query cancel <rid>` | 8 | BLOCKED: metadata-only mode active |

PERMITTED metadata operations (`foundry-streams subscriber get-read-position <rid> master sub1` and `foundry-sql-queries query get-status <rid>`) passed the ACL gate and proceeded to network retries (ConnectionError against the dummy hostname, exit 6), proving the allowed paths are not blocked by the policy. Invalid input returned exit 1 (UserInputError). All ACL checks executed from the installed site-packages policy files.

## Quality, compatibility, and security

Checks ran against the clean candidate archive, not the shared worktree. Both interpreters used isolated virtual environments with complete `.[dev]` dependency installation.

| Command | Result |
|---|---|
| Python 3.11.9 full pytest with branch coverage | 1148 passed in 56.60 s; 86.06% (gate >=80% met) |
| Python 3.12.9 full pytest with branch coverage | 1148 passed in 54.40 s; 86.06% (gate >=80% met) |
| Focused streams + sql_queries suites (3.11) | 57 passed in 1.81 s |
| `python -m ruff check src tests .claude/skills/foundry-sql-queries .claude/skills/foundry-streams` | Exit 0; all checks passed |
| `python -m mypy src` | Exit 0; no issues in 51 source files |
| `python -m bandit -r src --severity-level high` | Exit 0; 9,915 lines; zero findings at every severity |
| `python -m safety check --full-report` | Exit 0; zero known vulnerabilities |
| `python -m pip check` | Exit 0 for wheel, editable, and restored candidate |

Namespace branch coverage on 3.11: `foundry_streams_cli.py` 90%, `foundry_sql_queries_cli.py` 89%, both above the 80% gate. Same numbers on Python 3.12.

`ruff check .` is not the project gate. CI defines `ruff check src/ tests/`; this task adds the two new Claude skill directories because they contain the launchers. Running Ruff over `.` would also scan vendored SDK sources and separate tracker/skill tooling under `.ept/`, which are outside this product change.

## Configuration and deployment impact

Relative to rollback baseline, packaging changes add the two console entry points, packaged policy files, namespace-specific Ruff ignores, modules, tests, Claude skills, and shared ACL write-verb changes. They do not change:

- runtime or development dependency declarations;
- `.env.example` or environment-variable names;
- GitHub Actions workflows or release permissions;
- infrastructure, secrets, or secret-store configuration;
- retained console entry-point mappings.

Runtime requirements remain `foundry-platform-sdk>=1.0.0`, `python-dotenv>=1.0.0`, and `requests>=2.31.0`. Live environment validation was intentionally omitted because this task verifies packaging and prohibits external Foundry access.

## Rollback rehearsal

The rollback wheel came from a clean archive of `bd13955`.

| Item | Value |
|---|---|
| Rollback wheel | `foundry_cli-0.1.0-py3-none-any.whl` |
| Size | 102,587 bytes |
| SHA-256 | `2938af68255a73887c7e0ceb4188ea2fc9707346c80cb80cc780dff9ff0336ed` |
| Twine check | PASS |
| Candidate restoration | Verified after rollback |

Rehearsal steps and results:

1. Force-installed the rollback wheel into the isolated candidate environment with `--no-deps`. Exit 0.
2. Confirmed `foundry-streams.exe` and `foundry-sql-queries.exe` were absent, and `foundry_cli.streams` / `foundry_cli.sql_queries` had no import specification.
3. Confirmed all retained commands (audit, datasets, orchestration, and the rest) still returned help with exit 0.
4. Reinstalled the candidate wheel with `--no-deps`. Exit 0.
5. Confirmed `foundry-streams --help` and `foundry-sql-queries --help` returned exit 0, imports of both namespaces succeeded, and `pip check` exited 0.

Operational rollback must install the recorded baseline wheel and restore its matching skill bundle. Candidate recovery must reinstall the recorded candidate wheel and its matching skill directory. Deleting source files is not the rollback procedure.

## Temporary files

Verification archives, build trees, virtual environments, user sites, and artifacts remain under `T:\tmp\foundry-devops015-016-20260810` for reproduction. They contain public dependencies and generated build/test files, not credentials or Foundry data. No broad cleanup was attempted.

## Final status

DEVOPS-016 is READY. Candidate `0c88063` is production-ready for controlled package and Claude skill bundle release. Publication and live deployment remain separate authorized actions. Deployment activates after the parent story DEV-STORY-016 passes QA (TESTEXEC-016).
