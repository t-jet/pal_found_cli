# DEVOPS-021 - Foundry Third-Party Applications packaging and deployment report

## Result

| Field | Value |
|---|---|
| Story | DEV-STORY-021 |
| Task | DEVOPS-021 |
| Result | READY |
| Candidate commit | `1b15565` (feat(third_party_applications) `74094bc` + feat(widgets) `1b15565`) |
| Rollback commit | `f63a12c` (parent of `74094bc`; no third_party_applications code) |
| Verification window | 2026-08-11 Europe/Sofia |
| Host | Windows, PowerShell, Python 3.11.9 and Python 3.12.0 |
| Target | Isolated local package environments only |
| External deployment | Not performed |
| Foundry calls | Not performed |
| Package publication | Not performed |
| Temporary path | `T:\tmp\foundry-devops021-022-20260811` |
| Time spent | 1.0 hours |

Candidate `1b15565` is ready for release as a Python package plus matching Claude skill bundle. Clean-archive build (sdist + wheel per PEP 517), wheel and editable installation, console entry-point smoke tests, packaged metadata policy verification (4 PERMITTED / 5 BLOCKED for third-party-applications), Python 3.11/3.12 gates, security gates, and rehearsed rollback all passed. No live credential, Foundry environment, cloud resource, registry, or shared-worktree package was changed.

## Candidate and baseline

The candidate came from a clean `git archive` of commit `1b15565`, which contains both the Third-Party Applications (`74094bc`) and Widgets (`1b15565`) namespace implementations. The rollback baseline is the parent commit `f63a12c`, which has no `third_party_applications/` package, no `foundry-third-party-applications` entry point, and no corresponding Claude skill directory.

| Archive | Files |
|---|---|
| Candidate `1b15565` | 3,557 |
| Rollback `f63a12c` | 3,476 |

Clean candidate and rollback archives contained no `.git` directory and no unrelated files from the dirty shared worktree. DESIGN-021 and TESTCASE-021 supplied the verification contracts; documentation outside the candidate commit was not copied into its package source.

## Build artifacts

Python 3.11.9 built the candidate with `python -m build` in an isolated build environment after upgrading `pip`, `setuptools`, and `wheel`.

| Artifact | Size | SHA-256 | Result |
|---|---:|---|---|
| `foundry_cli-0.1.0-py3-none-any.whl` | 158,410 | `82CFA1BE50F8443CA6EDBF71DCE6454D521B718FE49924A4B2E1EC6F5ABD8DC7` | PASS |
| `foundry_cli-0.1.0.tar.gz` | 214,374 | `B7E9E4EB51C4E9E01B8C2308CBF5E2F9CC5AC29FBB7E6C4202D74A4AAB27BE7B` | PASS |

Twine accepted both artifacts (`PASSED`). Wheel inspection confirmed these required files:

```text
foundry_cli/third_party_applications/__init__.py
foundry_cli/third_party_applications/metadata-allow-list.md
foundry_cli/third_party_applications/scripts/__init__.py
foundry_cli/third_party_applications/scripts/foundry_third_party_applications_cli.py
```

Wheel inspection found no `tests/`, `.claude/`, `.ept/`, `.github/`, `.env`, private-key, or certificate file. The Claude skill remains a separate repository asset, matching the established launcher pattern (DEVOPS-010/011/012/013/014/015/016/017/018/019/020).

## Entry points and policy

Installed wheel metadata exposed the two new commands and retained every console script from the rollback baseline. All 18 `foundry-*` console entry points were present in `entry_points.txt`, including:

```text
foundry-third-party-applications = foundry_cli.third_party_applications.scripts.foundry_third_party_applications_cli:console_main
foundry-widgets = foundry_cli.widgets.scripts.foundry_widgets_cli:console_main
```

The installed Third-Party Applications policy has exactly 4 `PERMITTED` and 5 `BLOCKED` rows. It matches the candidate source byte-for-byte (installed=901B vs src=901B identical=True).

## Installation and smoke checks

The wheel used a fresh Python 3.11.9 environment. The editable install used a fresh Python 3.11.9 environment. Both used normal dependency resolution and passed `python -m pip check`. Smoke checks ran from empty directories with `PYTHONPATH` and all inherited `FOUNDRY*` variables unset.

| Check | Wheel | Editable |
|---|---:|---:|
| `foundry-third-party-applications --help` | Exit 0 | Exit 0 |
| `foundry-widgets --help` | Exit 0 | Covered |
| Third-Party Applications route help (`version --help`, `version list --help`) | Exit 0 | Covered |
| Widgets route help (`release --help`, `dev-mode-settings set-widget-set-by-id --help`) | Exit 0 | Covered |
| Retained commands (admin, aip-agents, audit, checkpoints, connectivity, data-health, datasets, filesystem, functions, language-models, media-sets, models, ontologies, orchestration, sql-queries, streams) | Exit 0 each | Covered |
| Package imports (`foundry_cli.third_party_applications`) | PASS | PASS |
| Empty working directory after checks | Yes | Yes |

Package import probes confirmed 9 Third-Party Applications operations in the OP_SPECS catalog, with `version list` the only paginated operation. The smoke directory contained only the probe `.env` file during ACL checks; no `.foundry-data` directory or stray artifacts were created by the CLI itself.

## ACL policy verification (metadata-only tier)

With `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` and a dummy credential `.env`, write operations were blocked before client creation with exit code 8 (AccessControlError):

| Command | Exit | Result |
|---|---:|---|
| `foundry-third-party-applications website deploy <rid> --version 1.0` | 8 | BLOCKED: metadata-only mode active |
| `foundry-third-party-applications website undeploy <rid>` | 8 | BLOCKED: metadata-only mode active |
| `foundry-third-party-applications version delete <rid> <rid>` | 8 | BLOCKED: metadata-only mode active |
| `foundry-third-party-applications version upload <rid> --file dummy.zip --version 1.0` | 8 | BLOCKED: metadata-only mode active |
| `foundry-third-party-applications version upload-snapshot <rid> --version 1.0 --file dummy.zip --snapshot-identifier s1` | 8 | BLOCKED: metadata-only mode active |

PERMITTED metadata operations (`third-party-application get`, `website get`, `version get` with SDK-valid RIDs) passed the ACL gate and proceeded to network retries (ConnectionError against the dummy hostname, exit 6), proving the allowed paths are not blocked by the policy. All ACL checks executed from the installed site-packages policy file.

## Quality, compatibility, and security

Checks ran against the clean candidate archive, not the shared worktree. Both interpreters used isolated virtual environments with complete `.[dev]` dependency installation.

| Command | Result |
|---|---|
| Python 3.11.9 full pytest with branch coverage | 1362 passed in 54.01 s; 86.53% (gate >=80% met) |
| Python 3.12.0 full pytest with branch coverage | 1362 passed in 49.08 s; 86.53% (gate >=80% met) |
| Namespace branch coverage (3.11) | third_party_applications 87%, widgets 85% (both above 80%) |
| `python -m ruff check src tests .claude/skills/foundry-third-party-applications .claude/skills/foundry-widgets` | Exit 0; all checks passed |
| `python -m mypy src` | Exit 0; no issues in 69 source files |
| `python -m bandit -r src --severity-level high` | Exit 0; zero findings at every severity |
| `python -m safety check --full-report` | Exit 0; 87 packages scanned, zero known vulnerabilities |
| `python -m pip check` | Exit 0 for wheel, editable, and restored candidate |
| Hardcoded-secret scan (`src/`) | 0 hits |

`ruff check .` is not the project gate. CI defines `ruff check src/ tests/`; this task adds the two new Claude skill directories because they contain the launchers. Running Ruff over `.` would also scan vendored SDK sources and separate tracker/skill tooling under `.ept/`, which are outside this product change.

## Configuration and deployment impact

Relative to rollback baseline, packaging changes add the two console entry points, packaged policy files, namespace-specific Ruff ignores, modules, tests, Claude skills, and shared ACL write-verb additions. They do not change:

- runtime or development dependency declarations;
- `.env.example` or environment-variable names (byte-identical candidate vs baseline);
- GitHub Actions workflows or release permissions;
- infrastructure, secrets, or secret-store configuration;
- retained console entry-point mappings.

Runtime requirements remain `foundry-platform-sdk>=1.0.0`, `python-dotenv>=1.0.0`, and `requests>=2.31.0`. Live environment validation was intentionally omitted because this task verifies packaging and prohibits external Foundry access.

## Rollback rehearsal

The rollback wheel came from a clean archive of `f63a12c`.

| Item | Value |
|---|---|
| Rollback wheel | `foundry_cli-0.1.0-py3-none-any.whl` |
| Size | 143,828 bytes |
| SHA-256 | `5F5DF418DED4C7459AB42958C3A729CE7889EBCFBB1F2D10A2747BAE50FD80EC` |
| Twine check | PASS |
| Candidate restoration | Verified after rollback |

Rehearsal steps and results:

1. Force-installed the candidate wheel into the isolated rollback environment. Exit 0; 18 launchers present.
2. Force-installed the rollback wheel into the same environment with `--no-deps`. Exit 0.
3. Confirmed `foundry-third-party-applications.exe` and `foundry-widgets.exe` were absent, and launcher count returned to 16 (baseline surface).
4. Confirmed all retained commands (admin, datasets, streams, models) still returned help with exit 0.
5. Reinstalled the candidate wheel with `--no-deps`. Exit 0.
6. Confirmed `foundry-third-party-applications --help` and `foundry-widgets --help` returned exit 0, imports of both namespaces succeeded, and `pip check` exited 0.

Operational rollback must install the recorded baseline wheel and restore its matching skill bundle. Candidate recovery must reinstall the recorded candidate wheel and its matching skill directory. Deleting source files is not the rollback procedure.

## Temporary files

Verification archives, build trees, virtual environments, user sites, and artifacts remain under `T:\tmp\foundry-devops021-022-20260811` for reproduction. They contain public dependencies and generated build/test files, not credentials or Foundry data. No broad cleanup was attempted.

## Final status

DEVOPS-021 is READY. Candidate `1b15565` is production-ready for controlled package and Claude skill bundle release. Publication and live deployment remain separate authorized actions. Deployment activates after the parent story DEV-STORY-021 passes QA (TESTEXEC-021).
