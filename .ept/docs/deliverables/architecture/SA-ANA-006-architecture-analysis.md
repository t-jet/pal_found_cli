# Architecture Analysis — SA-ANA-006

## Store Skills in a Standard `.agents/skills` Folder for All Harnesses

| Field | Value |
| --- | --- |
| **Document ID** | SA-ANA-006 |
| **Feature** | FEATURE-006 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Solution Architect |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Affected Services and Interfaces

| Asset | Current state | Target state |
| --- | --- | --- |
| Skill folders (19 total: `foundry` + 18 namespace skills) | under `.claude/skills` | under `.agents/skills` |
| Supported agent harnesses | Claude Code reads `.claude/skills` | all harnesses read or point at `.agents/skills` |
| AGENTS.md and documentation | reference `.claude/skills` | reference `.agents/skills` |
| Skills repository layout | old layout | standard layout (consumed by FEATURE-007) |

Harnesses differ in how they discover skills. Some read `.agents/skills`
natively; others need a settings entry or a copy step. The migration keeps one
canonical copy (BR-006-03) and documents per-harness onboarding (BR-006-05).

## 2. Architecture Approach

`.agents/skills` becomes the single canonical location for all skill content.
Each harness is then wired to that location:

- Harnesses that support `.agents/skills` natively: no configuration.
- Harnesses that do not: explicit onboarding instructions in the README and in
  AGENTS.md describing how to point the harness at the folder (settings,
  symlink, or copy).

After all harnesses are verified against the new location, the old
`.claude/skills` content is removed so no skill content lives only there
(BR-006-04). This layout is also the distribution unit for FEATURE-007 (git
clone and skill copy).

## 3. Technology Stack

- File and folder layout only (markdown skill files)
- Optional per-harness configuration files (settings, symlinks)
- No new runtime dependencies or code changes

## 4. General Implementation Approach

1. Move the 19 skill folders from `.claude/skills` to `.agents/skills`.
2. Verify discovery on each supported harness (AC-006-01); fix any harness
   that needs configuration or a pointer.
3. Update AGENTS.md and all documentation references to the new location.
4. Verify a skill author can update one copy and all harnesses use it
   (AC-006-02).
5. Remove the old `.claude/skills` location after verification (AC-006-03).
6. Publish harness onboarding instructions for harnesses that do not recognize
   the standard folder (AC-006-04).

## 5. General Migration Approach

- Phase 1 (move): relocate folders, keep old location until verified.
- Phase 2 (verify): harness-by-harness discovery checks.
- Phase 3 (repair): fix references in docs and AGENTS.md.
- Phase 4 (cleanup): remove the old location and record completion.

## 6. Risks and Constraints

| Item | Risk | Mitigation |
| --- | --- | --- |
| Silent ignore | A harness does not recognize the folder and loads no skills | Per-harness discovery verification (AC-006-01) |
| Content drift | Old and new locations diverge during migration | Remove old location after verification (AC-006-03) |
| Broken references | Docs still point at `.claude/skills` | Reference sweep in phase 3 |
| Harness gap | A harness needs non-standard wiring | Documented onboarding instructions (BR-006-05) |

## 7. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-006 (Analysis) |
| Epic | EPIC-009 |
| BA sub-task | BA-ANA-006 |
| SA sub-task | SA-ANA-006 |
| BA deliverable | BA-ANA-006-business-analysis.md |
| Requirement source | PO architecture-change request 2026-08-11 |
