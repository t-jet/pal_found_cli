# Architecture Analysis — SA-ANA-007

## Distribute foundry_cli_skills via Git Clone and Skill Copy

| Field | Value |
| --- | --- |
| **Document ID** | SA-ANA-007 |
| **Feature** | FEATURE-007 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Solution Architect |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Affected Services and Interfaces

| Asset | Current state | Target state |
| --- | --- | --- |
| foundry_cli_skills repository | nested repo, LICENSE only | populated with skills and README |
| Skill content | in the design repo under `.claude/skills` | in the skills repo under `.agents/skills` |
| README | absent | clone, copy, and update instructions |
| Supported harnesses | not distributed | per-harness copy instructions |

Distribution is repository-based, not package-based: the repository state is the
release. No artifact publication step exists for skills.

## 2. Architecture Approach

The foundry_cli_skills repository is the single distribution unit. It holds all
skill content in the standard `.agents/skills` layout (FEATURE-006) and a README
that documents the full flow:

1. Clone the repository (BR-007-01).
2. Copy the skill folders into the target harness following the per-harness
   instruction (BR-007-02, BR-007-04).
3. Update by pulling or re-cloning and re-copying (BR-007-05).

The copy target path differs per harness, so the README keeps one section per
supported harness. Versioning is expressed by repository tags; the README tells
users how to check out a specific release if needed.

## 3. Technology Stack

- git and GitHub for hosting and updates
- Markdown instructions (README)
- No package manager, no build step, no runtime dependencies

## 4. General Implementation Approach

1. Populate the skills repo: move the 19 skill folders into `.agents/skills`
   and add the LICENSE and README.
2. Write the README: system requirements (git), clone command, per-harness
   copy instructions, and the update flow (pull, re-copy).
3. Verify a fresh clone yields all skill content (AC-007-01).
4. Verify the copy instructions make skills available in each supported harness
   (AC-007-02, AC-007-04).
5. Verify the update flow delivers the latest content (AC-007-03).

## 5. General Migration Approach

- Phase 1 (populate): move content into the skills repo.
- Phase 2 (document): write the README instructions.
- Phase 3 (verify): fresh-clone and per-harness copy checks.
- Phase 4 (hand off): point users at the repo; retire old distribution notes.

## 6. Risks and Constraints

| Item | Risk | Mitigation |
| --- | --- | --- |
| Wrong copy target | Harness does not load the skills | Per-harness instructions with exact target paths |
| Local drift | Local copies diverge from the repo | Update-by-re-clone guidance (BR-007-05) |
| Missing instructions | Users cannot find the steps | README at the repository root |
| Layout mismatch | Skills copied to a non-standard location | Copy target matches `.agents/skills` (FEATURE-006) |

## 7. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-007 (Analysis) |
| Epic | EPIC-009 |
| BA sub-task | BA-ANA-007 |
| SA sub-task | SA-ANA-007 |
| BA deliverable | BA-ANA-007-business-analysis.md |
| Requirement source | PO architecture-change request 2026-08-11 |
