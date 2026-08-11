Subject: Implementation complete — files, verification, OWASP self-review
Created: 2026-08-10T23:59:59
Updated: 2026-08-10T23:59:59
---
## Files created/modified (commit 74094bc)

### Created
1. `src/foundry_cli/third_party_applications/__init__.py` — package export.
2. `src/foundry_cli/third_party_applications/scripts/__init__.py` — scripts package.
3. `src/foundry_cli/third_party_applications/scripts/foundry_third_party_applications_cli.py` — 9-op CLI per DESIGN-021.
4. `src/foundry_cli/third_party_applications/metadata-allow-list.md` — packaged 4/9 policy (4 PERMITTED / 5 BLOCKED).
5. `.claude/skills/foundry-third-party-applications/SKILL.md` — Claude skill doc.
6. `.claude/skills/foundry-third-party-applications/scripts/foundry_third_party_applications_cli.py` — thin launcher.
7. `tests/test_foundry_third_party_applications_cli.py` — 40 unit/integration tests.
8. `tests/test_third_party_applications_console_wrapper.py` — 3 console/launcher tests.

### Modified
9. `src/foundry_cli/common/access_control_guard.py` — added `deploy`, `undeploy` to `_WRITE_VERBS` (DESIGN-021 write set).
10. `tests/test_access_control_guard.py` — regression test `test_third_party_application_verbs_are_writes` (deploy/undeploy).
11. `pyproject.toml` — entry point `foundry-third-party-applications`, package-data, ruff E402 ignore.

## Verification (all green)

- `compileall src` exit 0.
- `ruff check` clean on all new/modified files.
- `mypy` 0 errors (source CLI + guard).
- Focused new tests: **42 passed** (40 CLI + 2 wrapper with launcher); namespace branch coverage **87%** (threshold 80%).
- ACL guard suite: **78 passed** (incl. new deploy/undeploy regression).
- Full suite: **1318 passed, 0 failed**, repo branch coverage **86.61%**.
- Runtime ACL probe: `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` → `version upload` exit 8 (blocked), `version get` passes ACL (reaches client construction).
- Launcher `--help` exit 0; catalog probe: OP_SPECS=9, PAGINATED_OPS={(version, list)}.

## Decisions

- `version upload`/`upload-snapshot` append zip bytes positionally (`_file_bytes`) after bounded 16 MiB read that happens AFTER the ACL decision and BEFORE client construction (DESIGN-021 binary contract; precedent connectivity/media-sets/streams).
- `version list` routed through `with_raw_response` + PaginationHelper (`--page-size`/`--page-token`/`--all`/`--max-pages`).
- `include_attribution=False` on factory + invocation_scope (outside FR-ATTR-4).
- Duplicate-version caveat under at-least-once retries documented in SKILL.md.
- OP_SPECS ordered alphabetically by resource (third_party_application, version, website) per catalog convention.

## OWASP Top-10 self-review

- A01 Broken Access Control: AccessControlGuard runs before client creation and file effects; 5-op write set blocked in READONLY/METADATA_ONLY; metadata policy fail-closed.
- A02 Cryptographic Failures: no crypto in scope; tokens only via env/.env; never echoed.
- A03 Injection: argparse/JSON parsing local; no shell interpolation; RIDs validated non-empty.
- A05 Security Misconfiguration: no secrets hardcoded; error envelopes privacy-safe (generic message for SDK errors).
- A07/A09/A10: no auth/identity changes; no logging of sensitive data; all external calls timeout-configurable.
- A06/A08: no vulnerable deps introduced; no insecure deserialization (json.loads only).

No findings requiring escalation. Ready for code review (CODEREVIEW-021).
