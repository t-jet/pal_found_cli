---
id: BUG-034
type: bug
title: Data Health CLI omits required preview query on six endpoints
status: Open
affected_version: b9c5f8a1a0595fc5fa0cbb27a7a92dba9c1bc67e
created: 2026-10-16
updated: 2026-10-16
priority: High
assignee: python-developer
reporter: qa-engineer
component: data-health-cli
---

# BUG-034: Data Health CLI omits required preview query on six endpoints

## Description

## Observed defect
At tool commit b9c5f8a and foundry-platform-sdk 1.101.0, all six Data Health Check and CheckReport CLI operations omit preview=true. Official Palantir API references label each endpoint preview and require preview=true.

## Steps to reproduce
1. Inspect OP_SPECS, build_parser and _build_kwargs in pal_found_cli_tool/src/pal_found_cli/data_health/scripts/pal_found_data_health_cli.py. No preview option is exposed or forwarded.
2. With httpx.MockTransport and FoundryClient, call client.data_health.Check.get(check_rid) and record request URL. It is /api/v2/dataHealth/checks/{checkRid}, with no query.
3. Call same SDK method with preview=True. Request URL ends ?preview=true.
4. Compare official Get Check API reference: https://www.palantir.com/docs/foundry/api/v2/data-health-v2-resources/checks/get-check. It instructs adding preview=true. Same instruction appears on Create/Delete/Replace Check and Get/Get Latest Check Reports.

## Expected behavior
CLI can send required preview=true to every supported Data Health endpoint, or explicitly blocks unsupported preview calls and skills guide users to a supported path.

## Actual behavior
CLI cannot express preview=true. Six documented calls omit required query. No live tenant call was made; server rejection is inferred from the published API contract.

## Severity and affected acceptance
High. FEATURE-012 supported CLI documentation and FEATURE-015 offline skill audit cannot approve Data Health operations until corrected and independently retested. TESTEXEC-048 previously accepted content without this preview case.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
