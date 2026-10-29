---
id: DEV-STORY-059
type: dev_story
title: Write Foundry REST API development guide
status: Closed
feature_request: FEATURE-013
epic: EPIC-013
created: 2026-10-04
updated: 2026-10-05
priority: High
resolution: Done
assignee: python-developer
reporter: ba
component: skills
story_points: 3
release_notes: A separate development guide explains Foundry REST API use and its SDK relationship.
---

# DEV-STORY-059: Write Foundry REST API development guide

## Description

## Scope and ownership
Own pal-found-dev REST API guide. Explain API resource choice, documented version and enrollment host, credentials and authorization, request/response parts, JSON/binary/stream forms, pagination, errors, rate limits, timeouts, write uncertainty, and SDK relationship. Include a source-checked read-only example. Coordinate entry-point link with DEV-STORY-057; do not edit its files.

## Acceptance criteria
- AC-D-014-05, AC-D-014-06, and AC-D-014-07 pass.
- Direct HTTP, Python SDK, OSDK, and installed CLI remain distinct.
- Example matches official API and local SDK docs; private or unsupported operations are not presented as generally available.

## Sources
FEATURE-013; BA-ANA-014; BA-DES-014; SA-DES-013. Grooming confirms one-sprint fit.
