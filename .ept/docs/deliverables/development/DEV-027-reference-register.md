# Cross-repository reference register

| Reference | Canonical location | Rule |
| --- | --- | --- |
| Design repository | `https://github.com/t-jet/pal_found_cli` | Use absolute URL from other repositories. |
| CLI tool repository | `https://github.com/t-jet/pal_found_cli_tool` | Use absolute URL for source, releases, and package metadata. |
| Skills repository | `https://github.com/t-jet/pal_found_cli_skills` | Use absolute URL for clone and distribution instructions. |

Links within one repository stay relative. Links across repositories include a
stable tag or file path when they target versioned content. The `.gitmodules`
file is the authoritative submodule URL map for this checkout.
