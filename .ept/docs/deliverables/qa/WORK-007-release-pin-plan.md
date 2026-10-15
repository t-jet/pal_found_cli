# WORK-007 release pin verification

Snapshot: 2026-10-15. FEATURE-012 skills, CLI tool, and parent pins are published. The CLI package is available on PyPI and Anaconda.

## Published candidate

| Component | Revision or result |
| --- | --- |
| Parent pin commit | `634ef7ae21b53fa9b461f7da07a364c382327d38` |
| Skills gitlink | `3bbf551eef30290799d7b790d5244adb694ec66c` |
| CLI tool gitlink | `b9c5f8a1a0595fc5fa0cbb27a7a92dba9c1bc67e` |
| SDK evidence revision | `2da67907be429c35f747eef565867ce81dd2cafc` |

`git ls-tree HEAD pal_found_cli_skills pal_found_cli_tool` in the isolated parent worktree confirms both gitlinks. A fresh clone of the remote parent release branch with `--recurse-submodules` resolved the same pair. The skills commit has tag `feature-012-offline-qa-20261014-v2`; skills CI run `38636503091` succeeded. Tool tag `v0.1.5` resolves to its pinned commit; tool CI run `38636495025` passed all eight jobs.

Parent `main` was published at `2a95dfbc697e5b9bb999da8bb617d6352ac388e2`. A fresh recursive clone from that ref resolved the skills, tool, and SDK revisions in the table and passed the 351-operation audit again.

## Verification from fresh clone

| Check | Result |
| --- | --- |
| Source and semantic audit | 351/351 pass |
| Skills test suite | 33 passed |
| Complete copied distribution | 20 skill folders; 108 source and copy SHA-256 hashes match |
| Copied-bundle gate | 9 passed |
| Installed CLI tool wheel | 18 CLI help commands pass |
| PyPI `pal_found_cli==0.1.5` | Clean target install; 18 CLI help commands pass |

Earlier local QA also passed WORK-006's five focused offline novice cases. BUG-031 is fixed and closed. The [skills candidate evidence](WORK-007-skills-candidate-evidence.md), [historical 83-file manifest](WORK-007-skills-candidate-manifest.json), and [tool candidate evidence](WORK-007-tool-candidate-evidence.md) record prior isolated candidates. Their commit IDs and file hashes describe those earlier snapshots, not the final gitlink pair above.

## Package publication

Tool publish run `38637176438` succeeded. It built the release, published to Test PyPI, installed the staged package in a clean environment, published to PyPI, and built and uploaded the conda package. PyPI serves wheel `pal_found_cli-0.1.5-py3-none-any.whl` with SHA-256 `7bcbd479d9b3a4b8fac8d14bbf590a2485d34e9a1b81a113a3c512791aee08f7` and source archive `pal_found_cli-0.1.5.tar.gz` with SHA-256 `be5db56dd1fafdaa53bf39e497137b4c0967772db2d0d1720d37d344a9a0e969`. Anaconda serves `noarch/pal_found_cli-0.1.5-py_0.conda`.

The paired parent revision, copied skill bundle, installed CLI, and package artifacts have passed release checks. WORK-007 can be closed after the tracker records this evidence.
