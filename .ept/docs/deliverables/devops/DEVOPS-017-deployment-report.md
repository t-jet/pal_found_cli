# DEVOPS-017 - Foundry Connectivity packaging and deployment report

## Result

| Field | Value |
|---|---|
| Story | DEV-STORY-017 |
| Task | DEVOPS-017 |
| Result | READY |
| Candidate commit | `063f72d` (feat(connectivity,media_sets) `62c269f` + fix(connectivity) CODEREVIEW-017 P1 fix `063f72d`) |
| Rollback commit | `c548c1b` (parent of candidate; no connectivity/media_sets code) |
| Verification window | 2026-08-10 Europe/Sofia |
| Host | Windows, PowerShell, Python 3.11.9 and Python 3.12.0 |
| Target | Isolated local package environments only |
| External deployment | Not performed |
| Foundry calls | Not performed |
| Package publication | Not performed |
| Temporary path | `T:\tmp\foundry-devops017-018-20260810` |
| Time spent | 1.0 hours |

Candidate `063f72d` is ready for release as a Python package plus matching Claude skill bundle. Clean-archive build (sdist + wheel per PEP 517), wheel and editable installation, console entry-point smoke tests, packaged metadata policy verification (7 PERMITTED / 13 BLOCKED), Python 3.11/3.12 gates, security gates, and rehearsed rollback all passed. No live credential, Foundry environment, cloud resource, registry, or shared-worktree package was changed.

## Candidate and baseline

The candidate came from a clean `git archive` of commit `063f72d`, which contains both the Connectivity and Media Sets namespace implementations (DEV-017/DEV-018 share base commit `62c269f`) plus the CODEREVIEW-017 P1 corrective fix committing the `file_import_filters` keyword dispatch. The rollback baseline is the parent commit `c548c1b`, which has no `connectivity/` package, no `foundry-connectivity` entry point, and no corresponding Claude skill directory.

| Archive | Files |
|---|---|
| Candidate `063f72d` | 3,234 |
| Rollback `c548c1b` | 3,220 |

Clean candidate and rollback archives contained no `.git` directory and no unrelated files from the dirty shared worktree. DESIGN-017 and TESTCASE-017 supplied the verification contracts; documentation outside the candidate commit was not copied into its package source.

## Build artifacts

Python 3.11.9 built the candidate with `python -m build` in an isolated build environment after upgrading `pip`, `setuptools`, and `wheel`.

| Artifact | Size | SHA-256 | Result |
|---|---:|---|---|
| `foundry_cli-0.1.0-py3-none-any.whl` | 131,238 | `C42AF5FC09A1DEEF6D85151D68A2169504E88CEDB70C6FEFBCAD75AA4E3ABFC2` | PASS |
| `foundry_cli-0.1.0.tar.gz` | 188,341 | `D8A15EFA631C74E7668A419CEE04926CC6CBAF961152B6CC3800E0F0AAEF18A9` | PASS |

Twine accepted both artifacts (`PASSED`). Wheel inspection confirmed these required files:

```text
foundry_cli/connectivity/__init__.py
foundry_cli/connectivity/metadata-allow-list.md
foundry_cli/connectivity/scripts/__init__.py
foundry_cli/connectivity/scripts/foundry_connectivity_cli.py
foundry_cli/media_sets/__init__.py
foundry_cli/media_sets/metadata-allow-list.md
foundry_cli/media_sets/scripts/__init__.py
foundry_cli/media_sets/scripts/foundry_media_sets_cli.py
```

Wheel inspection found no `tests/`, `.claude/`, `.ept/`, `.github/`, `.env`, private-key, or certificate file. The Claude skill remains a separate repository asset, matching the established launcher pattern (DEVOPS-010/011/012/013/014/015/016).

## Entry points and policy

Installed wheel metadata exposed the new command and retained every console script from the rollback baseline. All 14 console entry points were present in `entry_points.txt`, including:

```text
foundry-connectivity = foundry_cli.connectivity.scripts.foundry_connectivity_cli:console_main
foundry-media-sets = foundry_cli.media_sets.scripts.foundry_media_sets_cli:console_main
```

The installed Connectivity policy has exactly 7 `PERMITTED` and 13 `BLOCKED` rows. The installed Media Sets policy has exactly 5 `PERMITTED` and 14 `BLOCKED` rows. Both match the candidate source byte-for-byte (installed=1,702B vs src=1,702B identical=True for connectivity; 1,498B identical=True for media_sets).

## Installation and smoke checks

The wheel used a fresh Python 3.11.9 environment. The editable install used a fresh Python 3.11.9 environment. Both used normal dependency resolution and passed `python -m pip check`. Smoke checks ran from empty directories with `PYTHONPATH` and all inherited `FOUNDRY*` variables unset.

| Check | Wheel | Editable |
|---|---:|---:|
| `foundry-connectivity --help` | Exit 0 | Exit 0 |
| `foundry-media-sets --help` | Exit 0 | Exit 0 |
| Connectivity route help (`file-import get --help`, `connection get-configuration-batch --help`) | Exit 0 | Covered |
| Media Sets route help (`media-set get --help`, `media-set transform --help`) | Exit 0 | Covered |
| Retained commands (admin, aip-agents, audit, datasets, filesystem, functions, language-models, models, ontologies, orchestration, sql-queries, streams) | Exit 0 each | Covered |
| Package imports (`foundry_cli.connectivity`, `foundry_cli.media_sets`) | PASS | PASS |
| Empty working directory after checks | Yes | Yes |

Package import probes confirmed 20 Connectivity operations and 19 Media Sets operations in the OP_SPECS catalogs. The smoke directory contained only the test `.env` file during ACL checks; no `.foundry-data` directory or stray artifacts were created by the CLI itself.

## ACL policy verification (metadata-only tier)

With `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` and a dummy credential `.env`, write operations were blocked before client creation with exit code 8 (AccessControlError):

| Command | Exit | Result |
|---|---:|---|
| `foundry-connectivity file-import create ri.conn --dataset-rid ri.dataset --display-name imp --filters-json [...] --import-mode SNAPSHOT` | 8 | BLOCKED: metadata-only mode active |
| `foundry-media-sets media-set create ri.media` | 8 | BLOCKED: metadata-only mode active |

PERMITTED metadata operations (`foundry-connectivity connection get ri.connection.main.connection.12345` and `foundry-media-sets media-set get ri.media-set.main.media-set.12345`) passed the ACL gate and proceeded to network retries (ConnectionError against the dummy hostname, exit 6), proving the allowed paths are not blocked by the policy. Invalid RIDs returned exit 1 (UserInputError). All ACL checks executed from the installed site-packages policy files.

## Quality, compatibility, and security

Checks ran against the clean candidate archive, not the shared worktree. Both interpreters used isolated virtual environments with complete `.[dev]` dependency installation.

| Command | Result |
|---|---|
| Python 3.11.9 full pytest with branch coverage | 1215 passed in 53.80 s; 86.27% (gate >=80% met) |
| Python 3.12.0 full pytest with branch coverage | 1215 passed in 49.46 s; 86.27% (gate >=80% met) |
| Focused connectivity + media_sets + ACL suites (3.11) | 141 passed in 1.86 s |
| Namespace branch coverage (3.11) | connectivity 88%, media_sets 87% (both above 80%) |
| `python -m ruff check src tests .claude/skills/foundry-connectivity .claude/skills/foundry-media-sets` | Exit 0; all checks passed |
| `python -m mypy src` | Exit 0; no issues in 57 source files |
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

The rollback wheel came from a clean archive of `c548c1b`.

| Item | Value |
|---|---|
| Rollback wheel | `foundry_cli-0.1.0-py3-none-any.whl` |
| Size | 126,376 bytes |
| SHA-256 | `110D5446F6A9EE300F19D07E36DBB3D742DEDD043BE9CF52DF52AB763178094B` |
| Twine check | PASS |
| Candidate restoration | Verified after rollback |

Rehearsal steps and results:

1. Force-installed the rollback wheel into the isolated candidate environment with `--no-deps`. Exit 0.
2. Confirmed `foundry-connectivity.exe` and `foundry-media-sets.exe` were absent, and `foundry_cli.connectivity` / `foundry_cli.media_sets` had no import specification.
3. Confirmed all retained commands (datasets, streams, and the rest) still returned help with exit 0.
4. Reinstalled the candidate wheel with `--no-deps`. Exit 0.
5. Confirmed `foundry-connectivity --help` and `foundry-media-sets --help` returned exit 0, imports of both namespaces succeeded, and `pip check` exited 0.

Operational rollback must install the recorded baseline wheel and restore its matching skill bundle. Candidate recovery must reinstall the recorded candidate wheel and its matching skill directory. Deleting source files is not the rollback procedure.

## Temporary files

Verification archives, build trees, virtual environments, user sites, and artifacts remain under `T:\tmp\foundry-devops017-018-20260810` for reproduction. They contain public dependencies and generated build/test files, not credentials or Foundry data. No broad cleanup was attempted.

## Final status

DEVOPS-017 is READY. Candidate `063f72d` is production-ready for controlled package and Claude skill bundle release. Publication and live deployment remain separate authorized actions. Deployment activates after the parent story DEV-STORY-017 passes QA (TESTEXEC-017).
