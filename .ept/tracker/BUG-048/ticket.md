---
id: BUG-048
type: bug
title: Third-party Website and Version CLI routes omit ThirdPartyApplication SDK parent
status: In Progress
affected_version: db72226c97c55af290f09906dc04f53037513636
created: 2026-11-16
updated: 2026-11-16
priority: High
assignee: python-developer
reporter: qa-engineer
component: cli
---

# Third-party Website and Version CLI commands resolve wrong SDK parent

## Reproduction and environment

Independent offline whole-page review of `pal-found-third-party-applications` at integration `523fd81d238d7a482db3c67af7b97d514c34bd2f`. Tool candidate `db72226c97c55af290f09906dc04f53037513636`, tree `1b12d3b0881d04a6e3c7953149cd9167f0ca42a4`, is tree-identical to published main `223d2c0bfe3b4ed9a1f8aa35cc98a07cf2a3238f`. CLI module SHA-256: `b3a976e0c90c11fab60d0dca01dfd1baed37c4e6ecb24018bc085a9743aa4989`.

Prepared SDK `1.101.0`, tag commit `168d51910570b6966afa2320333ab36f6a3f7ccf`. Installed six namespace sources match this frozen tag. Fake credential, native HTTP and DNS denied, HTTPX MockTransport only. Script: `.ept/tmp/thirdparty_whole_pages_review_20261116.py`. Raw proof: `.ept/tmp/thirdparty_whole_pages_review_20261116/raw_proof.json`. Separate actual console process proof: `console_process.json` in same directory.

Set synthetic FOUNDRY_HOSTNAME=https://qa.invalid, FOUNDRY_TOKEN=offline-qa-fake, FOUNDRY_AGENTIC_CLI_READONLY=false and isolated empty env file. Run `pal-found-third-party-applications website get ri.third-party-applications.main.application.00000000-0000-0000-0000-000000000001` through frozen console repro. Process return code is 6. Stdout error envelope has `exception_type=AttributeError`. Full internal traceback: `_get_client` line 261, called by `main` line 508: `'AsyncThirdPartyApplicationsClient' object has no attribute 'Website'`. Zero HTTP requests occur.

All eight commands fail likewise: website deploy/get/undeploy; version delete/get/list/upload/upload-snapshot. Third-party-application get succeeds with actual SDK HTTP GET. CLI OP_SPECS uses `(Website,)` and `(Website, Version)` while public SDK route is `root.third_party_applications.ThirdPartyApplication.Website` and nested `.Version`. Nine independent SDK reference probes reach exact source HTTP routes; these are reference evidence, not a replacement CLI workaround.

## Expected and actual

Expected supported CLI operations to resolve native public SDK clients and issue frozen request contracts. Actual eight documented operations and five paging cases stop before transport. Initial matrix: 26 actual CLI cases, 13 PASS and 13 FAIL. Auth 401/403/404, missing credentials, read-only guards and file/argument validation pass. Paging semantics remain unaccepted until route correction.

## Acceptance criteria

- Correct all eight public SDK client paths without monkeypatching SDK, adding REST substitutes, or changing policy.
- Independently run all nine documented commands against native SDK 1.101.0 and 1.111.0 with fake HTTP transport and native network denied. Preserve wire body/query fields, binary upload bytes, response models and deletion output.
- Verify first page, cursor resume, bounded pages, --all cap, invalid arguments and interrupted-page recovery through actual CLI parser/guard/SDK. Check stdout records and stderr continuation separately.
- Preserve auth, access guard ordering, upload bounds, configurable timeouts, retry limits, tracing and operation inventory. Add meaningful regression coverage for nested native SDK resolution.
- Record exact source revisions, request assertions and full independent QA results. No live tenant behavior claimed.

## Ownership and blockers

Runtime remediation belongs to original DEV-STORY-021 and FEATURE-012 operation behavior ownership. FEATURE-015 and DEV-STORY-070 G6 release acceptance remain blocked until independent verification. Existing Closed DEV-STORY-021 and BUG-019 are historical and remain unchanged. Separate guidance remediation owns page prerequisites.

## Related documentation

Indexed BA-DES-015 and SA-DES-014, especially content-architecture.md and verification-and-delivery.md. Whole-page report: `.ept/tmp/thirdparty_whole_pages_review_20261116/review.json`.
