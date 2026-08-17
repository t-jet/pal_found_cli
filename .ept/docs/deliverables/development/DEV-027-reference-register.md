# Cross-repository reference register

| Reference | Canonical location | Rule |
| --- | --- | --- |
| Design repository | `https://github.com/t-jet/pal_found_cli` | Use absolute URL from other repositories. |
| CLI tool repository | `https://github.com/t-jet/pal_found_cli_tool` | Use absolute URL for source, releases, and package metadata. Current verified commit: `370c971`. |
| Skills repository | `https://github.com/t-jet/pal_found_cli_skills` | Use absolute URL for clone and distribution instructions. Current verified commit: `34b6c40`. |

Links within one repository stay relative. Links across repositories include a
stable tag or file path when they target versioned content. The `.gitmodules`
file and recorded gitlinks are the authoritative URL and commit map for this
checkout.
