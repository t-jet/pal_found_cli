# WORK-007 historical CLI tool candidate

Snapshot: 2026-10-14. Candidate: `.ept/tmp/feature012_tool_candidate`.

This record preserves the earlier `6d35ff444b4353601ce678f01d6168dd75d4c74d` candidate. The final parent release branch pins tool `b9c5f8a1a0595fc5fa0cbb27a7a92dba9c1bc67e`; see the [release pin verification](WORK-007-release-pin-plan.md). File hashes and the 1,207-test result below apply to this earlier candidate only.

The candidate was cloned from `pal_found_cli_tool` at `bfdee7388ce2a8b2d592f17f1ba1d6f10a0424aa`, which was both local `HEAD` and upstream `main` when copied. It contains only the ten accepted FEATURE-012 tool paths below: nine modified tracked files and one new test file. Every candidate file hash matched the live source at snapshot time. No live source file or parent gitlink was changed.

| Path | SHA-256 |
| --- | --- |
| `src/pal_found_cli/admin/scripts/pal_found_admin_cli.py` | `7b5b52084f9db6534885a9b6a294f01e63607fcb84f44530f8b0136b30ff16e5` |
| `src/pal_found_cli/common/pagination_helper.py` | `b831ea4c2d64b48e5ed5a9558da2a19f4933d27d4290922d266030db1796e5db` |
| `src/pal_found_cli/filesystem/scripts/pal_found_filesystem_cli.py` | `44f4c4affc4edd3d4a74d30f93f851c51acd83bb152c050e5d953d1e3d04ba41` |
| `src/pal_found_cli/functions/scripts/pal_found_functions_cli.py` | `9132a926528f1e9c290b5a5da75beaea61f8c4e0799be0673856d190248dddc6` |
| `src/pal_found_cli/ontologies/scripts/pal_found_ontologies_cli.py` | `e7e4eb42ef1b4c6347ea26aa88c29e6310dae18a8109e9c2fe8e7b435631c12d` |
| `tests/test_pagination_helper.py` | `c67c5a4373249a3571be87dc904301386c7c346cf7e2352998289857045d95f4` |
| `tests/test_pal_found_admin_cli.py` | `b5ee155fe75188283e55ea01f26924e2955868bfbafcc33563300ccd20480a44` |
| `tests/test_pal_found_filesystem_cli.py` | `f2941a4b288067face606db267e88cffda5508cc0545aaf58aa330578b46496d` |
| `tests/test_pal_found_functions_cli.py` | `4173a1ca8b54bc853440dd30ff9cf6a83eb3303161a9773d3f3900793bddd0aa` |
| `tests/test_pal_found_ontologies_cli.py` | `f47b1bf3fdbd7520b3c2d46f2dbb1385a920e274b0b2ae20003a4ac7e84178da` |

Manifest SHA-256: `0be30a480e0e5ddb4fb9328d81a30b63dd0ee57bc7102f93f67547babbd6843b`. To reproduce it, sort paths as shown, encode each row as `<path><tab><lowercase file SHA-256><LF>`, concatenate rows, and SHA-256 hash the UTF-8 bytes.

## Checks

- `git status --short`: exactly the ten paths above. No other changed path was excluded.
- `git diff --check`: passed.
- `PYTHONPATH=<candidate>/src python -m pytest -q`: **1,207 passed**, six runtime warnings, exit code 0, in 39.07 seconds. Import path check confirmed tests loaded `pal_found_cli` from the candidate. Warnings arose in Connectivity, Data Health, Models, Widgets, and Session Manager tests, outside the candidate edits.

The source changes cover Admin and Filesystem pagination and errors, Ontology input validation, pagination and response metadata, Functions attribution parsing, and the shared pagination helper. Tests for each changed component are included.

## Publication

After verifying the staged tree and ten staged paths, the candidate was committed locally as `6d35ff444b4353601ce678f01d6168dd75d4c74d` (`fix(feature-012): ship offline QA CLI corrections`). Its tree is `bfcfc9afdff6baa04f983b4974a581e21f7fc99c` and its parent is `bfdee7388ce2a8b2d592f17f1ba1d6f10a0424aa`. The candidate worktree is clean.

The initial HTTPS push could not find a noninteractive credential. Retrying with Git Credential Manager selected explicitly (`git -c credential.helper=manager push`) succeeded. GitHub now advertises `refs/heads/release/feature-012-offline-qa` at `6d35ff444b4353601ce678f01d6168dd75d4c74d`. A subsequent `git ls-remote` verified that SHA and showed `main` unchanged at `bfdee7388ce2a8b2d592f17f1ba1d6f10a0424aa`. The release commit was not pushed to `main` or the local clone's `origin`.

At this snapshot, the parent repository still pinned tool commit `86b060271bbff50b4fc8a4d62b09d489099ae6fb`, which excluded these fixes. Later parent pinning and recursive-clone results are recorded in the release pin verification.
