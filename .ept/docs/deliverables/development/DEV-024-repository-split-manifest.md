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
- Hosted CI initially failed at job setup because the combined repository had
  pinned `actions/setup-python` to a nonexistent SHA. Tool commit `7655433`
  and skills commit `34b6c40` correct the pin to the official `v5.4.0` commit
  `42375524e23c412d93fb67b49958b491fce71c38`.

## Publication evidence

On 2026-08-17, the repository owner renamed the three public GitHub
repositories from their former `foundry_*` names. Root and nested origins plus
`.gitmodules` use canonical `pal_found_*` URLs.

A credential-disabled recursive clone from
`https://github.com/t-jet/pal_found_cli.git` completed successfully after the
split was published. Root and both destination worktrees were clean and the
clone checked out these commits:

| Repository | Verified commit |
| --- | --- |
| `pal_found_cli` | `17919823a3a348abdc9f8deedfe1f7f04cd211eb` |
| `pal_found_cli_tool` | `7655433334dd3b57a841c6faa5a63b742f30057f` |
| `pal_found_cli_skills` | `34b6c404994cdcc4f97b18d2a493fff6c1d3d895` |
| `foundry-platform-python` | `2da67907be429c35f747eef565867ce81dd2cafc` |

The clone used `GIT_TERMINAL_PROMPT=0`, an empty askpass value, and
`credential.helper=`. This proves public anonymous access without cached
credentials. Root owns no tracked `src`, `tests`, `.agents/skills`, package
metadata, or release workflow after the split.
