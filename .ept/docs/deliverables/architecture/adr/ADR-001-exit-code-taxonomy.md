# ADR-001: Exit Code Taxonomy

| Field | Value |
|---|---|
| **ID** | ADR-001 |
| **Status** | Accepted |
| **Date** | 2026-04-13 |
| **Deciders** | Solution Architect |
| **Feature** | FEATURE-001 |
| **Context ticket** | SA-ANA-001 |

## Context

The CLI contract requires non-zero exit codes on failure so that agent callers and subprocess orchestrators can programmatically distinguish error types without parsing stdout JSON. The exact taxonomy must be defined before implementation begins.

Standard POSIX exit codes (0 = success, 1 = generic error) are insufficient for a system with multiple distinguishable error categories. Agents benefit from knowing immediately whether the failure was a transient network issue, an auth problem, or a misconfiguration — each implies a different recovery strategy.

## Decision

Adopt the following exit code taxonomy:

| Code | Name | Conditions |
|---|---|---|
| `0` | **Success** | Operation completed without error |
| `1` | **UserInputError** | Invalid CLI arguments, validation failure, missing required parameter |
| `2` | **AuthenticationError** | Missing or invalid `FOUNDRY_TOKEN` / `FOUNDRY_HOSTNAME`; SDK auth failure |
| `3` | **PermissionDeniedError** | API returns 403 / `PermissionDeniedError` from SDK |
| `4` | **NotFoundError** | API returns 404 / resource does not exist |
| `5` | **TimeoutError** | `asyncio.wait_for()` timeout exceeded; `SIGINT`/`SIGTERM` received |
| `6` | **ServerError** | API returns 5xx (excluding 503 which is retried); SDK internal error |
| `7` | **RateLimitExhausted** | HTTP 429 received and maximum retry attempts exhausted |
| `8` | **AccessControlError** | Operation blocked by CLI access control policy (enabled/readonly/metadata-only) |
| `9` | **ConfigurationError** | Missing required env var or malformed configuration |

All errors also produce a JSON object on stdout using the error schema defined in FR-ERR-2.

## Rationale

- **Distinct auth vs config (2 vs 9):** Agents should retry auth errors by prompting for a new token; config errors require human intervention.
- **Rate limit as distinct code (7):** Distinguishes "exhausted retries" from server errors; agent can apply its own back-pressure.
- **Access control as distinct code (8):** Allows orchestrators to escalate to a human immediately rather than retrying.
- **Not Found (4):** Very common in exploratory workflows; agents can handle gracefully without treating as a system error.
- **Codes 1-9** avoid conflicts with shell reserved codes (126 = permission denied on exec, 127 = command not found, 128+ = signal).

## Alternatives Considered

| Alternative | Reason Rejected |
|---|---|
| Single non-zero code (1) for all errors | Insufficient disambiguation for agent callers |
| HTTP status codes as exit codes | Exit codes > 127 are reserved by shell signal semantics; 403, 404, 429, 503 all conflict |
| Named error only in JSON, single exit code | Some orchestrators don't parse JSON; exit code is the primary diagnostic channel |

## Consequences

- All error handling in `_foundry_cli_common.py` must map SDK exceptions to these codes
- SDKs `PalantirRPCException` subclasses must be mapped: implementation must maintain a mapping table
- Test suite must verify exit codes for each error category
- Documentation must advise agents on recovery strategy per exit code

## References

- SRS FR-ERR-1 through FR-ERR-5
- SRS NFR-IFACE-1
- `foundry-platform-python/foundry_sdk/_errors/` — SDK exception hierarchy
