# TESTCASE-023 - Foundry Knowledge Skill QA test cases

## Scope

These cases cover DEV-STORY-023: QA test case design for the static `foundry/` general knowledge skill deliverable `.claude/skills/foundry/SKILL.md`. The skill is a documentation-only artifact (no executable scripts, no console entry points, no `pyproject.toml` packaging changes). Unlike the namespace CLI stories, the "unit under test" is markdown content; therefore every case verifies **content accuracy** of the authored skill against authoritative sources, not runtime behavior.

The case set covers: the 8 required content sections (platform concept primer, 20-namespace overview table, operation catalogue reference, authentication setup guide, access control configuration guide, TOON format explanation, troubleshooting reference, known limitations); the 20-namespace operation counts cross-verified against the implemented CLI `OP_SPECS` surfaces (351 implemented across 18 namespaces; 355 documented including 4 widgets design rows not present in the installed SDK); the auth guide (UserTokenAuth from `FOUNDRY_TOKEN`, `FOUNDRY_HOSTNAME` consumed by `AsyncClientFactory`, ADR-006 search order); the access control guide (ADR-007 8-step precedence, control variable naming patterns, Tier-3 metadata-only allow-list 162 permitted / 193 blocked, exit code 8); TOON vs JSON selection (ADR-004); exit-code taxonomy (ADR-001); retry policy (ADR-002); NDJSON logging (ADR-005); troubleshooting failure-mode table; known limitations accuracy (geo/core zero-op per SAD-001 AA-3, widgets 12-design vs 8-runtime drift per QUESTION-043, snapshot vs installed SDK versioning, binary size bounds, preview exclusion, attribution scope per FR-ATTR-4); authoritative reference resolution (SRS-001, SAD-001, ADR-001..007, ENV-REF-001, META-ALLOW-001); and markdown validity/frontmatter.

> **Acceptance criteria note:** The DEV-STORY-023 ticket body's Acceptance Criteria field still carries the grooming template placeholder; the authoritative acceptance criteria are the DEV-023 scope (already verified at gate), the DEV-023 acceptance criteria (`[x]` checked: 8 sections present, counts cross-verified, widgets drift recorded, authoritative references, lint-clean markdown, document index registration), and the DESIGN-023 content specification.
>
> **Testability note:** The knowledge skill is static markdown. TESTEXEC-023 executes these cases by reading the skill file and comparing its content against the authoritative sources — no live Foundry access and no CLI invocation is required for the mandatory evidence.

## Source baseline

- [DESIGN-023](../architecture/DESIGN-023-knowledge-skill.md) — the 8-section content specification (platform primer, namespace overview with operation counts, operation catalogue, UserTokenAuth + `.env` auth guide, access control guide, TOON explanation, troubleshooting reference, known limitations).
- Implementation under test: `.claude/skills/foundry/SKILL.md` (218 lines), committed at `a4d48ab` (HEAD, "docs(foundry): add foundry/ knowledge skill - 8 sections (DEV-023, UNITTEST-023)").
- [SAD-001](../architecture/SAD-001-foundry-cli.md) — 355-operation catalog across 20 namespaces (L45, L78); assumption AA-3 (geo/core 0 public operations, L691).
- [SRS-001](../business_analysis/SRS-001-foundry-cli.md) — FR-ACL three-tier access model (Section 4, L351-358), FR-ATTR attribution scope (L304-311).
- [ADR-001](../architecture/adr/ADR-001-exit-code-taxonomy.md) — exit codes 0-9.
- [ADR-002](../architecture/adr/ADR-002-call-timeout-defaults.md) — timeout 30 s default, 3600 s max, streams 120 s; retry policy.
- [ADR-003](../architecture/adr/ADR-003-streams-batch-strategy.md) — streams batch strategy (referenced in the concept table).
- [ADR-004](../architecture/adr/ADR-004-format-auto-algorithm.md) — TOON vs JSON auto-selection rule.
- [ADR-005](../architecture/adr/ADR-005-log-format.md) — NDJSON logging to stderr, required fields, log level.
- [ADR-006](../architecture/adr/ADR-006-env-file-search-path.md) — `.env` search order.
- [ADR-007](../architecture/adr/ADR-007-operation-level-readonly.md) — operation-level READONLY override-only rule and 8-step precedence model reference.
- [Canonical Environment Variable Reference](../architecture/canonical-env-var-reference.md) (ENV-REF-001) — global/namespace/operation variable naming patterns, 355 operation variables.
- [Metadata Allow-list](../architecture/metadata-allow-list.md) (META-ALLOW-001) — 355 total, 162 Tier-3 permitted, 193 blocked (default-deny).
- QUESTION-043 (Closed, tech-lead decision 2026-08-11) — installed SDK 1.102.0 widgets surface = 8 operations; `DevModeSettingsV2` out of scope.
- The 18 implemented namespace CLI sources under `src/foundry_cli/*/scripts/*_cli.py` and their test-asserted `OP_SPECS` counts (verified via AST probe for this deliverable).
- Sibling namespace skill files under `.claude/skills/` — the cross-check targets for the operation catalogue section.

## Preconditions and shared fixtures

- The repository is checked out at HEAD `a4d48ab` (the approved DEV-023 commit); `.claude/skills/foundry/SKILL.md` exists, is 218 lines, and contains 8 `##`-level sections.
- The authoritative source documents exist on disk: SRS-001, SAD-001, ADR-001..007, ENV-REF-001 (`canonical-env-var-reference.md`), META-ALLOW-001 (`metadata-allow-list.md`), DESIGN-023, and the 18 namespace CLI sources.
- Expected-value anchors for operation counts are the AST-verified `OP_SPECS` surfaces of the 18 namespace CLIs (probe `misc_dos/probe_testcase_023_opcounts.py`), cross-checked against each namespace's test-asserted count (e.g. `tests/test_foundry_ontologies_cli.py::test_operation_catalog_has_67_unique_operations`).
- No live Foundry access, no credentials, and no CLI invocation are required for any mandatory case.
- TESTEXEC records, for every case: the checked skill file lines, the authoritative source reference, the expected value, the actual value found in the skill, and a PASS/FAIL/BLOCKED verdict with evidence (line numbers, verbatim quotes where relevant).

## Test data

| Name | Expected value (authoritative source) |
| --- | --- |
| Skill file | `.claude/skills/foundry/SKILL.md`, 218 lines, committed `a4d48ab` |
| Frontmatter | `name: foundry`; description mentions the 8 content areas (platform concepts, 20-namespace catalogue, UserTokenAuth + `.env`, 8-step access control, TOON vs JSON, exit-code troubleshooting, known limitations) |
| Section count | exactly 8 top-level `##` sections (1 Platform concepts, 2 Namespace overview, 3 Operation catalogue, 4 Authentication setup, 5 Access control configuration, 6 Output format: TOON vs JSON, 7 Troubleshooting, 8 Known limitations and open items) |
| Concept table rows | 22 rows covering projects/folders, datasets, branches/transactions, schemas, files, views, ontologies, object types/sets, links, functions, AIP agents/sessions, media sets, streams, models, platform administration, audit logs, checkpoints, data health, connectivity, SQL queries, language models, third-party applications, widgets |
| Namespace counts (implemented `OP_SPECS`) | admin 66, aip_agents 15, audit 2, checkpoints 3, connectivity 20, data_health 6, datasets 33, filesystem 31, functions 7, language_models 2, media_sets 19, models 23, ontologies 67, orchestration 20, sql_queries 5, streams 15, third_party_applications 9, widgets 8, geo 0, core 0 |
| Implemented total | 351 (18 namespaces, widgets at runtime 8-op surface) |
| Documented total | 355 (ENV-REF-001 / META-ALLOW-001 / SAD-001; includes 4 widgets design rows `dev-mode-settings disable/get/pause/set-widget-set`) |
| Auth guide | `FOUNDRY_TOKEN` → `UserTokenAuth` (token only); `FOUNDRY_HOSTNAME` → `AsyncClientFactory`; ADR-006 order: (1) explicit `FOUNDRY_AGENTIC_CLI_ENV_FILE` override with exit 9 on missing file, (2) git-root `.env` walk-up, (3) env-vars-only; home dir never searched; `load_dotenv(override=False)` |
| ADR-006 failure exit | exit code 9 (ConfigurationError) when the explicit env-file path is missing |
| 8-step precedence (ADR-007) | 1 operation `_ENABLED=false` block; 2 namespace `_ENABLED=false` block; 3 operation `_READONLY=false` overrides parent read-only → permit write; 4 namespace `_READONLY=true` blocks writes; 5 global `FOUNDRY_AGENTIC_CLI_READONLY=true` blocks writes; 6 namespace `_METADATA_ONLY=true` applies metadata-only; 7 global `FOUNDRY_AGENTIC_CLI_METADATA_ONLY=true` applies metadata-only; 8 permit (default) |
| Naming patterns (ENV-REF-001) | global `FOUNDRY_AGENTIC_CLI_{KEY}`; namespace `FOUNDRY_AGENTIC_CLI_{NS}_{CONTROL}`; operation `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_{CONTROL}`; suffixes `_ENABLED`, `_READONLY`, `_METADATA_ONLY` |
| Metadata allow-list (META-ALLOW-001) | 355 total; 162 Tier-3 permitted; 193 blocked; default-deny; per-namespace `metadata-allow-list.md` packaged policy; blocked → exit 8 before network |
| TOON rule (ADR-004) | TOON only when top-level result is a list AND every item is a dict with identical field set; JSON otherwise (errors, single objects, empty lists, mixed/heterogeneous arrays, binary envelopes, pagination metadata); separator `# ---metadata-start---` precedes stderr metadata |
| Exit codes (ADR-001) | 0 success, 1 user input, 2 auth, 3 permission denied, 4 not found, 5 timeout, 6 server error, 7 rate limit, 8 access control, 9 configuration; all failures emit a JSON error object on stdout |
| Retry (ADR-002) | exponential backoff with jitter; max 4 total attempts (1 + 3 retries); default per-call timeout 30 s, range 1-3600 (`FOUNDRY_AGENTIC_CLI_TIMEOUT_S`); streams 120 s (`FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S`) |
| Logging (ADR-005) | NDJSON on stderr; required fields `ts`, `level`, `logger`, `msg`; context fields `op`, `call_id`, `attempt`, `delay_ms`, `access_decision`, `http_status` when relevant; `FOUNDRY_AGENTIC_CLI_LOG_LEVEL` default `WARNING` |
| Binary bounds | download 1.5 MiB (`FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES`); upload 16 MiB |
| Attribution (FR-ATTR-4) | `FOUNDRY_ENABLE_ATTRIBUTION`/`_ATTRIBUTION_RIDS` apply only to namespaces in FR-ATTR-4 scope (media_sets currently); other namespaces set `include_attribution=False` |
| Known limitations | geo/core zero-op (SAD-001 AA-3); widgets 12-design vs 8-runtime (QUESTION-043), `DevModeSettingsV2` out of scope; vendored SDK snapshot `0.0.0` vs installed `foundry-platform-sdk 1.102.0`; operation counts re-verified each SDK minor release |
| Reference documents | SRS-001, SAD-001, ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-007, ENV-REF-001, META-ALLOW-001, QUESTION-043 — all must be resolvable on disk and cited in the skill |

## Test cases

### KNW-TC-001 - Skill file exists, frontmatter valid, 8 sections present

- Type: positive, structural.
- Given the implementation at HEAD `a4d48ab`, when the skill file is inspected, then `.claude/skills/foundry/SKILL.md` exists, opens with valid frontmatter (`name: foundry`, a description naming the content areas), and contains exactly the 8 required `##` sections per DESIGN-023.
- File/function under test: `.claude/skills/foundry/SKILL.md` — frontmatter (L1-4), `# Foundry Platform Knowledge` (L6), sections at L10, L40, L69, L111, L135, L162, L171, L211.
- Prerequisites/fixtures: repo at `a4d48ab`; `Get-Content` on the file.
- Steps: assert file exists and is 218 lines; parse frontmatter and check `name == foundry`; list all `##` headings; compare the 8 headings against DESIGN-023 section 1-8.
- Expected: file exists; frontmatter `name` is `foundry` and description covers the 8 areas; exactly 8 top-level sections: `1. Foundry platform concepts`, `2. Namespace overview`, `3. Operation catalogue`, `4. Authentication setup`, `5. Access control configuration`, `6. Output format: TOON vs JSON`, `7. Troubleshooting`, `8. Known limitations and open items`.
- Cleanup: none (read-only).
- Evidence mapping: DESIGN-023 section-by-section spec; DEV-023 AC "Content covers all 8 sections per the story body and DESIGN-023".

### KNW-TC-002 - Platform concept primer covers all 22 concept rows with correct namespace skill mapping

- Type: positive, structural, consistency.
- Given Section 1 (L10-38), when the concept table is compared against the implemented namespace skills, then every concept row names a real `foundry-*` skill and the mapping is consistent with the namespace overview (Section 2).
- File/function under test: Section 1 concept table (L12-37).
- Prerequisites/fixtures: the 18 namespace skill names on disk.
- Steps: for each concept row, verify the namespace skill column references one of the 18 existing skills (`foundry-filesystem`, `foundry-datasets`, `foundry-ontologies`, `foundry-functions`, `foundry-aip-agents`, `foundry-media-sets`, `foundry-streams`, `foundry-models`, `foundry-admin`, `foundry-audit`, `foundry-checkpoints`, `foundry-data-health`, `foundry-connectivity`, `foundry-sql-queries`, `foundry-language-models`, `foundry-third-party-applications`, `foundry-widgets`); verify the streams row cites ADR-003; verify no row references a non-existent skill.
- Expected: every row maps to a real skill folder; streams row mentions ADR-003 batch strategy; no orphan or misspelled skill names.
- Cleanup: none.
- Evidence mapping: DESIGN-023 Section 1 spec (each concept lists the namespace skill(s) that operate on it); DEV-023 AC platform primer.

### KNW-TC-003 - Namespace overview: exact 20-row table with per-namespace counts

- Type: positive, structural, accuracy.
- Given Section 2 (L40-67), when the 20-row namespace table is compared to the AST-verified `OP_SPECS` surfaces of the 18 namespace CLIs plus geo/core = 0, then every count matches exactly.
- File/function under test: namespace overview table (L43-63).
- Prerequisites/fixtures: `misc_dos/probe_testcase_023_opcounts.py` (AST probe) output; namespace CLI sources under `src/foundry_cli/*/scripts/`.
- Steps: read the table; for each of the 18 implemented namespaces compare the Operations column to the AST probe count and the namespace test-asserted count (e.g. ontologies 67 via `test_operation_catalog_has_67_unique_operations`); assert geo and core rows exist with value 0; assert exactly 20 rows total.
- Expected: admin 66, aip_agents 15, audit 2, checkpoints 3, connectivity 20, data_health 6, datasets 33, filesystem 31, functions 7, language_models 2, media_sets 19, models 23, ontologies 67, orchestration 20, sql_queries 5, streams 15, third_party_applications 9, widgets 8, geo 0, core 0. (See Test data table.)
- Cleanup: none.
- Evidence mapping: DESIGN-023 namespace overview table; UNITTEST-023 AC "Verify all 20 namespace entries and operation counts"; SAD-001 AA-3.

### KNW-TC-004 - Implemented total 351 and documented total 355 explained

- Type: positive, accuracy, explanatory.
- Given the skill's total-statement paragraph (L64-66), when the arithmetic is verified, then the skill states an implemented total of 351 (sum of the 18 implemented namespace counts) and a documented total of 355, and explains the difference as the 4 widgets design rows absent from the installed SDK.
- File/function under test: totals paragraph (L64-66).
- Prerequisites/fixtures: AST probe output; ENV-REF-001 and META-ALLOW-001 headers (355 operations).
- Steps: sum the 18 implemented counts (66+15+2+3+20+6+33+31+7+2+19+23+67+20+5+15+9+8 = 351); confirm the skill states 351 and 355; confirm the 4-row explanation names `dev-mode-settings disable/get/pause/set-widget-set`.
- Expected: skill states 351 implemented and 355 documented; difference exactly 4 widgets design rows; the named rows match DESIGN-022's stale-12 catalog minus the installed 8-op surface (QUESTION-043).
- Cleanup: none.
- Evidence mapping: DEV-023 AC "Operation counts cross-verified against the canonical env-var reference and test-asserted OP_SPECS counts (355 total)"; DESIGN-023 Section 2.

### KNW-TC-005 - widgets row reflects the runtime 8-op surface, not the stale 12

- Type: accuracy, consistency.
- Given the widgets row (L60), when compared to QUESTION-043 and the installed SDK surface, then the table shows widgets = 8 (not the DESIGN-022 baseline 12) and the skill flags the drift in Section 8.
- File/function under test: Section 2 widgets row (L60); Section 8 widgets bullet (L213).
- Prerequisites/fixtures: `tests/test_foundry_widgets_cli.py` (8-op assertions); `src/foundry_cli/widgets/scripts/foundry_widgets_cli.py` `OP_SPECS` (8 entries).
- Steps: assert the table shows 8 for widgets; assert the 8-op surface (dev_mode_settings enable/set_widget_set_by_id, release delete/get/list, repository get/publish, widget_set get) matches the implemented CLI; assert Section 8 documents the 12-design vs 8-runtime drift and `DevModeSettingsV2` out of scope.
- Expected: widgets = 8 in the table; Section 8 names the drift, DESIGN-022's 12-op baseline, installed `foundry-platform-sdk` 1.102.0, and the QUESTION-043 reference.
- Cleanup: none.
- Evidence mapping: QUESTION-043 decision; DEV-023 AC "widgets runtime drift (12 design vs 8 installed per QUESTION-043) recorded".

### KNW-TC-006 - geo and core rows documented as zero-op

- Type: accuracy, consistency.
- Given the geo and core rows (L62-63) and the Section 8 bullet (L212), when compared to SAD-001 AA-3, then both namespaces show 0 operations, no CLI skill column, and the skill explains they expose only error/model types.
- File/function under test: Section 2 rows (L62-63); Section 3 `geo / core (0)` line (L109); Section 8 bullet (L212).
- Prerequisites/fixtures: SAD-001 L691 (AA-3).
- Steps: assert `geo` and `core` rows exist with Operations = 0 and `—` skill; assert Section 3 lists them as 0; assert Section 8 states no skill folders exist for them.
- Expected: consistent 0-op treatment across Sections 2, 3, and 8; AA-3 cited.
- Cleanup: none.
- Evidence mapping: SAD-001 AA-3; DESIGN-023 Section 2 and 8.

### KNW-TC-007 - Operation catalogue covers all 18 namespace blocks

- Type: positive, structural, completeness.
- Given Section 3 (L69-109), when the catalogue is checked, then all 18 implemented namespaces appear as `**namespace (N)**` blocks with their operation lists.
- File/function under test: Section 3 blocks (L73-109).
- Prerequisites/fixtures: the 18 namespace CLI sources.
- Steps: enumerate the `**...**` heading blocks; assert all 18 implemented namespaces are present (admin, aip_agents, audit, checkpoints, connectivity, data_health, datasets, filesystem, functions, language_models, media_sets, models, ontologies, orchestration, sql_queries, streams, third_party_applications, widgets); assert each block's `(N)` equals the AST-verified count; assert geo/core appear only as the final zero-op block.
- Expected: exactly 18 named blocks plus one `geo / core (0)` block; per-block counts match the Test data table; no namespace missing, duplicated, or mislabeled.
- Cleanup: none.
- Evidence mapping: DESIGN-023 Section 3 (resource grouped tables with kebab-case command names).

### KNW-TC-008 - admin block operation list matches the implemented 66-op surface

- Type: positive, accuracy, spot-check.
- Given the admin block (L73), when each listed operation is checked against `src/foundry_cli/admin/scripts/foundry_admin_cli.py` `OP_SPECS`, then the resource groups and operation names match the implemented 66-op catalog.
- File/function under test: Section 3 admin block (L73).
- Prerequisites/fixtures: admin CLI `OP_SPECS`; `tests/test_foundry_admin_cli.py` count assertions.
- Steps: parse the block's `resource` group names (authentication_provider, cbac_banner, cbac_marking_restrictions, enrollment, enrollment_role_assignment, group, group_member, group_membership, group_membership_expiration_policy, group_provider_info, host, marking, marking_category, marking_member, marking_role_assignment, organization, organization_guest_member, organization_role_assignment, role, user, user_provider_info); for each group verify every listed operation exists in the CLI `OP_SPECS`; verify no listed operation is absent and no implemented operation is omitted.
- Expected: every admin operation listed in the skill matches an implemented `OP_SPECS` entry; the (66) count is consistent.
- Cleanup: none.
- Evidence mapping: DESIGN-023 Section 3; admin namespace skill `foundry-admin`; DEV-023 AC cross-verified counts.

### KNW-TC-009 - ontologies block operation list matches the implemented 67-op surface

- Type: positive, accuracy, spot-check.
- Given the ontologies block (L97), when each operation is checked against `src/foundry_cli/ontologies/scripts/foundry_ontologies_cli.py` `OP_SPECS`, then the 67-op surface is fully represented (this is the largest catalogue and the one corrected from the stale 55-op SAD-001 figure).
- File/function under test: Section 3 ontologies block (L97).
- Prerequisites/fixtures: ontologies CLI `OP_SPECS`; `tests/test_foundry_ontologies_cli.py::test_operation_catalog_has_67_unique_operations`.
- Steps: parse the block's resource groups (action, action_type, action_type_full_metadata, attachment, attachment_property, cipher_text_property, geotemporal_series_property, linked_object, media_reference_property, object_type, ontology, ontology_interface, ontology_object, ontology_object_set, ontology_transaction, ontology_value_type, query, query_type, time_series_property_v2, time_series_value_bank_property); verify group/operation names against the CLI `OP_SPECS`; verify count 67.
- Expected: all 67 operations represented; group names match the CLI resource clients; no missing or extra operations.
- Cleanup: none.
- Evidence mapping: DESIGN-023 Section 3; document index "SAD-001 DEV-STORY-007 ontology scope corrected from 55 to 67 operations" (2026-08-11).

### KNW-TC-010 - datasets block operation list matches the implemented 33-op surface

- Type: positive, accuracy, spot-check.
- Given the datasets block (L77), when each operation is checked against `src/foundry_cli/datasets/scripts/foundry_datasets_cli.py` (the dispatch-style CLI, no `OP_SPECS`), then the 33-op surface is fully represented across the 5 resource clients (Dataset 11, Branch 5, File 5, Transaction 6, View 6).
- File/function under test: Section 3 datasets block (L77).
- Prerequisites/fixtures: datasets CLI docstring (L2-3: "33 operations across 5 resource clients"), dispatch branches in `_invoke`, and `tests/test_foundry_datasets_cli.py` (33-op coverage).
- Steps: parse the block's resource groups; for each group verify every listed operation has a dispatch branch in `_invoke`; verify counts per group (dataset 11, branch 5, file 5, transaction 6, view 6); verify the skill's (33) total.
- Expected: dataset 11 (create, get, get_health_check_reports, get_health_checks, get_schedules, get_schema, get_schema_batch, jobs, put_schema, read_table, transactions), branch 5, file 5, transaction 6, view 6; total 33.
- Cleanup: none.
- Evidence mapping: DESIGN-023 Section 3; datasets CLI docstring; TESTCASE-001 datasets precedent.

### KNW-TC-011 - Auth guide: FOUNDRY_TOKEN builds UserTokenAuth

- Type: positive, accuracy.
- Given Section 4 (L111-134), when the token row is verified, then the skill states `FOUNDRY_TOKEN` is required and that the SDK builds `UserTokenAuth` from this token alone.
- File/function under test: Section 4 token row (L117).
- Prerequisites/fixtures: ENV-REF-001 global variable table (`FOUNDRY_TOKEN` — SDK-native, no prefix); `_foundry_cli_common.py` auth construction.
- Steps: assert the skill marks `FOUNDRY_TOKEN` as required; assert it names `UserTokenAuth` and says "from this token alone"; cross-check ENV-REF-001 for the same required flag and no-prefix behavior.
- Expected: skill states `FOUNDRY_TOKEN` required → `UserTokenAuth`; no other token source mentioned for auth.
- Cleanup: none.
- Evidence mapping: DEV-023 AC "auth guide correctness (UserTokenAuth from FOUNDRY_TOKEN)"; UNITTEST-023 AC same.

### KNW-TC-012 - Auth guide: FOUNDRY_HOSTNAME consumed by AsyncClientFactory

- Type: positive, accuracy.
- Given Section 4 (L111-134), when the hostname row is verified, then the skill states `FOUNDRY_HOSTNAME` is required and consumed by `AsyncClientFactory` at client construction, with a valid example hostname format.
- File/function under test: Section 4 hostname row (L118).
- Prerequisites/fixtures: ENV-REF-001 global variable table (`FOUNDRY_HOSTNAME` — SDK-native).
- Steps: assert the skill marks `FOUNDRY_HOSTNAME` as required; assert it names `AsyncClientFactory`; verify the example `https://foundry.example.com` is a syntactically valid hostname URL.
- Expected: required + `AsyncClientFactory` + valid example; consistent with ENV-REF-001.
- Cleanup: none.
- Evidence mapping: DEV-023 AC "FOUNDRY_HOSTNAME via AsyncClientFactory".

### KNW-TC-013 - Auth guide: ADR-006 search order, no home-dir, override=False

- Type: positive, accuracy, boundary.
- Given the loader steps (L120-130), when compared to ADR-006, then the skill states the exact 3-step order (explicit env-file override with exit 9 on missing file; git-root `.env` walk-up with CWD fallback; env-vars-only with no error), never searches the home directory, and uses `load_dotenv(override=False)`.
- File/function under test: Section 4 loader steps (L120-129).
- Prerequisites/fixtures: ADR-006 decision section (Orders 1-3, no-home-dir, override=False).
- Steps: assert all three search orders appear in the documented order; assert the exit code 9 statement for a missing explicit env-file; assert the home-directory exclusion is explicit; assert `override=False` and "shell environment takes precedence".
- Expected: skill's order matches ADR-006 Order 1 → 2 → 3 exactly; exit 9 on missing explicit file; no home-dir search; override=False semantics.
- Cleanup: none.
- Evidence mapping: ADR-006; DEV-023 AC "`.env` per ADR-006"; ENV-REF-001 `FOUNDRY_AGENTIC_CLI_ENV_FILE` row.

### KNW-TC-014 - Access control: exact 8-step precedence model matches ADR-007

- Type: positive, accuracy, negative.
- Given the 8-step table (L139-149), when compared to ADR-007's model, then the skill states the exact 8 steps with the correct per-step outcomes (ENABLED blocks, READONLY write-blocks, operation-level `_READONLY=false` override, METADATA_ONLY application, default permit).
- File/function under test: Section 5 8-step table (L139-149).
- Prerequisites/fixtures: ADR-007 (operation-level READONLY override-only; SRS Section 4.2 8-step model reference).
- Steps: assert 8 rows exist; verify row semantics: (1) op `_ENABLED` false → block; (2) ns `_ENABLED` false → block; (3) op `_READONLY=false` overrides parent read-only → permit write; (4) ns `_READONLY` true → block writes; (5) global READONLY true → block writes; (6) ns `_METADATA_ONLY` true → metadata-only applies; (7) global METADATA_ONLY true → metadata-only applies; (8) permit default; assert the prose (L151) states operation-level `_READONLY=true` is not supported and `_ENABLED=false` blocks a single write.
- Expected: 8 steps present, ordered, and semantically identical to ADR-007/SRS 4.2; the READONLY override-only rule stated.
- Cleanup: none.
- Evidence mapping: ADR-007; UNITTEST-023 AC "8-step precedence per ADR-007".

### KNW-TC-015 - Access control: control-variable naming patterns match ENV-REF-001

- Type: positive, accuracy.
- Given the naming-pattern table (L151-156) and suffix list (L158), when compared to ENV-REF-001, then the skill states global `FOUNDRY_AGENTIC_CLI_{KEY}`, namespace `FOUNDRY_AGENTIC_CLI_{NS}_{CONTROL}`, operation `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_{CONTROL}`, and the `_ENABLED`/`_READONLY`/`_METADATA_ONLY` suffixes, with the example `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_GET_ENABLED` matching ENV-REF-001's admin-style row pattern.
- File/function under test: Section 5 naming patterns (L151-158).
- Prerequisites/fixtures: ENV-REF-001 "Naming conventions" and "Control suffixes" tables.
- Steps: assert the three scope patterns match ENV-REF-001 verbatim in structure; assert the example operation variable follows the pattern `{NS}_{CLASS}_{OP}` for datasets; assert the suffix semantics (ENABLED true/false, READONLY override-only, METADATA_ONLY true/false) match ENV-REF-001.
- Expected: patterns and suffixes identical to ENV-REF-001; example variable well-formed.
- Cleanup: none.
- Evidence mapping: ENV-REF-001 naming conventions; UNITTEST-023 AC "control variable naming patterns".

### KNW-TC-016 - Metadata-only policy: 162/193, exit 8, per-namespace allow-list

- Type: positive, accuracy, negative.
- Given the metadata-only paragraph (L160), when compared to META-ALLOW-001, then the skill states the default-deny Tier-3 policy with exactly 162 permitted and 193 blocked of 355, names the packaged `metadata-allow-list.md` per namespace, and states blocked operations exit 8 (`AccessControlError`) before any network call.
- File/function under test: Section 5 metadata-only paragraph (L160); Section 7 failure-mode rows (L199-200).
- Prerequisites/fixtures: META-ALLOW-001 header (Total 355, Tier-3 permitted 162, Tier-3 blocked 193, default-deny); ADR-001 exit code 8.
- Steps: assert 162/193/355 figures; assert default-deny wording; assert per-namespace `metadata-allow-list.md` reference; assert exit 8 stated for blocked operations, before network.
- Expected: all figures exact; policy described as default-deny; exit 8 and pre-network timing stated.
- Cleanup: none.
- Evidence mapping: META-ALLOW-001; ADR-001; DEV-023 AC Tier-3 policy accuracy.

### KNW-TC-017 - TOON vs JSON rule matches ADR-004

- Type: positive, accuracy, negative.
- Given Section 6 (L162-169), when compared to ADR-004, then the skill states `--format {json,toon,auto}` and `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT` (default `auto`), and the auto rule: TOON only when the top-level result is a list AND every item is a dict with an identical field set; JSON for everything else (errors, single objects, empty lists, mixed-type arrays, heterogeneous-field arrays, binary download envelopes, pagination metadata).
- File/function under test: Section 6 (L162-169).
- Prerequisites/fixtures: ADR-004 decision and algorithm (L14-22, L37-54, L65-71).
- Steps: assert the format values and default; assert the two TOON conditions; assert the JSON fallback list includes errors, single objects, empty lists, mixed arrays, heterogeneous arrays, binary envelopes, and pagination metadata; assert data-on-stdout/metadata-on-stderr and the `# ---metadata-start---` separator line.
- Expected: rule matches ADR-004 exactly; separator line `# ---metadata-start---` present; `toon-python` named for rendering.
- Cleanup: none.
- Evidence mapping: ADR-004; UNITTEST-023 AC "TOON explanation matches ADR-004 rule".

### KNW-TC-018 - Exit-code taxonomy table matches ADR-001

- Type: positive, accuracy.
- Given the exit-code table (L173-184), when compared to ADR-001, then the skill lists codes 0-9 with meanings matching the ADR (0 success, 1 user input, 2 auth, 3 permission denied, 4 not found, 5 timeout, 6 server error, 7 rate limit, 8 access control, 9 configuration) and notes all failures emit a JSON error object on stdout.
- File/function under test: Section 7 exit-code table (L173-184) and the following note (L186).
- Prerequisites/fixtures: ADR-001 decision table (codes 0-9 with conditions).
- Steps: assert all 10 rows in order with the correct meanings; spot-check 2 (auth), 5 (timeout), 7 (rate limit), 8 (access control), 9 (configuration); assert the "All failures also emit a JSON error object on stdout" statement (FR-ERR-2).
- Expected: table matches ADR-001 verbatim in codes and meanings; JSON error statement present.
- Cleanup: none.
- Evidence mapping: ADR-001; DEV-023 AC "exit codes ADR-001".

### KNW-TC-019 - Retry and timeout policy matches ADR-002

- Type: positive, accuracy, boundary.
- Given the retries paragraph (L190-192), when compared to ADR-002, then the skill states exponential backoff with jitter, max 4 total attempts (1 + 3 retries), per-call timeout default 30 s with range 1-3600 (`FOUNDRY_AGENTIC_CLI_TIMEOUT_S`), and the streams timeout default 120 s (`FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S`).
- File/function under test: Section 7 retries paragraph (L190-192).
- Prerequisites/fixtures: ADR-002 (default 30, max 3600, streams 120).
- Steps: assert backoff-with-jitter and 4-total-attempt wording; assert 30 s default and 1-3600 range; assert streams 120 s with the dedicated env var.
- Expected: all numbers and env-var names match ADR-002/ENV-REF-001.
- Cleanup: none.
- Evidence mapping: ADR-002; ENV-REF-001 `FOUNDRY_AGENTIC_CLI_TIMEOUT_S` / `FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S`.

### KNW-TC-020 - NDJSON logging description matches ADR-005

- Type: positive, accuracy.
- Given the logs paragraph (L194-197), when compared to ADR-005, then the skill states NDJSON structured logs go to stderr with required fields `ts`, `level`, `logger`, `msg`, optional context fields (`op`, `call_id`, `attempt`, `delay_ms`, `access_decision`, `http_status`), and log-level control via `FOUNDRY_AGENTIC_CLI_LOG_LEVEL` (default `WARNING`).
- File/function under test: Section 7 logs paragraph (L194-197).
- Prerequisites/fixtures: ADR-005 (L23-60).
- Steps: assert NDJSON-on-stderr; assert the required field names; assert the context fields; assert the log-level env var and default.
- Expected: field names and default level match ADR-005; stderr target stated.
- Cleanup: none.
- Evidence mapping: ADR-005; ENV-REF-001 `FOUNDRY_AGENTIC_CLI_LOG_LEVEL`.

### KNW-TC-021 - Troubleshooting failure-mode table is accurate and actionable

- Type: positive, accuracy, negative.
- Given the failure-mode table (L199-209), when each row is verified, then the symptom/cause/fix mapping is consistent with the exit-code taxonomy, ACL model, binary bounds, and validation rules.
- File/function under test: Section 7 failure-mode table (L199-209).
- Prerequisites/fixtures: ADR-001, ADR-002, ADR-006, META-ALLOW-001, binary bounds (1.5 MiB download / 16 MiB upload), JSON `-json` flag validation (exit 1).
- Steps: verify each row: exit 9 at startup (missing token/hostname or bad env-file path) → set vars / fix path; exit 2 on a call (token rejected) → replace token; exit 8 read-only write block → set `_READONLY=false` or remove global; exit 8 metadata-only block → disable metadata-only or use permitted op; download >1.5 MiB → stream outside CLI; upload >16 MiB → split/transfer outside CLI; exit 7 under load (429) → back off; exit 1 on `-json` flag (invalid JSON) → validate locally.
- Expected: every row's exit code and fix is consistent with the governing ADR/allow-list; no row contradicts another section of the skill.
- Cleanup: none.
- Evidence mapping: ADR-001/002/006; META-ALLOW-001; binary bounds contract; `-json` validation behavior.

### KNW-TC-022 - Known limitations: all six bullets accurate

- Type: positive, accuracy, negative.
- Given Section 8 (L211-218), when each bullet is verified, then the skill correctly documents: geo/core zero-op (AA-3); widgets 12-vs-8 drift with `DevModeSettingsV2` out of scope (QUESTION-043); vendored snapshot `0.0.0` vs installed `1.102.0` with a re-verification cycle per SDK minor release; 1.5 MiB download / 16 MiB upload bounds; preview parameters excluded; attribution scope limited to FR-ATTR-4 namespaces (media_sets currently).
- File/function under test: Section 8 (L211-218).
- Prerequisites/fixtures: SAD-001 AA-3; QUESTION-043 decision; ENV-REF-001 review cycle note; binary bounds; preview exclusion convention; SRS FR-ATTR-4.
- Steps: assert all six bullets exist; verify each against its source; assert the attribution bullet names `FOUNDRY_ENABLE_ATTRIBUTION`/`_ATTRIBUTION_RIDS` (or the project's canonical names) and states `include_attribution=False` for other namespaces; assert no bullet contradicts Section 2 or 3 counts.
- Expected: all six bullets accurate and internally consistent; attribution scope matches FR-ATTR-4 (media_sets currently the only in-scope namespace).
- Cleanup: none.
- Evidence mapping: DESIGN-023 Section 8; QUESTION-043; SAD-001 AA-3; SRS FR-ATTR-4.

### KNW-TC-023 - Authoritative references all resolve and are cited

- Type: positive, completeness.
- Given the skill's citations, when every referenced document is checked on disk, then all of SRS-001, SAD-001, ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-007, ENV-REF-001, META-ALLOW-001, and QUESTION-043 resolve to existing artifacts, and no cited identifier is invented or misspelled.
- File/function under test: full skill (citation scan).
- Prerequisites/fixtures: `.ept/docs/deliverables/` document tree; `.ept/docs/deliverables/architecture/adr/` ADR files.
- Steps: extract all citation-like tokens (`SRS-001`, `SAD-001`, `ADR-00N`, `ENV-REF-001`, `META-ALLOW-001`, `QUESTION-043`, `AA-3`, `FR-ACL`, `FR-ATTR-4`); for each, assert the referenced document/decision exists on disk (or is a closed tracker ticket for QUESTION-043); assert the citation context is accurate (e.g. ADR-006 cited only for the `.env` search order).
- Expected: every citation resolves; no stale or invented identifiers; citation contexts match the governing documents.
- Cleanup: none.
- Evidence mapping: DEV-023 AC "Content references authoritative documents (SRS-001, SAD-001, ADR-001..007, ENV-REF-001, META-ALLOW-001) rather than re-deriving facts".

### KNW-TC-024 - Markdown validity and table integrity

- Type: structural, negative.
- Given the full skill text, when markdown structure is validated, then all tables have consistent column counts and space-padded separators per convention, all headings are well-formed, no line exceeds the file's convention, and the file contains no leftover template or TODO markers.
- File/function under test: full skill (218 lines).
- Prerequisites/fixtures: a markdown table validator or manual column-count check per table; the project's space-padded separator convention (e.g. `| --- | --- |`).
- Steps: for every table, assert every row has the same number of columns as its separator row; assert every `##`/`###` heading is non-empty; assert no `TODO`, `TBD`, or placeholder text; assert the frontmatter block is terminated by `---` (L4) and contains only `name` and `description` keys.
- Expected: all tables structurally valid; no TODO/TBD markers; frontmatter well-formed (see also the description-style convention shared by the 18 sibling skill files).
- Cleanup: none.
- Evidence mapping: DEV-023 AC "Markdown lint-clean (space-padded table separators per established convention)".

## Traceability matrix

| Requirement area | Story/design criteria | Cases |
| --- | --- | --- |
| File existence, frontmatter, 8 sections present | DEV-023 AC 1, 2; DESIGN-023 section-by-section spec | KNW-TC-001 |
| Platform concept primer, namespace skill mapping | DEV-023 AC 2 (concepts); DESIGN-023 Section 1 | KNW-TC-002 |
| 20-namespace overview table, per-namespace counts, totals 351/355 | DEV-023 AC 3; DESIGN-023 Section 2; SAD-001 AA-3 | KNW-TC-003 through 006 |
| Operation catalogue, per-resource groups, spot-checks | DEV-023 AC 3; DESIGN-023 Section 3 | KNW-TC-007 through 010 |
| Auth guide: UserTokenAuth, AsyncClientFactory, ADR-006 order | DEV-023 AC 2; UNITTEST-023 AC 2 | KNW-TC-011 through 013 |
| Access control: 8-step precedence, naming patterns, 162/193 policy | DEV-023 AC 2; UNITTEST-023 AC 3; ADR-007; META-ALLOW-001 | KNW-TC-014 through 016 |
| TOON vs JSON rule | DEV-023 AC 2; UNITTEST-023 AC 4; ADR-004 | KNW-TC-017 |
| Exit codes, retry, logging | DEV-023 AC 2; ADR-001/002/005 | KNW-TC-018 through 020 |
| Troubleshooting failure modes | DEV-023 AC 2; DESIGN-023 Section 7 | KNW-TC-021 |
| Known limitations incl. widgets drift | DEV-023 AC 4; DESIGN-023 Section 8; QUESTION-043 | KNW-TC-022 |
| Authoritative references resolve | DEV-023 AC 5 | KNW-TC-023 |
| Markdown validity / lint cleanliness | DEV-023 AC 6 | KNW-TC-024 |

All DEV-023 acceptance criteria have at least one positive case; where meaningful, negative, boundary, and structural cases are included. The eight content sections are fully covered: Section 1 via KNW-TC-002; Section 2 via KNW-TC-003 through 006; Section 3 via KNW-TC-007 through 010; Section 4 via KNW-TC-011 through 013; Section 5 via KNW-TC-014 through 016; Section 6 via KNW-TC-017; Section 7 via KNW-TC-018 through 021; Section 8 via KNW-TC-022; the whole artifact via KNW-TC-001, KNW-TC-023, and KNW-TC-024.

## Execution and approval criteria

TESTEXEC-023 may begin only after DEV, UNITTEST, CODEREVIEW, and TESTCASE-023 reach their required completed states and the approved commit `a4d48ab` is available. Execute all 24 cases as content-accuracy checks against the authoritative sources; no live Foundry access, credentials, or CLI invocation is required for any mandatory case.

For every case, record PASS, FAIL, or BLOCKED with the checked skill lines, the authoritative source reference, expected and actual content, and linked evidence. Any failure requires a BUG-SUB before TESTEXEC-023 can close. Final QA sign-off also requires all linked defects to be terminal and every DEV-023 acceptance criterion to have passing evidence.
