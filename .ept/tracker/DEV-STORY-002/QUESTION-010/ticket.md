---
id: QUESTION-010
type: question
title: 'QUESTION: TC1.R1 env var naming — FOUNDRY_* vs FOUNDRY_AGENTIC_CLI_RETRY_* (AC conflict)'
status: New
addressed_to: architect
created: 2026-07-04
updated: 2026-07-04
priority: Critical
reporter: qa-engineer
---

# QUESTION-010: QUESTION: TC1.R1 env var naming — FOUNDRY_* vs FOUNDRY_AGENTIC_CLI_RETRY_* (AC conflict)

## Description

AC for DEV-STORY-002 RetryHandler specifies env var prefix FOUNDRY_AGENTIC_CLI_RETRY_* but implementation uses FOUNDRY_MAX_RETRIES/RETRY_BASE_DELAY/RETRY_MAX_DELAY/RETRY_JITTER (prefix FOUNDRY_*). Which is authoritative? Source: TESTCASE-001 comment 20260704-224649-qa-engineer. Need decision: (a) update AC and keep FOUNDRY_*, (b) update implementation to FOUNDRY_AGENTIC_CLI_RETRY_*, or (c) support both with deprecation. ADR/env-var documentation references need to be aligned either way.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
