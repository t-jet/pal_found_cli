Subject: 2026-10-23 In Progress DoD: root cause, fix implementation and verification (56ec439)
Created: 2026-10-23T19:41:43
Updated: 2026-10-23T19:41:43
---
## In Progress DoD evidence (developer)

Ticket moved Open -> In Progress by python-developer. This comment records root cause, fix implementation and fix verification for the In Progress -> Resolved DoD.

### 1. Root cause identified

Single shared kwarg builder omits the endpoint-required selector.

- File: `pal_found_cli_tool/src/pal_found_cli/data_health/scripts/pal_found_data_health_cli.py`.
- `_build_kwargs` is the only kwarg builder for the whole catalog. It iterates `spec["required"]` and `spec["optional"]` and adds `request_timeout`. `preview` is present in no `OP_SPECS` entry, so it is never placed in kwargs.
- Because one builder serves all six operations, the omission is systematic across check create, delete, get, replace and check_report get, get_latest, not a per-operation oversight.
- `build_parser` adds arguments only from `positional`, `required` and `optional`, so `--preview` is not a user-facing flag either. The CLI could not express the value in any way, which matches the reported expected-vs-actual gap.
- Palantir documents each of the six endpoints as preview and instructs callers to add `preview=true`; SDK 1.101.0 exposes `preview: Optional[bool]` on all six methods (`maybe_ignore_preview` strips it only when a signature omits it). Local reproduction (below) confirms the released CLI never sends it.

Baseline reproduction, tree of `b9c5f8a1a0595fc5fa0cbb27a7a92dba9c1bc67e` extracted to `.ept/tmp/dh034-base`:

- `.ept/tmp/dh034-base/probe_kwargs.py` (calls `_build_kwargs` per `OP_SPECS` entry): `preview=None` for all six operations; `FAIL: preview missing for [check.create, check.delete, check.get, check.replace, check_report.get, check_report.get_latest]`.
- `.ept/tmp/dh034-base/probe_wire.py` (six real CLI runs through `AsyncFoundryClient` with `httpx.MockTransport`): every request has `preview=[]` on the query string; exit 1 with 12 FAIL lines.

### 2. Fix implemented and documented

- Fix commit: `56ec4390c0164ef06b2dc68d3c8ec1462fc7e3e8` (parent `b9c5f8a`), branch `feature015/data-health-preview-fix`, pushed as `origin/feature015/data-health-preview-fix` (tip `a3a38ec434fdb046c329b850e716dc541fa87ecd`; `git merge-base --is-ancestor 56ec439 origin/feature015/data-health-preview-fix` exits 0). Not merged to tool main; no branch content was pushed or merged by this task.
- Diff scope: `src/pal_found_cli/data_health/scripts/pal_found_data_health_cli.py` (+1) adds `kwargs["preview"] = True` in `_build_kwargs`; `tests/test_pal_found_data_health_cli.py` (+38/-4) adds `test_sdk_preview_flag_reaches_wire` and updates six dispatch assertions. No other file changes.
- Authority: DESIGN-020-preview-correction addendum, committed as `193e1e90f15ae189ad3bc0a457ac4fcf8b95b402` in foundry_cli (`.ept/docs/deliverables/architecture/DESIGN-020-preview-correction.md`). The addendum supersedes the historical preview-exclusion lines in DESIGN-020 and states: pass `preview=True` internally on all six operations, expose no user flag, keep access control, write set, metadata-only policy, retry, timeout and formatting contracts.
- Design conformance: no `--preview` flag added (`OP_SPECS` unchanged); `git diff b9c5f8a 56ec439 -- src/pal_found_cli/data_health/metadata-allow-list.md` is empty, so the policy file is byte-identical; write classification and access control code are untouched.

### 3. Fix tested and verified (independent probes plus suites)

Tree of `56ec439` extracted to `.ept/tmp/dh034`; venv interpreter has `toon_format` and `foundry-platform-sdk 1.102.0`.

| Check | Command | Result |
| --- | --- | --- |
| Kwarg builder | `PYTHONPATH=src python probe_kwargs.py` | PASS: `preview=True` on all six operations |
| CLI-to-wire, six operations | `PYTHONPATH=src python probe_wire.py` | PASS: `POST/DELETE/GET/PUT` and both CheckReport `GET` all carry exactly one `preview=true`; exit 0 |
| No user override | `PYTHONPATH=src python probe_no_override.py` | PASS: `--preview false` returns exit 1 `UserInputError` before client creation on all six |
| Fix-commit suite | `PYTHONPATH=src python -m pytest tests/test_pal_found_data_health_cli.py -q` | 31 passed |
| Branch-tip suite | same file at `a3a38ec` | 49 passed |
| Preview-selected cases | `-k preview` at tip | 19 passed |
| Focused contract suites at tip | `test_cli_parser_contract`, `test_shared_cli_contracts`, `test_retry_timeout_contract`, `test_output_format_contract`, `test_required_preview_wire`, `unit_test_common_components`, `unit_test_retry_error_output_log`, `test_pal_found_data_health_cli` | 506 passed |
| Lint | `ruff check src/pal_found_cli/data_health/scripts/pal_found_data_health_cli.py tests/test_pal_found_data_health_cli.py` | All checks passed |

Observed wire matrix at `56ec439` (independent probe, no branch test code reused): `check-create POST /api/v2/dataHealth/checks`, `check-delete DELETE /api/v2/dataHealth/checks/{rid}`, `check-get GET /api/v2/dataHealth/checks/{rid}`, `check-replace PUT /api/v2/dataHealth/checks/{rid}`, `check-report-get GET .../checkReports/{rid}`, `check-report-get-latest GET .../checkReports/getLatest`; each with `preview=true` and no `attribution` or `_sdk_internal` kwarg.

Corroborating independent evidence already on this ticket: Tech Lead review `20261023-192452-@tech-lead` verdict APPROVE, no blocking defects (four P3 notes); QA `20261016-200453-@qa-engineer` 33/33 plus 6/6 mock-transport; TESTCASE-085 and TESTEXEC-085 Closed with 18/18 CLI scenarios and 51/51 focused suite.

### 4. OWASP Top-10 self-review

- A01 Broken access control: `AccessControlGuard(...).check(resource, operation)` still runs before client construction; no guard code changed. No new capability is reachable.
- A02 Cryptographic failures: no secret handling change; no credential, token or key added to source or tests (synthetic token only in tests).
- A03 Injection: no string-built request; `preview` is a boolean kwarg serialized by the SDK, not concatenated into a URL.
- A04 Insecure design: fix follows the approved addendum; the value is not user-overridable, which prevents a caller from silently dropping a required server-side contract.
- A05 Misconfiguration: no configuration, environment or policy file changed (`metadata-allow-list.md` byte-identical).
- A06 Vulnerable components: no dependency added or bumped.
- A07 Identification/authentication failures: auth path unchanged.
- A08 Integrity failures: no deserialization or artifact-trust change.
- A09 Logging/monitoring failures: no log statement added or removed; error envelope behavior unchanged.
- A10 Server-side request forgery: no new outbound target; the existing endpoint set is unchanged.

No hardcoded credentials, no inline logging configuration, no network activity at import time, full type annotations and docstrings retained on the touched function.

### 5. Residual non-blocking note

The Tech Lead review P3 note stands: the addendum also requires Data Health skill guidance to tell offline users that the CLI opts into preview. That deliverable is outside `56ec439` and outside this bug fix. FEATURE-015 acceptance should confirm it is covered (candidate owner: the affected skill story). Recorded here so QA can weigh it at Resolved -> Closed; it is not a defect in the fix.

Moving to Resolved for QA verification.
