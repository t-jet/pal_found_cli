---
id: DEV-STORY-041
type: dev_story
title: Document offline Foundry platform primer and navigation
status: New
feature_request: FEATURE-012
epic: EPIC-012
created: 2026-10-03
updated: 2026-10-03
priority: Medium
assignee: ba
reporter: ba
component: skills
release_notes: Agents can use an offline Foundry primer and namespace navigation to select supported capabilities.
---

# Offline Foundry platform primer and navigation

## Scope
Own the general `pal-found` skill entry point and any local reference parts. Explain Foundry resources, identifiers, relationships, authorization, shared result/failure concepts, and how a novice agent chooses a namespace and follow-up. Preserve FEATURE-008 descriptions and FEATURE-011 installed-command prerequisite. The general skill is broad context; each namespace folder remains independently usable.

## Acceptance criteria
- Given a novice agent offline, when it reads the general skill, then it can map a supported task to the relevant Foundry resource and namespace without a web page.
- Given a copied general skill folder, when its local links are checked, then every required part resolves within that folder.
- Given shared access, output, paging, retry or timeout guidance, when it is reviewed against installed CLI behavior and authoritative Foundry sources, then its meaning and limits are accurate and traceable.

Trace: BR-012-01,02,07,09,10; AC-D-013-01,06,07,08. No CLI or Foundry operation is added. Grooming must confirm one-sprint fit.

## Source documents

- `.ept/docs/deliverables/business_analysis/BA-ANA-013-offline-foundry-knowledge.md`
- `.ept/docs/deliverables/business_design/BA-DES-013-offline-foundry-skill-guidance.md`
- `.ept/docs/deliverables/architecture/SA-DES-012-offline-foundry-skill-technical-design.md`
