---
id: DEV-STORY-055
type: dev_story
title: Verify all offline Foundry skill coverage and copied bundles
status: Closed
feature_request: FEATURE-012
epic: EPIC-012
created: 2026-10-03
updated: 2026-10-12
priority: Medium
resolution: Done
assignee: python-developer
reporter: ba
component: skills
story_points: 16
release_notes: All 351 supported Foundry operations are covered and copied skill bundles work offline.
---

# Verify all offline Foundry skill coverage and copied bundles

## Scope
Own reusable supported-operation coverage, local-link, and offline mock/recorded-response checks plus final copied-bundle integration. Audit all 19 skill folders and the signed 351-operation review register; reject the four unsupported Widgets design rows as callable. This story does not replace each content story source-backed semantic review.

## Acceptance criteria
- Given the installed 351-operation parser and dispatch inventory, when compared in both directions with the copied skill bundle, then every supported operation has exactly one reachable record and no unsupported Widgets entry is callable.
- Given each operation record, when its signed 351-row trace is audited, then resource, effect, side effect, every applicable input meaning, result and failure interpretation, example, source and reviewer decision are present.
- Given all 19 copied skill folders without network access, when local links are checked and representative mocked or recorded paths are exercised in each of 18 namespaces, then an agent can select, prepare and interpret supported calls without missing guidance.

Trace: FEATURE-012, BA-ANA-013 BR-012-01..11 as applicable, BA-DES-013 AC-D-013-01..09 as applicable, and SA-DES-012. Grooming confirms one-sprint fit; no new CLI or Foundry operation. Remain New until FEATURE-012 reaches Waiting for Implementation.

The content stories own semantic signoff. This story verifies their signed rows and integration evidence; it does not repeat all 351 human semantic reviews.

## Source documents

- `.ept/docs/deliverables/business_analysis/BA-ANA-013-offline-foundry-knowledge.md`
- `.ept/docs/deliverables/business_design/BA-DES-013-offline-foundry-skill-guidance.md`
- `.ept/docs/deliverables/architecture/SA-DES-012-offline-foundry-skill-technical-design.md`
