Subject: 2026-10-23 Resolved: developer work complete, handed to QA for verification
Created: 2026-10-23T19:42:23
Updated: 2026-10-23T19:42:23
---
## Resolved hand-off (developer)

Status is Resolved. Developer work for BUG-034 is complete; this ticket now moves to QA for verification and closure. Per the PM plan 20261023-185942-@project-manager, QA owns Resolved -> Closed and the resolution value.

### DoD check for In Progress -> Resolved

| Criterion | Status | Evidence |
| --- | --- | --- |
| Studied related documentation from `.ept/docs/document_index.md` | Met | Comment `20261023-193512-@python-developer`; DESIGN-020-preview-correction (`193e1e90`) is the authority |
| Critical thinking applied | Met | Same comment: supersession of DESIGN-020 preview-exclusion lines, no remaining ambiguity |
| All required questions asked and in terminal status | Met | No QUESTION sub-tasks exist. Children: TESTCASE-085 Closed, TESTEXEC-085 Closed, CODEREVIEW-086 Canceled |
| Root cause identified and documented | Met | Comment `20261023-194143-@python-developer` section 1: `_build_kwargs` is the single catalog kwarg builder and no `OP_SPECS` entry carries `preview`, so all six operations omit it |
| Fix implemented and documented | Met | Same comment section 2: `56ec4390c0164ef06b2dc68d3c8ec1462fc7e3e8` (+1 source line, +38/-4 tests); design conformance and unchanged policy file recorded |
| Fix tested and verified | Met | Same comment section 3: independent kwarg probe PASS on six operations, independent six-case CLI-to-wire probe PASS, `--preview` override rejected before client creation PASS, 31/31 fix-commit suite, 49/49 branch-tip suite, 506/506 focused contract suites, Ruff clean; Tech Lead review APPROVE `20261023-192452-@tech-lead`; QA retests `20261016-200453-@qa-engineer` and TESTEXEC-085 evidence |

### Blocker and dependent-link state for QA

- No active is-blocked-by link. `link list BUG-034` shows only `RelatesTo` inbound (`LINK-02011` from BUG-041) and `RelatesTo` outbound; no inbound `Blocks`.
- Outbound `Blocks` links still exist: `LINK-01958` -> DEV-STORY-061 and `LINK-01959` -> DEV-STORY-070, both currently in Development. The Closed DoD for this bug requires that these dependents are unblocked or resolved, so QA should confirm that state at closure or coordinate link removal with the owning role.
- Resolution value was not set by the developer; the PM plan assigns it to QA at closure.

### Constraints honoured

- Branch `feature015/data-health-preview-fix` was not merged, no code was pushed, no tool or skill file was modified by this task. `pal_found_cli_tool` and `pal_found_cli_skills` working trees remain clean at `b9c5f8a` and `716a85b`.
- BUG-034 was not closed.
- All scratch probes live under `.ept/tmp/` (`dh034`, `dh034-base`, `dh034-tip`).

### Residual note for QA

Tech Lead P3 note remains open by design: Data Health skill guidance must state that the CLI opts into preview. It sits outside `56ec439` and outside this bug fix; FEATURE-015 acceptance should confirm the skill deliverable covers it.
