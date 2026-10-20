---
id: BUG-042
type: bug
title: Orchestration build search parser accepts missing SDK-required where filter
status: In Progress
affected_version: 0963e6e006f82ad1997be0e22c6b750ed0bbce3b
created: 2026-10-20
updated: 2026-10-20
priority: High
assignee: python-developer
reporter: project-manager
component: orchestration-cli
---

# BUG-042: Orchestration build search parser accepts missing SDK-required where filter

## Description

## Observed defect
Pinned tool0963e6e006f82ad1997be0e22c6b750ed0bbce3b with SDK1.101.0 permits orchestration build.search invocation without --where-json, although the SDK method requires where. Independent QA found unfiltered example fails real SDK validation; guide now supplies valid STATUS/RUNNING filter but parser defect remains.

## Reproduce and evidence
Inspect build.search OP_SPECS/parser and SDK v2/orchestration/build.py SearchBuildsRequest in src/pal_found_cli/orchestration/scripts/pal_found_orchestration_cli.py. Parse build search without --where-json: parser accepts omission. Invoke SDK-decorated method through adapter with synthetic client/request capture: missing required where fails validation. Independent review .ept/tmp/feature015_core_schedule_final_review.json resolved_findings documents exact gap; feature015_core_schedule_probe.json captures current example checks. No live Foundry request made.

## Expected versus actual
Required SDK search filter must be required in CLI input contract or supplied via an explicitly approved valid semantic default. Current parser accepts an invocation that cannot satisfy SDK-required where. Existing revised skill guide correctly supplies --where-json; source-accurate documentation PASS does not fix parser validation.

## Acceptance criteria
- Align build.search parser and adapter with real SDK-required where contract; avoid inventing a broad default query.
- Independent tests show missing/malformed filters fail as structured user input before SDK request; valid STATUS/RUNNING and another supported filter serialize as actual SDK request correctly.
- Preserve pagination behavior and correctly separate valid empty result from invalid missing request.
- Record code review and independent QA against exact tool revision; retest affected guide example.

## Ownership and dependency
Relates to archived FEATURE-012 CLI correctness and existing Orchestration namespace ownership; blocks DEV-STORY-070 affected shared-operation acceptance under BD-015-09/11/12 until corrected/retested. BUG-022 corrected documentation inputs/paging and is Closed; it does not cover permissive parser missing required SDK filter. No reopening or waiver.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
