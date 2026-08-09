# DEVOPS-012 - Foundry Language Models deployment report

| Field | Value |
|---|---|
| Story | DEV-STORY-012 |
| Candidate | `cb8e8d2f54a459b6a2750f2ef813d0cb71dd9682` |
| Rollback baseline | `bf1c10d647c3cda3cf2f5336059361384164b3bc` |
| Verified | 2026-08-09T15:30:06+03:00 |
| Target | Isolated Windows package and Claude skill bundle |
| Result | PASS |
| Estimate | 2 hours; completed within estimate |

The candidate is ready for a controlled package and Claude skill bundle release. No package was published and no cloud resource, credential, or live Foundry API was used.

## Candidate isolation

Verification used clean `git archive` exports instead of the dirty shared worktree. All Story 012 commits from DESIGN-012 through the final global-disable regression are ancestors of the candidate. The candidate archive contained 1,433 files; the rollback archive contained 1,423 files.

| Archive | SHA-256 |
|---|---|
| Candidate `cb8e8d2` | `8e3b4996afa6ab911c8376a6890545562c00f4eef9fb89ce1a0f77f322a0fa10` |
| Rollback `bf1c10d` | `ad78f36c87bab6e6a123d3d263132ab87209fe8bc7fa6a2b530bc803602752d3` |

Temporary build trees, virtual environments, and artifacts remain under `T:\tmp\DEVOPS-012-20260809-152150` for reproduction. They contain public dependencies and generated test data only.

## Build artifacts

Python 3.11.9 built the wheel and sdist with `python -m build`. Twine 7.0.0 accepted both artifacts.

| Artifact | Size | SHA-256 | Result |
|---|---:|---|---|
| `foundry_cli-0.1.0-py3-none-any.whl` | 76,812 bytes | `ab8ab2b55459b8b18b6d9762d4df444ae59c3a73b3a1e76b866cbeaffdf7fbb7` | PASS |
| `foundry_cli-0.1.0.tar.gz` | 117,656 bytes | `ea5513648d8d13ad613950b913b9ee4954c0455470520a2eee03168253ffab06` | PASS |

Wheel inspection found the Language Models module, console metadata, and packaged `metadata-allow-list.md`. Its 41 members contained no `tests/`, `.claude/`, `.ept/`, `.github/`, environment file, private key, or certificate. The sdist contained the package source and policy. As with DEVOPS-011, the `.claude` skill is a separate release asset rather than wheel or sdist package data.

## Installation and smoke checks

The wheel used a fresh Python 3.11 environment. The editable install used a fresh Python 3.12 environment. Both used normal dependency resolution and passed `python -m pip check`. Smoke checks ran from empty directories with `PYTHONPATH` and all inherited `FOUNDRY*` variables unset.

| Check | Wheel | Editable |
|---|---:|---:|
| `foundry-language-models --help` | Exit 0 | Exit 0 |
| Claude launcher `--help` | Exit 0 | Exit 0 |
| Datasets, Filesystem, Ontologies, Audit, and AIP Agents help | Exit 0 each | Exit 0 each |
| Package and launcher import | PASS | Covered by suite and editable smoke |
| Import changed environment or empty CWD | No | No |

Installed metadata exposed exactly these console scripts:

```text
foundry-aip-agents
foundry-audit
foundry-datasets
foundry-filesystem
foundry-language-models
foundry-ontologies
```

The installed Language Models policy had exactly two operation rows: zero `PERMITTED` and two `BLOCKED`. Installed-package metadata-only smokes returned exit 8 for both `anthropic-model messages` and `open-ai-model embeddings` before client creation.

## Quality, compatibility, and security

| Command | Result |
|---|---|
| Python 3.11.9 full pytest with branch coverage | 755 passed in 31.19 s; 84.73% |
| Python 3.12.9 full pytest with branch coverage | 755 passed in 28.18 s; 84.73% |
| `python -m ruff check src tests .claude/skills/foundry-language-models` | PASS |
| `python -m mypy src` | PASS; 33 source files |
| `python -m bandit -r src --severity-level high` | PASS; 6,832 lines, zero findings |
| `python -m safety check --full-report` | PASS; 87 packages, zero known vulnerabilities, zero ignored |
| `python -m pip check` | PASS for wheel, editable, and restored candidate |

The project CI gate is `ruff check src/ tests/`; the deployment check adds the new Claude launcher directory. `ruff check .` is not the product gate because `.` also includes vendored SDK, tracker, and agent-skill tooling under `.ept/`. Safety completed without authentication against its open-source database and printed its existing deprecation warning for `safety check`.

## Rollback rehearsal

The rollback wheel was built from clean baseline `bf1c10d` and passed Twine validation.

| Artifact | Size | SHA-256 |
|---|---:|---|
| Rollback wheel | 71,741 bytes | `6a2079c7d6d8700e185c237fb26c9cc5bf5a47b9737bd68c2e7169492660f6e2` |

Rehearsal results:

1. Force-installed the rollback wheel into the isolated candidate environment with `--no-deps`.
2. Confirmed `foundry-language-models.exe`, `foundry_cli.language_models`, and the rollback Language Models skill were absent.
3. Confirmed all five retained console commands still returned help with exit 0.
4. Reinstalled the candidate wheel with `--no-deps`.
5. Confirmed the Language Models console, module, and Claude launcher returned; all retained command help checks and `pip check` passed.

Operational rollback must install the recorded baseline wheel and restore its matching skill bundle. Candidate recovery must reinstall the recorded candidate wheel and matching Language Models skill directory.

## Final status

DEVOPS-012 is READY. Candidate `cb8e8d2f54a459b6a2750f2ef813d0cb71dd9682` is production-ready for controlled package and Claude skill bundle release. Publication and live deployment require separate authorization.
