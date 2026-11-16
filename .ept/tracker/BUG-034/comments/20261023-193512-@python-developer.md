Subject: 2026-10-23 Open DoD evidence: reproduction, environment and docs confirmed
Created: 2026-10-23T19:35:12
Updated: 2026-10-23T19:35:12
---
## Open DoD evidence (developer)

### Documentation studied
- `.ept/docs/document_index.md` entries consulted: DESIGN-020 (Data Health CLI, including the superseded preview-exclusion lines 12 and 46), DESIGN-020-preview-correction (authority, commit 193e1e90), SA-DES-014 rest-and-sources, metadata-allow-list, canonical-env-var-reference.
- DESIGN-020-preview-correction supersedes DESIGN-020 for the six operations: pass `preview=True` internally on every call, expose no user flag, keep access control, the write set and the metadata-only policy unchanged.

### Critical thinking and open questions
- No open QUESTION sub-tasks. Children of BUG-034: TESTCASE-085 (Closed), TESTEXEC-085 (Closed), CODEREVIEW-086 (Canceled).
- Independent Tech Lead review 20261023-192452-@tech-lead verdict APPROVE with no blocking defects (four P3 notes only).
- PM coordination plan 20261023-185942-@project-manager sets the route Open -> In Progress -> Resolved -> Closed, merge after closure.
- No ambiguity remains that would require an assumption, so no new question is needed.

### Repro steps (confirmed)
1. Inspect `OP_SPECS`, `build_parser` and `_build_kwargs` in `pal_found_cli_tool/src/pal_found_cli/data_health/scripts/pal_found_data_health_cli.py`.
2. At baseline `b9c5f8a`, `_build_kwargs` builds kwargs from `required` and `optional` entries plus `request_timeout`; `preview` appears in no entry, so it is never sent.
3. Six operations affected: check create, delete, get, replace and check_report get, get_latest.
4. Independent probe on the baseline tree reproduces the omission for all six operations (see the In Progress comment for the command and result).

### Environment
- Tool baseline commit `b9c5f8a1a0595fc5fa0cbb27a7a92dba9c1bc67e` (v0.1.5, tool main).
- `foundry-platform-sdk` 1.101.0 (system interpreter) and 1.102.0 (project venv).
- Windows, Python 3.11.9. No live tenant was called; the defect is reproduced locally through a mock transport.

### Expected vs actual
- Expected: the CLI sends the endpoint-required `preview=true` query on all six Data Health operations.
- Actual at baseline: `preview` is absent from every request, so six documented calls omit the required query.
- Application logs: not applicable. The defect reproduces with local mock transport and no deployed service log is available.

Moving to In Progress for root cause and fix documentation.
