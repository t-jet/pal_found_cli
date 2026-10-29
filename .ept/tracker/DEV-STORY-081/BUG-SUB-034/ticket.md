---
id: BUG-SUB-034
type: bug_subtask
title: DEV-STORY-081 Scenario edited responses use full objects instead of locators
status: Closed
created: 2026-10-18
updated: 2026-10-18
priority: High
assignee: python-developer
reporter: project-manager
time_spent_hours: 0.2
---

# BUG-SUB-034: DEV-STORY-081 Scenario edited responses use full objects instead of locators

## Description

Independent semantic QA of skills candidate 416747d found two REST-081 Scenario example responses that use complete Order and Worker objects where SDK 1.101.0 requires locators.

Reproduce: run and inspect `.agents/skills/pal-found-dev/examples/rest/081/v2/ontologies/OntologyScenario/invoke_list_scenario_edited_objects.py` and `invoke_list_scenario_edited_links.py`. Both scripts pass their own mocked response assertions, but SUCCESS.data includes domain properties such as `orderId` and `status`.

Expected: `list_scenario_edited_objects` returns locator entries with only `__primaryKey` and `__apiName`, such as `{'__primaryKey':'ORD-101','__apiName':'Order'}`. For `list_scenario_edited_links`, `sourceObject` and nested `targetObject` are locators; `linkType:'assignedWorker'` remains. SDK source types `ListScenarioEditedObjectsResponse`, `LinksFromObject`, and `LinkedObjectLocator` document this shape. The conflicting-object response has a different `ObjectLocator` shape and is outside this defect.

Acceptance: correct both examples, preserve meaningful assertions, execute them against their mocked SDK transport, and obtain independent semantic QA retest at the new SHA. TESTCASE-080 and TESTEXEC-080 remain open; this review is diagnostic, not formal sign-off.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
