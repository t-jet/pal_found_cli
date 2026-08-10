---
name: foundry-data-health
description: Run Foundry Data Health API v2 operations across the Check client and its nested CheckReport client: check create/delete/get/replace and check-report get/get-latest.
---

# Foundry Data Health

Run `foundry-data-health --help` for syntax. The CLI exposes exactly 6 Data Health v2 operations: `check create|delete|get|replace`; `check-report get|get-latest`.

`check create` and `check replace` take the required `--config-json` flag — the `CheckConfig` discriminated union (`type` discriminator across all check config kinds) — plus the optional `--intent` string. `check delete` and `check get` take a positional `check_rid`. `check-report get` takes positional `check_rid` and `check_report_rid`. `check-report get-latest` takes a positional `check_rid` and the optional integer `--limit` (default 10, maximum 100; validated locally).

`check-report get-latest` is a single-response bound, not a cursor: no operation returns a `ResourceIterator` and there are no pagination flags anywhere. Structured options use the `-json` suffix and are validated locally before any client is created.

Access control runs before client construction. The write set is `check.create`, `check.delete`, and `check.replace` (3 operations); read-only mode blocks them before any work. `check.get`, `check_report.get`, and `check_report.get_latest` are semantic reads. Metadata-only policy is fail closed: exactly 3 operations (`check.get`, `check_report.get`, `check_report.get_latest`) are permitted and the other 3 are blocked.

Client creation and invocation scope use `include_attribution=False`. SDK-native B3 context remains active across client creation and every retry, then restores the caller's prior context. Retries have at-least-once semantics; retrying `check create` or `check replace` can duplicate checks or re-run validation. Do not add another automatic retry loop after this CLI exhausts its policy.

Successful results go only to stdout. Logs and errors must not contain check configurations, credentials, tokens, or attribution RIDs.
