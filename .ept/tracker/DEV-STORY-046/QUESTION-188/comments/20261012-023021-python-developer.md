Subject: Answer: replace labels with reader prose and extend the hygiene gate
Created: 2026-10-12T02:30:21
Updated: 2026-10-12T02:30:21
---
## Answer (python-developer)

Yes to both parts of the question. The two parenthetical labels are internal
tracker sub-task ids that must not reach a reader, and the hygiene gate must
reject the bare `DEV-<n>` form as well.

### Ruling

- The labels `(DEV-046)` and `(DEV-047)` are internal development sub-task ids
  from this project's tracker. They carry no meaning for a reader who receives
  the copied skill folder, and BA-ANA-014 requires distributed skills to carry
  no internal project development references.
- Replace them with reader-facing wording that keeps the same meaning, and do
  not introduce any other ticket id in their place.
- The hygiene test must be extended. The existing
  `test_foundry_development_skill.py::test_distributed_skills_omit_project_internals_and_copy_directions`
  match only covers `FEATURE|DEV-STORY|CODEREVIEW-<n>`; the bare sub-task form
  (`DEV-046`) is the same class of internal reference and slipped through.

### Wording chosen

The two parts are already named by the sentence itself ("the discovery part"
and "the action/rich-property part") and by the table below it, so the
parentheticals can simply drop:

> The 67 operations are split into two disjoint parts. The discovery part
> covers reading the ontology model; the action/rich-property part covers
> executing actions and reading attachments, media, and time series.

The sentence keeps the exact same meaning and the part split stays traceable
through the `## Operation index` table rows that follow.

### Ownership

The fix is a content fix and it is owned by the developer for the story, as
the requester stated. No tracker link changes are needed here.
