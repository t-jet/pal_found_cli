# Business Design — BA-DES-006

## Publish the CLI Tool to a Conda Channel

| Field | Value |
| --- | --- |
| **Document ID** | BA-DES-006 |
| **Feature** | FEATURE-005 |
| **Status** | In Progress |
| **Date** | 2026-08-13 |
| **Author** | Business Analyst |
| **Based on** | BA-ANA-005, SA-ANA-005 (Closed, PO-approved) |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Design Overview

The design defines how the CLI tool is published to a conda channel so
conda-based users can install it with one command. The package is published
under the confirmed name `pal_found_cli` (ND-010-02), complementing the PyPI
channel (FEATURE-004). The design covers channel selection, release
publication, version alignment between channels, and the user-facing install
experience.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-D-006-01 | The tool must be published to a conda channel so it can be installed with conda. |
| BR-D-006-02 | Installing must not require manual configuration beyond the channel setup. |
| BR-D-006-03 | Versioned releases must be published and users must be able to update. |
| BR-D-006-04 | A user without channel access must receive a clear error when installation is not possible. |
| BR-D-006-05 | The channel must describe what the tool does and how to install and use it. |
| BR-D-006-06 | Conda and PyPI releases must be published from the same versioned source. |
| BR-D-006-07 | The published artifact must contain no embedded credentials. |

## 3. Logical Flow (business terms)

1. A maintainer chooses a public conda channel suitable for the tool and
  confirms publishing rights.
2. A release is prepared from the same versioned source state used for the
  PyPI release (FEATURE-004), with the same version number.
3. The conda package is built and installed into a clean conda environment;
  a smoke run verifies the tool starts and executes a basic command.
4. The artifact is uploaded to the channel and the channel page is updated
  with description and install instructions.
5. Version alignment is checked between the conda and PyPI releases.
6. Users install or update with conda and receive the tool with its
  dependencies resolved against the environment.

## 4. UI/UX (abstract)

The design assumes the standard channel web interface; no custom interface
is built. Abstract user experience:

- A conda user runs the install command and the tool becomes available in
  their environment.
- A user opens the channel page and sees the description, install command,
  and version list.
- A user updates the package and receives the new version.
- Error experience: a user without channel access sees a clear failure
  message and the documented way to obtain the channel.

## 5. API Specification (abstract)

No new tool interfaces are introduced. The design relies on the channel
service behaviour:

- A publish action that uploads a versioned conda package to the channel.
- A download action that serves the package to conda during install or
  update.
- A metadata record (description, dependencies, install command) shown on
  the channel page.
- Channel credentials used only by maintainers at publish time; never
  embedded in the artifact.

## 6. Data Structures (business terms)

- Channel record: channel name, access model (public/restricted), owner,
  package list.
- Release record: version number, source state reference, conda artifact,
  PyPI counterpart version, verification result, publication timestamp.
- Verification checklist record: clean conda-install result, smoke-run
  result, version-alignment result, secret scan result.

## 7. Acceptance Criteria

- AC-D-006-01: Given a user with conda installed, when they install the
  package from the configured channel, then the tool installs successfully.
- AC-D-006-02: Given an installed release, when the user runs a tool
  command, then it works as documented.
- AC-D-006-03: Given a published new version, when a user updates the
  package via conda, then they receive the new version.
- AC-D-006-04: Given a user without channel access, when they try to
  install, then the attempt fails with a clear message.
- AC-D-006-05: Given the channel page, when a user opens it, then it
  explains what the tool does and how to install it.
- AC-D-006-06: Given the conda and PyPI releases, when versions are
  compared, then they match the same versioned source.
- AC-D-006-07: Given the published artifact, when it is scanned, then it
  contains no embedded credentials.

## 8. Migration Procedure

1. Select the channel and confirm publishing rights and access model.
2. Prepare the first conda release from the same versioned source state as
  the PyPI release; align metadata with the confirmed package name and
  `pal-found-` command prefix.
3. Build, install, and smoke-run in a clean conda environment; record the
  verification checklist.
4. Upload the first release and complete the channel page content.
5. Check version alignment with the PyPI release and record the result.
6. Update installation documentation across the programme to document both
  channels (pip and conda) with the confirmed name.
7. Announce the first stable conda release.
8. Rollback: if a release fails verification, do not announce it; keep the
  previous channel version available and fix forward from the versioned
  source.

## 9. Developer Story Scope

One story covers channel setup, first release publication, version
alignment, and channel documentation.

## 10. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-005 |
| Epic | EPIC-010 |
| BA design sub-task | BA-DES-006 |
| SA counterpart | SA-DES-005 |
| Analysis | BA-ANA-005, SA-ANA-005 (Closed, PO-approved) |
| Naming decisions | ND-010-02, ND-010-03 (QUESTION-073, QUESTION-074, Closed) |
