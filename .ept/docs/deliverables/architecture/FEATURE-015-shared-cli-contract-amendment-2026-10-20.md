# Shared CLI contract amendment

Recorded: 2026-10-20. Scope: BUG-037, BUG-039 and BUG-040.
Authority: architect answers on QUESTION-192 (`20261020-103158-@architect`)
and QUESTION-193 (`20261020-103239-@architect`). Implementation, independent
QA and distribution verification remain separate release gates.

This addendum records the approved technical corrections to SRS-001,
SAD-001 and ADR-004. Their original text remains available as decision history.

## TOON dependency and API

Use the official [TOON Python repository](https://github.com/toon-format/toon-python)
through distribution `toon-format==1.2.0`, imported as `toon_format`.
Encode normalized JSON-compatible values with `toon_format.dumps(data)`.
Independent verification uses `toon_format.loads(text)`.

This decision explicitly replaces the historical `toon-python >=0.9,<1.0`
dependency and guessed `toon.from_list()` API in SRS-001 section 2.4/C-2,
SAD-001 dependency guidance and ADR-004 implementation references. The old
literal version interval is not satisfied. The approved version requires
Python 3.10 or later, compatible with the project's Python 3.11 minimum.
Primary package metadata is available from
[PyPI](https://pypi.org/pypi/toon-format/1.2.0/json).

Preserve the actual-library decision in QUESTION-012 and ADR-004 selection
rules: nonempty uniform arrays of objects qualify for TOON; errors, empty
arrays, non-list results, mixed values and heterogeneous objects remain JSON.
The aligned custom table does not satisfy this requirement. A missing mandatory
dependency is a packaging failure; defensive JSON fallback for an unexpected
encoder failure must not conceal a missing dependency.

Independent QA must verify actual TOON headers and scalar escaping, decode
subprocess output with the real library, and exercise format selection and
stdout/stderr separation. DevOps must verify built wheel/sdist installation,
the declared package version, `pip check`, and private-mirror requirements.
Package/API research alone proves neither completed QA nor deployment.

## One effective timeout per attempt

Resolve one timeout before invocation and pass it to both SDK `request_timeout`
and outer `asyncio.wait_for`. An explicit CLI `--timeout` wins in both layers.
CLI values must be integer seconds from 1 through 3600; reject invalid values
with exit 1 and JSON stdout before SDK invocation.

Without an override, ordinary namespaces use
`FOUNDRY_AGENTIC_CLI_TIMEOUT_S`, default 30. Streams uses its separate
`FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S`, default 120. Clamp environment integers
to 1 through 3600; malformed, fractional or nonfinite values use the relevant
default. This normalization is an implementation clarification in QUESTION-192.

Explicit internal constructor `timeout_s=None` may retain its test bypass;
public CLI configuration cannot disable the timeout. Finite subsecond internal
values may support bounded tests. Each attempt receives its own timeout, so
total command duration can also include retries and backoff. This addendum
does not change terminal error serialization or cancellation policy.

## Total attempt count

`FOUNDRY_AGENTIC_CLI_RETRY_MAX_ATTEMPTS` counts all calls, including the first.
Default 4 preserves DEV-STORY-008 AC-5. Value 1 permits one call and no retry.
Malformed, fractional or nonfinite environment values use 4; nonpositive
integers normalize to 1. No upper cap is introduced.

Canonical constructor `max_attempts` accepts a positive integer. Explicit
legacy `max_retries=N` retains N retries plus the initial call. Reject boolean,
noninteger and invalid nonpositive values for `max_attempts`, negative values
for `max_retries`, and simultaneous non-None arguments. Count real invocations
and delays in regression tests; retain the established retryability taxonomy.

## Acceptance

The amendment resolves technical interpretation. BUG-037, BUG-039 and BUG-040
remain open until implementation, code review, independent QA and required
packaging checks pass. FEATURE-015 acceptance and release remain pending.
