---
id: BUG-050
type: bug
title: Restore retained Geotemporal latest and historic CLI contracts on admitted SDK versions
status: Blocked
affected_version: 1e2e61bc0a56afe9af75e77170358d93ff6cf9d1
created: 2026-11-17
updated: 2026-11-18
priority: High
assignee: python-developer
reporter: project-manager
component: cli-ontologies
---

# BUG-050: Restore retained Geotemporal latest and historic CLI contracts on admitted SDK versions

## Description

# Compatibility defect

## Observed behavior
Two retained GeotemporalSeriesProperty operations, get_geotemporal_series_latest_value and stream_geotemporal_series_historic_values, fail when enabled on native foundry-platform-sdk 1.101.0 and 1.111.0: exit 1 UserInputError with underlying AttributeError and zero HTTP dispatch. Tool tested candidate 9e5a83d6ef5c5e6b3c2d76a09eb5cf4d2f359705 has tree 485f9bb1ac510ce1850e757d07980b276f3e824a, identical to published main 1e2e61bc0a56afe9af75e77170358d93ff6cf9d1. No introducing CLI change identified. Global ENABLED=false exits 8 before SDK construction; this is not proof of every operation flag.

## Expected behavior and contract
Preserve both existing operation identities, arguments, 351 inventory and original DEV-STORY-007 ownership. Native old SDK methods remain unchanged when present, including admitted 1.79.0. SDK 1.79.0 commit 2da67907be429c35f747eef565867ce81dd2cafc defines GET .../geotemporalSeries/{propertyName}/latestValue returning Optional legacy typed GeotemporalSeriesEntry and POST .../streamHistoricValues returning bytes with optional TimeRange request. Exact paths, query/header/body and minimal model closure are specified in Closed QUESTION-196 architect comment 20261117-144539-@architect~001. Current loadEntries has a different contract and cannot substitute.

## Reproduction and evidence
Inspect retained .ept/tmp/geotemporal_cli_compat_qa_20261117.py and results_1.101.0.json/results_1.111.0.json beneath .ept/tmp/geotemporal_cli_compat_qa_20261117/. The script records exact CLI calls with native client factory/auth and mocked transport, public networking denied. Prepared SDK environments: .ept/tmp/feature015_shared_cli_qa_env/Scripts/python.exe and .ept/tmp/feature015_functions_sdk111_env/Scripts/python.exe. Preserve retained results before rerunning because script overwrites them. Script SHA256 0deb1f6e9adffa3660be85eae89fdba9b6f703a12c95f067af6baafcd1b0af7b; SDK101 result b366fa9f43e01f5018de92ff5e0090425f64cc7719684a5a1c6d15f58319f73f; SDK111 result b824a03d24eef3fd83442a49a12f1ccb05166f9ee470c96ee369ff987f7a7467.

## Acceptance criteria
- Before implementation, independently reviewed grooming/prototype proves resource-scoped authenticated SDK AsyncApiClient transport and minimal legacy model compatibility on both 1.101.0 and 1.111.0. Preserve native 1.79 method route. No replacement HTTP/auth stack or global SDK patch.
- Preserve exact legacy routes, escaped positionals, optional SDK query fields, headers, omitted/null/absolute/relative range validation and serialization, typed latest/null output and historic bytes/download metadata. Use general SDK error decoding; source throwable_errors is empty.
- Preserve AsyncClientFactory/invocation_scope, UserTokenAuth, host/context/preview, AccessControlGuard precedence and global/namespace/operation/read-only/metadata policies, shared timeout/retry bounds, B3 attribution restoration, JSON/TOON normalization, BinaryDownloadHandler bounds/checksum and partial-failure/cancellation cleanup.
- Independent native-client MockTransport QA verifies exact candidate on 1.101.0 and 1.111.0 plus 1.79 native positive control, wire contracts, meaningful failures, access denial before SDK/network, retry/timeout/cancellation and inventory equality. Preserve accepted 425 REST evidence separately; no counting these two legacy identities into REST425.
- Reviewed corrective commit published through normal tool workflow, exact remote SHA/CI/parent pin verified, then independent QA records acceptance before removing BUG blocker or closing.

## Scope and limits
Closed QUESTION-196 accepted compatibility-defect classification with source/runtime evidence. No all-versions >=1.0 testing, live tenant success, backend removal or task-critical J1-J10 impact is established. Legacy backend availability remains unverified. G6 remains unresolved pending independent repair acceptance. If exact contract cannot be retained, create appropriate owner QUESTION before retirement, support narrowing, reconstructed latest results, substitution or policy change. No waiver accepted.

## References
Closed QUESTION-196 four architect answer comments 20261117-144539 through 20261117-144540~001; BA-DES-015; SA-DES-014 and verification-and-delivery G6; FEATURE-012; FEATURE-015; DEV-STORY-007; DEV-STORY-070; Closed DEV-006/UNITTEST-006/CODEREVIEW-006; DEV-047 and BUG-016. Similar adapter defect BUG-048 is independently Closed and does not repair these two operations.
