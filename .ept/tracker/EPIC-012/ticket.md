---
id: EPIC-012
type: epic
title: Use Foundry CLI skills with no external guidance
status: In Progress
created: 2026-10-03
updated: 2026-10-03
priority: Medium
assignee: project-manager
reporter: project-manager
---

# Use Foundry CLI skills with no external guidance

## Description

End-to-end scenario: an agent unfamiliar with Palantir Foundry receives a user task, reads the distributed skill definitions offline, chooses a supported CLI operation, supplies Foundry-specific inputs, predicts its effect, invokes it, and interprets the returned result or failure. The skills carry the platform and operation knowledge needed for this path.

## Acceptance Criteria

- The linked Feature covers the complete path from understanding Foundry to interpreting operation results.
- The skill documentation remains consistent with the supported CLI surface and Foundry concepts.
- Later Developer Stories cover the skill groups and shared guidance needed to satisfy the Feature's acceptance criteria.
