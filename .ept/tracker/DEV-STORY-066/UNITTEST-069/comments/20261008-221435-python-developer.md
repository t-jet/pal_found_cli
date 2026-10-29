Subject: Unit closure evidence
Created: 2026-10-08T22:14:35
Updated: 2026-10-08T22:14:35
---
## Verified tests
- `node examples/applications/timeout_unit_fixture.mjs` passed with injected transport and no network: timeout abort, caller abort, transport error, timer cleanup, recovery.
- Pinned strict TypeScript compile passed. Localhost HTTP fixture passed with three server-observed canceled connections; actual OSDK `fetchMetadata` probe passed and exposed `PalantirApiError` wrapping `TimeoutError` in `cause.originalError`. Those are separate integration checks.
- Unit file committed in `cffd00e4b2e6eb1df26ccf31edf9c6b49bbed8a1`; `link list UNITTEST-069` has no active Blocks link. No live Foundry or browser OAuth test claimed.
