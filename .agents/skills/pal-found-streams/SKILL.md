---
name: pal-found-streams
description: Run Foundry Streams API v2 operations across Dataset, Stream, and Subscriber: create, get, end-offsets, record reads and publishes, subscriber offset management.
---

# Foundry Streams

## Capability and source

Foundry Streams provides ordered records, partitions, publishers, subscribers,
and committed read offsets. This CLI exposes 15 Dataset, Stream, and Subscriber
operations, including bounded batch reads and binary record publishing.

Source: [Palantir Foundry documentation](https://www.palantir.com/docs/foundry); reviewed 2026-08-13.

Run `pal-found-streams --help` for syntax. The CLI exposes exactly 15 Streams v2 operations: `dataset create`; `stream create|get|get-end-offsets|get-records|publish-binary-record|publish-record|publish-records|reset`; `subscriber create|commit-offsets|delete|get-read-position|read-records|reset-offsets`.

Structured public options use a `-json` suffix (`--schema-json`, `--record-json`, `--records-json`, `--offsets-json`, `--position-json`, `--read-position-json`, `--partition-ids-json`) and are validated locally before any client is created. Record reads implement the ADR-003 batch pattern: `stream get-records` and `subscriber read-records` accept `--max-records` (default 100; up to 10,000 for get-records, 1,000 for read-records), aggregate records, and emit them once on exit — never progressively. Subscriber offsets are committed only with `--auto-commit` or an explicit `commit-offsets` call. `stream publish-binary-record` reads the `--file` content (bounded at 16 MiB) and uploads it.

Access control runs before client and filesystem effects. The write set is all creates, all publishes, `stream reset`, `subscriber commit-offsets`, `subscriber delete`, and `subscriber reset-offsets` (10 operations); read-only mode blocks them before any work. Metadata-only policy is fail closed: exactly 3 operations (`stream get`, `stream get-end-offsets`, `subscriber get-read-position`) are permitted and the other 12 are blocked.

Client creation and invocation scope use `include_attribution=False`. Streams uses the namespace timeout `FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S` (default 120s) per ADR-003. SDK-native B3 context remains active across client creation and every retry, then restores the caller's prior context. Retries have at-least-once semantics; retrying creates, publishes, reset, commit, or delete can duplicate records or cost. Offset state is mutated only by explicit `commit-offsets` or `--auto-commit` reads; retried reads without auto-commit are safe. Do not add another automatic retry loop after this CLI exhausts its policy.

Successful results go only to stdout. Logs and errors must not contain records, prompts, credentials, tokens, or attribution RIDs.

### Parameters and JSON

Every command accepts `--timeout`, `--format json|toon|auto`, and `--pretty`.
Dataset/stream creation requires `--schema-json` where shown; publish commands
use required `--record-json` or `--records-json`, and binary publish uses
`--file`. Subscriber create/read/reset variants use `--read-position-json`,
`--partition-ids-json`, or `--position-json`; commit uses required
`--offsets-json`. `--branch-name`, `--parent-folder-rid`,
`--subscriber-id`, `--partition-id`, `--max-records`, `--start-offset`,
`--partitions-count`, `--stream-type`, `--view-rid`, `--compressed`, and
`--auto-commit` are scalar or boolean variants; dataset creation also requires
`--name`. Positional forms are the
dataset, stream branch, and subscriber IDs shown by help.
