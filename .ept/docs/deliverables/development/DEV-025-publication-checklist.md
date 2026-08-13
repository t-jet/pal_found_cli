# Public repository publication checklist

Use this checklist only after the three repositories exist and the maintainer
has owner permissions. No publication is recorded by this file.

For each of `pal_found_cli`, `pal_found_cli_tool`, and `pal_found_cli_skills`:

- [ ] Secret scan is clean; no credentials or private customer data remain.
- [ ] Repository is public and its README is readable without login.
- [ ] Anonymous clone succeeds over HTTPS.
- [ ] Issues, pull requests, tags, releases, and release assets are readable.
- [ ] Maintainer write access and branch protection remain restricted.
- [ ] Making the repository private again blocks anonymous access.

Publish in dependency order: skills, tool, then design. Record the repository
URL, commit/tag, verification command, and result in the release record. If a
check fails, make the repository private again and do not announce it.
