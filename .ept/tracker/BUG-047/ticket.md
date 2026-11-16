---
id: BUG-047
type: bug
title: Models standalone guidance lacks required contracts and uses invalid trainer ID
status: In Progress
affected_version: 6df64cce16bf0619bee124f831e1e8686c08cccf
created: 2026-10-29
updated: 2026-10-29
priority: High
assignee: python-developer
reporter: qa-engineer
component: skills
---

# BUG-047: Models standalone guidance lacks required contracts and uses invalid trainer ID

## Description

## Reproduction and environment
Independent 14-page Models QA at .ept/tmp/feature015_models_pages_review_20261029.json reports 5 PASS, 8 FAIL, 1 UNCERTAIN with all 23 examples exercised against SDK 1.101.0 and actual CLI under denied network. Skill revision: 6df64cce16bf0619bee124f831e1e8686c08cccf. Literal trainer ID autogluon fails SDK RID validation before transport.
## Expected and actual
Standalone Models skill must contain supported prerequisite, search, response and lifecycle knowledge. Nine failed or uncertain pages omit essential knowledge; config-version get also has separate CLI defect BUG-046. Historical BUG-020 remains Closed and unchanged.
## Acceptance criteria
Repair auth/service-user/resource and dependency prerequisites; search where/orderBy discriminants, fields, operators and examples; series entries/value/timestamp-ms/step; trainer schema and inputs/outputs; optional run build_status/resolved_outputs and bounded completion/recovery; supported model-version variant knowledge. Preserve valid tabular/dill example and 14-file navigation. No leaf exceeds 300 lines. No installer, sibling-skill or internal development-document dependencies. Ground claims in frozen SDK 1.101.0 and actual CLI; record source silence and per-route output limits. Independent QA retests all pages and examples against corrected BUG-046 tool candidate before acceptance.
## Boundaries
Only .agents/skills/pal-found-models in isolated feature015/models-standalone-guidance worktree; no CLI source, ledger edits, commit or push before fresh review. Coordination with BUG-046 remains separate.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
