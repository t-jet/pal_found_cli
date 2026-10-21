---
id: UNITTEST-058
type: unittest
title: Verify cleanup content boundaries
status: Closed
created: 2026-10-05
updated: 2026-10-05
priority: High
assignee: python-developer
reporter: project-manager
estimated_hours: 2
time_spent_hours: 0.5
---

# UNITTEST-058: Verify cleanup content boundaries

## Scope
Add focused static regression checks for the existing 19 distributed skill folders.

## Acceptance criteria
- Tests detect internal ADR, tracker, BA/SA, and local SDK path references addressed to users.
- Tests detect copy-folder instructions while allowing local navigation and public Palantir citations.
- Tests report offending file and text with useful failures and avoid rejecting normal Foundry development terminology.
- Existing 351-operation coverage and local-link checks continue to pass.
- Record command, result, and test evidence in the ticket.
