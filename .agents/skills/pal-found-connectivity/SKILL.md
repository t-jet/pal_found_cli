---
name: pal-found-connectivity
description: Run Foundry Connectivity API v2 operations across Connection, FileImport, TableImport, and VirtualTable: create/get/update connections, secrets, JDBC drivers, and file/table import management.
---

# Foundry Connectivity

## Capability and source

Foundry Connectivity manages connections and file/table imports, including
virtual-table creation, secret/export settings, and custom JDBC drivers. This
skill exposes the 20 operations listed in the command overview.

Source: [Palantir data connectivity](https://www.palantir.com/docs/foundry/data-integration/application-reference); reviewed 2026-08-13.

Run `pal-found-connectivity --help` for syntax. The CLI exposes exactly 20 Connectivity v2 operations: `connection create|get|get-configuration|get-configuration-batch|update-export-settings|update-secrets|upload-custom-jdbc-drivers`; `file-import create|delete|execute|get|list|replace`; `table-import create|delete|execute|get|list|replace`; `virtual-table create`.

Structured public options use a `-json` suffix (`--configuration-json`, `--worker-json`, `--body-json`, `--export-settings-json`, `--secrets-json`, `--file-import-filters-json`, `--config-json`, `--markings-json`) and are validated locally before any client is created. `file-import list` and `table-import list` use the ADR-003 cursor-paged pattern with `--page-size`/`--page-token`/`--all`/`--max-pages`. `connection upload-custom-jdbc-drivers` reads the `--file` content (bounded at 16 MiB; `--file-name` must end with `.jar`) and uploads it.

Access control runs before client and filesystem effects. The write set is `connection create/update-export-settings/update-secrets/upload-custom-jdbc-drivers`, `file-import create/delete/execute/replace`, `table-import create/delete/execute/replace`, and `virtual-table create` (13 operations); read-only mode blocks them before any work. `connection get-configuration-batch` is a POST request but a semantic read. Metadata-only policy is fail closed: exactly 7 operations (`connection get/get-configuration/get-configuration-batch`, `file-import get/list`, `table-import get/list`) are permitted and the other 13 are blocked.

Client creation and invocation scope use `include_attribution=False`. SDK-native B3 context remains active across client creation and every retry, then restores the caller's prior context. Retries have at-least-once semantics; retrying create, execute, replace, delete, or upload can duplicate syncs, re-run builds, or cost. Do not add another automatic retry loop after this CLI exhausts its policy.

Secrets and export settings never echo values. `connection update-secrets` and `connection update-export-settings` inputs arrive only via their `-json` flags and are never logged or printed. Successful results go only to stdout; logs and errors must not contain secrets, credentials, tokens, or attribution RIDs.

### Parameters and JSON

All commands accept `--timeout`, `--format json|toon|auto`, and `--pretty`.
Paged import lists add `--page-size`, `--page-token`, `--all`, and
`--max-pages`. Required JSON flags are `--configuration-json`, `--worker-json`,
`--body-json`, `--export-settings-json`, `--secrets-json`, and
`--file-import-filters-json`; optional JSON flags are `--config-json` and
`--markings-json`. Other variants include connection/import RIDs, `--name`,
`--display-name`, `--parent-rid`, `--parent-folder-rid`, `--dataset-rid`,
`--branch-name`, `--import-mode`, `--allow-schema-changes`, `--subfolder`,
`--file`, and `--file-name`. `--file-name` must end in `.jar`.
