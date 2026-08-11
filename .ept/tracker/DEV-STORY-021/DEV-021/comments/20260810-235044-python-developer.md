Subject: Implementation plan — foundry-third-party-applications CLI (9 ops)
Created: 2026-08-10T23:50:44
Updated: 2026-08-10T23:50:44
---
## Implementation plan (DEV-021)

### Deliverables
1. `src/foundry_cli/third_party_applications/__init__.py` — package export (build_parser, console_main, main).
2. `src/foundry_cli/third_party_applications/scripts/__init__.py` — scripts package.
3. `src/foundry_cli/third_party_applications/scripts/foundry_third_party_applications_cli.py` — 9-op CLI per DESIGN-021.
4. `src/foundry_cli/third_party_applications/metadata-allow-list.md` — 4 PERMITTED / 5 BLOCKED (third_party_application.get, website.get, version.get, version.list permitted; website.deploy/undeploy, version.delete/upload/upload_snapshot blocked).
5. `.claude/skills/foundry-third-party-applications/SKILL.md` + launcher script (mirror connectivity skill pattern).
6. `pyproject.toml` — console entry point `foundry-third-party-applications`, package-data, ruff E402 per-file-ignore.
7. `src/foundry_cli/common/access_control_guard.py` — add `deploy`, `undeploy` verbs to _WRITE_VERBS (upload already present).

### Catalog (9 ops, snake_case keys, kebab-case CLI)
- third-party-application get — client_path ("ThirdPartyApplication",) — positional third_party_application_rid
- website deploy — ("Website",) — positional rid + required version (write)
- website get — ("Website",) — positional rid
- website undeploy — ("Website",) — positional rid (write)
- version delete — ("Website","Version") — positionals rid + version_version (write, DELETE)
- version get — ("Website","Version") — positionals rid + version_version
- version list — ("Website","Version") — positional rid; PAGINATED via PaginationHelper (--page-size/--page-token/--all/--max-pages)
- version upload — ("Website","Version") — positional rid + required version + file; bounded zip read 16 MiB AFTER ACL, BEFORE client (write)
- version upload-snapshot — ("Website","Version") — positional rid + required version + file + optional snapshot_identifier; same bounded read (write)

### Implementation decisions
- `_UPLOAD_OPS = {"version.upload", "version.upload_snapshot"}` — positional bytes body appended in _invoke (precedent streams publish_binary_record / connectivity upload_custom_jdbc_drivers).
- `PAGINATED_OPS = {("version","list")}` — with_raw_response + PaginationHelper (precedent connectivity).
- include_attribution=False; B3 via invocation_scope; retry via RetryHandler; metadata policy via packaged allow-list; AccessControlGuard(cfg, "THIRD_PARTY_APPLICATIONS", ...).
- Duplicate-safety caveat for version upload under at-least-once retries documented in skill doc.
- CLIInputError exit 1; error serialization per ADR-001.

### Acceptance criteria (derived from DESIGN-021)
- AC1: 9 OP_SPECS entries exactly, catalog keys snake_case.
- AC2: All 9 commands parse (--help exit 0); dispatch resolves client_path via root_client.third_party_applications.
- AC3: version list paginated (page-size/page-token/all/max-pages), result + metadata emitted.
- AC4: upload/upload-snapshot read zip bounded 16 MiB after ACL decision, before client; --file never forwarded.
- AC5: Write set 5 blocked in READONLY/METADATA_ONLY; 4 reads permitted per allow-list.
- AC6: include_attribution=False; no preview params; optional args omitted when absent.
- AC7: All external connections timeout-configurable (--timeout, default cfg.timeout_s).
- AC8: OWASP self-review documented; no secrets; no network on import.

### Related docs
- DESIGN-021: `.ept/docs/deliverables/architecture/DESIGN-021-third-party-applications-cli.md`
- Pattern refs: connectivity/media-sets CLIs; common library `src/foundry_cli/common/`.

### Verification plan
compileall, ruff, mypy, focused pytest for new namespace, full regression suite, ACL runtime probes (metadata-only), --help smoke.
