---
name: pal-found-filesystem
description: Foundry Filesystem API v2 CLI with 31 canonical operations across folders, projects, resources, resource roles, and spaces.
---

# Foundry Filesystem CLI

## Capability and source

Foundry Filesystem organizes projects, folders, resources, spaces, markings,
and resource roles. This CLI exposes 31 operations across those five resource
clients, including create, lookup, access metadata, restore, and deletion.

Source: [Palantir Foundry overview](https://www.palantir.com/docs/foundry/getting-started/overview); reviewed 2026-08-13.

31 Foundry Filesystem API v2 operations are available through `pal_found_filesystem_cli.py`.

## Operations

| Resource | Operations | Count |
|---|---|---|
| folder | children, create, get, get-batch, replace | 5 |
| project | add-organizations, create, create-from-template, get, organizations, remove-organizations, replace | 7 |
| resource | add-markings, delete, get, get-access-requirements, get-batch, get-by-path, get-by-path-batch, markings, permanently-delete, remove-markings, restore | 11 |
| resource-role | add, list, remove | 3 |
| space | create, delete, get, list, replace | 5 |

## Usage

```bash
python pal_found_filesystem_cli.py <resource> <operation> [options]
```

Common options: `--timeout`, `--format json|toon|auto`, `--pretty`, `--page-size`, `--page-token`, and `--batch-pages`.

Paginated operations are folder children, project organizations, resource markings, resource-role list, and space list.

The CLI uses the shared config loader, access control guard, retry handler, pagination helper, structured error serializer, output formatter, and SDK-native B3 tracing scope.

### Parameters and JSON

Every operation accepts `--timeout`, `--format json|toon|auto`, and `--pretty`.
Paged operations add `--page-size`, `--page-token`, and `--batch-pages`.
JSON payloads use positional `body` for batch and replacement bodies, plus
`--organizations`, `--organization-rids`, `--roles`, `--role-grants`,
`--default-roles`, `--deletion-policy-organizations`, and
`--variable-values` where command help shows them. Other variants include
required `--enrollment-rid`, `--parent-folder-rid`, `--template-rid`,
`--project-description`, `--display-name`, `--path`, `--marking-ids`,
`--space-rid`, and `--file-system-id`, with `--preview` and
`--include-inherited` as booleans. Additional scalar variants are
`--default-role-set-id`, `--description`, `--resource-level-role-grants-allowed`,
and `--usage-account-rid`.
