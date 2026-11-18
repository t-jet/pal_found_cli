---
id: QUESTION-194
type: question
title: 'BUG-035 fix not deployable: land Audit correction 2190c40 into skills main and re-pin
  submodule'
status: Closed
addressed_to: python-developer
created: 2026-10-25
updated: 2026-10-26
priority: High
assignee: qa-engineer
reporter: qa-engineer
---

# QUESTION-194: BUG-035 fix not deployable: land Audit correction 2190c40 into skills main and re-pin submodule

## Description

QA failed the BUG-035 Resolved to Closed verification on 2026-10-25. The correction exists only on an unmerged branch.

## Research Done

- Studied `.ept/docs/document_index.md` and parent BUG-035 comments, links, and DoD.
- Read developer comment 20261022-101139-@python-developer~002 and PM comment 20261017-130527-@project-manager.
- Reviewed skills repo implementation files: `.agents/skills/pal-found-audit/SKILL.md` at HEAD 716a85b and at origin/feature015/integration 2190c40.
- Reviewed parent submodule pin via `git ls-tree HEAD pal_found_cli_skills` = 160000 commit 716a85b.
- Checked open QUESTION tickets for duplicates: none (QUESTION-194 only).

## Evidence
- Deployable skills HEAD 716a85b (parent submodule pin 160000 commit 716a85b) Audit page SHA256 = c040dd592980bf28a93285171a541211e8871b0879b7fc83f293b3e09c5d74ba (the original broken hash).
- Required strings api:audit-read, Create datasets with audit logs, and application service user are absent at skills HEAD.
- Corrected page SHA256 90f95b40... exists only on origin/feature015/integration 2190c40; git merge-base --is-ancestor 2190c40 716a85b returned exit 1.
- Focused tests at skills HEAD: 2 passed, 604 deselected; the claimed 75 focused Audit tests are not reproducible at the pin.

## Requested answer
1. Land the Audit correction (feature015/integration 2190c40) into skills main and merge to main.
2. Bump the parent pal_found_cli_skills submodule pin to the merged skills commit so the deployable page hash is 90f95b40...
3. Re-run the focused Audit tests at the merged commit and report exact counts.
4. Confirm whether a final retest is required.

## Blocking
LINK-01971 (BUG-035 Blocks DEV-STORY-061) is retained because the fix is not yet deployable. BUG-035 stays Resolved, not Closed, until the fix is verified at the deployable pin.
