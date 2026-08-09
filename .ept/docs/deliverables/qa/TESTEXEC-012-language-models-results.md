# TESTEXEC-012 - Foundry Language Models CLI QA results

## Result

**Pass.** All 21 mandatory cases passed. BUG-SUB-011 corrected the global
enablement gate at `a74d3f4`, and the focused and full retest is green on Python
3.11 and 3.12. LM-TC-022 was not run by design because live access was not
approved or required.

Recommended time: **1 hour for BUG-SUB-011 implementation and regression; 3
hours for TESTEXEC-012 execution and QA retest**.

## Baseline and environments

| Item | Value |
|---|---|
| Initial execution commit | `7f26564bc7ef2f2ea1164e72c95688e8828ec820` |
| BUG-SUB-011 retest commit | `a74d3f466c6f6824a2382c76f530e8018901981a` |
| Workspace | Windows 11 Pro; shared working tree with unrelated in-progress changes |
| Python 3.11 | CPython 3.11.9; `foundry-sdk 1.101.0`; `pytest 8.3.5` |
| Python 3.12 | CPython 3.12.0 disposable fully provisioned home; `foundry-sdk 1.102.0`; `pytest 9.1.1` |
| Transport | Nested async SDK fakes, installed SDK models, and installed SDK exceptions |
| External access | No credentials, network transport, live inference, cloud change, or publishing |

The Python 3.12 home was assembled under the operating-system temporary
directory so package tests that create nested `--system-site-packages`
environments inherited a complete dependency set. No production or test source
was changed during execution.

## Command evidence

| ID | Environment and exact command/probe | Expected | Actual | Result |
|---|---|---|---|---|
| E1 | 3.11: `python -m pytest -q tests/test_foundry_language_models_cli.py tests/test_language_models_console_wrapper.py` | Focused Story 012 suite passes | 23 passed in 1.68 s; exit 0 | Pass |
| E2 | 3.11 inline `AnthropicMessagesRequest` invalid-role privacy probe plus real `_serialize_error` | Installed nested validation exits 1 without echoing sentinel | `ValidationError`; SDK/public sentinel checks false; exit 1 envelope; probe exit 0 | Pass |
| E3 | 3.11 inline real `AccessControlGuard` read-only/Tier-3 probe | Both writes blocked in read-only; overrides exact; Tier-3 0/2; missing policy closed | 5/5 checks passed; exit 0 | Pass |
| E4 | 3.11 inline installed `_errors` plus real `RetryHandler` and serializer | All SDK categories use documented attempts/exits and safe messages | 13/13 categories passed; exit 0 | Pass |
| E5 | 3.11: `python -m pytest -q tests/test_tracing_provider.py tests/test_foundry_language_models_cli.py::test_concurrent_attribution_scopes_are_isolated_and_restored` | B3 and attribution contexts are isolated, stable, and restored | 14 passed in 0.13 s; exit 0 | Pass |
| E6 | `rg -n -i "at-least-once\|billable\|retry\|different\|idempot\|application" .claude/skills/foundry-language-models/SKILL.md` | Skill states duplicate-cost risk and forbids an added retry loop | Required warning found on line 12; exit 0 | Pass |
| E7 | 3.11: `python -m pytest -q` | Full active regression passes | 1,013 passed in 26.53 s; exit 0 | Pass |
| E8 | 3.11: `python -m pytest -q --cov=foundry_cli --cov-branch --cov-report=term --cov-fail-under=80` | Full suite passes with branch coverage at least 80% | 1,013 passed in 32.85 s; 84.37%; exit 0 | Pass |
| E9 | 3.11: `python -m pytest -q tests/unit_test_retry_error_output_log.py` | Dormant common suite passes | 149 passed in 0.22 s; exit 0 | Pass |
| E10 | 3.11: `python -m ruff check src tests .claude/skills/foundry-language-models`; `python -m mypy src`; `python -m bandit -q -r src` | Canonical style, type, and security gates pass | Ruff clean; mypy clean across 39 files; Bandit no findings; all exit 0 | Pass |
| E11 | Fully provisioned 3.12: focused command from E1 | Focused Story 012 suite passes | 23 passed in 1.87 s; exit 0 | Pass |
| E12 | Fully provisioned 3.12: `python -m pytest -q` | Full active regression passes | 1,013 passed in 25.28 s; exit 0 | Pass |
| E13 | Fully provisioned 3.12: coverage command from E8 | Full suite passes with branch coverage at least 80% | 1,013 passed in 29.59 s; 84.37%; exit 0 | Pass |
| E14 | Fully provisioned 3.12: dormant command from E9 | Dormant common suite passes | 149 passed in 0.35 s; exit 0 | Pass |
| E15 | Fully provisioned 3.12: canonical Ruff, mypy, Bandit, and `python -m pip check` | Static/security gates pass and dependencies are consistent | Ruff clean; mypy clean across 39 files; Bandit no findings; no broken requirements; all exit 0 | Pass |
| E16 | Base 3.12: `python -m build --wheel --no-isolation --outdir <temp>/wheelhouse <temp-snapshot>` | Clean local wheel builds | `foundry_cli-0.1.0-py3-none-any.whl` built; exit 0 | Pass |
| E17 | Inline wheel archive inspection | Policy and Language Models entry exist; prior entries remain | Policy present; exact entry present; 8 console entries retained | Pass |
| E18 | Isolated wheel install with `--no-deps`; console/Claude help, import, policy, and `pip check` from empty CWD | Installed package is CWD-independent and Tier-3 is 0/2 | Help/import exit 0; catalog 2; blocked 2; policy inside site-packages; empty CWD unchanged; dependencies clean | Pass |
| E19 | Isolated editable install with `--no-deps --no-build-isolation`; same empty-CWD probes | Editable package has the same behavior | Console, Claude launcher, import, and `pip check` exit 0; empty CWD unchanged | Pass |
| E20 | 3.11 inline real guard with `FOUNDRY_AGENTIC_CLI_ENABLED=false` across both catalog rows | Global disable blocks both operations before client work | `anthropic_model.messages` permitted; `open_ai_model.embeddings` permitted; probe exit 1 | Initial fail, resolved by E22 |
| E21 | 3.11 inline real guard with namespace and exact operation `_ENABLED=false` variables | Each lower scope blocks both matching operations | 4/4 checks passed; exit 0 | Pass |
| E22 | `a74d3f4`, 3.11 inline real `ConfigLoader`/guard and CLI retest for both Language Models operations, Datasets, and Audit | Global false blocks all representatives with exit 8 before client; lower-scope controls remain unchanged | 10/10 checks passed; both CLI calls returned exit 8 without reaching the bomb client factory; exit 0 | Pass |
| E23 | `a74d3f4`, 3.11: `python -m pytest -q tests/test_foundry_language_models_cli.py tests/test_language_models_console_wrapper.py tests/test_access_control_guard.py` | Focused ACL and Story suite passes | 93 passed in 1.75 s; exit 0 | Pass |
| E24 | `a74d3f4`, 3.11: `python -m pytest -q` | Full regression passes | 1,020 passed in 26.20 s; exit 0 | Pass |
| E25 | `a74d3f4`, fully provisioned 3.12: focused command from E23 | Focused ACL and Story suite passes | 93 passed in 1.81 s; exit 0 | Pass |
| E26 | `a74d3f4`, fully provisioned 3.12: `python -m pytest -q` | Full regression passes | 1,020 passed in 23.94 s; exit 0 | Pass |

## Focused probe results

### ACL decision matrix

| Check | Actual |
|---|---|
| Global read-only blocks both inference writes | Pass |
| Namespace `_READONLY=false` permits both under parent read-only | Pass |
| Anthropic operation override permits only Anthropic under namespace read-only | Pass |
| Metadata-only permits 0 and blocks 2 | Pass |
| Missing policy fails closed | Pass |
| Namespace and operation enablement block their matching operations | Pass |
| Global `FOUNDRY_AGENTIC_CLI_ENABLED=false` blocks both operations | Initial fail at `7f26564`; retest pass at `a74d3f4` |

All blocked cases stopped before client/SDK work. The focused suite also covers
both canonical operation overrides and enabled/disabled precedence.

### Actual SDK exception taxonomy

The probe used the installed constructors, two retries with zero delay/jitter,
and mocked callables.

| Exceptions | Exit | Attempts | Actual |
|---|---:|---:|---|
| `UnauthorizedError`, `NotAuthenticated` | 2 | 1 | Pass |
| `PermissionDeniedError` | 3 | 1 | Pass |
| `NotFoundError`, `ApiNotFoundError` | 4 | 1 | Pass |
| `BadRequestError`, `ConflictError` | 1 | 1 | Pass |
| SDK `TimeoutError` | 5 | 3 | Pass |
| SDK `ConnectionError` | 6 | 3 | Pass |
| `EnvironmentNotConfigured` | 9 | 1 | Pass |
| `SDKInternalError` | 6 | 1 | Pass |
| `RateLimitError` | 7 | 3 | Pass |
| `ServiceUnavailable` | 6 | 3 | Pass |

Every public SDK envelope used a generic message and omitted injected exception
content. Nested generated-model validation also omitted the prompt sentinel.

### Packaging and import result

The wheel contains
`foundry_cli/language_models/metadata-allow-list.md` and the exact
`foundry-language-models` console entry. The seven existing console entries were
preserved. Wheel and editable environments both passed console and thin Claude
launcher help outside the repository, resolved policy from the installed
package, blocked both operations in Tier-3, passed import-side-effect checks, and
left the empty working directory unchanged.

## Case disposition

| Case | Status | Evidence |
|---|---|---|
| LM-TC-001 | Pass | E1, E11, E17 through E19 |
| LM-TC-002 | Pass | E1, E11 |
| LM-TC-003 | Pass | E1, E11 |
| LM-TC-004 | Pass | E1, E11 |
| LM-TC-005 | Pass | E1, E2, E11 |
| LM-TC-006 | Pass | E1, E2, E11 |
| LM-TC-007 | Pass | E20 through E26; E20 preserves the initial failure history |
| LM-TC-008 | Pass | E1, E3, E7, E11, E12 |
| LM-TC-009 | Pass | E3, E18, E19 |
| LM-TC-010 | Pass | E1, E4, E5, E11 |
| LM-TC-011 | Pass | E1, E5, E11 |
| LM-TC-012 | Pass | E4, E5 |
| LM-TC-013 | Pass | E5 |
| LM-TC-014 | Pass | E4, E6 |
| LM-TC-015 | Pass | E2, E4 |
| LM-TC-016 | Pass | E1, E11 |
| LM-TC-017 | Pass | E1, E11 |
| LM-TC-018 | Pass | E1, E2, E4, E5, E11 |
| LM-TC-019 | Pass | E1, E11, E18, E19 |
| LM-TC-020 | Pass | E16 through E19 |
| LM-TC-021 | Pass | E7 through E19 |
| LM-TC-022 | Not run (optional) | Live access was neither approved nor required |

## Deviations and warnings

- The first Python 3.12 full run used an outer virtual environment whose nested
  Audit package fixture inherited the incomplete machine Python home. It produced
  1,012 passes and one unrelated `ModuleNotFoundError: dotenv`. The definitive
  fully provisioned disposable Python home passed all 1,013 tests and closed the
  environment gap.
- The machine-wide Python 3.11 `pip check` reports conflicts among unrelated
  applications. Both isolated Story 012 install environments and the definitive
  Python 3.12 environment report no broken requirements; those isolated results
  are the canonical dependency evidence.
- The portable Python home initially lacked the Ruff executable and the local
  build module entry point. Adding the already-installed local Scripts directory
  made the canonical 3.12 Ruff gate pass; the base Python 3.12 build frontend then
  produced the wheel without isolation or network access.
- Requests on Python 3.11 warned about its globally installed urllib3 and
  character-detection versions. Pytest-asyncio warned that its future fixture
  loop default is unset. Bandit emitted comment-parser warnings but no finding.
- Disposable `testexec012-*` build, environment, coverage, and help artifacts
  remain in the operating-system temporary directory for evidence review. They
  contain no credentials or live service data.

## Resolved defect history

### BUG-SUB-011 - Global enablement switch was ignored

- Original severity: **High**. Both operations perform potentially billable inference, so
  a global administrative kill switch must stop them before client creation.
- Reproduction: clear `FOUNDRY_AGENTIC_CLI_*`; set
  `FOUNDRY_AGENTIC_CLI_ENABLED=false`; construct the real
  `AccessControlGuard(cfg, "LANGUAGE_MODELS", packaged_policy)`; call `check()`
  for `anthropic_model.messages` and `open_ai_model.embeddings`.
- Expected: both checks raise `AccessControlError`; the CLI emits one safe ACL
  envelope, exits `8`, and does not enter invocation scope or create a client.
- Initial actual result at `7f26564`: both guard checks returned successfully,
  permitting the operations. The focused probe exited `1` with
  `actual_all_blocked=False`.
- Control evidence: namespace and exact operation `_ENABLED=false` variables
  correctly block both matching operations (4/4 checks pass).
- Root cause: the shared guard had no absolute global enablement step, and
  `ConfigLoader` exposed no `global_enabled` property.
- Resolution at `a74d3f4`: BUG-SUB-011 added precedence step 0, made explicit
  global false an absolute denial, exposed the configuration property, and added
  regression cases for both Language Models operations plus Datasets and Audit.
- Retest: direct real-config checks, both CLI boundaries, lower-scope controls,
  focused suites, and full Python 3.11/3.12 regressions all pass. No open defect
  remains.

## QA sign-off

**PASS.** LM-TC-001 through LM-TC-021 passed. BUG-SUB-011 is verified at
`a74d3f4`; no open blocking defect remains. Branch coverage remains above 80%,
and the complete regression suite passes on Python 3.11 and 3.12. LM-TC-022
remains intentionally not run and does not block acceptance.
