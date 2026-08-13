---
name: pal-found-ontologies
description: Foundry Ontologies API v2 CLI with 67 canonical operations across ontology metadata, objects, object sets, actions, queries, attachments, media, time series, and transactions.
---

# Foundry Ontologies CLI

## Capability and source

Foundry Ontology APIs expose semantic object types, links, actions, queries,
attachments, media, and time-series values. This CLI maps those concepts to
67 operations across ontology metadata, objects, object sets, transactions,
and property clients.

Source: [Palantir Ontology-aware applications](https://www.palantir.com/docs/foundry/ontology/applications/index.html); reviewed 2026-08-13.

67 Foundry Ontologies API v2 operations are available through `pal_found_ontologies_cli.py`.

## Operations

| Resource | Operations | Count |
|---|---|---|
| action | apply, apply-batch, apply-with-overrides | 3 |
| action-type | get, get-by-rid, get-by-rid-batch, list | 4 |
| action-type-full-metadata | get, list | 2 |
| attachment | get, read, upload, upload-with-rid | 4 |
| attachment-property | get-attachment, get-attachment-by-rid, read-attachment, read-attachment-by-rid | 4 |
| cipher-text-property | decrypt | 1 |
| geotemporal-series-property | get-geotemporal-series-latest-value, stream-geotemporal-series-historic-values | 2 |
| linked-object | get-linked-object, list-linked-objects | 2 |
| media-reference-property | get-media-content, get-media-metadata, upload | 3 |
| object-type | get, get-by-rid-batch, get-edits-history, get-full-metadata, get-outgoing-link-type, list, list-outgoing-link-types | 7 |
| ontology | get, get-full-metadata, list, load-metadata | 4 |
| ontology-interface | aggregate, get, get-outgoing-interface-link-type, list, list-interface-linked-objects, list-objects-for-interface, list-outgoing-interface-link-types, search | 8 |
| ontology-object | aggregate, count, get, list, search | 5 |
| ontology-object-set | aggregate, create-temporary, get, load, load-links, load-multiple-object-types, load-objects-or-interfaces | 7 |
| ontology-transaction | post-edits | 1 |
| ontology-value-type | get, list | 2 |
| query | execute | 1 |
| query-type | get, list | 2 |
| time-series-property-v2 | get-first-point, get-last-point, stream-points | 3 |
| time-series-value-bank-property | get-latest-value, stream-values | 2 |

## Usage

```bash
python pal_found_ontologies_cli.py <resource> <operation> [options]
```

Common options: `--timeout`, `--format json|toon|auto`, `--pretty`, `--page-size`, `--page-token`, and `--batch-pages`.

Binary downloads use `BinaryDownloadHandler` and return a JSON/TOON metadata envelope with the saved file path and checksums. Binary uploads use `--body-file`; `--content-length` is inferred when omitted.

The CLI uses the shared config loader, access control guard, retry handler, pagination helper, structured error serializer, output formatter, and SDK-native B3 tracing scope.

## Parameters and JSON

Every operation accepts `--timeout`, `--format json|toon|auto`, and `--pretty`;
paginated operations add `--page-size`, `--page-token`, and `--batch-pages`.
JSON variants include `--parameters`, `--attribution`, `--filters`,
`--aggregation`, `--group-by`, `--order-by`, `--where`, `--select`,
`--select-v2`, `--options`, `--requests`, `--request`, `--edits`,
`--overrides`, `--links`, `--object-types`, `--interface-types`,
`--action-types`, `--query-types`, `--augmented-properties`,
`--augmented-interface-property-types`, `--augmented-shared-property-types`,
`--selected-object-types`, `--selected-interface-property-types`,
`--selected-shared-property-types`, `--object-type-api-names`, and `--range`
where help shows them. Binary attachment/media/time-series operations use
`--body-file`, `--output-filename`, `--content-type`, `--content-length`,
`--filename`, and `--media-item-path`. Positional variants are the ontology,
object, link, action, query, property, and transaction identifiers listed by
help; `--preview`, `--branch`, `--sdk-package-rid`, `--sdk-version`,
`--version`, and `--transaction-id` are optional scalar variants.

Additional scalar choices and switches are `--accuracy`, `--aggregate`,
`--exclude-rid`, `--include-all-previous-properties`, `--include-compute-usage`,
`--link-types`, `--load-property-securities`, `--object-primary-key`,
`--object-set`, `--other-interface-types`, `--snapshot`, `--sort-order`, and
`--stream-format`.
