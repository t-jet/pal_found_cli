---
name: foundry-admin
description: Foundry Admin API v2 CLI with 66 canonical operations across enrollment, groups, markings, organizations, roles, users, and related admin subresources.
---

# Foundry Admin CLI

66 Foundry Admin API v2 operations are available through `foundry_admin_cli.py`.

## Usage

```bash
python foundry_admin_cli.py <resource> <operation> [options]
```

Common options: `--timeout`, `--format json|toon|auto`, and `--pretty`.

Paginated operations also accept `--page-size`, `--page-token`, and `--batch-pages`.

JSON options are `attributes`, `administrators`, `body`, `initial_members`, `initial_permissions`, `initial_role_assignments`, `marking_ids`, `organizations`, `principal_ids`, `role_assignments`, and `where`.

Boolean flags are `--include-expirations`, `--preview`, and `--transitive`.

The CLI uses the shared config loader, ADMIN access control guard, retry handler, pagination helper, structured error serializer, output formatter, and SDK-native B3 tracing scope.

