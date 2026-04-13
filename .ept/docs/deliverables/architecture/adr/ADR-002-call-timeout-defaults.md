# ADR-002: Per-Call Timeout Defaults

| Field | Value |
|---|---|
| **ID** | ADR-002 |
| **Status** | Accepted |
| **Date** | 2026-04-13 |
| **Deciders** | Solution Architect |
| **Feature** | FEATURE-001 |
| **Context ticket** | SA-ANA-001 |

## Context

The CLI uses `asyncio.wait_for()` to enforce per-call timeouts. A default must be set so agents that do not configure `FOUNDRY_AGENTIC_CLI_TIMEOUT_S` get predictable behaviour. The default must balance:

- **Too short:** Fails legitimate slow operations (large `read_table`, model inference)
- **Too long:** Agent waits indefinitely if Foundry is degraded; poor agent UX

The value must be configurable because different operations have very different expected latencies (metadata reads: ~200ms; large dataset reads: potentially minutes).

## Decision

| Parameter | Value |
|---|---|
| `FOUNDRY_AGENTIC_CLI_TIMEOUT_S` default | `30` seconds |
| Minimum allowed value | `1` second |
| Maximum allowed value | `3600` seconds (1 hour) |
| Behaviour on breach | `asyncio.CancelledError` → exit code 5, JSON error on stdout |

Additionally, the `foundry-streams` namespace operations that inherently involve long-running connections (e.g., `stream.read_records`, `subscriber.read_records`) receive a separate env var `FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S` with default `120` seconds.

## Rationale

- **30 seconds** covers the vast majority of API operations including moderate dataset reads and function executions
- Following the "fail fast, not silently" principle: a 30s timeout surfaces degraded-API issues to agents promptly
- Agents performing large dataset extractions already know they need a longer timeout and will set it explicitly
- The Streams namespace has inherently longer latencies due to record buffering; its separate default prevents false timeouts on normal stream reads

## Alternatives Considered

| Alternative | Reason Rejected |
|---|---|
| 60-second default | Agents may wait too long during API degradation; 30s is standard HTTP timeout in enterprise tooling |
| 10-second default | Too short for operations like `functions.query.execute` which can take 15-25s |
| No default (must be set explicitly) | Too friction-heavy; would break agent workflows on first use |
| Per-operation timeout config | 355+ entries × 3 control vars = thousands of config lines; impractical at this stage |

## Consequences

- `_foundry_cli_common.py` must wrap all SDK calls in `asyncio.wait_for(coro, timeout=timeout_s)`
- `SIGINT`/`SIGTERM` must also cancel the wait (via `asyncio.shield` + signal handler pattern)
- Streams namespace client must use the separate `FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S` value
- Agents must be documented on how to increase timeout for long-running operations
- Test suite must verify timeout behaviour with a mock that simulates slow responses

## References

- SRS FR-ASYNC-3, FR-ASYNC-4
- ADR-003 (Streams namespace strategy)
- SRS Table 5.3 — `FOUNDRY_AGENTIC_CLI_TIMEOUT_S`
