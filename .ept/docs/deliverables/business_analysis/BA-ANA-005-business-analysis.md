# Business Analysis — BA-ANA-005

## Publish foundry_cli_tool to a Conda Channel

| Field | Value |
| --- | --- |
| **Document ID** | BA-ANA-005 |
| **Feature** | FEATURE-005 |
| **Status** | Resolved — pending Project Owner approval |
| **Date** | 2026-08-12 |
| **Author** | Business Analyst |
| **Requirement source** | Project Owner architecture-change request 2026-08-11 |

---

## 1. Business Case

Some users and environments are conda-based and do not use pip. Publishing
foundry_cli_tool to a conda channel lets those users run `conda install
foundry_cli_tool`. This complements the PyPI channel (FEATURE-004) and ensures the
tool is reachable by the widest possible set of Python environments.

## 2. Business Requirements

| ID | Requirement |
| --- | --- |
| BR-005-01 | The package must be published to a conda channel so it can be installed with conda. |
| BR-005-02 | Installing the package must not require manual configuration beyond the channel setup. |
| BR-005-03 | Versioned releases must be published; users must be able to update to a new version. |
| BR-005-04 | Users without access to the channel must receive a clear error when installation is not possible. |
| BR-005-05 | The channel must describe what the tool does and how to install and use it. |

## 3. Acceptance Criteria

- AC-005-01: Given a user with conda installed, when they run `conda install foundry_cli_tool`, then the tool installs successfully from the configured channel.
- AC-005-02: Given an installed release, when the user runs the tool's command, then it works as documented.
- AC-005-03: Given a published new version, when a user updates the package, then they receive the new version.
- AC-005-04: Given a user without channel access, when they try to install, then the attempt fails with a clear message.
- AC-005-05: Given the channel page, when a user opens it, then it explains what the tool does and how to install it.

## 4. Impact on End-to-End Business Processes

| Process | Impact |
| --- | --- |
| Installation | Conda users install the tool with one conda command instead of manual setup. |
| Upgrade | Users receive new releases through the conda update flow. |
| Release management | Releases follow the conda publication pipeline in addition to PyPI. |
| Environment management | Packages resolve against the conda environment's dependency set. |
| Support | Installation problems are reproducible against a known published version. |

## 5. Changes in Access Restrictions

- Publishing rights: restricted to maintainers with channel credentials.
- Consumers: no authentication required to install from a public channel.
- The published package must not embed credentials or expose secrets.

## 6. Assumptions and Risks

| Type | Item |
| --- | --- |
| Assumption | A suitable conda channel is available or can be created. |
| Assumption | Conda packaging of the tool's dependencies is feasible. |
| Risk | Conda and PyPI releases drift to different versions. |
| Risk | A broken conda release reaches users. |
| Mitigation | Release both channels from the same versioned source; verify installs before announcing. |

## 7. Request Rate Changes

Conda channel traffic is additional to PyPI traffic but small in scale. No consumer-side rate changes are required.

## 8. Data Size Changes

The conda package is small. Total published artifact size grows by one package per release; well within channel limits.

## 9. Traceability

| Artifact | Reference |
| --- | --- |
| Feature | FEATURE-005 (Open) |
| Epic | EPIC-010 — Public repositories and distribution of the Foundry CLI tool |
| BA sub-task | BA-ANA-005 |
| SA counterpart | SA-ANA-005 |
| Requirement source | Project Owner architecture-change request 2026-08-11 |
