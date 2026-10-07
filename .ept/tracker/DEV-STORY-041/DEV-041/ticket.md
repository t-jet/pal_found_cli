---
id: DEV-041
type: development
title: 'DEV-041: Author offline Foundry platform primer and namespace navigation in pal-found
  skill'
status: Resolved
created: 2026-10-03
updated: 2026-10-03
priority: High
assignee: python-developer
reporter: tech-lead
estimated_hours: 20
time_spent_hours: 3
---

# DEV-041: Author offline Foundry platform primer and namespace navigation in pal-found skill

## Description

Author the general pal-found skill deliverable per SA-DES-012/BA-DES-013: rewrite pal_found_cli_skills/.agents/skills/pal-found/SKILL.md as platform primer + navigation map, and author references/*.md local parts (identifiers, authorization, shared result/failure, output formats, exit codes, retry/timeout, paging). Keep each leaf <=300 lines, preserve FEATURE-008/009 content and FEATURE-011 install prerequisite block, use relative links that resolve offline. Docs-only; no CLI code.

## Acceptance Criteria

- Given a novice agent offline, when it reads the authored general skill, then it can map a supported task to the relevant Foundry resource and its namespace without a web page.
- Given the copied general skill folder, when its local links are checked, then every required part (navigation, references, namespace entry points) resolves within that folder.
- Given the shared guidance parts (identifiers, authorization, result/failure, output formats, exit codes, retry/timeout, paging), when reviewed against installed CLI behavior and authoritative Foundry sources, then meaning and limits are accurate and traceable.
- Given the authored leaf files, when their lengths and links are validated, then each leaf is <=300 lines and uses relative offline-resolving links.
- Given the skill folder, when FEATURE-008/009 topic content and the FEATURE-011 install prerequisite block are checked, then existing content is preserved and the block still states the python-package dependency with short conda/pip/uv install instructions.
- Given the general skill as the entry point, when it is read alongside any namespace skill, then no namespace is presented as callable unless it has a reachable, documented record.

## Related Documentation

- Parent story: DEV-STORY-041 (Offline Foundry platform primer and navigation)
- BA-DES-013: `.ept/docs/deliverables/business_design/BA-DES-013-offline-foundry-skill-guidance.md`
- SA-DES-012: `.ept/docs/deliverables/architecture/SA-DES-012-offline-foundry-skill-technical-design.md`
- BA-ANA-013: `.ept/docs/deliverables/business_analysis/BA-ANA-013-offline-foundry-knowledge.md`
- FEATURE-011 (install prerequisite) and FEATURE-012 (epic): feature_request = FEATURE-012

## Notes

Doc-only deliverable; no CLI or Foundry operation is added. This story owns the general `pal-found` entry point and navigation map; each namespace folder stays independently usable. No frozen op register applies (this is the general primer story).
