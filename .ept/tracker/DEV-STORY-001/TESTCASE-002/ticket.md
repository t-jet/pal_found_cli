---
id: TESTCASE-002
type: testcase
title: 'TESTCASE: DEV-STORY-001 — Integration & E2E Tests for ConfigLoader, AuthProvider,
  AsyncClientFactory'
status: Closed
created: 2026-05-17
updated: 2026-05-19
priority: Critical
assignee: qa-engineer
reporter: architect
estimated_hours: 16
---

# TESTCASE-002: TESTCASE: DEV-STORY-001 — Integration & E2E Tests for ConfigLoader, AuthProvider, AsyncClientFactory

## Description

Create integration and end-to-end test cases for ConfigLoader, AuthProvider, and AsyncClientFactory components.

## Test Scenarios

### ConfigLoader Integration Tests
- [ ] Test .env file loading from git root directory
- [ ] Test .env file loading from CWD when no git root
- [ ] Test FOUNDRY_AGENTIC_CLI_ENV_FILE override works
- [ ] Test env var precedence over .env values
- [ ] Test missing explicit env file path returns exit code 9
- [ ] Test all 20+ global env vars loaded and accessible with correct types

### AuthProvider Integration Tests
- [ ] Test token resolution from .env file
- [ ] Test token resolution from env var
- [ ] Test UserTokenAuth receives valid token string
- [ ] Test missing FOUNDRY_TOKEN returns exit code 9
- [ ] Test FOUNDRY_HOSTNAME resolved correctly
- [ ] Test credential never appears in logs or stdout

### AsyncClientFactory Integration Tests
- [ ] Test client creation with valid token
- [ ] Test attribution headers injected when ENABLE_ATTRIBUTION=true
- [ ] Test no attribution headers when ENABLE_ATTRIBUTION=false
- [ ] Test client NOT created when token missing (exit code 9)
- [ ] Test client receives FOUNDRY_HOSTNAME config
- [ ] Test stateless pattern - new instance per invocation

### E2E Scenario Tests
- [ ] Full invocation: load config → authenticate → create client → make API call
- [ ] Failure path: missing token → exit code 9
- [ ] Failure path: invalid env file path → exit code 9
- [ ] Failure path: missing FOUNDRY_HOSTNAME → graceful error
- [ ] Security: verify no credentials in any output or logs

### Test Environment Requirements
- [ ] Test fixtures create temporary .env files
- [ ] Test fixtures mock foundry-auth and foundry-platform-python SDK
- [ ] Test fixtures set up git repo for git root detection tests
- [ ] Clean up temp files after tests

Acceptance Criteria:
- [ ] All integration test cases defined and documented
- [ ] All E2E scenarios covered
- [ ] Test cases executable via pytest
- [ ] Security test cases verify no credential leakage
- [ ] Test environment properly isolated

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
