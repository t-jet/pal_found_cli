---
id: QUESTION-189
type: question
title: pal-found-data-health distributed folder contains an executable fixture script
status: Closed
addressed_to: tech-lead
created: 2026-10-12
updated: 2026-10-12
priority: High
assignee: tech-lead
reporter: devops-engineer
time_spent_hours: 2
---

# QUESTION-189: pal-found-data-health distributed folder contains an executable fixture script

## Description

## Question

The distributed `pal-found-data-health` skill folder contains a Python validation fixture and 16 JSON payload files:

- `.agents/skills/pal-found-data-health/examples/check_config_fixture.py` (SHA-256 `50bfd10a6b3722bac66c0b46936106704d0537a9b30c0d97c7a2b7f4b84dc5e6`, 3681 bytes, git-tracked)
- `.agents/skills/pal-found-data-health/examples/check-config/*.json` (16 tracked files)
- `.agents/skills/pal-found-data-health/references/check-config.md` L72 instructs the reader: `Run \`python -B examples/check_config_fixture.py\` from this skill directory.`

Found while validating the copied folder for DEVOPS-039 (DEV-STORY-048); the same fixture is inside the DEVOPS-046 bundle.

## Research done

- SA-DES-012 section 1.1: "A skill folder contains documentation only; the installed `pal_found_cli` package executes commands." Section 2: "No executable script belongs in a distributed skill folder." Section 5 local-distribution gate: "no script files or stale launcher commands".
- The fixture does not depend on repository-external paths: it reads the sibling `check-config/*.json` and imports `foundry_sdk` (the same SDK the CLI itself requires), so it is self-contained when the folder is copied.
- The repo gate `test_offline_skill_gate.py::test_leaf_files_respect_300_line_limit` and `test_relative_links_resolve_within_skill_folder` pass on this folder, so no current gate rejects the fixture.

## Question

Is `examples/check_config_fixture.py` (plus its JSON payloads) an approved offline validation payload for a distributed skill folder, or does the FEATURE-012 rule "no script files / documentation only" require it to move out of `.agents/skills/pal-found-data-health/`?

## Impact

- Blocks `DEVOPS-039` (DEV-STORY-048) and `DEVOPS-046` (DEV-STORY-055 bundle), which must both assert "no script files" for the copied folders.

## Requested answer

State the ruling (approved payload or must move) and, if it must move, which story owns the move.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
