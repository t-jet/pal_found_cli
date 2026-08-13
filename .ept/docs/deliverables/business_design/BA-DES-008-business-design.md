# Business Design — BA-DES-008

## Distribute the Skills via Git Clone and Skill Copy

| Field | Value |
| --- | --- |
| **Document ID** | BA-DES-008 |
| **Feature** | FEATURE-007 |
| **Status** | In Progress |
| **Date** | 2026-08-13 |
| **Author** | Business Analyst |
| **Based on** | BA-ANA-007, SA-ANA-007 (Closed, PO-approved) |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Design Overview

The design defines how users obtain the agent skills: clone the
`pal_found_cli_skills` repository (ND-010-01) and copy the `pal-found-*`
skill folders into the target harness. Distribution is file-based and
dependency-free. The design covers the user instructions, per-harness target
locations, and the update path.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-D-008-01 | Users must be able to obtain all skills by cloning the `pal_found_cli_skills` repository. |
| BR-D-008-02 | Users must be able to copy skill folders into a target harness following documented instructions. |
| BR-D-008-03 | The repository must provide clear instructions for cloning, copying, and updating skills. |
| BR-D-008-04 | Instructions must work for every supported harness. |
| BR-D-008-05 | Updating must be possible by re-cloning or pulling the repository and re-copying. |
| BR-D-008-06 | Instructions must cite the standard `.agents/skills` location where the harness supports it (FEATURE-006). |

## 3. Logical Flow (business terms)

1. A user clones the `pal_found_cli_skills` repository from its public
  location.
2. The user identifies their harness in the instructions and reads the
  target folder for that harness (the standard `.agents/skills` folder, or
  a documented harness-specific location).
3. The user copies the `pal-found-*` skill folders from the clone into the
  target folder.
4. The user verifies the harness discovers the skills.
5. When an update is available, the user pulls or re-clones the repository
  and re-copies the skill folders.

## 4. UI/UX (abstract)

No custom interface is built; the design defines documentation and file
layout. Abstract user experience:

- A user follows the README steps: clone, locate target folder, copy skill
  folders, verify.
- A user on any supported harness finds a matching section in the
  instructions with the correct target location.
- A user updating skills pulls the repository and re-copies; no package
  manager is involved.
- Error experience: if a user copies to the wrong folder, the instructions
  describe how to detect that the harness is not loading the skills and how
  to correct the location.

## 5. API Specification (abstract)

No application interfaces change. The design relies on standard file and
version-control capabilities:

- A clone or pull action that retrieves the skills repository content.
- A file-copy action that places skill folders into the harness target
  folder.
- A discovery action by the harness that reads the skill folders.

## 6. Data Structures (business terms)

- Skills repository record: repository name, clone URL, folder layout,
  README location.
- Harness target record: harness name, target folder path (standard or
  harness-specific), verification step.
- Copy instruction record: source folder, destination folder, update
  procedure per harness.

## 7. Acceptance Criteria

- AC-D-008-01: Given a user, when they clone the `pal_found_cli_skills`
  repository, then they receive all skill content.
- AC-D-008-02: Given a cloned repository, when the user follows the copy
  instructions, then the skills become available in the target harness.
- AC-D-008-03: Given a skills repository update, when a user pulls or
  re-clones, then they can refresh local skills to the latest version.
- AC-D-008-04: Given a user on any supported harness, when they follow the
  instructions, then the steps are clear and complete.
- AC-D-008-05: Given the repository documentation, when a user reads it,
  then cloning, copying, and updating steps are described.

## 8. Migration Procedure

1. Confirm the skills repository layout matches the standard
  `.agents/skills` folder (FEATURE-006) so the copy step is uniform.
2. Author the README with three sections: cloning, copying per harness,
  and updating.
3. Record each supported harness and its target folder in the instructions.
4. Publish the instructions with the first public release of the skills
  repository (FEATURE-002).
5. Verify the instructions end to end on each supported harness
  (AC-D-008-02, AC-D-008-04).
6. Announce the distribution method and keep the instructions versioned
  with the repository.
7. Rollback: distribution is file-based; an erroneous update is reverted by
  re-cloning the last good repository state and re-copying.

## 9. Developer Story Scope

One story covers the distribution instructions, per-harness target map, and
end-to-end verification.

## 10. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-007 |
| Epic | EPIC-009 |
| BA design sub-task | BA-DES-008 |
| SA counterpart | SA-DES-007 |
| Analysis | BA-ANA-007, SA-ANA-007 (Closed, PO-approved) |
| Naming decisions | ND-010-01 (QUESTION-072, Closed) |
