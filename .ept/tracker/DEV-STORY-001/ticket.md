---
id: DEV-STORY-001
type: dev_story
title: Implement ConfigLoader, AuthProvider, AsyncClientFactory
status: Grooming
feature_request: FEATURE-001
epic: EPIC-001
created: 2026-04-13
updated: 2026-05-17
priority: Critical
assignee: architect
reporter: architect
release_notes: 'Initial release of _foundry_cli_common.py foundational components: ConfigLoader (env
  file loading with git-root search per ADR-006), AuthProvider (UserTokenAuth wrapper
  with credential validation), AsyncClientFactory (stateless AsyncFoundryClient creation
  with attribution header support). Exit codes 2 (AuthenticationError) and 9 (ConfigurationError)
  implemented per ADR-001.'
---

# DEV-STORY-001: Implement ConfigLoader, AuthProvider, AsyncClientFactory

## Description

Implement the first batch of _foundry_cli_common.py components. ConfigLoader: loads .env via python-dotenv using search path (ADR-006); resolves env var hierarchy. AuthProvider: wraps UserTokenAuth with token-from-env resolution. AsyncClientFactory: creates AsyncFoundryClient per invocation; validates token present before creation.

## Acceptance Criteria

### ConfigLoader
- [ ] Implements ADR-006 search path: (1) explicit env file override via FOUNDRY_AGENTIC_CLI_ENV_FILE, (2) git root .env, (3) CWD fallback, (4) env vars only — no home dir fallback
- [ ] Uses python-dotenv load_dotenv(override=False); shell env vars take precedence
- [ ] Git root detection via pathlib ancestor walk with depth limit (max 20 levels)
- [ ] Raises ConfigurationError (exit code 9) if explicit env file path does not exist
- [ ] Exposes typed config values (bool, int, float, string, enum) for all 20+ global env vars from canonical-env-var-reference.md

### AuthProvider
- [ ] Resolves FOUNDRY_TOKEN from config (env var or .env)
- [ ] Constructs UserTokenAuth from token string
- [ ] Validates credential presence; returns exit code 9 on missing config
- [ ] Resolves FOUNDRY_HOSTNAME from config
- [ ] No credentials logged or written to stdout (security requirement)

### AsyncClientFactory
- [ ] Creates AsyncFoundryClient instance per invocation (stateless per invocation pattern)
- [ ] Injects attribution headers when ENABLE_ATTRIBUTION=true
- [ ] Validates token is present before client creation
- [ ] Accepts ConfigLoader instance as dependency

## Related Documentation

- [ADR-006 — .env File Search Path](.ept/docs/deliverables/architecture/adr/ADR-006-env-file-search-path.md)
- [ADR-001 — Exit Code Taxonomy](.ept/docs/deliverables/architecture/adr/ADR-001-exit-code-taxonomy.md) — Exit code 9 (ConfigurationError)
- [SAD-001 — Solution Architecture Document](.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md) — §4 C4 Component Diagram, §5 Code Structure, §6 Sequence Diagrams
- [SRS-001 — Software Requirements Specification](.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md)
- [Canonical Environment Variable Reference](.ept/docs/deliverables/architecture/canonical-env-var-reference.md) — Global Configuration Variables section

## Technical Scope

### Component: ConfigLoader
- **Purpose:** Load and validate configuration from .env file and environment variables
- **Search path (ADR-006):** FOUNDRY_AGENTIC_CLI_ENV_FILE → git root .env → CWD fallback → env vars only
- **Dependencies:** python-dotenv (load_dotenv with override=False)
- **Key methods:** load(), get_str(), get_bool(), get_int(), get_float(), get_enum()
- **Error handling:** ConfigurationError with exit code 9 per ADR-001

### Component: AuthProvider
- **Purpose:** Handle OAuth2 token acquisition and validation
- **Inputs:** FOUNDRY_TOKEN, FOUNDRY_HOSTNAME from ConfigLoader
- **Output:** UserTokenAuth instance from foundry-auth library
- **Error handling:** ConfigurationError (exit code 9) if token missing

### Component: AsyncClientFactory
- **Purpose:** Create configured AsyncFoundryClient instances per invocation
- **Inputs:** UserTokenAuth from AuthProvider, config from ConfigLoader
- **Output:** AsyncFoundryClient with attribution headers when enabled
- **Dependencies:** foundry-auth, foundry-platform-python SDK

## Notes

- All three components are foundational — every CLI operation depends on them
- ConfigLoader is called first in the invocation chain (see SAD-001 §6.1 sequence diagram)
- AuthProvider wraps foundry-auth's UserTokenAuth (SDK-native auth mechanism)
- AsyncClientFactory creates AsyncFoundryClient per invocation (no caching across invocations)
- Security constraint: No credentials logged or written to stdout
