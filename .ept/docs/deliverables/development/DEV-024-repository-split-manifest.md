# Repository split manifest

This manifest records the published repository split and its verification.

| Ownership | Destination | Current source paths |
| --- | --- | --- |
| Design, requirements, tracker | `pal_found_cli` | `.ept/`, `.github/agents/`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `misc_docs/` |
| CLI source, tests, packaging, CI | `pal_found_cli_tool` | `src/`, `tests/`, `pyproject.toml`, `.github/workflows/`, `README.md` |
| Agent skills | `pal_found_cli_skills` | `.agents/skills/` |

## Migration gate

1. Freeze changes and record the source commit.
2. Move each ownership group with `git filter-repo --path` in a disposable
   clone; retain commit history for moved paths.
3. Update submodule URLs and local remotes together.
4. Run a fresh-clone check, path ownership check, secret scan, and reference
   sweep before retiring the combined layout.
5. Keep the combined repository read-only until every check passes. Roll back
   by restoring the last tagged combined state if any check fails.

`.gitmodules` points at the final public names. The repositories are public at:

- `https://github.com/t-jet/pal_found_cli`
- `https://github.com/t-jet/pal_found_cli_tool`
- `https://github.com/t-jet/pal_found_cli_skills`

## Publication evidence

On 2026-08-17, the repository owner renamed the three public GitHub
repositories from their former `foundry_*` names. The root and nested origins,
plus `.gitmodules`, now use the canonical `pal_found_*` URLs.

A clean recursive clone from
`https://github.com/t-jet/pal_found_cli.git` completed successfully. The clone
had no worktree changes and checked out these published commits:

| Repository | Verified commit |
| --- | --- |
| `pal_found_cli` | `e4b2bccd8d2a01a41f2d57be26737230d5f42f24` |
| `pal_found_cli_tool` | `ac9c03f1086916a9145b89368bb3f671cb743144` |
| `pal_found_cli_skills` | `dcbdb4ec52862ecdf5c5d24e7de9c56b39a967d0` |
| `foundry-platform-python` | `2da67907be429c35f747eef565867ce81dd2cafc` |

The clone also contained the DEV-027 cross-repository reference register, and
that register resolved all three canonical repository URLs.
