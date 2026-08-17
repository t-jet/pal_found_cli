# Cross-repository reference register

| Reference | Canonical location | Verified production commit | Rule |
| --- | --- | --- | --- |
| Design repository | `https://github.com/t-jet/pal_found_cli` | Audit baseline `1b20819d7993629faa9e85453f1c82189d665c4b` | Use this absolute URL from other repositories. |
| CLI tool repository | `https://github.com/t-jet/pal_found_cli_tool` | `0dd826b02c4489eb35aa45cf689efcad4b0c31c9` | Use this absolute URL for source, releases, and package metadata. |
| Skills repository | `https://github.com/t-jet/pal_found_cli_skills` | `b961b2186ad2c8c98f67ab98d708beff6c944281` | Use this absolute URL for clone and distribution instructions. |

Links within one repository stay relative. Links across repositories include a
stable tag or file path when they target versioned content. The `.gitmodules`
file and recorded gitlinks are the authoritative URL and commit map for this
checkout.

## Production deployment audit

Deployment target: public GitHub `main` branches for the three repositories.
The audit ran on 2026-08-17 from a credential-disabled recursive clone under
`.ept/tmp`. Git prompts, askpass, and the credential helper were disabled.

| Check | Result |
| --- | --- |
| Anonymous repository access | `git ls-remote` returned the three commits above; each canonical web URL returned HTTP 200. |
| Recursive clone | Root, tool, skills, and SDK submodules cloned without credentials or prompts. All four worktrees were clean. |
| Root gitlinks | Tool pinned to `0dd826b02c4489eb35aa45cf689efcad4b0c31c9`; skills pinned to `b961b2186ad2c8c98f67ab98d708beff6c944281`. |
| `.gitmodules` | Tool and skills use the canonical HTTPS URLs above; SDK uses `https://github.com/palantir/foundry-platform-python.git`. |
| Relative links | 128 operational links across the three READMEs, document index, split manifest, this register, and rename guide resolved inside their owning repository. |
| Cross-repository links | Every registered canonical URL resolved. Versioned tool and skills links in the document index resolve at the pinned commits. |
| Former-name sweep | No former `t-jet/foundry_*` URL or operational repository name remains in active READMEs, package metadata, CI, or `.gitmodules`. Historical design records and the rename map retain old names intentionally. |
| Redirect compatibility | Former `foundry_cli`, `foundry_cli_tool`, and `foundry_cli_skills` web and git URLs redirect to the canonical repositories and resolve to the same heads. |

This satisfies AC-004-05 and AC-D-004-05: cross-repository references resolve
to the correct public locations. It also satisfies SA-DES-003 REF-1 and DOC-1:
the reference sweep is clean and repository entry points use final URLs. The
audit commit follows the root baseline above and changes only this register and
the document index; it does not change a submodule pin.

## Verification and rollback

For a new deployment, repeat anonymous `ls-remote`, the credential-disabled
recursive clone, clean-worktree checks, and the operational link sweep before
publishing reference changes. Use `git submodule sync --recursive` followed by
`git submodule update --init --recursive` when validating an existing clone.

If a reference-only deployment fails, create a normal revert commit for the
reference-register and index change, then repeat the same checks. Do not reset
or force-push any public branch. If a root gitlink itself is wrong, revert the
gitlink change through review; do not move a destination repository branch only
to match stale documentation. Keep GitHub redirects active throughout rollback.
