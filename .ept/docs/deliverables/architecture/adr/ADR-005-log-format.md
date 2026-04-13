# ADR-005: Structured Log Format

| Field | Value |
|---|---|
| **ID** | ADR-005 |
| **Status** | Accepted |
| **Date** | 2026-04-13 |
| **Deciders** | Solution Architect |
| **Feature** | FEATURE-001 |
| **Context ticket** | SA-ANA-001 |

## Context

The CLI emits diagnostic logs to stderr. Log output must be:
- Machine-parseable (stderr can be captured by orchestrators)
- Not interfere with the structured metadata JSON emitted to stderr on success
- Usable for debugging retry behaviour, access control decisions, and tracing

The log format must not collide with the metadata JSON object emitted at the end of successful calls.

## Decision

**Log format:** Newline-delimited JSON (NDJSON) on stderr.

**Log record schema:**

```json
{
  "ts": "2026-04-13T14:23:01.456Z",
  "level": "WARNING",
  "logger": "foundry_cli.common.retry",
  "msg": "Retrying after 429: attempt 2/4, delay 1000ms",
  "op": "datasets.dataset.read_table",
  "call_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "attempt": 2
}
```

**Required fields for all log records:**

| Field | Type | Description |
|---|---|---|
| `ts` | ISO 8601 string | Timestamp in UTC |
| `level` | string | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `logger` | string | Module path (e.g., `foundry_cli.common.retry`) |
| `msg` | string | Human-readable message |

**Optional context fields (included when applicable):**

| Field | Type | Description |
|---|---|---|
| `op` | string | SDK path of current operation (e.g., `datasets.dataset.get`) |
| `call_id` | UUID string | Unique ID for this CLI invocation |
| `attempt` | integer | Retry attempt number (1-indexed) |
| `delay_ms` | integer | Retry delay in milliseconds |
| `access_decision` | string | `BLOCKED` or `PERMITTED` (access control decisions) |
| `session_alias` | string | Session alias (session operations) |
| `http_status` | integer | HTTP status code (error cases) |

**Log level control:** `FOUNDRY_AGENTIC_CLI_LOG_LEVEL` (default: `WARNING`).

**Separation from metadata:** A separator comment line `# ---metadata-start---` precedes the metadata JSON object so parsers can distinguish NDJSON log lines from the metadata object.

## Rationale

- **NDJSON on stderr:** Each log line is independently parseable; orchestrators that capture stderr can process logs incrementally without a full JSON parser for the stream
- **ISO 8601 timestamps:** Standard, unambiguous, timezone-explicit; easily parsed by log aggregators
- **Default WARNING level:** Agents do not need DEBUG/INFO noise in normal operation; WARNING captures retry events which are operationally relevant
- **`call_id`:** Enables correlation across log lines, metadata output, and error output for a single CLI invocation
- **Metadata separator:** Prevents log+metadata confusion; orchestrators that look for the metadata object can scan for the separator

## Alternatives Considered

| Alternative | Reason Rejected |
|---|---|
| Human-readable text logs | Not machine-parseable; inconsistent format; harder to integrate with log aggregators |
| Structured logs to a file | Would require a log file path config; adds complexity; orchestrators already capture stderr |
| Suppress all logs by default | Debug capability is essential; WARNING level is a reasonable default that passes retry information to operators |
| Merge logs and metadata into a single JSON object | Makes metadata extraction fragile; agents would need to filter log entries from metadata |

## Consequences

- `_foundry_cli_common.py` must configure Python `logging` with a custom JSON formatter and direct it to stderr
- The metadata emitter must write the separator `# ---metadata-start---` before the metadata JSON object on stderr
- Test suite must verify that stderr contains valid NDJSON lines followed by the separator and metadata JSON
- Agent skill documentation must describe stderr format so agents can optionally process log lines

## References

- SRS NFR-IFACE-2
- SRS Table 5.3 — `FOUNDRY_AGENTIC_CLI_LOG_LEVEL`
- ADR-002 (call_id for timeout events)
