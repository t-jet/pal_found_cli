---
id: UNITTEST-002
type: unittest
title: 'UNITTEST: Write unit tests for RetryHandler, ErrorSerializer, OutputFormatter, LogSetup'
status: Resolved
created: 2026-05-17
updated: 2026-05-20
priority: Critical
assignee: developer
reporter: architect
estimated_hours: 20
---

# UNITTEST-002: UNITTEST: Write unit tests for RetryHandler, ErrorSerializer, OutputFormatter, LogSetup

## Description

## Unit Test Task

Write comprehensive unit tests for the four error handling library components.

### Test Module Structure
Create test files under 	ests/unit/utils/:
- 	est_retry_handler.py
- 	est_error_serializer.py
- 	est_output_formatter.py
- 	est_logging_setup.py

### AC1: RetryHandler Tests (	est_retry_handler.py)
- Test exponential backoff calculation
- Test configurable max_retries, base_delay, max_delay, jitter
- Test env var overrides (FOUNDRY_MAX_RETRIES, FOUNDRY_RETRY_BASE_DELAY, etc.)
- Test decorator protocol
- Test context manager protocol
- Test exception handling and retry on specific exception types
- Test retry exhaustion (max retries reached)
- Test last response returned on exhaustion
- Test jitter enabled/disabled
- Test edge cases (zero retries, single retry, negative delay handling)

### AC2: ErrorSerializer Tests (	est_error_serializer.py)
- Test all exit code mappings (1-9 per ADR-001)
- Test AuthError -> exit code 2
- Test ValidationError -> exit code 3
- Test ResourceNotFoundError -> exit code 4
- Test RateLimitError -> exit code 5
- Test TimeoutError -> exit code 6
- Test ConflictError -> exit code 7
- Test PermissionError -> exit code 8
- Test NetworkError -> exit code 9
- Test unknown exception -> exit code 1 (general error)
- Test error metadata in structured format
- Test nested exception handling

### AC3: OutputFormatter Tests (	est_output_formatter.py)
- Test JSON output format
- Test TOON output format
- Test auto-selection (terminal -> TOON, pipe -> JSON)
- Test --output flag override
- Test --pretty flag for JSON formatting
- Test error output goes to stderr
- Test empty data handling
- Test large data output

### AC4: LogSetup Tests (	est_logging_setup.py)
- Test NDJSON structured logging format
- Test log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Test --debug flag enables verbose output
- Test FOUNDRY_LOG_FILE env var for log file path
- Test file rotation
- Test required fields: timestamp, level, module, function, line, message
- Test context field inclusion

### DoD
- 100% pass rate on all unit tests
- Code coverage meets project standards (target: 90%+)
- All tests committed to repository
- Tests run successfully in CI pipeline

Estimated: 8 story points, 20 hours

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
