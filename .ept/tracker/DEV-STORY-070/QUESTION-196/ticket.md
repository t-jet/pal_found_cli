---
id: QUESTION-196
type: question
title: Classify legacy Geotemporal CLI availability under supported SDK versions
status: Closed
addressed_to: architect
created: 2026-11-17
updated: 2026-11-17
priority: High
assignee: project-manager
reporter: project-manager
time_spent_hours: 0.0231
---

# QUESTION-196: Classify legacy Geotemporal CLI availability under supported SDK versions

## Question
Determine whether the two enabled legacy Geotemporal CLI commands failing before HTTP on SDK 1.101.0 and 1.111.0 are an intended conditional availability contract or a regression under the approved 351-operation preservation gate. Cite the original story/design/feature-flag and supported SDK requirements. If a regression, propose the smallest compatible correction preserving original routes, results, auth, guards, timeouts, retries, tracing and streaming semantics. Do not assume current load_geotemporal_series_entries is equivalent to latest-value or historic streaming. No unsupported-operation waiver is requested.

## Research Done
Independent QA used published tool tree 485f9bb1ac510ce1850e757d07980b276f3e824a, equal to main 1e2e61bc0a56afe9af75e77170358d93ff6cf9d1. Both enabled command IDs fail with UserInputError and AttributeError before HTTP on both SDKs. Disabled feature guard returns exit 8 before SDK construction. Frozen SDK 1.79 has both old methods; tags 1.101.0 and 1.111.0 expose only load_geotemporal_series_entries. Existing adapter audit classified these two rows UNCERTAIN; eight separate Third-party rows were subsequently corrected under Closed BUG-048. No product source has been changed for this finding.

## Evidence
.ept/tmp/geotemporal_cli_compat_qa_20261117.py and .ept/tmp/geotemporal_cli_compat_qa_20261117/results_1.101.0.json and results_1.111.0.json; frozen old/current SDK files and guide in the same directory. Relevant original tickets found by CLI search: DEV-006, UNITTEST-006, CODEREVIEW-006, DEV-047 and BUG-016. Parent DEV-STORY-070 is Development before this question. Indexed BA-DES-015 and SA-DES-014 define G6 and source boundaries.

## Required answer
Provide an evidence-backed availability classification and technical plan or existing approved conditional-contract disposition. If current backend/API information is necessary, verify official primary sources and separate source-proven facts from unavailable tenant evidence. Identify any genuine product-policy decision that requires owner approval; do not invent ordering, latest-result guarantees, legacy model compatibility or deprecation policy. No live tenant calls or implementation requested in this question.


## Completion criteria
- Cite the approved availability/feature-flag and supported-version contract.
- Classify expected conditional behavior versus regression with source and runtime evidence.
- Provide a bounded technical correction plan if needed, retaining operation identities and actual semantics.
- Separate unavailable tenant/backend evidence and identify any real owner policy decision without accepting a waiver.
