---
id: DEV-STORY-039
type: dev_story
title: Migrate datasets and ontologies command implementations to the tool and remove stale skill copies
status: Closed
feature_request: FEATURE-011
epic: EPIC-011
created: 2026-09-30
updated: 2026-10-01
priority: High
resolution: Done
assignee: tech-lead
reporter: ba
component: skills
story_points: 5
release_notes: Remove the stale datasets and ontologies command copies from the skills repository and confirm pal-found-datasets and pal-found-ontologies preserve all operations and behavior as the single tool-side implementation.
---

# DEV-STORY-039: Migrate datasets and ontologies command implementations to the tool and remove stale skill copies

## Description

Remove the standalone datasets and ontologies command copies from the skills
repository: `scripts/pal_found_datasets_cli.py` (467 lines) and
`scripts/pal_found_ontologies_cli.py` (442 lines). Confirm the tool's
installed `pal-found-datasets` and `pal-found-ontologies` commands cover the
same operations with unchanged behavior (verified supersets at analysis; no
net-new tool command is expected). The tool becomes the single source of
behavior for both namespaces.

## Acceptance Criteria

- [ ] Given the datasets skill, when the skill copy is removed, then all datasets operations remain available through `pal-found-datasets` with unchanged behavior (AC-D-012-04).
- [ ] Given the ontologies skill, when the skill copy is removed, then all ontologies operations remain available through `pal-found-ontologies` with unchanged behavior (AC-D-012-05).
- [ ] Given an existing customer of the tool, when the migration ships, then all 18 `pal-found-*` commands remain installed and callable without change (AC-D-012-07).

## Related Documentation

- `.ept/docs/deliverables/business_design/BA-DES-012-doc-only-skills.md`
- `.ept/docs/deliverables/business_analysis/BA-ANA-012-doc-only-skills.md`
