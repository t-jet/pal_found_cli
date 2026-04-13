# ADR-003: Streams Namespace — Batch-Response Strategy

| Field | Value |
|---|---|
| **ID** | ADR-003 |
| **Status** | Accepted |
| **Date** | 2026-04-13 |
| **Deciders** | Solution Architect |
| **Feature** | FEATURE-001 |
| **Context ticket** | SA-ANA-001 |

## Context

The `streams` namespace includes operations that can produce continuous or high-volume data streams:
- `stream.get_records` — poll records from a stream partition
- `subscriber.read_records` — read records for a subscriber
- `stream.publish_binary_record` — publish binary content to a stream

Two strategies exist for implementing CLI exposure of streaming operations:

1. **Streaming handle:** Keep connection open, emit records progressively, terminated by signal or timeout
2. **Batch-response:** Retrieve up to N records, terminate cleanly, return structured output

A CLI process is inherently short-lived. Agent callers expect a subprocess to exit with a result; they cannot easily drive a persistent streaming connection or process incremental stdout.

## Decision

Adopt the **batch-response pattern** for all `streams` namespace operations.

**Behaviour per operation:**

| Operation | Batch Mode |
|---|---|
| `stream.get_records` | Retrieve up to `--max-records` (default: 100, max: 10,000) records then exit |
| `subscriber.read_records` | Retrieve up to `--max-records` records; commit offset manually via separate call |
| `subscriber.commit_offsets` | Single-call, synchronous — no change needed |
| `stream.publish_binary_record` | Write binary content to temp file, pass file path to SDK; streaming upload handled by SDK internally |
| `stream.publish_record`, `publish_records` | Single-call batch publish — no change needed |
| Other stream operations | Single-call — no change needed |

**Stream read timeout:** `FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S` (default: 120s) per ADR-002.

**Output format:** All stream records are aggregated into a JSON array (or TOON if uniform) and emitted to stdout on CLI exit. Records are not emitted progressively—this is a deliberate constraint of the batch-response model.

## Rationale

- **Process model compatibility:** VS Code skill runner and subprocess orchestrators expect processes that exit cleanly; persistent streaming processes cannot be managed by these hosts
- **Agent simplicity:** Agents can parse a single stdout payload; parsing interleaved streaming output requires complex state management in the agent
- **Volume control:** The `--max-records` cap prevents runaway memory usage; agents that need more records can call iteratively using `--subscriber-id` for paginated subscriber reads
- **Binary upload:** The SDK's internal streaming upload is transparent to the CLI; the agent only provides the file path, which the CLI reads and uploads

## Alternatives Considered

| Alternative | Reason Rejected |
|---|---|
| Streaming handle (persistent process) | Incompatible with subprocess/skill runner model; agents cannot drive a live process |
| Server-Sent Events over stdout | Requires agent-side SSE parser; no standard support in VS Code skill runners |
| Named pipe / socket IPC | Complex cross-platform setup; overkill for a CLI tool |

## Consequences

- `foundry_streams_cli.py` must implement `--max-records` argument for record-reading operations
- All records are buffered in memory up to `--max-records`; callers processing >10,000 records must use iterative calls
- Subscribers must use `commit_offsets` as a separate explicit call (not auto-committed after read)
- The `stream.get_records` operation is inherently non-deterministic in volume; callers must handle partial results gracefully
- Test suite must mock stream SDK methods to return bounded record sets

## References

- SRS FR-ASYNC-3 (timeout)
- ADR-002 (Streams timeout default)
- `foundry_sdk/v2/streams/` SDK source
