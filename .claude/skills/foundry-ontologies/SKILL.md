---
name: foundry-ontologies
description: Foundry Ontologies API v2 CLI with 67 canonical operations across ontology metadata, objects, object sets, actions, queries, attachments, media, time series, and transactions.
---

# Foundry Ontologies CLI

67 Foundry Ontologies API v2 operations are available through `foundry_ontologies_cli.py`.

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
python foundry_ontologies_cli.py <resource> <operation> [options]
```

Common options: `--timeout`, `--format json|toon|auto`, `--pretty`, `--page-size`, `--page-token`, and `--batch-pages`.

Binary downloads use `BinaryDownloadHandler` and return a JSON/TOON metadata envelope with the saved file path and checksums. Binary uploads use `--body-file`; `--content-length` is inferred when omitted.

The CLI uses the shared config loader, access control guard, retry handler, pagination helper, structured error serializer, output formatter, and SDK-native B3 tracing scope.
