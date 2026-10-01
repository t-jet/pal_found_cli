---
id: DEV-STORY-040
type: dev_story
title: Update distribution, onboarding, and evidence for documentation-only skills
status: Closed
feature_request: FEATURE-011
epic: EPIC-011
created: 2026-09-30
updated: 2026-10-01
priority: High
resolution: Done
assignee: qa-engineer
reporter: ba
component: skills
story_points: 3
release_notes: Update distribution and onboarding documentation to describe skills as documentation-only, state the tool install prerequisite, sweep all 18 SKILL.md files for stale python ..._cli.py references, and run the doc-only acceptance criteria and behavior checks.
---

# DEV-STORY-040: Update distribution, onboarding, and evidence for documentation-only skills

## Description

Update the distribution and onboarding documentation so skills are described
as documentation only and the tool install prerequisite is stated. Sweep all
18 namespace `SKILL.md` files for any stale `python ..._cli.py` reference or
script mention and remove them. Run the doc-only acceptance criteria,
including datasets and ontologies behavior checks, and capture evidence tied
to the delivered commit and final skill layout.

## Acceptance Criteria

- [ ] Given the skills repository, when it is distributed, then every delivered skill consists solely of documentation that references installed tool commands (AC-D-012-06).
- [ ] Given the distribution and onboarding docs, when they are read, then they state skills are documentation-only and that the tool must be installed first (AC-D-012-08).
- [ ] Given a sweep of all 18 `SKILL.md` files, when each is read, then no `python ..._cli.py` example or script reference remains (AC-D-012-02).
- [ ] Given the behavior checks, when datasets and ontologies are exercised, then behavior is unchanged via the tool commands (AC-D-012-04, AC-D-012-05).

## Related Documentation

- `.ept/docs/deliverables/business_design/BA-DES-012-doc-only-skills.md`
- `.ept/docs/deliverables/business_analysis/BA-ANA-012-doc-only-skills.md`
