---
id: FEATURE-012
type: feature
title: Make Foundry skill definitions sufficient for offline agents
status: Waiting for Implementation
created: 2026-10-03
updated: 2026-10-03
priority: Medium
assignee: project-manager
reporter: project-manager
component: skills
---

# Make Foundry skill definitions sufficient for offline agents

## Description

An agent with no prior knowledge of Palantir Foundry must be able to read the installed skill definitions and use the supported CLI capabilities without internet access or additional guidance. Extend the existing brief platform and capability descriptions and the existing JSON format catalogue with operational context.

## Acceptance Criteria

- The skill set explains what Palantir Foundry is and how each covered platform capability works, using terms an unfamiliar agent can understand.
- For every supported skill function or CLI operation, the relevant skill definition explains what invoking it does in Foundry, including its observable effect and any material side effects.
- Every documented parameter has its meaning in Foundry, applicable resource or identifier, units or format where relevant, required or optional status, and how its value changes the operation.
- Each operation explains the shape and meaning of successful results, including identifiers, state changes, pagination or asynchronous outcomes where applicable, and the meaning of relevant errors or permission failures.
- Examples connect inputs to Foundry effects and results without relying on external documentation to fill conceptual gaps.
- A reviewer can trace every claim to the supported CLI behavior and authoritative Foundry source material; shared concepts remain consistent across skills.
- An agent using only the distributed skill files and installed CLI can select an operation, supply valid inputs, anticipate its Foundry effect, and interpret its result for each covered capability.

## Scope and relationships

This requirement extends the completed work in FEATURE-008 and FEATURE-009. It covers skill documentation and its verification. QUESTION-152 approved packaged local Markdown reference parts linked from each skill entry point. Implementation planning, code changes, and release work follow later workflow stages.
