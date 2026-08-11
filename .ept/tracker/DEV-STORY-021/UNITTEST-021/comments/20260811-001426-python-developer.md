Subject: Test plan — foundry-third-party-applications CLI (9 ops)
Created: 2026-08-11T00:14:26
Updated: 2026-08-11T00:14:26
---
## Test plan (UNITTEST-021)

DEV-021 implementation is ready (commit 74094bc, Resolved). Unit tests are written in `tests/test_foundry_third_party_applications_cli.py` + `tests/test_third_party_applications_console_wrapper.py`; all SDK transport mocked, no external connections.

### Coverage areas (per DESIGN-021 + development type DoD)
1. **Catalog integrity**: exactly 9 OP_SPECS, unique pairs, 3 resources; PAGINATED_OPS exactly {(version, list)}; 5-op write set / 4-op read set map; upload ops declare `file` required.
2. **Parser surface**: every command parses with declared flags; unknown operation rejected (CLIInputError); missing required flag rejected; pagination flags rejected on non-paginated commands.
3. **Dispatch**: each of 9 operations dispatches exact SDK method with correct client_path resolution (root_client.third_party_applications), positional + kwarg args, request_timeout.
4. **Validation**: empty required values rejected before client creation (exit 1, factory.create_calls == 0).
5. **Binary upload**: `version upload`/`upload-snapshot` bounded file read; bytes passed positionally; `--file` never forwarded; `snapshot_identifier` optional omission; missing file exit 1; oversized file (16 MiB + 1) exit 1, no client.
6. **Pagination**: `version list` via with_raw_response + PaginationHelper; multi-page aggregation with page-token chaining; single-page default.
7. **Access control**: READONLY blocks all 5 writes (exit 8, no client); reads permitted; `_is_write_operation` classification matches DESIGN-021; deploy/undeploy registered globally.
8. **Metadata-only policy**: packaged allow-list permits exactly 4 / blocks 5; runtime METADATA_ONLY permits 4 reads, blocks 5 writes (exit 8).
9. **Attribution**: invocation_scope and create use include_attribution=False.
10. **Errors/timeouts/output/console**: ADR-002 timeout bounds; invalid timeout exit 1; SDK error exit 6 with privacy-safe message; TimeoutError exit 5; toon output; console_main wraps asyncio; launcher delegates; launcher --help exit 0.

### Acceptance criteria
- All unit tests passing (100% pass rate).
- Coverage >= 80% branch on new namespace (target ~87%).
- No real network calls in tests.
- Tests committed with implementation (commit 74094bc).

### Related docs
- DESIGN-021: `.ept/docs/deliverables/architecture/DESIGN-021-third-party-applications-cli.md`
- DEV-021 implementation comment: 20260810-235959-python-developer
