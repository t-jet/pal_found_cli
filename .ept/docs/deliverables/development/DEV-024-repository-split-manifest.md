# Repository split manifest

This manifest records the local split preparation. It does not claim that
remote repositories were created or published.

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

`.gitmodules` now points at the final public names. The nested repositories and
remote publication remain external prerequisites.

## Local rename blocker

This checkout can rename its submodule paths and local URL mapping, which it
now does. GitHub repository renames and permission changes require repository
owner access and were not performed here. The root checkout still uses its
existing filesystem location; update the remote and publish the renamed
repositories when owner access is available.
