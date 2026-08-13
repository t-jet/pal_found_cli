---
name: pal-found-admin
description: Foundry Admin API v2 CLI with 66 canonical operations across enrollment, groups, markings, organizations, roles, users, and related admin subresources.
---

# Foundry Admin CLI

66 Foundry Admin API v2 operations are available through `pal_found_admin_cli.py`.

## Capability and source

Foundry administration exposes enrollment, identity, groups, organizations,
roles, markings, and provider information. This skill maps those controls to
66 CLI operations; it does not grant access by itself.

Source: [Palantir Foundry security and governance](https://www.palantir.com/docs/foundry/security/overview); reviewed 2026-08-13.

Operation resources: `authentication-provider` (get, list, preregister-group,
preregister-user), `cbac-banner` (get), `cbac-marking-restrictions` (get),
`enrollment` (get, get-current), `enrollment-role-assignment` (add, list,
remove), `group` (create, delete, get, get-batch, list, list-current, replace,
search), `group-member` (add, list, remove), `group-membership` (list),
`group-membership-expiration-policy` (get, replace), `group-provider-info`
(get, replace), `host` (list), `marking` (create, get, get-batch, list,
replace), `marking-category` (create, get, list, replace), `marking-member`
(add, list, remove), `marking-role-assignment` (add, list, remove),
`organization` (create, get, list-available-roles, replace),
`organization-guest-member` (add, list, remove), `organization-role-assignment`
(add, list, remove), `role` (get, get-batch), `user` (delete, get, get-batch,
get-current, get-markings, list, profile-picture, revoke-all-tokens, search),
and `user-provider-info` (get, replace).

## Usage

```bash
python pal_found_admin_cli.py <resource> <operation> [options]
```

Common options: `--timeout`, `--format json|toon|auto`, and `--pretty`.

Paginated operations also accept `--page-size`, `--page-token`, and `--batch-pages`.

JSON options are `attributes`, `administrators`, `body`, `initial_members`, `initial_permissions`, `initial_role_assignments`, `marking_ids`, `organizations`, `principal_ids`, `role_assignments`, and `where`.

Boolean flags are `--include-expirations`, `--preview`, and `--transitive`.

### Parameters and JSON

Every operation accepts `--timeout`, `--format json|toon|auto`, and `--pretty`.
Paged operations add `--page-size`, `--page-token`, and `--batch-pages`.
JSON values use `--attributes`, `--administrators`,
`--initial-members`, `--initial-permissions`, `--initial-role-assignments`,
`--marking-ids`, `--organizations`, `--principal-ids`, `--role-assignments`,
and `--where`. `body` is the positional JSON batch form on get-batch
commands. Scalar or list parameter variants include `--category-id`, `--description`,
`--display-type`, `--email`, `--enrollment-rid`, `--expiration`,
`--family-name`, `--given-name`, `--host`, `--maximum-duration`,
`--maximum-value`, `--name`, `--organization`, `--provider-id`, `--status`,
`--username`, and `--include`.
Other positional variants are the resource RIDs shown by `--help`.

The CLI uses the shared config loader, ADMIN access control guard, retry handler, pagination helper, structured error serializer, output formatter, and SDK-native B3 tracing scope.
