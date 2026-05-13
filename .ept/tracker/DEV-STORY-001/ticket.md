---
id: DEV-STORY-001
type: dev_story
title: Implement ConfigLoader, AuthProvider, AsyncClientFactory
status: New
feature_request: FEATURE-001
epic: EPIC-001
created: 2026-04-13
updated: 2026-05-13
priority: Critical
assignee: architect
reporter: architect
---

# DEV-STORY-001: Implement ConfigLoader, AuthProvider, AsyncClientFactory

## Description

Implement the first batch of _foundry_cli_common.py components. ConfigLoader: loads .env via python-dotenv using search path (ADR-006); resolves env var hierarchy. AuthProvider: wraps UserTokenAuth with token-from-env resolution. AsyncClientFactory: creates AsyncFoundryClient per invocation; validates token present before creation.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
