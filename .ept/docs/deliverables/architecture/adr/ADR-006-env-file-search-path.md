# ADR-006: `.env` File Search Path Order

| Field | Value |
|---|---|
| **ID** | ADR-006 |
| **Status** | Accepted |
| **Date** | 2026-04-13 |
| **Deciders** | Solution Architect |
| **Feature** | FEATURE-001 |
| **Context ticket** | SA-ANA-001 |

## Context

The CLI loads configuration from a `.env` file. The search path order determines which file is loaded when the CLI is invoked from different directories. The design must:

- Be predictable (same result regardless of where the CLI script resides)
- Support monorepo layouts (multiple Foundry CLI deployments in different subdirectories)
- Not accidentally load credentials from an unrelated project or home directory
- Support CI/CD pipelines that set credentials via environment variables only

## Decision

The `.env` file search path is evaluated in the following order (first found wins):

**Order 1 — Explicit override:**  
If `FOUNDRY_AGENTIC_CLI_ENV_FILE` is set, load from that path. If the file does not exist, raise `ConfigurationError` (exit code 9). Do not fall through to other paths.

**Order 2 — Repo root `.env`:**  
Walk up the directory tree from the current working directory (CWD) until a directory containing `.git` is found. Load `.env` from that directory. If no `.git` directory is found, load `.env` from CWD itself (fallback for non-git deployments).

**Order 3 — No `.env` (env vars only):**  
If no `.env` file is found after the above search, proceed using environment variables only. Do not error — `FOUNDRY_TOKEN` and `FOUNDRY_HOSTNAME` may be set directly.

**Explicit no-home-dir fallback:**  
The user home directory (`~/.env`, `~/foundry/.env`, etc.) is deliberately **not** searched.

**Loading mechanism:** `python-dotenv` (`dotenv.load_dotenv()`). Environment variables already set in the shell take precedence over `.env` values (consistent with `load_dotenv(override=False)` default behaviour).

## Rationale

- **Explicit path first:** CI/CD pipelines frequently set `FOUNDRY_AGENTIC_CLI_ENV_FILE=/run/secrets/.env`; explicit > implicit
- **Git root detection:** Foundry CLI skills are always deployed inside a git repository; the git root is a stable anchor point across different CWDs (e.g., agent invokes from the project root, skill scripts reside in `.claude/skills/foundry-datasets/scripts/`)
- **No home-dir fallback:** A critical security decision. Home-dir credential files are often broader in scope than a single project; accidental cross-project credential leakage is a real risk. Developers who want global credentials must use shell environment variables
- **python-dotenv override=False:** Environment variables set before CLI invocation (e.g., in CI) take precedence; this is the standard and expected behaviour

## Alternatives Considered

| Alternative | Reason Rejected |
|---|---|
| Search `~/.foundry/.env` as final fallback | Security risk: credentials from one project contaminate another; violates DCC-3 (self-contained skill) |
| Use the script's `__file__` directory as anchor | Fragile: copied scripts may reside in deep subdirectories with no relation to the repo root |
| Require explicit `--env-file` CLI argument on every invocation | Too friction-heavy for agent use; agents should not need to manage config file paths |
| Search `XDG_CONFIG_HOME/foundry-cli/.env` | Linux-only convention; inconsistent on Windows; adds platform-detection complexity |

## Consequences

- `_foundry_cli_common.py` must implement the git-root walk using `pathlib` and check for `.git` in each ancestor
- The git-root walk must have a depth limit (e.g., 20 levels) to prevent infinite loops on misconfigured filesystems
- `python-dotenv` must be added to the dependency list (`pip install python-dotenv`)
- Documentation must clearly state that the CLI reads `.env` from repo root and that home-dir files are not loaded
- Test suite must verify: explicit path loaded, git root discovered, CWD fallback, env-var-only mode

## References

- SRS Table 5.1 — Configuration Loading Order
- SRS Table 5.3 — `FOUNDRY_AGENTIC_CLI_ENV_FILE`
- SRS DCC-3, DCC-6
- Q&A R2: A(Q2(R2).10-D)
