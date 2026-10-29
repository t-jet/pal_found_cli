---
id: BUG-044
type: bug
title: Filesystem positional JSON batch bodies reach SDK as strings
status: Closed
affected_version: ddfab5d13bd01a1f244a4446cd10764c9091f65a
created: 2026-10-21
updated: 2026-10-21
priority: High
resolution: Done
assignee: python-developer
reporter: python-developer
component: filesystem-cli
fix_version: 066970098011c90269aa975d14d7ac713106bbe5
---

# BUG-044: Filesystem positional JSON batch bodies reach SDK as strings

## Description

## Observed defect
Valid positional JSON batch bodies remain strings when the Filesystem CLI invokes the real SDK. Three operations fail before HTTP dispatch: folder.get_batch, resource.get_batch and resource.get_by_path_batch. Published affected tool revision: ddfab5d13bd01a1f244a4446cd10764c9091f65a; SDK 1.101.0. This prevents the documented batch reads from working.

## Reproduction and evidence
Independent reviewer /root/filesystem_pages_review executed all three documented commands through parser and SDK invocation with socket.connect and socket.create_connection denied and httpx.MockTransport capturing requests. Each parser accepted its JSON argument; each actual SDK method raised ValidationError: Input should be a valid list, input_type=str. Each recorded zero HTTP requests. Evidence: .ept/tmp/feature015_filesystem_pages_review_initial.json and .ept/tmp/feature015_filesystem_pages_probe.py. Commands and source hashes are recorded below. These are synthetic offline checks, not live Foundry execution.

## Root cause and expected behavior
The Filesystem CLI positional argument adapter passes the argparse string directly to SDK list parameters. Apply the existing JSON coercion used for keyword arguments to positional arguments, matching established Admin and Functions handling. A valid JSON list must reach real SDK validation and serialize as a JSON array. Preserve ordinary scalar positional values, existing keyword behavior, access checks, error mapping and all 31 Filesystem operations.

## Requirements and coverage boundary
DEV-STORY-006 AC-FS-OP-FOLDER and AC-FS-OP-RESOURCE require callable batch operations. FEATURE-012 requires examples that work through the supported CLI. DEV-STORY-070 and SA-DES-014 verification G6 require preservation of supported CLI behavior and resolution of essential shared defects before acceptance. Relevant documents were reviewed through .ept/docs/document_index.md, including SA-DES-014 verification-and-delivery.md. Prior DEV-STORY-073 REST SDK request/semantic evidence covers direct SDK contracts; it does not establish CLI positional argument conversion. BUG-038 parser error formatting, BUG-012 pagination and BUG-027 error mapping have separate causes. Historical closed results remain scoped to their recorded checks.

## Acceptance criteria
- Independently reproduce all three failures against the affected published revision using actual SDK types and a captured transport.
- Convert valid positional JSON arrays before SDK invocation; assert the exact outgoing request body for all three commands against SDK 1.101.0 and the supported compatibility release.
- Verify normal scalar positional arguments and keyword JSON behavior remain correct; cover malformed or wrong-shape batch inputs without claiming successful HTTP dispatch.
- Record source commit, review, independent candidate QA, affected guide retest and required CI before resolution. Preserve other active blockers and relationships.

## Current work
Fix author /root/filesystem_batch_fix is preparing minimal positional _coerce_arg reuse and real SDK regressions. Root reports 19 new regressions and 144 runtime tests passing on each SDK 1.101.0 and 1.111.0, with Ruff and mypy passing for 72 source files. These are attributed author reports, not checks executed by this tracker agent. Candidate publication, independent QA and required CI remain pending. No resolution or closure is claimed.

## Exact failing commands

    pal-found-filesystem folder get-batch '[{"folderRid":"ri.compass.main.folder.01a79a9d-e293-48db-a585-9ffe221536e8"}]'
    pal-found-filesystem resource get-batch '[{"resourceRid":"ri.foundry.main.dataset.c26f11c8-cdb3-4f44-9f5d-9816ea1c82da"}]'
    pal-found-filesystem resource get-by-path-batch '[{"path":"/My Organization-abcd/My Important Project/My Dataset"}]'

## Source identity

CLI script SHA256: 39ed94e3556a550baebed95f09a40258ba8fb93be237d357d53eeae722f239d7
foundry_sdk.v2.filesystem.folder SHA256: 71e0591612f76319049b0cf646633ea2445a3c5e73c85ca99717f6a63e6103e0; matches frozen source oracle.
foundry_sdk.v2.filesystem.resource SHA256: 70a48d6aab58350fc8d676af0cf4f7e5d1e61e7488752e209e46c9d4b6d6231a; matches frozen source oracle.


## Acceptance Criteria

- [ ] TODO: Define acceptance criteria

## Related Documentation

TODO: Add links to related documentation

## Notes

TODO: Add any additional notes
