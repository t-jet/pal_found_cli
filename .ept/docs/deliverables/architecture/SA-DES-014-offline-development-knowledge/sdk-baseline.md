# SDK inventory baseline and extraction evidence

## Frozen releases

| Evidence | Primary target | Customer comparison |
| --- | --- | --- |
| Package/tag | 1.101.0 | 1.79.0 |
| Commit | 168d51910570b6966afa2320333ab36f6a3f7ccf | 2da67907be429c35f747eef565867ce81dd2cafc |
| OpenAPI version | 1.1697.0 | 1.1545.0 |
| Operations / resources / version-service namespaces | 425 / 113 / 20 | 397 / 107 / 20 |
| Stable / Public Beta / Private Beta | 218 / 129 / 78 | 193 / 120 / 84 |
| Reachable model / error symbols | 2,278 / 964 | 2,099 / 876 |
| Full contract symbols inventoried | 4,315 | 4,011 |
| Model source modules / error source modules | 37 / 24 | 36 / 24 |

Installed distribution/module report SDK 1.101.0 and OpenAPI 1.1697.0. CLI metadata permits `foundry-platform-sdk>=1.0.0`; the skill must state its verified version. Publishing placeholders in repository metadata are not installed-version evidence. Official [1.101.0 release](https://github.com/palantir/foundry-platform-python/releases/tag/1.101.0) and [1.79.0 release](https://github.com/palantir/foundry-platform-python/releases/tag/1.79.0) checked 2026-10-06.

## Durable inventory

[Summary](sdk-inventory/summary.json) provides exact per-service counts. Each release folder contains one `<version>.<service>.jsonl` file per namespace, one operation per line, plus sharded `contract-symbols-*.jsonl`, `models-*.tsv` and `errors-*.tsv`. These are maintainer evidence; distributed skills require their own reader-facing indexes and full contracts.

Operation records include qualified identity, HTTP method/path from `RequestInfo`, signature/return type, stage, source/doc hashes, initial references and traversed contract-symbol sets. Symbol records include source and AST-definition hashes and dependency edges. Source ledgers cover all model/error inputs. Sync/async/raw/stream wrappers do not inflate canonical counts.

Sorted operation IDs joined by LF without trailing LF have SHA-256:

- 1.101.0: `a6542de72e2fd73a6197ddb6063cf76617b1c8c1bad95f53547dbbce87760bcd`.
- 1.79.0: `cf2d1079e465bf613c6a4eba5fea102bd4ab4087c1ee2cd8d7549f426a130a83`.

Reproduce design evidence from workspace root with `python .ept/docs/deliverables/architecture/SA-DES-014-offline-development-knowledge/inventory-extractor.py`. It reads immutable `git archive <tag>` inputs without modifying the customer checkout. Public sync Client methods with `RequestInfo` define canonical operations. Equivalent async and response wrappers supply additional references. Python/imported aliases and direct forward-reference names form edges; visited-set traversal handles cycles. Full definition ledgers preserve symbols outside the reachable set for reconciliation.

This extractor records design evidence. Implementation must independently reconcile source resource/doc tables, installed signatures and transport variants; detect indirect or compound forward references; and verify constraints against model/error definitions. Any discrepancy blocks full-coverage claims. Maintained tooling and contract generation are implementation work after design approval.

## Story sizing and acceptance

REST authoring separates common catalog/generation infrastructure from exclusive service/resource groups and independent QA. Generate structural contracts deterministically, then author capability behavior and review every operation/model. Shared schemas have one owner and stable local destinations. Exact story operation sets must partition all 425 IDs without overlap or omission.

Initial REST estimate is 160-240 contributor hours including tooling, original behavior guidance and reviews. This is a planning range, not an approved sprint commitment. Grooming samples ten diverse contracts, nested/recursive models and both governance/AIP workflows, measures effort, then splits any story exceeding one sprint. Review of 3,242 symbols uses generated structural diffs, source reconciliation and human review of semantic constraints; it cannot be declared complete by listing names. BA owns final bounded story partitions and estimates.

Acceptance requires empty identity differences between release source, register and local content; 425 reviewed contracts/examples; complete reachable model/error closure; per-operation serialization/response tests; and independent tasks across all 20 namespaces. Governance and AIP journeys supplement exhaustive coverage. Tenant restrictions remain documented execution prerequisites, while authoring contracts remain offline.

[Back to REST design](rest-and-sources.md)
