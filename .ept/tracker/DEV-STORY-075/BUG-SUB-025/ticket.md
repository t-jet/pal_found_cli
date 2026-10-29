---
id: BUG-SUB-025
type: bug_subtask
title: J12 guide lacks integrated transaction file verification and build outcome
status: In Progress
created: 2026-10-09
updated: 2026-10-11
priority: High
assignee: python-developer
reporter: qa-engineer
time_spent_hours: untracked
---

## Severity and version
High; SDK 1.101.0; pal_found_cli_skills candidate based on HEAD b40d0be, 2026-10-09.

## Reproduction
Source-blind J12 reader .ept/tmp/feature015-j12-reader/reader-results.md scored 4/6 in .ept/tmp/feature015_rest_semantic_review/j12_independent_score.md. It followed local Transaction.md lines 91-99 and 125-160, File.md upload section, and Build.md lines 59-90. The composed code omits staged File.get/content before commit and postcommit branch/file verification; it exits on any terminal Build state without marking FAILED/CANCELED unsuccessful. Six individual SDK fake-transport examples pass, but no composed sequence runs.

## Expected behavior
Offline guidance and a runnable root-client fixture verify transaction-view file state before commit, committed branch/file state afterward, and RUNNING/SUCCEEDED/FAILED/CANCELED/poll-exhaustion separately. Upload or commit timeout is reconciled before replay.

## Acceptance criteria
- Coordinate dataset-view portion with DEV-STORY-074; keep integrated Build journey under DEV-STORY-075.
- Add composed SDK1.101.0 fake-transport example and regression for all listed states and checks.
- Fresh source-blind reader passes all six J12 dimensions using only standalone skill/prepared runtime.
- Preserve failed artifact and distinguish fixture from tenant operation.

## Test reference
TESTEXEC-064 comment 20261009-092807-qa-engineer. Related to DEV-STORY-074; Blocks TESTEXEC-064. No FileImport or unrelated namespace scope.
