---
id: DEV-012
type: development
title: Implement Foundry Language Models CLI and Claude skill
status: Closed
created: 2026-08-09
updated: 2026-08-09
priority: High
assignee: python-developer
reporter: python-developer
estimated_hours: 10
time_spent_hours: 10
---

# DEV-012: Implement Foundry Language Models CLI and Claude skill

## Description

Implement the Language Models package and installed Claude skill for the corrected two-operation contract.

## Acceptance Criteria

- Add the exact catalog, nested SDK routing, parser, scalar options, and eight validated public JSON flags with exact internal SDK keywords.
- Add messages and embeddings to AccessControlGuard _WRITE_VERBS; enforce guard-before-client, read-only overrides, metadata-only, and Tier 3 behavior.
- Scope attribution=True and SDK-native B3 across retries with restoration on every exit path.
- Add structured JSON output/errors, privacy-safe logging, retry/timeout behavior, policy, skill, launcher, console entry, and package data.
- Ruff and mypy pass.

## Related Documentation

- DEV-STORY-012
- DESIGN-012

## Notes

Blocked on approved design.
