---
id: BUG-003
type: bug
title: Tracker status index/get inconsistency prevents FEATURE-001 transition
status: Closed
affected_version: tracker-workspace-2026-07-30
created: 2026-07-30
updated: 2026-07-30
priority: High
resolution: Done
assignee: python-developer
reporter: python-developer
component: tracking-system
labels: tracker-integrity
---

## Summary
FEATURE-001 exposes two different statuses through documented tracker commands. This prevents the valid Waiting for Implementation to Blocked transition.

## Reproduction
1. Run get FEATURE-001. It returns Waiting for Implementation.
2. Run list --non-terminal-only. It reports In Development.
3. Run build-queue all. It reports In Development.
4. Run update FEATURE-001 --status Blocked. Validation uses In Development and exits 2 because that status has no feature transitions.
5. Run type-info feature. In Development is not a valid feature status.
6. Inspect CLI help. No validate, repair, reconcile, import, forced-status, or index-rebuild command exists.

## Actual behavior
Read and validation paths disagree about FEATURE-001 status. Normal update cannot apply the configured transition.

## Expected behavior
All read surfaces and transition validation use one canonical ticket status. A supported reconciliation preserves ticket history, links, and comments. After reconciliation, Waiting for Implementation to Blocked succeeds and records Waiting for Implementation as prior status.

## Preserved evidence
Keep LINK-00413 and LINK-00414. Keep FEATURE-001 comment 20260730-145945-workflow-manager. Do not rewrite FEATURE-001 content or history.

## Acceptance criteria
- get, list, and build-queue report the same canonical status for FEATURE-001.
- update validates from that canonical status.
- Reconciliation preserves all existing links, comments, metadata, and history.
- Waiting for Implementation to Blocked succeeds after repair.
- Prior status is preserved as Waiting for Implementation.
- Regression tests cover get, list, build-queue, and update consistency.

## Affected path
.ept/skills/tracking-system/tracker/tracker_cli.py and the shared status persistence/index paths used by get, list, build-queue, and update.

## Target tests
Tracker CLI regression coverage for canonical status reads, indexed listing, queue output, validated transitions, and history-preserving reconciliation.
