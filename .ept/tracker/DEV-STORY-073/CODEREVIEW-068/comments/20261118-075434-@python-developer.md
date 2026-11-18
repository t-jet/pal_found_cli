Subject: Correction plan: exact result fields and six pending semantic bindings
Created: 2026-11-18T07:54:34
Updated: 2026-11-18T07:54:34
---
Responding to Architect review 20261118-013055-@architect under actual Correction ownership. Approved edit scope is exactly three tracked files: .agents/skills/pal-found-dev/references/rest/v2/third_party_applications/ThirdPartyApplication.md; .agents/skills/pal-found-dev/references/rest/v2/third_party_applications/Version.md; maintainer/rest-domain-authoring-register.json. Use isolated worktree .ept/tmp/cr068_result_guidance_correction_20261118 from published draft ff70c30c99410b3b0784bcad934625b88d5e6e5c.

Correct ThirdPartyApplication.get to returned rid only and Version.get/list to returned version values only. Keep application RID from request context. Website.get separately returns deployed_version/subdomains. Artifact identity, release/snapshot kind and expiry provenance must come from retained approved upload/release records or authorized verification; preserve pinned two-day snapshot statement. No backend policy inference. Nonblocking Space suggestion remains outside scope.

Whole-page hash protocol affects six rows: ThirdPartyApplication.get and Version.delete/get/list/upload/upload_snapshot. Refresh only those behavior_sha256 values and set their semantic_review_status accepted to pending. Preserve every other field, remaining 419 rows, original review ledger, fixtures, 291 model pages, test073, unit archive and seven existing generator drifts. Historical 425 acceptance does not approve these changed guide bytes. Fresh independent six-operation source/meaning review required before any accepted promotion. No formal QA or release approval supplied.

Verify frozen source rid/version/Website fields and snapshot documentation, local links and 300-line leaves, six affected SDK fixtures/native tests, and exact three-file diff plus every other tracked byte unchanged. No full-suite repeat for unchanged runtime code. No commits, pushes or status changes until reviewed. DEV remains Blocked with LINK-02091 and prior Resolved; no developer restoration or QA closure.
