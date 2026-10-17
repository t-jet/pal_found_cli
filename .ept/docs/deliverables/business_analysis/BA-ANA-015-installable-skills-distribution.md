# Business analysis: Installable Foundry skills distribution

| Field | Value |
| --- | --- |
| Document ID | BA-ANA-015 |
| Feature | FEATURE-014 |
| Status | Canceled on 2026-10-06; retained as an unapproved draft |
| Sources | Project Owner request of 2026-10-05; FEATURE-014; FEATURE-007; FEATURE-013; BA-ANA-007; BA-ANA-014; current `pal_found_cli_skills/README.md` |

This draft records the canceled FEATURE-014 proposal. The Project Owner directed the team to push the reviewed skills repository to GitHub without adding package installation. Its requirements and acceptance criteria were not approved for implementation.

## Business case and scope

Users currently clone the skills repository and copy skill folders into a workspace. Package distribution should let them obtain the same versioned skill set from PyPI or the `t-jet` Conda channel, then make it available to a supported agent harness without cloning Git. The existing clone and copy path remains available. This feature distributes skill content and installation guidance. It does not add Foundry API operations or change CLI behavior.

The current release contains 20 skills: one platform guide, 18 command skills, and `pal-found-dev`. Codex reads a workspace's `.agents/skills/`; Claude Code uses `.claude/skills/` linked to that tree. The 18 command skills need the separate `pal_found_cli` tool when executing commands. Users can read `pal-found-dev` without that tool.

## User journeys

1. A Codex user selects a published skills version from PyPI or `t-jet`, places its 20 folders in the workspace's supported skills location using documented package-based steps, starts a new session, and finds `pal-found` plus the other skills.
2. A Claude Code user obtains the same published bundle, follows the documented workspace setup, starts a new session, and finds the same skills. The workspace keeps one canonical copy of each folder.
3. A user working without network access after installation opens `SKILL.md` and its local references. The guidance remains readable; external source links are optional for reading.
4. A user installs a newer or pinned older skills version, refreshes the workspace, and can identify the version now in use. Removal affects only content installed through the documented path and leaves unrelated workspace skills intact.
5. A user who already follows the clone and copy instructions can continue doing so. The release guidance explains how to avoid mixing two versions in one workspace and how to switch distribution methods safely.

## Business requirements

| ID | Requirement |
| --- | --- |
| BR-014-01 | Publish a discoverable skills distribution for the `pal_found_cli_skills` project on PyPI and the `t-jet` Conda channel. `pal_found_cli_skills` is the proposed consumer-facing project name on both registries, subject to registry availability and Project Owner approval. |
| BR-014-02 | Both channels must deliver the same reviewed set of 20 current skill folders from one source revision, including each `SKILL.md` and all local references required for offline reading. Release verification must detect missing, extra, stale, or broken content. |
| BR-014-03 | Users must have documented package-based steps to make the installed skills discoverable in Codex and Claude Code without cloning Git. The steps must identify where the files go and how a new harness session detects them. The technical mechanism is for solution design. |
| BR-014-04 | Package installation and reading the skills must not require a Foundry account or `pal_found_cli`. Command use in the 18 namespace skills still requires `pal_found_cli`, and Foundry authorization still controls actual operations. User guidance must state these prerequisites clearly. |
| BR-014-05 | The two registry releases must carry the same skills version and source revision. Users must be able to install or pin a named version and determine which version their workspace uses. Skills and CLI version numbers may advance independently; any compatibility constraint must be published. |
| BR-014-06 | Users must have documented update, downgrade, rollback, and removal paths for both package managers and both harnesses. Refreshing or removing the bundle must not delete unrelated skills or user content. An existing conflicting `pal-found-*` folder must be handled explicitly before replacement. |
| BR-014-07 | Existing Git clone and copy distribution must remain documented and usable until a separate migration is approved. Users must know which source populated a workspace and how to avoid a mixed-version set. |
| BR-014-08 | Release notes and package metadata must identify the skills version, supported harnesses, CLI prerequisite for command skills, source revision, license, and differences affecting users. A release must pass installation and discovery checks from each published channel. |
| BR-014-09 | Package publication must use the approved public repositories and release rights. Registry publication must not expose Foundry credentials, internal development documents, or private source files in distributed skill content. |

## Acceptance criteria

| ID | Requirements | Given / when / then |
| --- | --- | --- |
| AC-014-01 | BR-014-01 | Given the approved project name and release version, when a user searches PyPI and the `t-jet` Conda channel, then a public `pal_found_cli_skills` distribution is available on each. |
| AC-014-02 | BR-014-02 | Given clean installs of the same version from both channels, when a reviewer compares the installed skill inventory with the approved source revision, then all 20 current folders and their required local files match, with no missing or stale folder. |
| AC-014-03 | BR-014-02 | Given a locally installed package and no network connection, when a user follows every local link from each skill entry point, then the target content opens and no local authoring file is required. |
| AC-014-04 | BR-014-03 | Given a clean Codex workspace, when a user follows the package-based onboarding steps and starts a new session, then all 20 skills are discoverable from the supported workspace location. |
| AC-014-05 | BR-014-03 | Given a clean Claude Code workspace, when a user follows the package-based onboarding steps and starts a new session, then all 20 skills are discoverable from its supported location, with one canonical content copy. |
| AC-014-06 | BR-014-04 | Given no Foundry credential or `pal_found_cli` installation, when a user installs the skills distribution and reads `pal-found-dev`, then those activities succeed. When the user attempts a documented command from a namespace skill, then the guide identifies the separate CLI prerequisite before use. |
| AC-014-07 | BR-014-05 | Given a named release in both registries, when a reviewer checks its published files and release metadata, then both channels report the same skills version and source revision. |
| AC-014-08 | BR-014-05 | Given an older pinned skills version, when a user follows documented upgrade or downgrade instructions, then the workspace contains the selected version and the user can identify it without relying on a Git checkout. |
| AC-014-09 | BR-014-06 | Given unrelated skills or user files in a workspace, when the bundle is updated or removed through documented steps, then those unrelated files remain intact. |
| AC-014-10 | BR-014-06, 07 | Given an existing `pal-found-*` folder or an earlier clone-based copy, when a user switches to package distribution, then the instructions identify the conflict and lead to one coherent version without silently merging content. |
| AC-014-11 | BR-014-07 | Given a user choosing the existing Git distribution, when they follow its current clone and copy instructions, then the 20 skills remain installable and discoverable. |
| AC-014-12 | BR-014-08 | Given a proposed publication, when reviewers inspect release notes, metadata, and validation evidence, then the stated version, revision, license, harness support, CLI prerequisite, inventory, and channel installation results are recorded before publication. |
| AC-014-13 | BR-014-08, 09 | Given a published PyPI or Conda release, when a reviewer installs it in a clean environment and scans its content, then no Foundry secret or internal project development document is distributed as user guidance. |
| AC-014-14 | BR-014-05 | Given a skills release used with a different CLI version, when a documented compatibility constraint applies, then the user can find it in release guidance and determine whether the combination is supported. |

## Impact, access, and volume

| Area | Effect |
| --- | --- |
| Onboarding | Users gain two package channels. Workspace registration remains an explicit, documented step because installing a distribution alone does not establish harness discovery. |
| Updates and support | A named release gives support staff a reproducible content version. Existing copy users retain their workflow. Instructions must expose version conflicts and a recovery path. |
| Access | Reading and installing public skill content needs no Foundry credential. Registry publication requires authorized maintainers. Foundry operations retain existing CLI, project, and resource permissions. |
| Request rate | Installing or upgrading creates registry downloads, not Foundry API requests. Reading skills offline creates neither. Command execution remains governed by existing CLI behavior. |
| Data size | The bundle includes all skill folders and local reference files. Release verification should compare the actual archive contents and size with the source inventory; no numeric limit is assumed. |

## Decisions, assumptions, and risks

The proposed registry name is `pal_found_cli_skills`, matching the repository. The release needs one skills version on both channels; it need not equal the `pal_found_cli` CLI version. The separate CLI prerequisite reflects the current documentation-only skills model. Solution design should select the package layout and workspace installation mechanism that satisfy these observable requirements.

| Type | Item | Response |
| --- | --- | --- |
| Assumption | Both public registries permit the proposed project name and release rights are available. | Verify before design approval; bring any conflict to Project Owner. |
| Assumption | Current Codex and Claude Code discovery paths in the skills README remain supported. | Verify with clean-workspace acceptance checks. |
| Risk | A package manager install may place files outside the harness search path. | Require a complete workspace onboarding journey and discovery proof. |
| Risk | Users may overlay package and clone copies or upgrade without removing stale files. | Document conflict handling and test a switch, downgrade, and rollback. |
| Risk | A release may contain different content on PyPI and Conda despite matching version labels. | Compare both installed bundles to the same source revision before release acceptance. |
| Risk | Bundled links or references may fail once separated from the repository. | Test local navigation from installed content without network access. |

## Traceability and deliverables

| Source | Coverage |
| --- | --- |
| FEATURE-014 and Project Owner request | BR-014-01 through BR-014-09; AC-014-01 through AC-014-14 |
| FEATURE-007; BA-ANA-007 | BR-014-06, BR-014-07; AC-014-09 through AC-014-11 |
| FEATURE-013; BA-ANA-014 | BR-014-02, BR-014-09; AC-014-02, AC-014-03, AC-014-13 |
| Current skills README | 20-skill inventory; Codex and Claude Code paths; separate CLI prerequisite |

BA-ANA-015 delivers this analysis and its document-index entry. SA-ANA-015 supplies architecture analysis. Later design and implementation work must provide package and harness instructions, release notes, clean-install evidence from both channels, inventory and offline-link checks, upgrade/removal checks, and publication evidence. Reviewers can map each test result to AC-014-01 through AC-014-14.
