"""Generate canonical env var reference table and metadata allow-list."""
import os
import re

BASE = r'.ept\docs\customer_input\foundry-platform-python\foundry_sdk\v2'

# Collect all operations: (namespace, class, method)
operations = []
for ns in sorted(os.listdir(BASE)):
    ns_path = os.path.join(BASE, ns)
    if not os.path.isdir(ns_path) or ns.startswith('_'):
        continue
    for fname in sorted(os.listdir(ns_path)):
        if not fname.endswith('.py') or fname.startswith('_') or fname in ('models.py', 'errors.py'):
            continue
        cls = fname[:-3]
        content = open(os.path.join(ns_path, fname)).read()
        methods = re.findall(r'^    def ([a-z][a-z0-9_]+)\(', content, re.MULTILINE)
        unique_methods = list(dict.fromkeys(methods))  # preserve order, deduplicate
        for m in unique_methods:
            operations.append((ns, cls, m))

def to_env_suffix(ns, cls, method):
    """Convert SDK path to uppercase env var suffix."""
    return f"{ns.upper()}_{cls.upper()}_{method.upper()}"

PREFIX = "FOUNDRY_AGENTIC_CLI_"

# Output canonical env var reference as markdown
lines = []
lines.append("# Canonical Environment Variable Reference\n")
lines.append("## Foundry CLI — Agentic Toolset\n")
lines.append("")
lines.append("| Field | Value |")
lines.append("|---|---|")
lines.append("| **Document ID** | ENV-REF-001 |")
lines.append("| **Version** | 1.0.0 |")
lines.append("| **Date** | 2026-04-13 |")
lines.append("| **Author** | Solution Architect |")
lines.append("| **Total entries** | ~415+ (20 namespace vars × 3 + 355 operation vars) |")
lines.append("")
lines.append("---\n")
lines.append("## Overview\n")
lines.append("")
lines.append("This document is the authoritative mapping of every SDK path to its corresponding")
lines.append("environment variable name. Review and update on every `foundry-platform-python` minor release.\n")
lines.append("")
lines.append("**Naming conventions:**")
lines.append("")
lines.append("| Scope | Pattern | Example |")
lines.append("|---|---|---|")
lines.append("| Global | `FOUNDRY_AGENTIC_CLI_{KEY}` | `FOUNDRY_AGENTIC_CLI_READONLY` |")
lines.append("| Namespace | `FOUNDRY_AGENTIC_CLI_{NS}_{CONTROL}` | `FOUNDRY_AGENTIC_CLI_DATASETS_READONLY` |")
lines.append("| Operation | `FOUNDRY_AGENTIC_CLI_{NS}_{CLASS}_{OP}_{CONTROL}` | `FOUNDRY_AGENTIC_CLI_DATASETS_DATASET_GET_ENABLED` |")
lines.append("")
lines.append("**Control suffixes:**")
lines.append("")
lines.append("| Suffix | Values | Applies to |")
lines.append("|---|---|---|")
lines.append("| `_ENABLED` | `true` (default) / `false` | Namespace, Operation |")
lines.append("| `_READONLY` | `false` (default) / `true` (override only) | Namespace-level (set) or operation-level (override only per ADR-007) |")
lines.append("| `_METADATA_ONLY` | `false` (default) / `true` | Namespace-level only |")
lines.append("")
lines.append("---\n")

# Global variables section
lines.append("## Global Configuration Variables\n")
lines.append("")
lines.append("| Variable | Default | Type | Description |")
lines.append("|---|---|---|---|")
lines.append("| `FOUNDRY_TOKEN` | *(required)* | string | Palantir bearer token (SDK-native, no prefix) |")
lines.append("| `FOUNDRY_HOSTNAME` | *(required)* | string | Foundry instance hostname (SDK-native) |")
lines.append("| `FOUNDRY_TRACE_ID` | — | string | W3C trace ID (SDK-native, used when ENABLE_TRACING=true) |")
lines.append("| `FOUNDRY_SPAN_ID` | — | string | W3C span ID (SDK-native) |")
lines.append("| `FOUNDRY_SAMPLED` | — | string | Trace sampling flag (SDK-native) |")
lines.append("| `FOUNDRY_AGENTIC_CLI_DEFAULT_FORMAT` | `auto` | enum | Output format: `json` / `toon` / `auto` |")
lines.append("| `FOUNDRY_AGENTIC_CLI_READONLY` | `false` | bool | Global read-only mode |")
lines.append("| `FOUNDRY_AGENTIC_CLI_METADATA_ONLY` | `false` | bool | Global metadata-only mode |")
lines.append("| `FOUNDRY_AGENTIC_CLI_ENABLE_ATTRIBUTION` | `false` | bool | Enable attribution header injection |")
lines.append("| `FOUNDRY_AGENTIC_CLI_ATTRIBUTION_RIDS` | *(empty)* | string | Comma-separated attribution RIDs |")
lines.append("| `FOUNDRY_AGENTIC_CLI_ENABLE_TRACING` | `false` | bool | Enable W3C/B3 trace propagation |")
lines.append("| `FOUNDRY_AGENTIC_CLI_RETRY_INITIAL_DELAY_MS` | `500` | int | Retry initial delay in milliseconds |")
lines.append("| `FOUNDRY_AGENTIC_CLI_RETRY_MAX_DELAY_MS` | `30000` | int | Retry maximum delay in milliseconds |")
lines.append("| `FOUNDRY_AGENTIC_CLI_RETRY_MULTIPLIER` | `2.0` | float | Retry exponential backoff multiplier |")
lines.append("| `FOUNDRY_AGENTIC_CLI_RETRY_MAX_ATTEMPTS` | `4` | int | Maximum total attempts (1 + 3 retries) |")
lines.append("| `FOUNDRY_AGENTIC_CLI_TIMEOUT_S` | `30` | int | Per-call timeout in seconds (ADR-002) |")
lines.append("| `FOUNDRY_AGENTIC_CLI_STREAMS_TIMEOUT_S` | `120` | int | Streams namespace per-call timeout (ADR-002) |")
lines.append("| `FOUNDRY_AGENTIC_CLI_DEFAULT_PAGE_SIZE` | `100` | int | Default page size for list operations |")
lines.append("| `FOUNDRY_AGENTIC_CLI_MAX_BATCH_PAGES` | `40` | int | Maximum pages in one --batch-pages call |")
lines.append("| `FOUNDRY_AGENTIC_CLI_MAX_DOWNLOAD_BYTES` | `1572864` | int | Max binary download size (1.5 MB) |")
lines.append("| `FOUNDRY_AGENTIC_CLI_DOWNLOAD_PATH` | `.foundry-data/downloads` | path | Base path for binary downloads |")
lines.append("| `FOUNDRY_AGENTIC_CLI_SESSION_PATH` | `.foundry-data/sessions` | path | Base path for session state |")
lines.append("| `FOUNDRY_AGENTIC_CLI_LOG_LEVEL` | `WARNING` | enum | Log verbosity: DEBUG / INFO / WARNING / ERROR |")
lines.append("| `FOUNDRY_AGENTIC_CLI_ENV_FILE` | *(none)* | path | Explicit .env file path override (ADR-006) |")
lines.append("")
lines.append("---\n")

# Per-namespace section
namespaces = sorted(set(ns for ns, _, _ in operations))

lines.append("## Namespace-Level Control Variables\n")
lines.append("")
lines.append("| Namespace | ENABLED | READONLY (override) | METADATA_ONLY (override) |")
lines.append("|---|---|---|---|")
for ns in namespaces:
    ns_up = ns.upper()
    lines.append(f"| `{ns}` | `{PREFIX}{ns_up}_ENABLED` | `{PREFIX}{ns_up}_READONLY` | `{PREFIX}{ns_up}_METADATA_ONLY` |")
lines.append("")
lines.append("**Defaults:** All `_ENABLED=true`, `_READONLY` inherits global, `_METADATA_ONLY` inherits global.\n")
lines.append("")
lines.append("---\n")

# Per-operation table
lines.append("## Operation-Level Control Variables\n")
lines.append("")
lines.append("355 total operations across 20 namespaces.\n")
lines.append("")
lines.append("> **Note:** Operation-level `_READONLY=true` is NOT supported as an independent setting (ADR-007).")
lines.append("> `_READONLY=false` is supported as an override when a parent READONLY=true is active.")
lines.append("")

current_ns = None
for ns, cls, method in operations:
    if ns != current_ns:
        if current_ns is not None:
            lines.append("")
        lines.append(f"### Namespace: `{ns}`\n")
        lines.append("")
        lines.append("| SDK Path | `_ENABLED` variable | `_READONLY=false` (write override) |")
        lines.append("|---|---|---|")
        current_ns = ns
    
    suffix = to_env_suffix(ns, cls, method)
    sdk_path = f"`{ns}.{cls}.{method}`"
    enabled_var = f"`{PREFIX}{suffix}_ENABLED`"
    readonly_var = f"`{PREFIX}{suffix}_READONLY=false`"
    lines.append(f"| {sdk_path} | {enabled_var} | {readonly_var} |")

lines.append("")
lines.append("---\n")
lines.append("*ENV-REF-001 v1.0.0 — Generated 2026-04-13 — Foundry CLI Agentic Toolset*")

print('\n'.join(lines))
print(f"\n<!-- Total operations: {len(operations)} -->")
