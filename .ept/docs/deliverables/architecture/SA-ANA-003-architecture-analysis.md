# Architecture Analysis — SA-ANA-003

## Split the Project into Three Repositories

| Field | Value |
| --- | --- |
| **Document ID** | SA-ANA-003 |
| **Feature** | FEATURE-003 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Solution Architect |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Affected Services and Interfaces

| Asset | Current state | Target state |
| --- | --- | --- |
| foundry_cli repository | monorepo: design, docs, tracking, CLI source, skills | design and documentation repo only |
| foundry_cli_tool repository | nested git repo, empty | CLI source, tests, packaging, CI |
| foundry_cli_skills repository | nested git repo, LICENSE only | agent skills (`.agents/skills`) |
| `.claude/skills` (19 skill folders) | in design repo | moved to skills repo |
| `src/foundry_cli`, `tests`, `pyproject.toml` | in design repo | moved to tool repo |
| `.ept` docs and tracker | in design repo | stay in design repo |
| GitHub Actions workflows | in design repo | reproduced per repo (tool and skills) |

The nested repositories already exist with their own remotes (`foundry_cli_skills`
points at `t-jet/foundry_cli_skills.git`; `foundry_cli_tool` has its own `.git`),
which matches the assumption recorded in BA-ANA-004.

## 2. Architecture Approach

Three independent repositories, each with its own version history and release
cadence. Content is classified by type before any move:

- Design repo: `.ept` docs, tracker, plans, ADRs, deliverables.
- Tool repo: `src/foundry_cli`, `tests`, `pyproject.toml`, README, CI/CD for the
  package, deployment docs.
- Skills repo: all skill folders under a standard `.agents/skills` layout
  (FEATURE-006), LICENSE, README with clone and copy instructions (FEATURE-007).

Cross-repository references become explicit pointers: absolute GitHub URLs for
docs that link into the tool or skills repos, and repository-relative links
inside each repo. Version coupling is expressed through tags and release notes,
not through shared files.

## 3. Technology Stack

- git and GitHub for hosting and history
- `git filter-repo` or `git subtree` for history-preserving content moves
- Existing Python packaging (setuptools) and CI (GitHub Actions) unchanged
- No new runtime dependencies

## 4. General Implementation Approach

1. Classify every top-level item into one of the three repositories; write the
   mapping down before moving anything.
2. Move content per repository. Prefer history-preserving moves with
   `git filter-repo`; fall back to clean moves when history is not required.
3. Reproduce the CI/CD pipeline in the tool repo and add a minimal pipeline to
   the skills repo.
4. Update cross-repository references and documentation links; run the full
   test suite in the tool repo after the move.
5. Promote the nested repos to standalone public-facing repositories with the
   split completing before visibility changes (FEATURE-002).

## 5. General Migration Approach

- Phase 1 (classification): content map reviewed against BR-004-01..05.
- Phase 2 (move): sequential per-repo moves; each move lands as reviewable
  commits with verified tests.
- Phase 3 (repair): resolve broken references (AC-004-05), update docs.
- Phase 4 (promote): point consumers at the new repos; keep the old monorepo as
  the design repo.

## 6. Risks and Constraints

| Item | Risk | Mitigation |
| --- | --- | --- |
| Wrong classification | Files land in the wrong repository | Written content map before the move |
| Broken references | Cross-repo links stop resolving | Verify every reference after the move (AC-004-05) |
| History loss | Valuable history not carried over | `git filter-repo` for history-preserving moves |
| CI drift | Tool repo loses pipeline coverage | Reproduce pipeline before removing source from design repo |

## 7. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-003 (Analysis) |
| Epic | EPIC-010 |
| BA sub-task | BA-ANA-004 |
| SA sub-task | SA-ANA-003 |
| BA deliverable | BA-ANA-004-business-analysis.md |
| Requirement source | PO architecture-change request 2026-08-11 |
