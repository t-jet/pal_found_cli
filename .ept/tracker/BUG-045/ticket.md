---
id: BUG-045
type: bug
title: Ontology SQL download drops the required query before SDK invocation
status: Closed
affected_version: 066970098011c90269aa975d14d7ac713106bbe5
created: 2026-10-21
updated: 2026-10-21
priority: High
resolution: Done
assignee: python-developer
reporter: project-manager
component: sql-queries-cli
fix_version: a3a38ec434fdb046c329b850e716dc541fa87ecd
---

# BUG-045: Ontology SQL download drops the required query before SDK invocation

## Description

## Observed defect
At published tool 066970098011c90269aa975d14d7ac713106bbe5, query execute-ontology --query "select 1"
accepts its required CLI input but drops query before calling the real SDK streaming wrapper.
SDK1.101 raises missing_keyword_only_argument for query, with no HTTP request. Every invocation
of this operation is affected. Independent explorer /root/streaming_adapter_resume reproduced it
using actual AsyncSqlQueryClient and MockTransport with sockets denied. Evidence is
.ept/tmp/feature015_streaming_adapter_scan.json, feature015_streaming_wire_results.json and
feature015_streaming_wire_probe.py. No live Foundry execution is claimed.

## Cause and expected behavior
SQL _download_operation builds kwargs from optional fields only, while execute_ontology declares
query as required. Reuse the existing required/optional/timeout builder, removing only the local
output filename before SDK invocation. Preserve the query text, typed parameters, dryRun,
rowLimit, timeout, bounded binary persistence, checksums and get_results scalar ID/output behavior.

## Ownership and acceptance
DEV-STORY-015 exposes all five SQL CLI operations including synchronous Ontology Arrow downloads.
DEV-STORY-070 requires essential CLI defects to be fixed before integrated acceptance. Relate the
archived original story and FEATURE-012/015 without reopening them; block only DEV-STORY-070.
Reproduce the old missing-query failure with the actual SDK. Verify exact HTTP body and download
metadata with SDK1.101 and SDK1.111, including optional typed parameters, bounded content and the
other download route. Require independent code/runtime review and all eight CI checks before
closure. Existing fake streaming tests accepted arbitrary kwargs and did not catch this adapter gap.
Historical direct SDK evidence remains scoped to its actual layer.

## Current correction
Root is implementing the minimal adapter correction and four real SDK HTTP regression cases.
Before correction, three execute_ontology cases failed for missing query; get_results passed.
Author now reports 30 SQL tests passed on each SDK1.101/1.111, Ruff src/tests and mypy72source
passed. Source commit a3a38ec434fdb046c329b850e716dc541fa87ecd is local and under independent
review. Publication, independent acceptance and exact-head CI remain pending; no resolution claim.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
