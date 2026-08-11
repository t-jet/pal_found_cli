"""Accurate operation-count verification per namespace CLI.

Strategies:
- OP_SPECS tuple assigned at module level: count tuple elements (dicts or calls).
- datasets: hand-rolled subparsers; count registered operations by simulating
  the _add_operation call graph (loops expand their iteration ranges).
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


def count_op_specs_tuple(path: str) -> int:
    """Count elements of the module-level OP_SPECS tuple assignment."""
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "OP_SPECS":
            if isinstance(node.value, ast.Tuple):
                return len(node.value.elts)
        if (
            isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "OP_SPECS" for t in node.targets)
            and isinstance(node.value, ast.Tuple)
        ):
            return len(node.value.elts)
    raise ValueError(f"OP_SPECS tuple not found in {path}")


def count_datasets_ops(path: str) -> int:
    """Count operations registered via _add_operation, expanding for-loops."""
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
                # Loop over a tuple of operation names: each iteration is one op.
                if isinstance(stmt.iter, ast.Tuple):
                    calls.append(len(stmt.iter.elts))
                else:
                    # Fallback: treat the whole loop body as a single call site.
                    visit_body(stmt.body)
            elif isinstance(stmt, ast.FunctionDef) and stmt.name == "build_parser":
                visit_body(stmt.body)

    visit_body(tree.body)
    return sum(calls)


def main() -> None:
    print(f"{'namespace':28s} {'ops':>5}  {'method':30s} file")
    total = 0
    for ns in NAMESPACES:
        path = os.path.join(SRC, ns, "scripts", f"foundry_{ns}_cli.py")
        if not os.path.isfile(path):
            print(f"{ns:28s} {'MISSING FILE':>5}")
            continue
        if ns == "datasets":
            count = count_datasets_ops(path)
            method = "datasets subparsers"
        else:
            count = count_op_specs_tuple(path)
            method = "OP_SPECS tuple"
        total += count
        print(f"{ns:28s} {count:>5}  {method:30s} {os.path.basename(path)}")
    print(f"{'TOTAL':28s} {total:>5}")


if __name__ == "__main__":
    main()
