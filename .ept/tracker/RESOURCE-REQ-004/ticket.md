---
id: RESOURCE-REQ-004
type: resource_req
title: Provision QA Engineer agent for Foundry CLI testing lifecycle
status: Closed
reporter: architect
created: 2026-05-01
updated: 2026-05-01
priority: High
assignee: hr
---

# RESOURCE-REQ-004: Provision QA Engineer agent for Foundry CLI testing lifecycle

## Description

﻿## Role Definition

**Role**: QA Engineer  
**Project**: Foundry CLI Agentic Toolset — 21 Claude Code skills exposing 355 Palantir Foundry API v2 operations

## Context / Business Need

The project has 23 DEV-STORYs, each requiring a complete QA sub-task chain: TESTCASE (test design) and TESTEXEC (test execution). A DEV-STORY cannot advance from QA to Deployment without all QA sub-tasks closed. With 355 API operations across 21 namespace skills, the QA workload is substantial and requires a dedicated engineer.

Additionally, defects found during TESTEXEC must be captured as BUG-SUB tickets and tracked through resolution. Without a QA Engineer, the entire Development → QA → Deployment pipeline stalls at the QA stage, blocking all 23 DEV-STORYs.

No QA Engineer role is currently provisioned.

## Responsibilities

1. Design test cases (TESTCASE sub-tasks) for all 23 DEV-STORYs: define test scenarios, input/output specifications, edge cases, and negative test cases for each Foundry API operation, covering the Given/When/Then acceptance criteria from DEV-STORY descriptions
2. Execute test cases (TESTEXEC sub-tasks): run tests in the target environment, validate actual vs. expected behavior, and record results
3. Create BUG-SUB tickets for defects found during test execution, with full reproduction steps, expected vs. actual behavior, and severity classification
4. Validate that all DEV-STORY acceptance criteria are met before approving QA stage closure
5. Maintain test documentation and coverage metrics across all 23 stories
6. Collaborate with Tech Lead and Python Developers to clarify expected behavior and resolve ambiguous acceptance criteria

## Required Skills

| Skill | Proficiency Level |
|---|---|
| QA/Testing Methodology | Expert |
| Test Case Design & Documentation | Expert |
| API Testing (REST/JSON) | Advanced |
| Python Scripting (for test automation) | Intermediate |
| Defect Management & Bug Reporting | Expert |
| Given/When/Then / BDD Testing | Advanced |
| CLI Tool Testing | Intermediate |
| Test Coverage Analysis | Advanced |

## Expected Deliverables

- TESTCASE sub-tasks (23 total): structured test cases for each DEV-STORY with full scenario coverage
- TESTEXEC sub-tasks (23 total): executed test results with pass/fail documentation
- BUG-SUB tickets: defect reports for all issues found during test execution
- QA sign-off comments on each DEV-STORY approving transition to Deployment stage

## References

- SAD-001: `.ept/docs/deliverables/architecture/SAD-001-foundry-cli.md`
- SRS-001: `.ept/docs/deliverables/business_analysis/SRS-001-foundry-cli.md` (acceptance criteria baseline)
- All 23 DEV-STORY tickets (test targets)


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
