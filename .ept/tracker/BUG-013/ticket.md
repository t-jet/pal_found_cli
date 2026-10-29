---
id: BUG-013
type: bug
title: Ontology edits history CLI passes object primary key as string
status: Closed
affected_version: pal_found_cli_tool-worktree
created: 2026-10-12
updated: 2026-10-14
priority: High
resolution: Done
assignee: python-developer
reporter: project-manager
component: ontologies
---

# BUG-013: Ontology edits history CLI passes object primary key as string

## Description

# Defect
object_type.get_edits_history accepts --object-primary-key as a plain string because the CLI operation spec omits it from json_args. The SDK requires ObjectPrimaryKeyV2, a mapping from property API name to typed primary-key value. A valid object key supplied through the CLI fails SDK validation.

## Expected
CLI parses JSON object input for --object-primary-key and forwards a mapping to SDK. Skill record explains the JSON shape and has a valid example.

## Acceptance criteria
- Add targeted JSON input coercion without changing unrelated string arguments.
- Test valid mapping, invalid JSON, SDK invocation, and CLI help/example.
- Independent QA verifies mocked get_edits_history request and offline skill guidance.

Related: FEATURE-012 DEV-STORY-047 and WORK-005.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
