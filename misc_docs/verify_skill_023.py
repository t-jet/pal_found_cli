"""UNITTEST-023 — content-accuracy verification of .claude/skills/foundry/SKILL.md.

Checks (mapped to ticket ACs):
1. 20 namespace entries + operation counts match canonical refs and source OP_SPECS.
2. Auth guide correctness (UserTokenAuth from FOUNDRY_TOKEN, FOUNDRY_HOSTNAME, ADR-006 order).
3. Access control 8-step precedence per ADR-007 + control variable naming patterns.
4. TOON explanation matches ADR-004 rule.
5. Exit-code taxonomy matches ADR-001.
6. widgets known-limitation matches QUESTION-043 decision.
7. Markdown lint clean (checked via VS Code markdown.validate; here structural checks).
8. References resolve to real documents.
9. .env variable names match ADR-006/canonical reference.
"""
import ast
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILL = os.path.join(ROOT, ".claude", "skills", "foundry", "SKILL.md")
SRC = os.path.join(ROOT, "src", "foundry_cli")
DOCS = os.path.join(ROOT, ".ept", "docs")

NAMESPACES = [
    "admin", "aip_agents", "audit", "checkpoints", "connectivity", "data_health",
    "datasets", "filesystem", "functions", "language_models", "media_sets", "models",
    "ontologies", "orchestration", "sql_queries", "streams", "third_party_applications",
    "widgets",
]

# Documented counts (355 = 351 + 4 widgets not-implemented rows; widgets shown at runtime 8).
DOCUMENTED = {
    "admin": 66, "aip_agents": 15, "audit": 2, "checkpoints": 3, "connectivity": 20,
    "data_health": 6, "datasets": 33, "filesystem": 31, "functions": 7,
    "language_models": 2, "media_sets": 19, "models": 23, "ontologies": 67,
    "orchestration": 20, "sql_queries": 5, "streams": 15,
    "third_party_applications": 9, "widgets": 8, "geo": 0, "core": 0,
}

failures: list[str] = []
checks: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    tag = "PASS" if ok else "FAIL"
    checks.append(f"[{tag}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def count_op_specs_tuple(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "OP_SPECS":
            if isinstance(node.value, ast.Tuple):
                return len(node.value.elts)
    raise ValueError(path)


def count_datasets_ops(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    calls: list[int] = []

    def visit_body(body: list[ast.stmt]) -> None:
        for stmt in body:
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                fn = stmt.value.func
                if isinstance(fn, ast.Name) and fn.id == "_add_operation":
                    calls.append(1)
            elif isinstance(stmt, ast.For):
                if isinstance(stmt.iter, ast.Tuple):
                    calls.append(len(stmt.iter.elts))
                else:
                    visit_body(stmt.body)
            elif isinstance(stmt, ast.FunctionDef) and stmt.name == "build_parser":
                visit_body(stmt.body)

    visit_body(tree.body)
    return sum(calls)


def main() -> int:
    text = open(SKILL, encoding="utf-8").read()

    # --- 1. Namespace overview table counts ---
    table = re.search(r"## 2\. Namespace overview.*?(?=\n## 3\.)", text, re.DOTALL)
    assert table, "section 2 not found"
    rows = re.findall(r"^\| (\S+) \| (?:foundry-[\w-]+|—) \| (\d+)\*? \|", table.group(0), re.MULTILINE)
    rows_dict = {name: int(count) for name, count in rows}
    check("1a. All 20 namespaces present in overview table", len(rows_dict) == 20,
          f"found {len(rows_dict)}: {sorted(rows_dict)}")
    check("1b. Overview counts match documented counts",
          all(rows_dict.get(ns) == DOCUMENTED.get(ns) for ns in NAMESPACES) and rows_dict.get("geo") == 0 and rows_dict.get("core") == 0,
          f"table={rows_dict}")

    # Source AST counts (implemented surface)
    src_counts: dict[str, int] = {}
    for ns in NAMESPACES:
        path = os.path.join(SRC, ns, "scripts", f"foundry_{ns}_cli.py")
        if ns == "datasets":
            src_counts[ns] = count_datasets_ops(path)
        else:
            src_counts[ns] = count_op_specs_tuple(path)
    impl_total = sum(src_counts.values())
    check("1c. Implemented total from source = 351", impl_total == 351, f"got {impl_total}")
    check("1d. Overview table matches implemented source counts",
          all(rows_dict.get(ns) == src_counts.get(ns) for ns in NAMESPACES),
          f"src={src_counts}")
    check("1e. Documented 355 total stated in skill",
          "355" in text and "351" in text,
          "both numbers present (355 documented, 351 implemented)")

    # --- 2. Auth guide ---
    check("2a. UserTokenAuth from FOUNDRY_TOKEN", "UserTokenAuth" in text and "`FOUNDRY_TOKEN`" in text)
    check("2b. FOUNDRY_HOSTNAME via AsyncClientFactory", "FOUNDRY_HOSTNAME" in text and "AsyncClientFactory" in text)
    check("2c. ADR-006 search order stated", "FOUNDRY_AGENTIC_CLI_ENV_FILE" in text
          and "Git-root" in text and "Environment variables only" in text)
    check("2d. No home-dir fallback stated", "home directory is deliberately never searched" in text)
    check("2e. override=False semantics", "override=False" in text)
    check("2f. .env.example reference", ".env.example" in text)

    # --- 3. Access control ---
    check("3a. 8-step precedence model present", "8-step precedence model" in text and "ADR-007" in text)
    check("3b. Control variable naming patterns", "FOUNDRY_AGENTIC_CLI_{NS}_{CONTROL}" in text
          and "FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_{CONTROL}" in text)
    check("3c. _ENABLED/_READONLY/_METADATA_ONLY suffixes", "_ENABLED" in text and "_READONLY" in text and "_METADATA_ONLY" in text)
    check("3d. Exit code 8 AccessControlError", "exit code 8" in text and "AccessControlError" in text)
    check("3e. Metadata-only 162/193 default-deny", "162" in text and "193" in text)
    check("3f. ADR-007 operation-level READONLY not independent", "_READONLY=true" in text)
    check("3g. SRS-001 FR-ACL cited in access control section", "SRS-001 Section 4" in text and "FR-ACL" in text)

    # --- 4. TOON ---
    check("4a. TOON condition (list + uniform field set)", "list" in text and "identical field set" in text)
    check("4b. JSON fallback cases", "single objects" in text and "empty lists" in text and "errors" in text)
    check("4c. --format and default format", "--format" in text and "FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT" in text and "auto" in text)
    check("4d. toon-python + metadata separator", "toon-python" in text and "# ---metadata-start---" in text)

    # --- 5. Exit codes (ADR-001) ---
    # Find the exit-code table section: rows like "| 0 | Success | ... |"
    exit_section = re.search(r"### Exit codes \(ADR-001\)(.*?)(?=\n### )", text, re.DOTALL)
    exit_rows = re.findall(r"^\| (\d) \| ([^|]+?) \|", exit_section.group(1) if exit_section else "", re.MULTILINE)
    exit_codes = {int(n): name.strip() for n, name in exit_rows}
    expected = {
        0: "Success", 1: "User input error", 2: "Authentication error",
        3: "Permission denied", 4: "Not found", 5: "Timeout",
        6: "Server error", 7: "Rate limit exhausted", 8: "Access control block",
        9: "Configuration error",
    }
    check("5a. All 10 exit codes present with names",
          all(k in exit_codes for k in expected),
          f"found {sorted(exit_codes)}")
    check("5b. Exit-code names match ADR-001 taxonomy",
          all(expected[k].lower() in exit_codes[k].lower() for k in expected),
          f"exit_codes={exit_codes}")
    check("5c. Missing token/hostname maps to exit 9 (ConfigurationError)",
          "Exit 9 at startup" in text and "ConfigurationError" in text and "Missing" not in text[:0])
    check("5d. Invalid token maps to exit 2 (SDK auth failure)",
          "Exit 2 on a call" in text and "SDK auth failure" in text)

    # --- 6. Widgets limitation ---
    check("6a. Widgets 12-vs-8 drift recorded", "12" in text and "8" in text and "QUESTION-043" in text)
    check("6b. Runtime surface authoritative", "runtime surface is authoritative" in text)
    check("6c. DevModeSettingsV2 out of scope", "DevModeSettingsV2" in text and "out of scope" in text)

    # --- 7. Markdown structure (lint is via VS Code; structural checks here) ---
    headings = re.findall(r"^#{1,2} .+", text, re.MULTILINE)
    needed = ["## 1. Foundry platform concepts", "## 2. Namespace overview", "## 3. Operation catalogue",
              "## 4. Authentication setup", "## 5. Access control configuration",
              "## 6. Output format: TOON vs JSON", "## 7. Troubleshooting", "## 8. Known limitations and open items"]
    check("7a. All 8 section headings present", all(h in headings for h in needed), f"headings={headings}")
    check("7b. Frontmatter name+description", re.search(r"^---\nname: foundry\ndescription: .+\n---", text, re.MULTILINE) is not None)
    check("7c. Table separator rows space-padded",
          all(re.match(r"^\|(?: [-\s]+ \|)+$", line) for line in text.splitlines() if "---" in line and line.startswith("|")))

    # --- 8. References resolve ---
    refs = {
        "SRS-001": os.path.join(DOCS, "deliverables", "business_analysis", "SRS-001-foundry-cli.md"),
        "SAD-001": os.path.join(DOCS, "deliverables", "architecture", "SAD-001-foundry-cli.md"),
        "ADR-001": os.path.join(DOCS, "deliverables", "architecture", "adr", "ADR-001-exit-code-taxonomy.md"),
        "ADR-002": os.path.join(DOCS, "deliverables", "architecture", "adr", "ADR-002-call-timeout-defaults.md"),
        "ADR-003": os.path.join(DOCS, "deliverables", "architecture", "adr", "ADR-003-streams-batch-strategy.md"),
        "ADR-004": os.path.join(DOCS, "deliverables", "architecture", "adr", "ADR-004-format-auto-algorithm.md"),
        "ADR-005": os.path.join(DOCS, "deliverables", "architecture", "adr", "ADR-005-log-format.md"),
        "ADR-006": os.path.join(DOCS, "deliverables", "architecture", "adr", "ADR-006-env-file-search-path.md"),
        "ADR-007": os.path.join(DOCS, "deliverables", "architecture", "adr", "ADR-007-operation-level-readonly.md"),
        "ENV-REF-001": os.path.join(DOCS, "deliverables", "architecture", "canonical-env-var-reference.md"),
        "META-ALLOW-001": os.path.join(DOCS, "deliverables", "architecture", "metadata-allow-list.md"),
    }
    missing = [name for name, path in refs.items() if not os.path.isfile(path)]
    check("8a. All cited reference documents exist", not missing, f"missing={missing}")
    for name, path in refs.items():
        if os.path.isfile(path):
            check(f"8b. {name} cited in skill", name in text)
    # --- 9. Env var names ---
    env_names = ["FOUNDRY_TOKEN", "FOUNDRY_HOSTNAME", "FOUNDRY_AGENTIC_CLI_ENV_FILE",
                 "FOUNDRY_AGENTIC_CLI_READONLY", "FOUNDRY_AGENTIC_CLI_METADATA_ONLY",
                 "FOUNDRY_AGENTIC_CLI_TIMEOUT_S", "FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S",
                 "FOUNDRY_AGENTIC_CLI_LOG_LEVEL", "FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT",
                 "FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES",
                 "FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION", "FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS"]
    missing_env = [e for e in env_names if e not in text]
    check("9a. All canonical env var names present", not missing_env, f"missing={missing_env}")
    env_ref = open(os.path.join(DOCS, "deliverables", "architecture", "canonical-env-var-reference.md"), encoding="utf-8").read()
    bad = [e for e in env_names if e not in env_ref]
    check("9b. All skill env var names exist in canonical reference", not bad, f"not-in-ref={bad}")

    print("\n".join(checks))
    print(f"\nTOTAL: {len(checks)} checks, {len(failures)} failures")
    if failures:
        print("FAILED:", *failures, sep="\n  - ")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
