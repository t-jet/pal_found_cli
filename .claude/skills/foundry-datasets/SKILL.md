---
name: foundry-datasets
description: Foundry Datasets API v2 CLI — 33 operations across 5 resource clients (Dataset, Branch, File, Transaction, View). Implements async REST API client patterns with access control, retry, pagination, and structured output.
---

# Foundry Datasets CLI

33 Foundry Datasets API v2 operations exposed as CLI subcommands via `foundry_datasets_cli.py`.

## Operations

| Resource | Operations | Count |
|---|---|---|
| **dataset** | create, get, get-health-check-reports, get-health-checks, get-schedules, get-schema, get-schema-batch, jobs, put-schema, read-table, transactions | 11 |
| **branch** | create, delete, get, list, transactions | 5 |
| **file** | content, delete, get, list, upload | 5 |
| **transaction** | abort, build, commit, create, get, job | 6 |
| **view** | add-backing-datasets, add-primary-key, create, get, remove-backing-datasets, replace-backing-datasets | 6 |

## Usage

```bash
python foundry_datasets_cli.py <resource> <operation> [options]
```

### Examples

```bash
# Get dataset info
python foundry_datasets_cli.py dataset get <DATASET_RID>

# List branches
python foundry_datasets_cli.py branch list <DATASET_RID> --page-size 50

# Read table data
python foundry_datasets_cli.py dataset read-table <DATASET_RID> --branch-name main

# Upload file
python foundry_datasets_cli.py file upload <DATASET_RID> --file-path ./data.csv

# Create view
python foundry_datasets_cli.py view create --name "My View" --parent-folder-rid "some_rid"

# Get schema batch
python foundry_datasets_cli.py dataset get-schema-batch --dataset-r '["rid1", "rid2"]'
```

### Common Options

| Option | Description |
|---|---|
| `--timeout <seconds>` | Request timeout in seconds |
| `--format json\|toon\|auto` | Output format (default: auto) |
| `--pretty` | Pretty-print JSON output |
| `--page-size <n>` | Page size for paginated operations |
| `--page-token <token>` | Resume pagination from token |
| `--batch-pages <n>` | Number of pages to fetch in batch |

## Architecture

### Shared Infrastructure (src/foundry_cli/common/)

| Module | Purpose | ADR |
|---|---|---|
| ConfigLoader | .env file search path (explicit → git root → env vars) | ADR-006 |
| AsyncClientFactory | Creates Foundry SDK client with auth/attribution | - |
| RetryHandler | Exponential backoff + jitter for transient errors | ADR-002 |
| ErrorSerializer | Maps exceptions to exit codes (0-9) | ADR-001 |
| OutputFormatter | JSON/TOON auto-selection on stdout | ADR-004 |
| LogSetup | NDJSON structured logging to stderr | ADR-005 |
| AccessControlGuard | 8-step access control precedence model | ADR-007 |
| PaginationHelper | --page-size, --page-token, --batch-pages | - |

### Exit Codes (ADR-001)

| Code | Name | Description |
|---|---|---|
| 0 | Success | Operation completed successfully |
| 1 | UserInputError | Invalid CLI args, validation failure |
| 2 | AuthenticationError | Missing/invalid token |
| 3 | PermissionDeniedError | API 403 |
| 4 | NotFoundError | API 404 |
| 5 | TimeoutError | Request timeout |
| 6 | ServerError | API 5xx |
| 7 | RateLimitExhausted | HTTP 429 + retries exhausted |
| 8 | AccessControlError | CLI access control policy |
| 9 | ConfigurationError | Missing env var, malformed config |

### Access Control (ADR-007)

8-step precedence model evaluated before each operation:
1. Operation-level ENABLED
2. Namespace-level ENABLED
3. Operation-level READONLY override (false = permit write)
4. Namespace-level READONLY override
5. Global READONLY
6. Namespace METADATA_ONLY
7. Global METADATA_ONLY
8. Permit

### Output (ADR-004)

- Data on stdout (JSON or TOON)
- Metadata on stderr with `# ---metadata-start---` separator
- Auto-selection: explicit format → error → non-list → empty list → field set comparison

## Configuration

| Environment Variable | Description |
|---|---|
| `FOUNDRY_TOKEN` | API token (required) |
| `FOUNDRY_HOSTNAME` | Foundry host URL (required) |
| `FOUNDRY_AGENTIC_CLI_TIMEOUT_S` | Default timeout (default: 30s) |
| `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT` | Default output format |
| `FOUNDRY_AGENTIC_CLI_READONLY` | Global read-only mode |
| `FOUNDRY_AGENTIC_CLI_METADATA_ONLY` | Global metadata-only mode |
| `FOUNDRY_AGENTIC_CLI_LOG_LEVEL` | Log level: DEBUG, INFO, WARNING, ERROR |
| `FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION` | Enable attribution |
| `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS` | Comma-separated attribution RIDs |

## File Location

```
.claude/skills/foundry-datasets/
├── SKILL.md
└── scripts/
    └── foundry_datasets_cli.py    # Main CLI entry point (33 operations)
```
