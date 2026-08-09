# TESTCASE-005 — QA Test Cases for Binary Downloads, Sessions, and Tracing

**Parent:** DEV-STORY-004
**Author:** qa-engineer
**Date:** 2026-07-28
**Design basis:** [DESIGN-005](../architecture/DESIGN-005-common-components.md) §3–§7 (authoritative; §7 Test Matrix maps 1:1 to ticket acceptance criteria)
**Implementation verified:** `src/foundry_cli/common/binary_download_handler.py`, `session_manager.py`, `tracing_provider.py` (runtime smoke confirmed importable, instantiable, and behaviorally correct on 2026-07-28).

## Scope

This deliverable defines QA coverage for the three components delivered in DEV-005 / DEV-STORY-004:

- `BinaryDownloadHandler` — bounded, atomic binary streaming with path containment.
- `SessionManager` — atomic local session persistence with cross-process alias locking and corruption safety.
- `TracingProvider` — SDK-native **B3 multi-header** generation and context isolation.
- Their integration with `RetryHandler` and `ErrorSerializer`.

Tracing coverage uses **B3 multi-header propagation** per DESIGN-005 §5.1 (`X-B3-TraceId` 32-hex / `X-B3-SpanId` 16-hex / `X-B3-Sampled` "0"|"1"), **not** W3C `traceparent`/`tracestate`. Validating W3C output would be a false design.

## Coverage matrix

| Requirement area (DESIGN-005 §7) | Test case IDs | Count |
|---|---|---:|
| Download — bounded streaming, truncation, path safety | TC-DL-001 through TC-DL-010 | 10 |
| Session — schema, locking, compensation, corruption, expiry races | TC-SS-001 through TC-SS-005 | 5 |
| Tracing — disabled, generation, scope restore, concurrency | TC-TR-001 through TC-TR-004 | 4 |
| Integration — retry-in-scope, error serialization | TC-INT-001 through TC-INT-002 | 2 |
| **Total** | | **21** |

Case IDs are assigned 1:1 against the DESIGN-005 §7 test matrix so acceptance-criterion traceability is mechanical.

## Preconditions

- Python 3.11 or 3.12 environment with project test dependencies installed and `.venv` activated.
- `src/` on `PYTHONPATH` (current pytest modules already configure this via `$env:PYTHONPATH="src"`).
- No real Foundry credentials required for unit tests; SDK calls are mocked (`AsyncMock`, fake `Session` with `.rid`).
- Filesystem/portability tests must run on both Windows and POSIX; permission assertions are platform-gated.
- Reference contracts: SRS-001 FR-DL, FR-SESSION, FR-TRACE; ADR-001 (exit codes), ADR-002 (timeouts), ADR-005 (log format); DESIGN-005 §3–§6.

## Test scenarios

### BinaryDownloadHandler (TC-DL-001 … TC-DL-010)

| ID | Scenario | Given | When | Then | Expected result & exit code |
|---|---|---|---|---|---|
| TC-DL-001 | Known length below limit | `Content-Length: 128`, limit 256 | `save()` consumes full stream | Full file stored | `file_size=128`, `truncated=false`, exact `source_size=128`, MD5+SHA256 of stored bytes; exit 0 |
| TC-DL-002 | Known length above limit | `Content-Length: 1024`, limit 256 | `save()` runs | Handler stores prefix and stops without probing EOF | Exactly 256 bytes stored; `truncated=true`; exact `source_size=1024` from header; checksums over stored prefix only |
| TC-DL-003 | Unknown length below limit | No usable `Content-Length`, EOF early | `save()` runs to EOF | Counted source size; no probe | `file_size=expected`, `truncated=false`, exact `source_size=bytes_seen` |
| TC-DL-004 | Unknown length exactly at limit | No usable length; stream ends at exactly limit | `save()` reads one probe byte that hits EOF | Probe reached EOF | `truncated=false`; `source_size=limit` |
| TC-DL-005 | Unknown length above limit | No usable length; stream longer than limit | `save()` reads `limit+1` bytes | One-byte probe observed extra byte | Limit bytes stored; `truncated=true`; `source_size=null`; `source_size_at_least=limit+1`; probe byte not stored, not hashed |
| TC-DL-006 | Malformed or compressed length treated as unknown | `Content-Length: "abc"`, or `Content-Encoding: gzip`, or negative | `save()` runs | Size treated as unknown | Unknown-length path taken (counting, no early truncation from header); exit 0 |
| TC-DL-007 | Traversal / absolute filename rejected | `original_filename="../../etc/passwd"`, `/abs/x`, `"a/b"`, NUL, empty sanitized | `save()` validates before file creation | Path stays below configured root | `InvalidDownloadError`, `exit_code=1`; no file, no UUID dir left behind |
| TC-DL-008 | Stream error or cancellation cleanup | Stream raises or task is cancelled mid-write, or timeout hits | `save()` propagates error | No published final file | Temp file removed; no `os.replace` publication; exit 5 (timeout) or 6 (server/stream) per ADR-001 |
| TC-DL-009 | Concurrent downloads with same name | Two `save()` calls, same `original_filename`, concurrently | Both run | UUID-isolated dirs | Two distinct `file_path` paths; neither overwrites the other; both succeed |
| TC-DL-010 | Filename sanitization and fallback | No `original_filename`, or unusable name, with `mime_type` available | `save()` derives name | Sanitized basename only | Filename is a single basename within UUID dir; derived from namespace/operation/mime fallback when supplied name unusable |

**Platform constraints:** UUID directory permissions `0o700` asserted only on POSIX (`os.name != 'nt'`); Windows relies on owner-restricted ACL where available (DESIGN-005 §3.3). Exclusive creation (`O_EXCL` / `x` mode) and `os.replace` atomicity are platform-agnostic.

### SessionManager (TC-SS-001 … TC-SS-005)

| ID | Scenario | Given | When | Then | Expected result & exit code |
|---|---|---|---|---|---|
| TC-SS-001 | SDK `Session.rid` persisted without token | Mock `create_remote()` returns `Session` with `.rid` (no token) | `create(alias, agent_rid, create_remote)` | RID becomes `session_id` | File written with `session_id=rid`, `session_token=null`, `status=active`; `load()` returns same record; resume uses only `session_id`+`agent_rid`; token never appears in logs/stdout |
| TC-SS-002 | Legacy file omits or contains token | Existing JSON with `session_token` absent, `null`, and present forms | `load(alias)` on each | All three read | Missing/null/string token all load; no `KeyError`; `SessionState.session_token` is `null` for missing/null |
| TC-SS-003 | Concurrent same-alias create | Two concurrent `create()` for identical alias; second sees active record under lock | Lock recheck | Exactly one succeeds; one conflict | First wins via lock + recheck; second raises `SessionAliasConflictError` (`exit_code=1`); exactly one remote `create_remote()` invocation total |
| TC-SS-004 | Persistence fails after remote create | `create_remote()` succeeds; local JSON write raises | Compensation attempted | Best-effort `delete_remote(rid)` once | Original error retained; `SessionPersistenceError` (`exit_code=6`) with `diagnostic_metadata["session_id"]=rid`; if compensation also fails, embedded in metadata without secret values |
| TC-SS-005 | Corrupt state file + expired-cleanup race | (a) JSON corrupt / schema mismatch / invalid status / invalid timestamp; (b) `cleanup_expired(now)` racing `update()` for same alias | Alias lock held during mutation | Warn without secrets; delete under lock; alias absent after | (a) Warning contains no token; `SessionCorruptionError`; file deleted while holding alias lock; subsequent `load()` → `SessionNotFoundError` (`exit_code=4`). (b) Alias lock serializes update vs cleanup; no lost/partial update |

**Platform constraints:** File `0o600` / dir `0o700` on POSIX (DESIGN-005 §4.3); owner-restricted ACL on Windows with graceful warning when not enforceable. Aliases normalized with Unicode NFKC + trim + casefold + whitespace-collapse; reject `.`, `..`, separators, controls, non-ASCII residue, Windows reserved names.

### TracingProvider (TC-TR-001 … TC-TR-004)

| ID | Scenario | Given | When | Then | Expected result |
|---|---|---|---|---|---|
| TC-TR-001 | Tracing disabled | `TracingProvider(enabled=False)` (or `cfg.enable_tracing` false) | `scope()` entered and exited | No SDK context mutation | `scope()` yields `None`; SDK `ContextVar`s untouched before and after; no reset tokens created |
| TC-TR-002 | Generated B3 context is valid | `enabled=True`, default `sampled="1"` | `scope()` entered without supplied context | Provider generates values | `trace_id` is 32 lowercase hex and nonzero; `span_id` is 16 lowercase hex and nonzero; `sampled` is `"0"` or `"1"`; `validate()` passes; values match B3 multi-header contract (`X-B3-TraceId`/`X-B3-SpanId`/`X-B3-Sampled`), **not** W3C |
| TC-TR-003 | Nested/failed scope restores prior values | SDK vars pre-set to known values; supplied context invalid OR scope body raises | `scope()` exits (normal or exception) | Reset tokens applied in `finally` | Prior `ContextVar` values restored on every exit path (success, exception, supplied-invalid → `InvalidTraceContextError`); generated nonzero constraint holds |
| TC-TR-004 | Concurrent async tasks isolated | Multiple async tasks enter `scope()` interleaved/back-to-back | Each enters/exits independently | No leakage | Each task observes its own context; after all exit, SDK vars return to baseline; back-to-back scopes do not reuse a prior generated context |

**Platform constraints:** None (pure-Python context-var isolation). Requires `foundry-sdk` installed for the SDK `ContextVar` import path; absence raises `ConfigurationError` (`exit_code=9`), covered as an edge case. Caller-supplied values pass the same validation as generated ones.

### Integration (TC-INT-001 … TC-INT-002)

| ID | Scenario | Given | When | Then | Expected result |
|---|---|---|---|---|---|
| TC-INT-001 | Retry within tracing scope keeps same B3 across attempts | `RetryHandler.execute_traced()` wrapping a transient-then-ok coroutine inside `TracingProvider.scope()` (DESIGN-005 §6 order: scope before client) | Retry exhausts N attempts then succeeds | Same B3 context through all attempts | Observed `trace_id`/`span_id`/`sampled` identical on every attempt; after return, all three SDK `ContextVar`s are `None`/baseline (no leak). Home: `tests/test_tracing_provider.py` (CODEREVIEW-005 D1) |
| TC-INT-002 | Error serialization leaks no secrets | A download, session, or tracing failure propagates through `ErrorSerializer` | Serialized output / logs inspected | ADR-005 stderr format | Exit codes per ADR-001 (1 user, 4 NF, 5 timeout, 6 server, 9 config); no `session_token`, bearer, request body, response content, or partial temp path appears in any emitted diagnostic |

**Platform constraints:** None beyond the components under test. TC-INT-001 is the CODEREVIEW-005 D1 integration test target.

## Edge cases

| ID | Case | Expected handling |
|---|---|---|
| EC-DL-001 | `max_download_bytes <= 0` or boolean or non-int | `InvalidDownloadError` (`exit_code=1`) before opening a file |
| EC-DL-002 | Unknown length ending exactly at limit → probe hits EOF | `truncated=false` (bounded streaming §3.2 step 6) |
| EC-DL-003 | UUID dir created with `mode=0o700` then umask-independent `chmod` (CODEREVIEW-005 D2) | On-disk `S_IMODE == 0o700` on POSIX; `os.name!='nt'`-gated assertion |
| EC-SS-001 | `session_token` missing vs `null` vs string in stored file | All three load; `SessionState` normalizes missing→`null` |
| EC-SS-002 | Alias normalization: `.` / `..` / NFKC-different / Windows reserved / control chars | `InvalidSessionAliasError` (`exit_code=1`); file name derived only from canonical alias |
| EC-TR-001 | `foundry-sdk` not installed | `ConfigurationError` (`exit_code=9`) raised from `scope()` |
| EC-TR-002 | Caller-supplied `sampled="2"` or non-lowercase/nonzero hex | `InvalidTraceContextError` (`exit_code=1`), raised before any SDK mutation |

## Negative cases

| ID | Case | Expected handling |
|---|---|---|
| NEG-DL-001 | `Content-Length` maliciously huge but stream short | Unknown-length path; never allocates `Content-Length` bytes |
| NEG-DL-002 | Filename resolving outside root after symlink / `resolve()` | Rejected; temp file/dir cleaned |
| NEG-SS-001 | Two writers race same alias without lock | Must not happen — lock + recheck prevents double create; second raises conflict |
| NEG-SS-002 | `cleanup_expired` vs `update` race without serialization | Lock serializes; no partial/lost update |
| NEG-TR-001 | Leak across retries (same span across attempts expected, not a leak) vs leak across *independent* calls (forbidden) | Independent calls get independent contexts; retries intentionally share |
| NEG-INT-001 | Token / temp path appears in serialized error or log | Forbidden; defect (severity High) if observed |

## Expected outputs (exit-code taxonomy — ADR-001)

| Outcome | Exit code |
|---|---:|
| Success — download published / session persisted / trace scope completed | `0` |
| Invalid download config or filename / invalid session alias / invalid B3 context | `1` (UserInput) |
| Tracing backend misconfigured / `.env` load failure | `2` (Auth) or `9` (Configuration) |
| Session not found | `4` (NotFound) |
| Timeout during bounded stream | `5` (Timeout) |
| Stream error / server failure / persistence failure after remote create | `6` (ServerError) |
| Rate-limit retryable (through RetryHandler) | `7` (RateLimit) |
| `foundry-sdk` not installed when tracing enabled | `9` (Configuration) |

Side effects: result payloads on stdout; logs/metadata on stderr per ADR-005; checksum envelopes include additive `source_size` / `source_size_at_least` (either nullable); older envelopes without those fields still parse.

## Test data

| Name | Value |
|---|---|
| Download limit | 256 bytes (TC-DL-001 … 006), 128 bytes (smoke) |
| Known-length payload | 128 B below, 1024 B above limit |
| Unknown-length content-lengths | `None`, `"abc"`, `"-1"`, `Content-Encoding: gzip` |
| Traversal filenames | `../../etc/passwd`, `/abs/x`, `a/b`, `"a\0b"`, `""` |
| Trace ID | 32 lowercase hex, e.g. `a3f…` (nonzero) |
| Span ID | 16 lowercase hex, e.g. `b2e…` (nonzero) |
| Sampled | `"0"`, `"1"` |
| Invalid sampled | `"2"`, `"true"` |
| Agent RID | `ri.aip-agents..agent.fake` |
| Session RID | `ri.session..fake-session-rid` |
| Alias valid | `my-session`, `s1` |
| Alias invalid | `.`, `..`, `a/b`, NFKC-ambiguous, `CON` |

## Platform and execution labels

| ID | Label | Scope | Dependency |
|---|---|---|---|
| TC-DL-001 … 010 | Unit, cross-platform; POSIX permission assertions gated | `tests/test_binary_download.py` | Local Python + `tmp_path` |
| TC-SS-001 … 005 | Unit, cross-platform; POSIX perms gated | `tests/test_session_manager.py` | Local Python + `tmp_path` |
| TC-TR-001 … 004 | Unit | `tests/test_tracing_provider.py` | Local Python, `foundry-sdk` ContextVar fixture |
| TC-INT-001 | Unit integration (CODEREVIEW-005 D1) | `tests/test_tracing_provider.py` | Local Python |
| TC-INT-002 | Unit integration | `tests/test_*_retry_error_output_log.py` | Local Python |

All 21 are unit/integration tests runnable in `.venv` with no live Foundry connection. No environment-dependent smoke is required for these component contracts (those belong to TESTEXEC-005).

## Existing automated coverage reviewed

As of 2026-07-28 the three DEV-005 test modules collect **53 tests** (`pytest --co`): existing cases already exercise truncation boundaries, unknown-length counting, exclusive UUID dir creation (`0o700` umask-independent, CODEREVIEW-005 D2), alias normalization, corruption-safe deletion under lock, persistence-compensation, B3 generation/validation, context isolation across concurrent tasks, back-to-back scopes, and the retry-in-scope integration case (CODEREVIEW-005 D1). This deliverable re-states those contracts under stable case IDs (TC-DL/SS/TR/INT) for TESTEXEC-005 traceability and acceptance-criterion mapping; it does not mandate new test code unless TESTEXEC-005 reveals a gap.

## Approval evidence

Design basis is approved (`DESIGN-005` status: Approved for implementation). The test design is complete and ready for Tech Lead or Architect review, but no ticket-helper evidence was available in this QA pass showing formal approval of `TESTCASE-005` itself. `TESTCASE-005` should not be moved to `Resolved` until that approval is recorded.

## Traceability to TESTCASE-005 acceptance criteria

| Acceptance criterion (ticket AC bullet group) | DESIGN-005 §7 row(s) | Covered by |
|---|---|---|
| Functional: successful downloads, session create/read/purge, config, CLI/SDK integration, tracing enabled/disabled | DL below/above unknown; Session rid no token; Tracing disabled/generated | TC-DL-001/002/003, TC-SS-001/002, TC-TR-001/002 |
| Boundary: exact & exceeded caps, unknown length, expiry boundaries, repeated cleanup | DL at limit, above limit; Session expired cleanup | TC-DL-002/004/005/006, TC-SS-005 |
| Corruption behavior: warn w/o secrets, delete under alias lock, alias absent after | Session corrupt state | TC-SS-005 |
| Schema-error tests; diagnostics hide tokens/credentials/sensitive values | Session legacy token; Integration error serialization | TC-SS-002, TC-INT-002 |
| Path security: traversal, sanitization, configured-root containment, symlink escape, partial-file cleanup | DL traversal/absolute; DL stream error cleanup | TC-DL-007/008/010, NEG-DL-002 |
| Concurrency & atomicity: same-alias create, lock contention, readers-during-replace, cleanup races, deterministic post-op state | Session concurrent create; expired cleanup race; DL concurrent same name | TC-SS-003/005, TC-DL-009 |
| Tracing: valid IDs, SDK propagation, invocation continuity, retry behavior, context reset on every exit, isolation concurrent/back-to-back | Tracing disabled/generated/nested-failed/concurrent; Integration retry-in-scope | TC-TR-001/002/003/004, TC-INT-001 |
| Evidence with case IDs, setup, expected results, platform constraints, execution links | — | This whole document + per-case rows above |

## Review gate

Test case design deliverable (this file). TESTEXEC-005 will execute these 21 scenarios after review/approval and file `BUG-SUB` defects for any failures before DEV-STORY-004 QA sign-off. DoD note: Tracing **must** be validated against **B3 multi-header** shape (`X-B3-TraceId`/`X-B3-SpanId`/`X-B3-Sampled`); asserting W3C headers would be a false negative against the DESIGN-005 §5.1 contract.
