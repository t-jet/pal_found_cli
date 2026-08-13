---
name: pal-found-third-party-applications
description: Run Foundry Third-Party Applications API v2 operations across ThirdPartyApplication, Website, and Version: get application and website state, deploy/undeploy websites, and manage website versions including bounded zip uploads and cursor-paged version listing.
---

# Foundry Third-Party Applications

## Capability and source

Foundry Third-Party Applications manages website state and versioned website
builds. This CLI exposes application get, website deploy/get/undeploy, and the
five version operations, including bounded zip uploads and version listing.

Source: [Palantir application reference](https://www.palantir.com/docs/foundry/getting-started/application-reference); reviewed 2026-08-13.

Run `pal-found-third-party-applications --help` for syntax. The CLI exposes exactly 9 Third-Party Applications v2 operations: `third-party-application get`; `website deploy|get|undeploy`; `version delete|get|list|upload|upload-snapshot`.

`version list` uses the ADR-003 cursor-paged pattern with `--page-size`/`--page-token`/`--all`/`--max-pages`. `version upload` and `version upload-snapshot` read the `--file` content (bounded at 16 MiB) and pass it as the Website build zip; `--version` is the SDK `version` query parameter. Snapshot versions are automatically deleted after two days. `version upload-snapshot` also accepts `--snapshot-identifier` (optional).

Access control runs before client and file effects. The write set is `website deploy|undeploy` and `version delete|upload|upload-snapshot` (5 operations); read-only mode blocks them before any work. Metadata-only policy is fail closed: exactly 4 operations (`third-party-application get`, `website get`, `version get`, `version list`) are permitted and the other 5 are blocked.

Client creation and invocation scope use `include_attribution=False`. SDK-native B3 context remains active across client creation and every retry, then restores the caller's prior context. Retries have at-least-once semantics: retrying `website deploy`/`website undeploy` re-applies the same version (idempotent target state), but retrying `version upload` can create a duplicate version record. Do not add another automatic retry loop after this CLI exhausts its policy.

Successful results go only to stdout; logs and errors must not contain secrets, credentials, tokens, or attribution RIDs.

### Parameters and JSON

All commands accept `--timeout`, `--format json|toon|auto`, and `--pretty`.
`version list` adds `--page-size`, `--page-token`, `--all`, and `--max-pages`.
Version upload and upload-snapshot require `--version` and `--file`; snapshot
upload optionally accepts `--snapshot-identifier`. Website deploy requires
`--version`. Other commands use positional `third_party_application_rid` and,
for version get/delete, `version_version`. This namespace has no JSON input
flags; zip content comes from `--file`.
