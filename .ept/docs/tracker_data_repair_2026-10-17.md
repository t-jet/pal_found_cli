# Tracker data repair, 2026-10-17

Commit `435ccb5c` records the live `.ept/tracker` directory byte for byte before these repairs. It is the source for any later recovery of discarded fragments or the unindexed ticket copy.

The link index had five stray CSV rows. Three held only fragments of already complete rows (`andoff.`, `2937`, and `55.502029`). Two followed broken rows. I removed all five fragments.

- Restored `LINK-01027` and `LINK-01028` from `origin/main`. The snapshot had a truncated `LINK-01027` and only a fragment of `LINK-01028`; the committed upstream rows contain their full fields.
- Rebuilt `LINK-01278` from its two surviving fragments. The source, target, type, timestamp, and author were present. Its standard `Contains` target role is `Contained In`; its comment remains empty.
- Kept both relationships recorded as `LINK-01612`. The `DEV-STORY-091` dependency keeps that ID. The `FEATURE-015` to `DEV-STORY-092` relationship was first reassigned `LINK-01980` in the repair commit. A later QA link used that ID in the live tracker, so the final branch assigns this historical relationship `LINK-01981`; its other recorded fields are unchanged.
- Moved the unindexed root `CODEREVIEW-002/ticket.md` to [legacy_codereview_002_unindexed.md](legacy_codereview_002_unindexed.md) without changing its bytes. The indexed `DEV-STORY-002/CODEREVIEW-002/ticket.md` remains the active ticket. The archived copy has SHA-256 `9351494e8b1522c534b4b7adefd10e1effc03c828d62256c39dff11471036d9f`.

`LINK-01279` has no recoverable row in the snapshot or `origin/main`. Its ID stays unused. This repair does not assert which tickets it linked or when it was created.

Validation of the repair commit found 1,012 indexed tickets and matching ticket files, 1,542 unique links with existing endpoints, and no duplicate relationship triples. Only the two config files and the archived root ticket differed from the raw tracker snapshot; comment files were untouched.

The follow-up QA ticket capture adds `TESTCASE-085`, `TESTEXEC-085`, and their live `LINK-01980` blocking relationship. The case is Open for QA review; execution is Blocked until that review is approved. The final branch has 1,014 indexed tickets, 1,543 unique links and a link counter of 1981. The raw snapshot and its repair commit remain unchanged in history.
