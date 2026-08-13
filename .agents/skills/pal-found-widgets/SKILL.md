---
name: pal-found-widgets
description: Run Foundry Widgets API v2 operations across DevModeSettings, Repository, WidgetSet, and WidgetSet.Release: enable dev mode, set dev-mode settings by widget ID, get/publish repositories, manage widget-set releases with cursor-paged listing, and bounded zip uploads.
---

# Foundry Widgets

Run `pal-found-widgets --help` for syntax. The CLI exposes exactly 8 Widgets v2 operations: `dev-mode-settings enable|set-widget-set-by-id`; `release delete|get|list`; `repository get|publish`; `widget-set get`.

`release list` uses the ADR-003 cursor-paged pattern with `--page-size`/`--page-token`/`--all`/`--max-pages`. `repository publish` reads the `--file` content (bounded at 16 MiB) and passes it as the widget-set build zip, which must include a valid manifest at `.palantir/widgets.config.json`; `--repository-version` is the SDK `repository_version` query parameter. `dev-mode-settings set-widget-set-by-id` takes `--widget-set-rid` and `--settings-json` (the `WidgetSetDevModeSettingsById` payload).

Access control runs before client and file effects. The write set is `dev-mode-settings enable|set-widget-set-by-id`, `release delete`, and `repository publish` (4 operations); read-only mode blocks them before any work. Metadata-only policy is fail closed: exactly 4 operations (`release get`, `release list`, `repository get`, `widget-set get`) are permitted and the other 4 are blocked.

Client creation and invocation scope use `include_attribution=False`. SDK-native B3 context remains active across client creation and every retry, then restores the caller's prior context. Retries have at-least-once semantics: retrying `repository publish` can create a duplicate release, and retrying `dev-mode-settings enable` re-applies the same target state. Do not add another automatic retry loop after this CLI exhausts its policy.

Successful results go only to stdout; logs and errors must not contain secrets, credentials, tokens, or attribution RIDs.
