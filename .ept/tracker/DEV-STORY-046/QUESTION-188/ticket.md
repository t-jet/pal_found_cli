---
id: QUESTION-188
type: question
title: pal-found-ontologies SKILL.md ships internal tracker labels DEV-046/DEV-047
status: Closed
addressed_to: python-developer
created: 2026-10-12
updated: 2026-10-12
priority: High
assignee: devops-engineer
reporter: devops-engineer
---

# QUESTION-188: pal-found-ontologies SKILL.md ships internal tracker labels DEV-046/DEV-047

## Description

## Question

The distributed `pal-found-ontologies` skill ships two internal tracker sub-task labels in reader prose:

- `.agents/skills/pal-found-ontologies/SKILL.md` L61: `(DEV-046) covers reading the ontology model; the action/rich-property part`
- `.agents/skills/pal-found-ontologies/SKILL.md` L62: `(DEV-047) covers executing actions and reading attachments, media, and time`

File SHA-256 `4852d2ee7cb06a2f42e9ef89d9f2a3a06de902172bccfad5e80ae6c539b9e09a` (5732 bytes) at the pinned skills commit `419b261`.
Found while validating the copied folder for DEVOPS-037 (DEV-STORY-046) and DEVOPS-038 (DEV-STORY-047); also inside the DEVOPS-046 bundle.

## Research done

- SA-DES-012 section 5 requires the copied folder to carry "no script files or stale launcher commands" and section 1.1 states "The source citations remain maintenance evidence, not runtime instructions". BA-ANA-014 requires removing internal project development references from distributed skills.
- The skills repo hygiene test `tests/test_foundry_development_skill.py::test_distributed_skills_omit_project_internals_and_copy_directions` forbids `.ept/`, `ADR-<n>`, `BA|SA-(ANA|DES)-<n>`, `FEATURE|DEV-STORY|CODEREVIEW-<n>`, `docs/customer_input`, and `copy <...> folder`. It does **not** match the bare `DEV-<n>` sub-task form, which is why this leak passes the gate today. The bare form is the same class of internal reference.
- `git log -S "DEV-046"` shows commit `45bc51d` reintroduced the label into the distributable paragraph; `090ebdf` (the DEV-046 story commit) introduced it.

## Question

Should the two parenthetical labels be replaced with reader-facing wording (for example "the discovery part" / "the action and rich-property part") and the hygiene test extended to also reject the bare `DEV-<n>` sub-task form?

## Impact

- Blocks `DEVOPS-037` (DEV-STORY-046), `DEVOPS-038` (DEV-STORY-047) and `DEVOPS-046` (DEV-STORY-055 bundle).

## Requested answer

Confirm the wording to use and whether the hygiene test must be extended (devops-engineer does not patch skill content; this is a content fix owned by the developer for the story).

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
