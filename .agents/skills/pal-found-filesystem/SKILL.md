---
name: pal-found-filesystem
description: Foundry Filesystem API v2 CLI with 31 canonical operations across folders, projects, resources, resource roles, and spaces.
---

# Foundry Filesystem CLI

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

