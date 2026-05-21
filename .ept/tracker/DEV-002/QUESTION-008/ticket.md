---
id: QUESTION-008
type: question
title: 'DEV-002: Exit code mapping in ErrorSerializer conflicts with ADR-001'
status: Closed
addressed_to: tech-lead
created: 2026-05-18
updated: 2026-05-18
priority: Critical
assignee: tech-lead,architect
reporter: developer
---

# QUESTION-008: DEV-002: Exit code mapping in ErrorSerializer conflicts with ADR-001

## Description

Exit code mapping defined in DEV-002 AC2 (ErrorSerializer) does NOT match the approved ADR-001 taxonomy.

DEV-002 ticket defines:
  1: General error
  2: Auth failure (AuthError)
  3: Validation error (ValidationError)
  4: Resource not found (ResourceNotFoundError)
  5: Rate limited (RateLimitError)
  6: Timeout (TimeoutError)
  7: Conflict (ConflictError)
  8: Permission denied (PermissionError)
  9: Network error (NetworkError)

ADR-001 (Accepted, 2026-04-13) defines:
  1: UserInputError (invalid CLI args, validation failure, missing param)
  2: AuthenticationError (missing/invalid token, SDK auth failure)
  3: PermissionDeniedError (API 403)
  4: NotFoundError (API 404, resource does not exist)
  5: TimeoutError (asyncio.wait_for timeout, SIGINT/SIGTERM)
  6: ServerError (API 5xx excluding 503)
  7: RateLimitExhausted (HTTP 429 + retries exhausted)
  8: AccessControlError (CLI access control policy)
  9: ConfigurationError (missing env var, malformed config)

Key mismatches:
- Code 3: DEV-002 says ValidationError; ADR-001 says PermissionDeniedError
- Code 5: DEV-002 says RateLimitError; ADR-001 says TimeoutError
- Code 6: DEV-002 says Timeout; ADR-001 says ServerError
- Code 7: DEV-002 says ConflictError; ADR-001 says RateLimitExhausted
- Code 8: DEV-002 says PermissionDeniedError; ADR-001 says AccessControlError
- Code 9: DEV-002 says NetworkError; ADR-001 says ConfigurationError

Resolution required before DEV-002 implementation can proceed.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
