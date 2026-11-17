# Filesystem and SQL adapter corrections

The paired draft pins are skills `2190c40c3f73636b91348167b86cdb1bd7fb6fd7`
and tool `a3a38ec434fdb046c329b850e716dc541fa87ecd`.
Both published heads passed GitHub validation. FEATURE-015 remains in review.

## Filesystem: BUG-044

Commit `066970098011c90269aa975d14d7ac713106bbe5` applies existing JSON
coercion to positional arguments. Previously, three batch commands passed strings
to SDK list parameters and failed before HTTP dispatch.

[Independent QA](filesystem-qa.json) verifies all 31 documented examples through
real SDK validation and HTTP serialization, eight boolean probes and five
pagination probes. Four complete pages passed at their recorded hashes after six
prose corrections. [Initial findings](filesystem-initial-findings.json) retain
the original failures. The author also ran 144 focused tests on each SDK 1.101
and 1.111, including 19 new regression cases.

All eight [CI checks](filesystem-ci.json) passed at `0669700`.
[Tracker evidence](filesystem-bug-closure.json) records BUG-044 Closed with
resolution Done and removal of only its verified blocking link. Resource.restore
still has an unresolved SDK semantic conflict; accurate page guidance does not
waive that separate operation review.

## SQL: BUG-045

Commit `a3a38ec` reuses the required/optional/timeout argument builder for Arrow
downloads and removes only the local output filename. Previously,
execute-ontology dropped required query text before calling the SDK.

[Independent QA](sql-qa.json) reproduces the old failure with zero HTTP requests
and verifies five corrected wire cases on each SDK 1.101 and 1.111. Checks cover
query text, typed parameters, dryRun, rowLimit, timeout, saved bytes, checksums,
bounded downloads, response closure and the unchanged get-results route. The
author's new wire tests and existing SQL suite passed 30 tests on each release.

All eight [CI checks](sql-ci.json) passed at `a3a38ec`.
[Tracker evidence](sql-bug-closure.json) records BUG-045 Closed with resolution
Done and removal of only its verified blocking link. [Two-page retest](sql-page-retest.json)
accepts five documented commands and corrected Public Beta/branch-resolution
guidance. [Original page findings](sql-page-initial-findings.json) remain available.

## Scope

All requests used synthetic inputs, real SDK types and mocked HTTP transport with
public sockets denied. No live tenant behavior, feature release, package upload
or tag is claimed. Earlier six-install package evidence remains tied to tool
`657215f`; the later CI builds and runtime checks have their own recorded heads.

The [adapter inventory](adapter-scan.json) preserves the original scan at
`0669700`: 318 metadata rows, 308 resolved SDK operations with matching source
hashes, the subsequently corrected SQL failure, and ten legacy metadata rows
marked UNCERTAIN. Structural return-mode checks are distinct from full operation
acceptance; those uncertain rows remain for further review.
