---
id: DEV-002
type: development
title: Implement RetryHandler, ErrorSerializer, OutputFormatter, LogSetup
status: Resolved
created: 2026-05-17
updated: 2026-07-04
priority: Critical
assignee: developer
reporter: architect
---

# DEV-002: Implement RetryHandler, ErrorSerializer, OutputFormatter, LogSetup

## Description

## Implementation Tasks

Implement the four core components of the common error handling library as specified in the technical design (DESIGN-001).

### AC1: RetryHandler (`src/foundry_cli/utils/retry.py`)
- Class `RetryHandler` with configurable max_retries, base_delay, max_delay, jitter
- Exponential backoff: delay = min(base_delay * (2 ^ attempt), max_delay)
- Read env vars: FOUNDRY_MAX_RETRIES (default 3), FOUNDRY_RETRY_BASE_DELAY (default 1.0), FOUNDRY_RETRY_MAX_DELAY (default 30.0), FOUNDRY_RETRY_JITTER (default true)
- Decorator and context manager protocols
- Retries on configurable exception types (default: (requests.RequestException, requests.ConnectionError))
- Returns last response on exhaustion or raises

### AC2: ErrorSerializer (`src/foundry_cli/utils/error_serializer.py`)
- Class `ErrorSerializer` with method `serialize(exception) -> int`
- Maps SDK exceptions to exit codes 1-9 per ADR-001:
  - 1: General error
  - 2: Auth failure (AuthError)
  - 3: Validation error (ValidationError)
  - 4: Resource not found (ResourceNotFoundError)
  - 5: Rate limited (RateLimitError)
  - 6: Timeout (TimeoutError)
  - 7: Conflict (ConflictError)
  - 8: Permission denied (PermissionError)
  - 9: Network error (NetworkError)
- Includes error metadata in structured format
- Handles unknown exceptions gracefully

### AC3: OutputFormatter (`src/foundry_cli/utils/output_formatter.py`)
- Class `OutputFormatter` with `format(data, format_type=None) -> str`
- Supports JSON and TOON output formats
- Auto-selection per ADR-004: if --output flag present, use specified; else if stdout is terminal, use TOON; else use JSON
- TOON format: human-readable table/line format
- JSON format: pretty-printed with --pretty flag support
- Error output always goes to stderr

### AC4: LogSetup (`src/foundry_cli/utils/logging_setup.py`)
- Function `setup_logging()` with configure logging per ADR-005
- NDJSON structured logging format (one JSON object per line)
- Supports --debug flag for verbose output
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Includes timestamp, level, module, function, line, message, and context fields
- Configurable log file path via env var FOUNDRY_LOG_FILE
- File rotation support

### Dependencies
- Depends on DESIGN-001 (technical design)
- CODEREVIEW-002 is linked to this task for code review

### Acceptance Criteria
- [ ] All four components implemented in src/foundry_cli/utils/
- [ ] Code follows project style guide and passes linting
- [ ] Unit tests pass (see UNITTEST-002)
- [ ] Code review completed (see CODEREVIEW-002)
- [ ] Documentation updated in docs/api/
- [ ] No regressions in existing tests

Estimated: 13 story points, 32 hours

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
