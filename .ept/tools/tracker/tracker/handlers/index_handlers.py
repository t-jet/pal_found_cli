"""Index consistency command handlers."""

from __future__ import annotations

import argparse

import yaml

from ..index import reconcile_index_statuses


def handle_reconcile_index(args: argparse.Namespace) -> None:
    """Report or repair status differences between ticket files and index."""
    drift = reconcile_index_statuses(apply=args.apply)
    result = {
        "mode": "apply" if args.apply else "check",
        "drift_count": len(drift),
        "changed": len(drift) if args.apply else 0,
        "status_drift": drift,
    }
    print(yaml.dump(result, default_flow_style=False, sort_keys=False))
