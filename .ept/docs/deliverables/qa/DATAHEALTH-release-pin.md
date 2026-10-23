# Data Health skills release pin

Snapshot: 2026-10-15. This parent candidate starts from published parent `ca32046a4b2a6dd2fc25f43423038a0b3e6fe9cd`.

| Submodule | Pinned commit |
| --- | --- |
| Skills | `04e860f30b0e136f52b0978daa084907431786f8` |
| CLI tool | `b9c5f8a1a0595fc5fa0cbb27a7a92dba9c1bc67e` |

The skills commit follows the published skills commit `3bbf551eef30290799d7b790d5244adb694ec66c`. It adds Data Health check configuration references, offline fixtures, and a QA ledger. The CLI tool pin stays at the published `v0.1.5` commit. The SDK submodule pin also stays unchanged.

This pin covers the Data Health skills addition. FEATURE-015 REST and development-guide work remains on a separate review branch. The active parent checkout contains unrelated work in progress outside this release.

The skills tag `data-health-offline-qa-20261015` resolves to the pinned commit. [Skills CI run 38724734019](https://github.com/t-jet/pal_found_cli_skills/actions/runs/38724734019) passed for that commit.

A fresh recursive clone of this local parent candidate resolved skills `04e860f30b0e136f52b0978daa084907431786f8`, tool `b9c5f8a1a0595fc5fa0cbb27a7a92dba9c1bc67e`, and SDK `2da67907be429c35f747eef565867ce81dd2cafc`. In that clone, the skills suite passed 33 tests. The FEATURE-012 audit reported 351 of 351 rows passing with no failed or pending semantic decisions. The Data Health fixture parsed 32 configuration payloads and rejected five documented empty cross-field choices. The clone was clean after the generated audit file was restored.

`git diff HEAD^ HEAD --check` passed for the parent candidate. Remote parent pin confirmation follows publication.
