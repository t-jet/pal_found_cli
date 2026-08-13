---
name: pal-found-functions
description: Foundry Functions API v2 CLI with 7 canonical operations across queries, value types, and version IDs.
---

# Foundry Functions CLI

## Capability and source

Foundry Functions exposes versioned server-side functions, their value types,
and query execution. This CLI maps Query, ValueType, and VersionId to seven
operations, including streaming execution and batch lookup.

Source: [Palantir Functions documentation](https://www.palantir.com/docs/foundry/functions/overview); reviewed 2026-08-13.

7 Foundry Functions API v2 operations are available through `pal_found_functions_cli.py`.

## Operations

| Resource | Operations | Count |
|---|---|---|
| query | execute, get, get-by-rid, get-by-rid-batch, streaming-execute | 5 |
| value-type | get | 1 |
| version-id | get | 1 |

## Usage

```bash
python pal_found_functions_cli.py <resource> <operation> [options]
```

Common options: `--timeout`, `--format json|toon|auto`, and `--pretty`.

JSON options are `--parameters`, `--attribution`, and positional `body`.
Boolean flags are `--include-prerelease` and `--preview`.

The CLI uses the shared config loader, access control guard, retry handler, structured error serializer, output formatter, and SDK-native B3 tracing scope.

### Parameters and JSON

Every operation accepts `--timeout`, `--format json|toon|auto`, and `--pretty`.
Query execute and streaming-execute require JSON `--parameters`; get and
get-by-rid variants use positional query/API identifiers shown by help.
Optional variants are `--attribution`, `--branch`, `--ontology`,
`--transaction-id`, `--trace-parent`, `--trace-state`, `--version`,
`--include-prerelease`, and `--preview`. Query get-by-rid-batch uses required
positional JSON `body`; `--rid` and the version-id value are scalar forms.
