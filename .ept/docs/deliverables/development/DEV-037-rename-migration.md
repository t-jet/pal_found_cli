# Rename migration guide

This guide covers the public rename from `foundry_` to `pal_found_`. The
runtime operations, authentication, access control, output formats, exit codes,
retry handling, and tracing stay unchanged.

## New names

| Old public name | New public name |
| --- | --- |
| `foundry_cli` package | `pal_found_cli` package |
| `foundry_cli` repository | `pal_found_cli` repository |
| `foundry_cli_tool` repository | `pal_found_cli_tool` repository |
| `foundry_cli_skills` repository | `pal_found_cli_skills` repository |
| `foundry-datasets` | `pal-found-datasets` |
| `foundry-filesystem` | `pal-found-filesystem` |
| `foundry-functions` | `pal-found-functions` |
| `foundry-ontologies` | `pal-found-ontologies` |
| `foundry-admin` | `pal-found-admin` |
| `foundry-audit` | `pal-found-audit` |
| `foundry-aip-agents` | `pal-found-aip-agents` |
| `foundry-language-models` | `pal-found-language-models` |
| `foundry-models` | `pal-found-models` |
| `foundry-orchestration` | `pal-found-orchestration` |
| `foundry-sql-queries` | `pal-found-sql-queries` |
| `foundry-streams` | `pal-found-streams` |
| `foundry-connectivity` | `pal-found-connectivity` |
| `foundry-media-sets` | `pal-found-media-sets` |
| `foundry-checkpoints` | `pal-found-checkpoints` |
| `foundry-data-health` | `pal-found-data-health` |
| `foundry-third-party-applications` | `pal-found-third-party-applications` |
| `foundry-widgets` | `pal-found-widgets` |

## Existing clones

Update each remote and submodule URL to the new repository name, then fetch the
new default branch:

```bash
git remote set-url origin https://github.com/t-jet/pal_found_cli.git
git submodule sync --recursive
git submodule update --init --recursive
git pull --ff-only
```

GitHub redirects keep old repository URLs resolving during the transition. New
documentation and new clones must use the `pal_found_*` URLs in `.gitmodules`.

## Package and scripts

Install or upgrade the renamed distribution, then update scripts to use the
`pal-found-*` commands:

```bash
python -m pip install --upgrade pal_found_cli
pal-found-datasets --help
```

The old command names are not compatibility aliases. Existing scripts need the
command substitutions listed above. Conda users install `pal_found_cli` from
the configured channel.

## Skills

Copy the 19 `pal-found*` folders from `pal_found_cli_skills/.agents/skills/`
into the target workspace's `.agents/skills/` directory. Codex discovers that
directory directly. Claude Code users can link `.claude/skills/` to it; the
legacy directory in this repository contains only a migration pointer. See
`pal_found_cli_skills/README.md` for the PowerShell and POSIX commands.

## Rollback

Keep the last known-good release tag before upgrading. If the renamed release
fails verification, reinstall that tagged artifact or check out the tag in the
clone, run the previous test and smoke checks, and copy its skill folders back
to the target harness. Keep the GitHub redirects in place while deciding
whether to retry the rename. Rollback restores the previous release; it does
not make old command names valid in the renamed release.

## Verification

Run the focused migration tests and all 18 launcher help probes before using
the renamed installation in automation. The repository gate remains Ruff,
mypy, compileall, pytest with at least 80% branch coverage, and the security
checks defined by CI.

## Names that remain unchanged

`foundry_sdk`, `foundry-platform-sdk`, `FOUNDRY_TOKEN`, and `FOUNDRY_HOSTNAME`
belong to the SDK or runtime configuration and are not part of this rename.
Older design and execution records retain their original names as historical
references.
