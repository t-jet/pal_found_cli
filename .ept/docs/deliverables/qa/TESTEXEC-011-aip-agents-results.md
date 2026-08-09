# TESTEXEC-011 - Foundry AIP Agents CLI QA results

## Result

**Pass.** The Story 011 functional, security, privacy, packaging, compatibility,
and delivery-gate checks passed. No blocking defect was found, and no BUG-SUB is
recommended from this run.

Recommended QA effort for this execution and evidence record: **8 hours**.

## Baseline and environment

| Item | Value |
|---|---|
| Candidate commits | `ee2cef7`, `8a533fd`, `02920aa`, `224ca5d` |
| Workspace | Windows 11 Pro; current shared working tree |
| Python | CPython 3.11.9 and CPython 3.12.0 |
| SDK | `foundry-sdk 1.101.0` |
| Test runner | `pytest 8.3.5` |
| Transport | Mocked SDK clients and local isolated environments only |
| External systems | No credentials, live Foundry calls, cloud changes, or publishing |

The shared working tree contained unrelated in-progress changes. QA evidence
covers the listed candidate commits and the current Story 011 implementation;
no production or test source was changed during execution. Clean candidate
verification remains a DevOps deployment task and is not a QA blocker.

## Evidence summary

| ID | Command or probe | Expected | Actual | Result |
|---|---|---|---|---|
| E1 | `python -m pytest -q tests/test_foundry_aip_agents_cli.py tests/test_aip_agents_console_wrapper.py` | Focused AIP suite passes on 3.11 | 54 passed in 0.28 s; exit 0 | Pass |
| E2 | Same focused suite in the isolated Python 3.12 environment | Focused AIP suite passes on 3.12 | 54 passed in 0.35 s; exit 0 | Pass |
| E3 | Inline probe using installed `foundry_sdk._errors` classes and the real serializer/retry handler | All ADR categories map to the documented exits and retries | 13/13 passed; exit 0 | Pass |
| E4 | `python -m pytest -q` | Active regression passes on 3.11 | 988 passed in 25.24 s; exit 0 | Pass |
| E5 | `python -m pytest -q --cov=foundry_cli --cov-branch --cov-report=term --cov-fail-under=80` | Branch coverage is at least 80% | 988 passed; 84.27% total in 30.13 s; exit 0 | Pass |
| E6 | `python -m pytest -q tests/unit_test_retry_error_output_log.py` | Dormant common suite passes | 149 passed on 3.11 in 0.22 s and 149 passed on 3.12 in 0.37 s | Pass |
| E7 | Full active suite and branch coverage in a fully provisioned Python 3.12 environment | Regression passes and coverage is at least 80% | 988 passed in 22.86 s; coverage run 988 passed with 84.27% in 27.63 s; both exit 0 | Pass |
| E8 | `python -m ruff check src tests .claude/skills/foundry-aip-agents` | Story source, tests, and skill are clean | All checks passed; exit 0 | Pass |
| E9 | `python -m mypy src` and `python -m bandit -q -r src` | Type and security gates pass | Mypy: 36 files clean. Bandit: no findings. Both exit 0 | Pass |
| E10 | Offline `python -m build --wheel --no-isolation`, wheel inspection, and install with `--no-deps` | Wheel builds and contains policy plus all console entries | `foundry_cli-0.1.0-py3-none-any.whl` built; policy and AIP entry present; exit 0 | Pass |
| E11 | Wheel and editable installs; console and Claude launcher help/import from an empty CWD without `PYTHONPATH` | Entry points and policy are independent of the repository CWD | Both install forms passed; both help paths exit 0; policy exists; empty CWD remained empty | Pass |
| E12 | Installed-package metadata-only guard probe | Exactly 6 SDK operations permitted, 9 denied, and purge denied | Exact expected six permitted; 9 blocked; purge blocked; exit 0 | Pass |
| E13 | `python -m pip check` in the fully provisioned Python 3.12 environment | Installed dependencies are consistent | No broken requirements; exit 0 | Pass |

### Actual SDK error-class probe

| SDK category | Expected exit | Expected attempts | Actual |
|---|---:|---:|---|
| `UnauthorizedError`, `NotAuthenticated` | 2 | 1 | Pass |
| `PermissionDeniedError` | 3 | 1 | Pass |
| `NotFoundError`, `ApiNotFoundError` | 4 | 1 | Pass |
| `BadRequestError`, `ConflictError` | 1 | 1 | Pass |
| SDK `TimeoutError` | 5 | 3 | Pass |
| SDK `ConnectionError` | 6 | 3 | Pass |
| `EnvironmentNotConfigured` | 9 | 1 | Pass |
| `SDKInternalError` | 6 | 1 | Pass |
| `RateLimitError` (429) | 7 | 3 | Pass |
| `ServiceUnavailable` (503) | 6 | 3 | Pass |

The probe used real installed exception constructors and local callables. Retry
delay was set to zero; no network request was made.

### Installed policy result

The installed guard permitted only:

- `agent.get`
- `agent_version.get`
- `agent_version.list`
- `session.get`
- `session.list`
- `session_trace.get`

The other nine SDK operations were denied, and local `session.purge` was denied
separately. The policy was loaded from
`foundry_cli/aip_agents/metadata-allow-list.md` inside the installed package.

## Test-case disposition

| Case | Status | Primary evidence |
|---|---|---|
| AIP-TC-001 | Pass | E1, E2 |
| AIP-TC-002 | Pass | E1, E2 |
| AIP-TC-003 | Pass | E1, E2 |
| AIP-TC-004 | Pass | E1, E2 |
| AIP-TC-005 | Pass | E1, E2 |
| AIP-TC-006 | Pass | E1, E2 |
| AIP-TC-007 | Pass | E1, E2 |
| AIP-TC-008 | Pass | E1, E2 |
| AIP-TC-009 | Pass | E1, E2 |
| AIP-TC-010 | Pass | E1, E2 |
| AIP-TC-011 | Pass | E1, E2 |
| AIP-TC-012 | Pass | E1, E2 |
| AIP-TC-013 | Pass | E1, E2 |
| AIP-TC-014 | Pass | E1, E2 |
| AIP-TC-015 | Pass | E1, E2 |
| AIP-TC-016 | Pass | E1, E12 |
| AIP-TC-017 | Pass | E1, E2 |
| AIP-TC-018 | Pass | E1, E2 |
| AIP-TC-019 | Pass | E1, E2 |
| AIP-TC-020 | Pass | E1, E2, E3 |
| AIP-TC-021 | Pass | E1, E2 |
| AIP-TC-022 | Pass | E1, E2 |
| AIP-TC-023 | Pass | E1, E3, E6 |
| AIP-TC-024 | Pass | E1, E2 |
| AIP-TC-025 | Pass | E1, E2 |
| AIP-TC-026 | Pass | E1, E2, E3 |
| AIP-TC-027 | Pass | E1, E2, E11 |
| AIP-TC-028 | Pass | E10, E11, E12 |
| AIP-TC-029 | Pass | E4 through E10, E13 |
| AIP-TC-030 | Not run (optional) | Live access was neither approved nor required |

## Deviations and warnings

### Resolved Python 3.12 environment gap

The first isolated Python 3.12 attempt produced 987 passes and one environment
failure:

`tests/test_audit_console_wrapper.py::test_wheel_and_editable_installs_work_from_arbitrary_cwd_without_pythonpath`

That test creates another virtual environment with `--system-site-packages`,
installs the wheel with `--no-deps`, and launches `foundry-audit --help`. The
nested environment inherits the incomplete base Python 3.12 packages and fails
with `ModuleNotFoundError: dotenv`. Story 011 focused tests pass on the same
interpreter, and the AIP wheel and editable checks pass in complete isolated
environments. Classification: test-environment dependency gap, not a Story 011
functional defect. DevOps reran the gates in a fully provisioned Python 3.12
environment: the full suite passed 988 tests in 22.86 seconds, the coverage run
passed 988 tests at 84.27% in 27.63 seconds, and `pip check` reported no broken
requirements. This closes the earlier evidence gap.

### Repository-wide Ruff result

`python -m ruff check .` returned 312 findings outside the canonical gate scope.
The dot scan includes vendored `.ept/docs` SDK content, unrelated `.ept/skills`,
and other non-Story tooling. CI and prior DevOps execution define the canonical
scope as `src`, `tests`, and the Story skill. That scoped command passes, as do
mypy and Bandit. The dot-scan result is retained for transparency but does not
block Story 011 sign-off.

### Non-blocking warnings and setup retries

- Requests emitted a dependency compatibility warning for the installed
  `urllib3`/character-detection versions.
- Pytest-asyncio warned that `asyncio_default_fixture_loop_scope` is unset.
- The initial isolated Python 3.12 coverage attempt used the pure-Python tracer
  because its optional C tracer was unavailable; it still measured 84.27%.
- Bandit printed comment-parser warnings but reported no security finding.
- The first offline Python 3.11 build/editable attempts lacked local build
  backends (`setuptools>=68`/`wheel` and `bdist_wheel`). They were rerun without
  network using the already-installed Python 3.12 build backend and passed.
- Disposable `testexec011-*` environments and logs remain under the operating
  system temporary directory because the execution policy rejected recursive
  cleanup. They contain no credentials or live service data.

## QA recommendation

**QA sign-off: PASS.** Cases AIP-TC-001 through AIP-TC-029 passed. No blocking
functional, security, packaging, compatibility, or regression defect remains,
and no BUG-SUB is required. AIP-TC-030 remains not run by design because the
optional live smoke was neither approved nor needed for mocked acceptance.

The dirty shared-worktree context is recorded above. Verification of a clean
assembled candidate remains part of DevOps deployment and does not block this
QA sign-off.

The named tech-lead approval gate from TESTCASE-011 remains separate from this
execution record; this document does not claim that approval.
