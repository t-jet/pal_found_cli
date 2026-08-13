---
name: pal-found-orchestration
description: Run Foundry Orchestration API v2 operations across builds, jobs, schedules, and schedule versions.
---

# Foundry Orchestration

## Capability and source

Foundry Orchestration creates and observes builds, jobs, schedules, and
schedule versions. This CLI exposes 20 operations, including build search and
schedule run controls.

Source: [Palantir Foundry overview](https://www.palantir.com/docs/foundry/getting-started/overview); reviewed 2026-08-13.

Run `pal-found-orchestration --help` for syntax. The CLI exposes exactly 20 Orchestration v2 operations: `build cancel|create|get|get-batch|jobs|search`; `job get|get-batch`; `schedule create|delete|get|get-affected-resources|get-batch|pause|replace|run|runs|unpause`; `schedule-version get|schedule`.

Structured public options use a `-json` suffix and are validated locally before any client is created. Three cursor-paged commands (`build jobs`, `build search`, `schedule runs`) accept `--page-size`, `--page-token`, `--all`, and `--max-pages` (at most 40 actual pages). Batch `get-batch` commands and search responses are single-call and never paged. The ScheduleRun client has no public methods and no commands.

Access control runs before client construction. The 8 mutating operations (`build.cancel`, `build.create`, `schedule.create`, `schedule.delete`, `schedule.pause`, `schedule.replace`, `schedule.run`, `schedule.unpause`) are blocked under read-only mode; `build search` and `schedule get-affected-resources` remain semantic reads. Metadata-only policy is fail closed: exactly 12 operations are permitted and the other 8 are blocked.

Client creation and invocation scope use `include_attribution=False`. SDK-native B3 context remains active across client creation and every retry, then restores the caller's prior context. Retries have at-least-once semantics; retrying create, replace, run, cancel, pause, unpause, or delete can duplicate work or cost. Do not add another automatic retry loop after this CLI exhausts its policy.

Successful results go only to stdout. Logs and errors must not contain schedule or build content, credentials, tokens, or attribution RIDs.

### Parameters and JSON

All commands accept `--timeout`, `--format json|toon|auto`, and `--pretty`.
Paged build jobs/search and schedule runs add `--page-size`, `--page-token`,
`--all`, and `--max-pages`. Required JSON forms are `--target-json`,
`--fallback-branches-json`, `--action-json`, `--trigger-json`, and
`--scope-mode-json`; batch operations use required `--build-rids-json`,
`--job-rids-json`, or `--schedule-rids-json`. Optional JSON forms are
`--retry-backoff-duration-json`, `--where-json`, and `--order-by-json`.
Scalar variants include `--branch-name`, `--force-build`, `--retry-count`,
`--abort-on-failure`, `--notifications-enabled`, `--display-name`, and
`--description`; positional forms are build, job, schedule, and schedule
version RIDs.
