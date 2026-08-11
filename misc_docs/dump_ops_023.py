"""Dump resource -> operations mapping per namespace CLI from OP_SPECS.

Ground truth for the foundry/ knowledge skill operation catalogue (Section 3).
"""
import ast
import os

SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "foundry_cli"))

NAMESPACES = [
    "admin", "aip_agents", "audit", "checkpoints", "connectivity", "data_health",
    "datasets", "filesystem", "functions", "language_models", "media_sets", "models",
    "ontologies", "orchestration", "sql_queries", "streams", "third_party_applications",
    "widgets",
]


def get_op_specs(path: str) -> list[dict]:
    """Return list of {resource, operation} dicts from the OP_SPECS tuple."""
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "OP_SPECS":
            if isinstance(node.value, ast.Tuple):
                out = []
                for elt in node.value.elts:
                    if isinstance(elt, ast.Call):
                        # _op("resource", "operation", "client_path", "method", ...)
                        args = [a for a in elt.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
                        if len(args) >= 2:
                            out.append({"resource": args[0].value, "operation": args[1].value})
                    elif isinstance(elt, ast.Dict):
                        d = {}
                        for k, v in zip(elt.keys, elt.values):
                            if isinstance(k, ast.Constant) and k.value in ("resource", "operation") and isinstance(v, ast.Constant):
                                d[k.value] = v.value
                        if "resource" in d and "operation" in d:
                            out.append(d)
                return out
    return []


def main() -> None:
    for ns in NAMESPACES:
        path = os.path.join(SRC, ns, "scripts", f"foundry_{ns}_cli.py")
        if not os.path.isfile(path) or ns == "datasets":
            print(f"\n### {ns} — SKIPPED (hand-rolled CLI, see docstring)")
            continue
        specs = get_op_specs(path)
        by_resource: dict[str, list[str]] = {}
        for s in specs:
            by_resource.setdefault(s["resource"], []).append(s["operation"])
        print(f"\n### {ns} ({len(specs)} ops)")
        for res, ops in sorted(by_resource.items()):
            print(f"  {res}: {', '.join(ops)}")


if __name__ == "__main__":
    main()
