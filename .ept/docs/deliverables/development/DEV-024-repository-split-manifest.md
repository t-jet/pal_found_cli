# Repository split manifest

This manifest records the local split preparation. It does not claim that
remote repositories were created or published.

| Ownership | Destination | Current source paths |
| --- | --- | --- |
| Design, requirements, tracker | `pal_found_cli` | `.ept/`, `.github/agents/`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `misc_docs/` |
| CLI source, tests, packaging, CI | `pal_found_cli_tool` | `src/`, `tests/`, `pyproject.toml`, `.github/workflows/`, `README.md` |
| Agent skills | `pal_found_cli_skills` | `.agents/skills/` and the skills currently staged under `.claude/skills/` |

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
