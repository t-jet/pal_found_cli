---
id: BUG-046
type: bug
title: Models CLI config-version get fails before HTTP on SDK 1.101.0
status: Closed
affected_version: a3a38ec434fdb046c329b850e716dc541fa87ecd
created: 2026-10-29
updated: 2026-10-29
priority: High
resolution: Done
assignee: python-developer
reporter: qa-engineer
component: tool
fix_version: 223d2c0bfe3b4ed9a1f8aa35cc98a07cf2a3238f
---

# Model Studio config-version get fails before HTTP on SDK 1.101.0

## Reproduction and environment

Independent reporter: qa-engineer, reviewer `/root/models_pages_20261029`.
Tool revision: `a3a38ec434fdb046c329b850e716dc541fa87ecd`; installed `foundry-platform-sdk==1.101.0`.
Run the documented command through actual CLI main/parser/guard and SDK with an authorized synthetic HTTP MockTransport:

```text
pal-found-models model-studio-config-version get ri.models.main.model-studio.00000000-0000-0000-0000-000000000001 1
```

Raw independent evidence: `.ept/tmp/models_pages_probe_20261029.json`, result `documented_model-studio-config-version_get`; includes revision, source hashes, argv, actual exit, requests, stdout and exception stack. Public network was denied. This reproduction does not establish live enrollment access or server acceptance.

## Expected and actual

Expected: the supported command serializes the decimal version into the exact GET `/api/v2/models/modelStudios/{modelStudioRid}/configVersions/1` route, reaches transport, and preserves typed Models success/error handling through the existing CLI contract.

Actual: exit 1, zero requests, standard error envelope with exception_type TypeError. SDK `_core/api_client.py:529` passes integer path value to `quote(v, safe="")`, raising `quote_from_bytes() expected bytes`. CLI `_invoke` forwards the typed integer into native SDK and has no bounded operation bridge.

## Scope and historical context

Fix source behavior for this Models CLI operation. Original CLI ownership is DEV-STORY-013. FEATURE-015 and DEV-STORY-061 audit existing operations; DEV-STORY-070 owns final integrated acceptance/release and requires zero essential CLI blockers. Keep archived FEATURE-012 unchanged.

Closed BUG-SUB-023 under DEV-STORY-087 addressed offline REST authoring guidance and its scoped direct REST example. Its independent QA comment `20261007-231330-qa-engineer` explicitly preserves the native SDK failure. That accepted documentation fix does not correct this CLI runtime path. Closed BUG-020 concerns skill content. The hardcoded `autogluon` trainer-id example is a separate DEV-STORY-061 content correction.

No global SDK monkeypatch, SDK baseline modification, new runtime policy, operation removal, or publication work belongs here. Preserve existing ACL, auth, timeout, retry, tracing, output and privacy behavior. Use the smallest typed bridge justified by the exact failing operation.

## Acceptance criteria

- Preserve an actual pre-fix CLI failure showing exit 1 and zero HTTP requests on SDK 1.101.0.
- With a valid RID and integer version, actual CLI execution reaches the exact encoded route and returns the typed success output on SDK 1.101.0 and current supported SDK 1.111.0.
- Exercise named and generic SDK error handling through actual CLI transport fixtures; preserve standard error envelopes, privacy and request limits.
- Verify denied access prevents transport; preserve existing timeout/retry/tracing behavior and operation inventory without adding runtime policy.
- Independent source/code review and QA verify the bounded implementation and both SDK versions before resolution/closure. Record source revision and commands/results. Synthetic transport success must not claim live server acceptance or publication.

## Related documentation

- `.ept/docs/document_index.md`
- `.ept/docs/deliverables/architecture/DESIGN-013-models-cli.md`
- `.ept/docs/deliverables/architecture/SA-DES-014-offline-development-knowledge/verification-and-delivery.md`, G6 preservation and essential operation blockers
- BUG-SUB-023 and DEV-STORY-087 scoped REST limitation guidance
