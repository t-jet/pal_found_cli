# Repository split manifest

This manifest records the published repository split and its verification.

| Ownership | Destination | Canonical paths |
| --- | --- | --- |
| Design, requirements, tracker | `pal_found_cli` | `.ept/`, `.github/agents/`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `misc_docs/` |
| CLI source, tests, packaging, CI | [`pal_found_cli_tool`](https://github.com/t-jet/pal_found_cli_tool) | `src/`, `tests/`, `pyproject.toml`, `conda.recipe/`, `.github/workflows/`, `README.md` |
| Agent skills | [`pal_found_cli_skills`](https://github.com/t-jet/pal_found_cli_skills) | `.agents/skills/`, `tests/`, `.github/workflows/`, `pyproject.toml` |

## Migration gate

1. Freeze changes and record the source commit.
2. Filter each ownership group with `git-filter-repo --path` in a disposable
   clone under `.ept/tmp`; merge that lineage into the existing destination
   `main` with `--allow-unrelated-histories` and without squashing.
3. Update submodule URLs and local remotes together.
4. Run a fresh-clone check, path ownership check, secret scan, and reference
   sweep before retiring the combined layout.
5. Keep the combined repository read-only until every check passes. Roll back
   by restoring the last tagged combined state if any check fails.

`.gitmodules` points at the final public names. The repositories are public at:

- `https://github.com/t-jet/pal_found_cli`
- `https://github.com/t-jet/pal_found_cli_tool`
- `https://github.com/t-jet/pal_found_cli_skills`

## History-preservation evidence

The split used `git-filter-repo` 2.47.0 against committed root source
`5bca5d7`; dirty tracker and agent-memory files were never included. The
filtered lineages were merged into the existing public repository histories,
so no published commit was rewritten:

| Repository | Existing public ancestor | Filtered lineage tip | Split commit |
| --- | --- | --- | --- |
| `pal_found_cli_tool` | `ac9c03f` | `a21cae5` | `eb7febe` |
| `pal_found_cli_skills` | `dcbdb4e` | `349bc28` | `d347ed4` |

`git merge-base --is-ancestor` returned 0 for both existing public ancestors.
The retained commit maps provide source-to-destination traceability. Examples:

- Tool: source `5746815` maps to `4e1ce16`; source `2d96c2f` maps to
  `a43e4be`; source `62c269f` maps to `89e0d14`.
- Skills: source `2d96c2f` maps to `996ff06`; source `229efe0` maps to
  `349bc28`.

`git log --follow` in each destination shows the filtered source commits for
the moved paths. Destination pushes must remain fast-forward-only.

## Verification evidence

Local verification on 2026-08-17:

- Clean tool venv: editable install passed.
- Tool: Ruff passed; mypy passed for 70 source files; 1,110 tests passed with
  86.40% branch coverage; Bandit found zero high-severity issues.
- Tool package: sdist and wheel built; `twine check dist/*` passed; all 18
  installed `pal-found-* --help` launchers passed within the test suite.
- Skills: Ruff passed and 7 validation tests passed.

## Publication evidence

On 2026-08-17, the repository owner renamed the three public GitHub
repositories from their former `foundry_*` names. Root and nested origins plus
`.gitmodules` use canonical `pal_found_*` URLs.

A clean recursive clone from
`https://github.com/t-jet/pal_found_cli.git` completed successfully. The clone
had no worktree changes and checked out these published commits:

| Repository | Verified commit |
| --- | --- |
| `pal_found_cli` | `e4b2bccd8d2a01a41f2d57be26737230d5f42f24` |
| `pal_found_cli_tool` | `ac9c03f1086916a9145b89368bb3f671cb743144` |
| `pal_found_cli_skills` | `dcbdb4ec52862ecdf5c5d24e7de9c56b39a967d0` |
| `foundry-platform-python` | `2da67907be429c35f747eef565867ce81dd2cafc` |

This earlier clone proved URL and submodule accessibility before content
migration. The post-split recursive-clone proof is recorded after the three
split commits are published.
