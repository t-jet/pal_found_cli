---
id: BUG-SUB-012
type: bug_subtask
title: publish.yml conda upload glob targets .tar.bz2 but conda-build 26.7.0 produces .conda artifact
status: Closed
created: 2026-08-14
updated: 2026-08-14
priority: High
assignee: qa-engineer
reporter: qa-engineer
time_spent_hours: 2.0
---

# BUG-SUB-012: publish.yml conda upload glob targets .tar.bz2 but conda-build 26.7.0 produces .conda artifact

## Description

## Defect

The conda upload step in .github/workflows/publish.yml uses the file glob conda-channel/*/*.tar.bz2, but conda-build 26.7.0 produces .conda artifacts only. The glob matches zero files, so the built package can never be uploaded even when ANACONDA_API_TOKEN is configured.

## Steps to Reproduce

1. Build the recipe with conda-build 26.7.0: conda build conda.recipe --output-folder .ept/tmp/conda-channel (verified exit 0, 2026-08-14).
2. List the output folder: only pal_found_cli-0.1.0-py_0.conda exists (80499 bytes); no .tar.bz2 file is produced (build log BUILD START line names the .conda target).
3. Simulate the workflow glob: Get-ChildItem -Recurse .ept/tmp/conda-channel -File where Name like *.tar.bz2 returns 0 matches; Name like *.conda returns 1.
4. The workflow upload command anaconda -t $ANACONDA_API_TOKEN upload --user t-jet conda-channel/*/*.tar.bz2 --force therefore receives no matching file and cannot publish the artifact.

## Expected Behavior

The upload step must target the artifact format actually produced by conda-build 26.7.0 (pal_found_cli-0.1.0-py_0.conda), so anaconda upload publishes the built package when a valid token is present. Reference SA-DES-005 UC-4 and AC-D-006-01.

## Actual Behavior

The glob targets the legacy .tar.bz2 format which conda-build 26.7.0 does not produce; the upload step silently matches nothing or fails on the literal path when the token is present. Found at HEAD 5746815 (2026-08-14).

## Test Execution Reference

TESTEXEC-028, case COND-TC-012 (token-present branch).

## Severity

High: blocks the core publication objective of DEV-STORY-028 (publish the CLI to a conda channel).

## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
