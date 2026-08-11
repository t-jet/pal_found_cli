# DEVOPS-023 - Foundry Knowledge Skill packaging and deployment report

## Result

| Field | Value |
|---|---|
| Story | DEV-STORY-023 |
| Task | DEVOPS-023 |
| Result | READY |
| Candidate commit | `a4d48ab` (docs(foundry): add foundry/ knowledge skill, 8 sections per DESIGN-023) |
| Rollback commit | `1b15565` (parent of `a4d48ab`; no `.claude/skills/foundry/`) |
| Verification window | 2026-08-11 Europe/Sofia |
| Host | Windows, PowerShell, Python 3.11.9 and Python 3.12.0 |
| Target | Isolated local package environments only |
| External deployment | Not performed |
| Foundry calls | Not performed |
| Package publication | Not performed |
| Temporary path | `T:\tmp\foundry-devops023-20260811` |
| Time spent | 1.0 hours |

Candidate `a4d48ab` is ready for release. This is a documentation-only story: the deliverable is the static markdown knowledge skill `.claude/skills/foundry/SKILL.md` (18,919 bytes, 218 lines, 8 sections). Clean-archive build (sdist + wheel per PEP 517), wheel and editable installation, all 18 console entry-point smoke tests, packaged metadata policy verification (13 allow-lists), Python 3.11/3.12 gates, security gates, and rehearsed rollback all passed. No code changed, so the built wheel is byte-identical to the previous release and the 18 `foundry-*` entry points are unchanged. No live credential, Foundry environment, cloud resource, registry, or shared-worktree package was changed.

## Candidate and baseline

The candidate came from a clean `git archive` of commit `a4d48ab`, the DEV-023/UNITTEST-023 knowledge skill commit. The rollback baseline is the parent commit `1b15565`, which has no `.claude/skills/foundry/` directory.

| Archive | Files |
|---|---|
| Candidate `a4d48ab` | 3,494 |
| Rollback `1b15565` | 3,493 |

The only tracked-content difference between the archives is the skill folder (one file: `.claude/skills/foundry/SKILL.md`, mode 100644, not executable). `pyproject.toml` is byte-identical between candidate and baseline (zero diff). Clean archives contained no `.git` directory and no unrelated files from the dirty shared worktree.

## Skill deliverable checks

| Check | Result |
|---|---|
| Skill tracked in candidate commit | PASS (`git ls-tree a4d48ab` shows `.claude/skills/foundry/SKILL.md`) |
| Skill folder contains executable scripts | NONE (single markdown file, mode 100644) |
| Skill registered in `.ept/docs/document_index.md` | PASS (knowledge skill entry present) |
| No pyproject.toml changes required | CONFIRMED (documentation-only story) |
| Skill in editable install source tree | PASS (editable install points at candidate, skill present) |

## Build artifacts

Python 3.11.9 built the candidate with `python -m build` in an isolated build environment.

| Artifact | Size | SHA-256 | Result |
|---|---:|---|---|
| `foundry_cli-0.1.0-py3-none-any.whl` | 158,410 | `F90F9CE4AF79B970C4B0A460CFFCE7CC1EF3AD594E7844C356CF7F5BAFE9ABE6` | PASS |
| `foundry_cli-0.1.0.tar.gz` | 214,319 | `88BB6ED48DE564E877B3D8187F02BC7481AA5A9F6D9E69011BAABB4056C090D5` | PASS |

Twine accepted both artifacts (`PASSED`). The wheel contains only `foundry_cli/` and `foundry_cli-0.1.0.dist-info/`; no `tests/`, `.claude/`, `.ept/`, `.github/`, or `.env` file leaked into either artifact. The skill stays a separate repository asset, matching the established pattern (DEVOPS-010..022).

The candidate wheel and the rollback baseline wheel have identical member lists and identical bytes for every shared member (0 differing members). The skill change therefore adds nothing to the installed package, which is the expected outcome for a documentation-only release.

## Entry points and policy

Installed wheel metadata exposes the same 18 `foundry-*` console entry points as the previous release; no entry point was added, removed, or remapped:

```text
foundry-admin, foundry-aip-agents, foundry-audit, foundry-checkpoints,
foundry-connectivity, foundry-data-health, foundry-datasets, foundry-filesystem,
foundry-functions, foundry-language-models, foundry-media-sets, foundry-models,
foundry-ontologies, foundry-orchestration, foundry-sql-queries, foundry-streams,
foundry-third-party-applications, foundry-widgets
```

All 13 packaged metadata allow-lists are byte-identical to their source files (audit 123 B, aip_agents 1134 B, language_models 255 B, models 1815 B, orchestration 1466 B, sql_queries 505 B, streams 1162 B, connectivity 1702 B, media_sets 1498 B, checkpoints 302 B, data_health 518 B, third_party_applications 901 B, widgets 708 B; 0 diffs).

## Installation and smoke checks

The wheel used a fresh Python 3.11.9 environment. The editable install used a fresh Python 3.11.9 environment. Both passed `python -m pip check`. Smoke checks ran from an empty working directory with `PYTHONPATH` and all inherited `FOUNDRY*` variables unset.

| Check | Wheel | Editable |
|---|---:|---:|
| All 18 `foundry-* --help` | Exit 0 each | Covered (4 spot-checked) |
| Package imports (`foundry_cli.widgets`, `.datasets`, `.third_party_applications`) | PASS | PASS |
| `pip check` | Exit 0 | Exit 0 |
| Empty working directory after checks | Yes | Yes |

## ACL policy spot check (metadata-only tier)

With `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` and a dummy credential `.env`, write operations on the installed wheel were blocked before client creation with exit code 8 (AccessControlError):

| Command | Exit | Result |
|---|---:|---|
| `foundry-widgets dev-mode-settings enable` | 8 | BLOCKED: metadata-only mode active |
| `foundry-widgets release delete <rid> <rid>` | 8 | BLOCKED: metadata-only mode active |

The policy gate is active in the installed package. Because the wheel is byte-identical to the previous release, ACL behavior across all namespaces is unchanged from the DEVOPS-022 verification.

## Quality, compatibility, and security

Checks ran against the clean candidate archive, not the shared worktree. Both interpreters used isolated virtual environments with complete `.[dev]` dependency installation.

| Command | Result |
|---|---|
| Python 3.11.9 full pytest with branch coverage | 1362 passed in 57.53 s; 86.53% (gate >=80% met) |
| Python 3.12.0 full pytest with branch coverage | 1362 passed in 50.14 s; 86.53% (gate >=80% met) |
| `python -m ruff check src tests .claude/skills/foundry` | Exit 0; all checks passed |
| `python -m mypy src` | Exit 0; no issues in 69 source files |
| `python -m bandit -r src --severity-level high` | Exit 0; zero findings at every severity |
| `python -m safety check --full-report` | Exit 0; 69 packages scanned after tooling bootstrap, zero known vulnerabilities |
| `python -m pip check` | Exit 0 for wheel, editable, and restored candidate |
| Hardcoded-secret scan (`src/`) | 0 hits |

The safety scan reports 9 findings only when run against a stale bootstrap `setuptools 65.5.0` in a fresh venv. After applying the CI bootstrap order (upgrade `pip`, `setuptools`, `wheel` first), the scan is clean. These findings are tooling artifacts, not project dependencies.

`.env.example` is byte-identical between candidate and baseline.

## Configuration and deployment impact

Relative to rollback baseline, the candidate adds one file (`.claude/skills/foundry/SKILL.md`) and the document_index entry. It does not change:

- console entry points, runtime or development dependency declarations;
- packaged metadata policies;
- `.env.example` or environment-variable names;
- GitHub Actions workflows or release permissions;
- infrastructure, secrets, or secret-store configuration.

Runtime requirements remain `foundry-platform-sdk>=1.0.0`, `python-dotenv>=1.0.0`, and `requests>=2.31.0`. Live environment validation was intentionally omitted because this task verifies packaging and prohibits external Foundry access.

## Rollback rehearsal

The rollback wheel came from a clean archive of `1b15565`.

| Item | Value |
|---|---|
| Rollback wheel | `foundry_cli-0.1.0-py3-none-any.whl` |
| Size | 158,410 bytes |
| SHA-256 | `9688C4B9B0D854D3A550BA7C2407519BA130CE7EE91E743AA9C617175632600C` |
| Twine check | PASS |
| Candidate restoration | Verified after rollback |

Rehearsal steps and results:

1. Force-installed the candidate wheel into the isolated rollback environment. Exit 0; 18 launchers present.
2. Force-installed the rollback wheel into the same environment with `--no-deps`. Exit 0; 18 launchers retained.
3. Confirmed retained commands still returned help with exit 0.
4. Reinstalled the candidate wheel with `--no-deps`. Exit 0; 18 launchers present; smoke exit 0.

The `pip check` warnings during the rollback steps are rehearsal-environment artifacts (`--no-deps` swaps in a venv that never had dependencies installed). A full dependency install is always clean.

Operational rollback for this story is simpler than for code releases: reinstall the recorded baseline wheel, or simply skip the skill folder when distributing the source tree, since the skill is not part of the package. Candidate recovery means reinstalling the recorded candidate wheel or restoring the skill folder from the candidate commit.

## Temporary files

Verification archives, build trees, virtual environments, and user sites remain under `T:\tmp\foundry-devops023-20260811` for reproduction. They contain public dependencies and generated build/test files, not credentials or Foundry data. No broad cleanup was attempted.
