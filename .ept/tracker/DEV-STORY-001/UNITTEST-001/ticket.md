---
id: UNITTEST-001
type: unittest
title: 'UNITTEST: DEV-STORY-001 — ConfigLoader, AuthProvider, AsyncClientFactory'
status: Closed
created: 2026-05-17
updated: 2026-05-20
priority: Critical
assignee: developer
reporter: architect
estimated_hours: 20
---

Create unit tests for ConfigLoader, AuthProvider, and AsyncClientFactory components.

## Test Categories

### ConfigLoader Tests
- [ ] Test search path: explicit env file path exists
- [ ] Test search path: git root .env detection (pathlib ancestor walk)
- [ ] Test search path: CWD fallback when no git root
- [ ] Test search path: env vars only when no .env found
- [ ] Test FOUNDRY_AGENTIC_CLI_ENV_FILE override
- [ ] Test load_dotenv(override=False) - shell env vars take precedence
- [ ] Test ConfigurationError raised when explicit env file path doesn't exist
- [ ] Test get_str() returns correct string values
- [ ] Test get_bool() parses true/false, yes/no, 1/0 correctly
- [ ] Test get_int() parses integer values correctly
- [ ] Test get_float() parses float values correctly
- [ ] Test get_enum() validates against allowed values
- [ ] Test typed config for all 20+ global env vars
- [ ] Test git root detection max depth (20 levels)
- [ ] Test config value hierarchy resolution

### AuthProvider Tests
- [ ] Test FOUNDRY_TOKEN resolution from config
- [ ] Test UserTokenAuth construction from token string
- [ ] Test credential presence validation
- [ ] Test exit code 9 on missing token config
- [ ] Test FOUNDRY_HOSTNAME resolution from config
- [ ] Test no credential logging (security test)
- [ ] Test empty token handling
- [ ] Test invalid token format handling

### AsyncClientFactory Tests
- [ ] Test AsyncFoundryClient creation per invocation (stateless)
- [ ] Test attribution header injection when ENABLE_ATTRIBUTION=true
- [ ] Test no attribution headers when ENABLE_ATTRIBUTION=false
- [ ] Test token validation before client creation
- [ ] Test ConfigLoader dependency injection
- [ ] Test missing token raises ConfigurationError
- [ ] Test client creation with FOUNDRY_HOSTNAME

### Test Quality Requirements
- [ ] All tests use pytest framework
- [ ] Test coverage target: 90%+ for all three components
- [ ] Mock external dependencies (foundry-auth, foundry-platform-python SDK)
- [ ] No integration tests in this sub-task (handled by TESTCASE-001)
- [ ] Tests are fast and deterministic

Acceptance Criteria:
- [ ] All unit tests pass with pytest
- [ ] Test coverage meets 90%+ target
- [ ] No flaky tests
- [ ] Tests run in CI pipeline successfully
