Subject: Implementation Plan — Open to In Progress
Created: 2026-05-18T19:13:00
Updated: 2026-05-18T19:13:00
---
## Implementation Plan — Open → In Progress

### Overview
Implement all 26 Foundry datasets namespace operations as CLI commands under the oundry-datasets skill package.

### 26 Operations (from SDK v2)

**Dataset Client (6 operations):**
1. create — POST /v2/datasets (create dataset + default branch)
2. get — GET /v2/datasets/{datasetRid}
3. get-health-check-reports — GET /v2/datasets/{datasetRid}/getHealthCheckReports
4. get-health-checks — GET /v2/datasets/{datasetRid}/getHealthChecks
5. get-schedules — GET /v2/datasets/{datasetRid}/getSchedules
6. get-schema — GET /v2/datasets/{datasetRid}/getSchema
7. get-schema-batch — POST /v2/datasets/getSchemaBatch

**Branch Client (operations from branch.py):**
8-11. Branch CRUD operations (create, get, delete, list)

**Transaction Client (operations from transaction.py):**
12-16. Transaction operations (create, commit, abort, get, get-schema)

**File Client (operations from file.py):**
17-19. File operations (upload, download, get)

**View Client (operations from view.py):**
20-21. View operations

**Dataset Row/Item Operations:**
22-26. Row-level and metadata operations

### Deliverables

1. .claude/skills/foundry-datasets/SKILL.md — Skill definition
2. .claude/skills/foundry-datasets/scripts/foundry_datasets_cli.py — CLI entry point
3. .claude/skills/foundry-datasets/scripts/_foundry_cli_common.py — Shared utilities (from DEV-STORY-001 to DEV-STORY-004)

### Architecture Alignment
- Per SAD-001: Subprocess-compatible CLI, JSON/TOON on stdout, metadata on stderr
- Per ADR-001: Structured exit codes
- Per ADR-002: Configurable timeouts
- Per ADR-004: Format auto-selection
- Per ADR-005: NDJSON structured logging to stderr
- Per ADR-007: Operation-level READONLY independence
- Access control: Auth → Access Control → API call order

### Implementation Order
1. Create directory structure
2. Copy/update _foundry_cli_common.py from shared infrastructure
3. Implement CLI entry point with argparse subcommands
4. Implement Dataset operations (7)
5. Implement Branch operations
6. Implement Transaction operations
7. Implement File operations
8. Implement View operations
9. Create SKILL.md
10. Validate all 26 operations

### Risk: Dependencies
- DEV-STORY-003 (AccessControlGuard, PaginationHelper): Status New
- DEV-STORY-004 (BinaryDownloadHandler, SessionManager, TracingProvider): Status New
- Will stub/mock unavailable shared components and integrate once available
