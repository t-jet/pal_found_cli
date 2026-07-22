---
id: DEV-001
type: development
title: 'DEV-STORY-001: Implement ConfigLoader, AuthProvider, AsyncClientFactory'
status: Closed
created: 2026-05-17
updated: 2026-07-05
priority: Critical
assignee: architect
reporter: architect
estimated_hours: 40
---

# DEV-001: DEV-STORY-001: Implement ConfigLoader, AuthProvider, AsyncClientFactory

## Description

Implement the three foundational components for _foundry_cli_common.py.

## Component 1: ConfigLoader
- Load .env via python-dotenv using search path per ADR-006:
  1. Explicit env file override via FOUNDRY_AGENTIC_CLI_ENV_FILE
  2. Git root .env (pathlib ancestor walk, max 20 levels)
  3. CWD fallback
  4. Env vars only (no home dir fallback)
- Uses load_dotenv(override=False); shell env vars take precedence
- Raises ConfigurationError (exit code 9) if explicit env file path doesn't exist
- Exposes typed config values: get_str(), get_bool(), get_int(), get_float(), get_enum()
- Typed config for all 20+ global env vars from canonical-env-var-reference.md

## Component 2: AuthProvider
- Resolve FOUNDRY_TOKEN from config (env var or .env)
- Construct UserTokenAuth from token string
- Validate credential presence; return exit code 9 on missing config
- Resolve FOUNDRY_HOSTNAME from config
- No credentials logged or written to stdout (security requirement)

## Component 3: AsyncClientFactory
- Create AsyncFoundryClient instance per invocation (stateless)
- Inject attribution headers when ENABLE_ATTRIBUTION=true
- Validate token present before client creation
- Accept ConfigLoader instance as dependency

Acceptance Criteria:
- [ ] ConfigLoader implements ADR-006 search path correctly
- [ ] ConfigLoader uses load_dotenv(override=False)
- [ ] ConfigLoader raises ConfigurationError (exit code 9) for missing explicit env file
- [ ] ConfigLoader exposes typed config accessors (get_str, get_bool, get_int, get_float, get_enum)
- [ ] AuthProvider resolves FOUNDRY_TOKEN from config
- [ ] AuthProvider constructs UserTokenAuth
- [ ] AuthProvider validates credential presence
- [ ] AuthProvider resolves FOUNDRY_HOSTNAME
- [ ] AuthProvider does NOT log credentials
- [ ] AsyncClientFactory creates stateless AsyncFoundryClient per invocation
- [ ] AsyncClientFactory injects attribution headers when ENABLE_ATTRIBUTION=true
- [ ] AsyncClientFactory validates token before client creation
- [ ] AsyncClientFactory accepts ConfigLoader as dependency

Related Documentation:
- ADR-006 - .env File Search Path
- ADR-001 - Exit Code Taxonomy (exit code 9)
- SAD-001 - Solution Architecture Document
- Canonical Environment Variable Reference


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
