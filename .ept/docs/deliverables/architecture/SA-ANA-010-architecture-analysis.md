# Architecture Analysis — SA-ANA-010

## Rename `foundry_` Prefix to `pal_found_` Across All Three Projects

| Field | Value |
| --- | --- |
| **Document ID** | SA-ANA-010 |
| **Feature** | FEATURE-010 |
| **Status** | Resolved — pending Project Owner approval; naming decisions confirmed 2026-08-12 |
| **Date** | 2026-08-12 (updated 2026-08-12) |
| **Author** | Solution Architect |
| **Requirement source** | Project Owner change request 2026-08-12 |

> **Naming status.** All target names in section 2 are CONFIRMED by the Project
> Owner on 2026-08-12 through the BA-ANA-010 naming QUESTIONS (QUESTION-072..075,
> all Closed). Repositories and the Python package use the underscore form
> `pal_found_`; CLI entry points and skill folders use the hyphen form
> `pal-found-`. The ticket stays Resolved (not Closed) pending Project Owner
> approval via the SA-ANA-010 approval QUESTION.

---

## 1. Affected Components Inventory

### 1.1 Three repositories

| Asset | Current | Location / reference |
| --- | --- | --- |
| Design, docs, tracking repo | `foundry_cli` | `https://github.com/t-jet/foundry_cli.git` (parent, branch main) |
| CLI tool repo | `foundry_cli_tool` | `https://github.com/t-jet/foundry_cli_tool.git` (submodule, currently empty) |
| Skills repo | `foundry_cli_skills` | `https://github.com/t-jet/foundry_cli_skills.git` (submodule, LICENSE only) |
| Submodule registration | `foundry_cli_tool`, `foundry_cli_skills` | Parent `.git/config` `[submodule]` URL entries and `.gitmodules` |

Repo renames affect every submodule URL, clone command, and CI checkout reference.

### 1.2 Python package and distribution

| Asset | Current | Reference |
| --- | --- | --- |
| Import namespace package | `foundry_cli` (18 namespace subpackages + `common`) | `src/foundry_cli/` |
| Distribution name (PyPI) | `foundry-cli` | `pyproject.toml` `[project] name` |
| Package data | `foundry_cli.<ns>` = `metadata-allow-list.md` | `pyproject.toml` `[tool.setuptools.package-data]` |
| Coverage source | `foundry_cli` | `pyproject.toml` `[tool.coverage.run] source` |
| Ruff per-file ignores | `src/foundry_cli/<ns>/scripts/*.py` | `pyproject.toml` `[tool.ruff.lint.per-file-ignores]` |
| Coverage omit paths | `src/foundry_cli/...` | `pyproject.toml` `[tool.coverage.run] omit` |

### 1.3 Console entry points (18, in `pyproject.toml` `[project.scripts]`)

`foundry-datasets`, `foundry-filesystem`, `foundry-functions`, `foundry-ontologies`,
`foundry-admin`, `foundry-audit`, `foundry-aip-agents`, `foundry-language-models`,
`foundry-models`, `foundry-orchestration`, `foundry-sql-queries`, `foundry-streams`,
`foundry-connectivity`, `foundry-media-sets`, `foundry-checkpoints`, `foundry-data-health`,
`foundry-third-party-applications`, `foundry-widgets`.

Each maps to `foundry_cli.<ns>.scripts.foundry_<ns>_cli:console_main` (datasets uses
`:main`, an existing inconsistency to normalize during rename).

### 1.4 Agent skills (19 folders in `.claude/skills/`)

Main skill `foundry` plus 18 namespace skills (`foundry-admin` ... `foundry-widgets`).
Each folder holds `SKILL.md` with `name:` frontmatter plus `scripts/foundry_<ns>_cli.py`.
Skills are not yet in `.agents/skills` (FEATURE-006 moves them there); the rename must
apply to both layouts. The `foundry` main skill references every `foundry-*` skill by
name in its content.

### 1.5 Documentation references

| Document | Impact |
| --- | --- |
| `document_index.md` | Every index entry naming `foundry-*` skills, `foundry_cli` package, doc filenames |
| `SRS-001-foundry-cli.md`, `SAD-001-foundry-cli.md` | Filenames and body references |
| `canonical-env-var-reference.md` (ENV-REF-001) | 789 `FOUNDRY_AGENTIC_CLI_*` occurrences (measured 2026-08-12) plus naming-convention table |
| `metadata-allow-list.md` | Namespace block labels (`foundry_cli.<ns>`) |
| DESIGN-005..023, DEVOPS-010..023, TESTCASE/TESTEXEC logs | Entry-point and package references |
| `.env.example` | ~19 `FOUNDRY_AGENTIC_CLI_*` sample variables |

### 1.6 Build, CI/CD, QA

| Asset | Current reference | Impact |
| --- | --- | --- |
| `ci.yml` | `pytest tests/ --cov=foundry_cli ...`, `mypy src/`, `bandit -r src/` | `--cov` value, paths unchanged except package rename |
| `publish.yml` | PyPI upload on `v*` tag | PyPI project name change, token scope |
| `pyproject.toml` | name, scripts, package-data, ruff, coverage | All package-name references |
| Tests | ~50+ files import `foundry_cli.*`; names `test_foundry_*_cli.py` | Import paths, file names |
| QA/build artifacts | `build/`, `coverage.xml`, `htmlcov/` | Regenerated, not renamed in place |

### 1.7 Out of scope (external SDK names, keep unchanged)

`foundry_sdk`, `foundry-platform-sdk`, `FOUNDRY_TOKEN`, `FOUNDRY_HOSTNAME`,
`foundry_sdk.v2` imports, Palantir SDK env vars. These are Palantir-owned names, not
project-owned, and renaming them would break the SDK contract.

---

## 2. Confirmed Rename Mapping (PO decisions 2026-08-12)

| # | Old | New (CONFIRMED) | Notes |
| --- | --- | --- | --- |
| 1 | repo `foundry_cli` | `pal_found_cli` | Design/docs/tracking repo |
| 2 | repo `foundry_cli_tool` | `pal_found_cli_tool` | CLI source repo |
| 3 | repo `foundry_cli_skills` | `pal_found_cli_skills` | Skills repo |
| 4 | submodule URLs `t-jet/foundry_cli_tool.git`, `t-jet/foundry_cli_skills.git` | `t-jet/pal_found_cli_tool.git`, `t-jet/pal_found_cli_skills.git` | Update `.git/config` + `.gitmodules`; GitHub redirects keep old URLs resolving |
| 5 | package `foundry_cli` | `pal_found_cli` | `src/` tree, all imports |
| 6 | distribution `foundry-cli` | `pal_found_cli` | PyPI project name; import package `pal_found_cli` |
| 7 | entry points `foundry-*` (18) | `pal-found-*` (18) | e.g. `foundry-datasets` → `pal-found-datasets` |
| 8 | skill `foundry` (main) | `pal-found` | Folder, `name:` frontmatter |
| 9 | skills `foundry-*` (18) | `pal-found-*` (18) | Folders, frontmatter, cross-references |
| 10 | skill scripts `foundry_<ns>_cli.py` | `pal_found_<ns>_cli.py` | Python module files keep underscores; folders use `pal-found-*` |
| 11 | env vars `FOUNDRY_AGENTIC_CLI_*` | `PAL_FOUND_AGENTIC_CLI_*` | OPEN — PO decision; 789 occurrences in ENV-REF-001, 19 in `.env.example`, retry/session code |
| 12 | test files `test_foundry_*_cli.py` | `test_pal_found_*_cli.py` | Tests directory |
| 13 | docs `SRS-001-foundry-cli.md`, `SAD-001-foundry-cli.md` | `SRS-001-pal-found-cli.md`, `SAD-001-pal-found-cli.md` | PROPOSED; PO decides whether historical docs rename |
| 14 | coverage `source = ["foundry_cli"]` | `source = ["pal_found_cli"]` | `pyproject.toml`, `ci.yml --cov` |
| 15 | package-data, ruff ignores paths | prefix swap `foundry_cli` → `pal_found_cli` | `pyproject.toml` |

Rows 1–10 are CONFIRMED by the PO (2026-08-12). Rows 11 (env vars) and 13
(historical doc filenames) remain OPEN PO decisions; row 12 follows the package
rename mechanically. Nothing in this table is implemented until approval.

---

## 3. Architecture Approach

Pure identity rename with zero functional change. One rule: every project-owned
identifier carrying the `foundry_` prefix moves to `pal_found_`; every Palantir-owned
identifier stays. The rename removes the ambiguity named in the PO change request
(confusion with Microsoft Foundry and other projects) while keeping the platform
context that `pal_found` still signals.

Consistency constraints that make the rename mechanical and verifiable:

- Repo names, package import namespace, distribution name, entry-point names, and
  skill names all derive from one canonical list of 19 names (main skill + 18 namespaces).
- Skill cross-references are content-coupled: the `foundry`/`pal_found` main skill
  names every namespace skill, and each skill names its own `scripts/` launcher and
  env vars. The rename is one coordinated sweep, not per-file edits.
- CI/CD and packaging config (`pyproject.toml`, `ci.yml`, `publish.yml`) reference the
  package and entry-point names and must change atomically with the code, or the
  pipeline breaks at build time.
- No runtime behavior changes: auth, access control, output formats, exit codes,
  retry, tracing are untouched. The only runtime-visible change is the env-var prefix
  if the PO confirms row 11, which then needs a compatibility note for existing users.

## 4. Technology Stack (unchanged)

- Python 3.11+, setuptools, PEP 517 build
- `foundry-platform-sdk>=1.0.0`, `python-dotenv`, `requests`
- pytest, pytest-cov, mypy, ruff, bandit
- GitHub Actions (ci.yml six-stage, publish.yml tag-triggered)
- pip and conda distribution channels (EPIC-010)

No new dependencies. Stack is untouched by the rename; only names change.

## 5. General Implementation Approach

1. PO naming decisions landed (QUESTION-072..075 Closed 2026-08-12); the targets
   in section 2 are CONFIRMED.
2. Rename GitHub repos; GitHub redirects keep old URLs resolving; update submodule
   URLs in parent `.git/config` and `.gitmodules`; update local remotes.
3. Rename package: move `src/foundry_cli/` to `src/pal_found_cli/`, rewrite imports
   across `src/` and `tests/`, rename entry-point modules and `[project.scripts]`.
4. Update `pyproject.toml` (name, scripts, package-data, ruff ignores, coverage),
   `ci.yml` (`--cov=pal_found_cli`), `.env.example`, env-var code paths per PO row 11.
5. Rename skills: 19 folders and frontmatter, `scripts/` launchers, cross-references
   in the main skill; apply to `.claude/skills` and the `.agents/skills` layout
   (FEATURE-006 dependency).
6. Update docs: `document_index.md`, SRS/SAD filenames per PO, ENV-REF-001 entries,
   metadata-allow-list labels, DEVOPS report references.
7. Rebuild, re-run full suite (pytest, mypy, ruff, bandit), rebuild wheel, rerun
   entry-point smoke on all 18 commands, verify coverage gate ≥ 80%.
8. Publish `pal_found_cli` to pip (FEATURE-004) and conda (FEATURE-005);
   optionally keep a deprecated `foundry-cli` stub on PyPI redirecting to the new
   name (PO decision).

## 6. General Migration Approach

Sequenced phases, each gated:

- Phase 0 — Decisions: PO naming decisions confirmed (QUESTION-072..075 Closed,
  2026-08-12). COMPLETE.
- Phase 1 — Repos: rename the three GitHub repos, fix submodule URLs, update all
  local clones. History is preserved through GitHub repo rename (redirects).
- Phase 2 — Package and pipeline: code move, imports, entry points, config, CI, tests.
  Gate: full suite green with coverage ≥ 80% and 18 entry-point smoke pass.
- Phase 3 — Skills: rename 19 skill folders/frontmatter/scripts in both layouts
  (`.claude/skills`, `.agents/skills`), update cross-references, re-verify skill
  content against FEATURE-008/009 deliverables.
- Phase 4 — Docs: sweep `document_index.md`, SRS/SAD, ENV-REF-001, metadata-allow-list,
  DEVOPS/TESTCASE/TESTEXEC references.
- Phase 5 — Release: bump version (0.2.0), publish pip + conda as `pal_found_cli`,
  update publish pipeline, announce rename with migration note for env-var row 11.

Coordination: EPIC-010 publishing features (FEATURE-004/005) and EPIC-009 skills
distribution (FEATURE-006/007) are downstream consumers; their designs (SA-ANA-002..009)
assume the current names and receive impact comments when the PO confirms targets.

## 7. Risks and Dependencies

| Item | Risk | Mitigation |
| --- | --- | --- |
| Repo renames | Submodule URLs and clones break; stale remote refs | GitHub redirects; update `.gitmodules` + local remotes; verify fresh clones |
| Package rename | Imports, entry points, coverage, ruff, package-data drift apart | Single atomic change set; full suite + entry-point smoke gate |
| Env-var rename (row 11) | Existing user configs break | PO decision; compatibility note, deprecated alias period |
| Skills rename | Main skill cross-references to 18 skills go stale | Scripted sweep + content verification against FEATURE-008/009 |
| Docs sweep | Missed `foundry_` references in historical docs | Full-tree grep gate (`foundry_` remaining = failure except out-of-scope SDK names) |
| Publishing | PyPI project name change, token scope, conda recipe | New project name publish; keep old name stub if PO approves |
| Cross-cutting | FEATURE-002..009 designs assumed current names | SA cross-reviews posted on BA-ANA-002..009 2026-08-12 flag design-phase naming updates; SA-ANA-002..009 receive impact notes at design |
| External SDK | Accidental rename of `foundry_sdk` breaks SDK contract | Out-of-scope list enforced in grep gate |

## 8. Coordination with BA and Project Owner

- BA-ANA-010 resolved the naming QUESTIONS to the PO (QUESTION-072..075 Closed
  2026-08-12). Section 2 carries the CONFIRMED targets.
- SA-ANA-010 created its own PO approval QUESTION (2026-08-12, addressed to
  project-owner, no blocking link) and stays Resolved (not Closed) until approval.
- In Progress → Resolved gate was met: BA-ANA-010 was at In Progress or later when
  SA-ANA-010 moved to Resolved (verified before transition).

## 9. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-010 (Analysis, PO change request 2026-08-12) |
| BA sub-task | BA-ANA-010 (naming QUESTIONS to PO) |
| SA sub-task | SA-ANA-010 |
| Related analysis | SA-ANA-002..009 (affected by rename), BA-ANA-002..009 |
| Related docs | document_index.md, SAD-001, SRS-001, ENV-REF-001, metadata-allow-list |
| Config surface | pyproject.toml, ci.yml, publish.yml, .env.example |
