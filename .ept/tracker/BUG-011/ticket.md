---
id: BUG-011
type: bug
title: Ontology paginated CLI operations mishandle SDK iterators and page envelopes
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

# BUG-011: Ontology paginated CLI operations mishandle SDK iterators and page envelopes

## Description

# Defect
Ontology CLI routes 16 paged operations through PaginationHelper.paginate. Ten async SDK methods return AsyncResourceIterator, which helper wraps as one item instead of consuming; output then fails JSON serialization. Six other methods return response page envelopes with data, which helper wraps as items rather than extracting records or continuation.

## Reproduction
An isolated mocked AsyncResourceIterator through ontology _invoke_paginated returns [iterator], total_items=1; JSON serialization raises TypeError. Probe: .ept/tmp/ontology_paging_probe.py. SDK signatures and CLI routing recorded in QA evidence.

## Expected
CLI emits actual item records with correct page-token metadata and bounded batch behavior for all 16 paged ontology operations. Empty and oversized pages do not lose records.

## Acceptance criteria
- Handle SDK async iterators and page envelopes according to each operation's public contract.
- Regression tests cover iterator, envelope data, continuation, empty/oversized pages, and serialization.
- Skill records describe truthful result and pagination behavior.
- Independent QA verifies representative operations in isolated mocks and full relevant test suites.

Related: FEATURE-012 DEV-STORY-046/047, WORK-005.

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
