#!/usr/bin/env python3
"""Foundry Datasets CLI - 33 operations across 5 resource clients.

Exposes all Foundry Datasets API v2 operations as CLI subcommands:
- Dataset (11): create, get, get-health-check-reports, get-health-checks,
  get-schedules, get-schema, get-schema-batch, jobs, put-schema, read-table, transactions
- Branch (5): create, delete, get, list, transactions
- File (5): content, delete, get, list, upload
- Transaction (6): abort, build, commit, create, get, job
- View (6): add-backing-datasets, add-primary-key, create, get,
  remove-backing-datasets, replace-backing-datasets

Usage: python pal_found_datasets_cli.py <resource> <operation> [options]
Output: JSON/TOON on stdout, metadata on stderr (ADR-004, ADR-005).
Exit codes per ADR-001 taxonomy.
Access Control: Auth -> Access Control -> API call order (SRS 4.2, ADR-007).
Retry: Exponential backoff with jitter per ADR-002.
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any, Optional

# Robust project-root discovery: walk up from this script until the
# `pal_found_cli` package (src/pal_found_cli) is located. This avoids the fragile
# fixed-depth `parents[4]` assumption that breaks if the skill is relocated.
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT: Optional[str] = None
_candidate = _SCRIPT_DIR
for _depth in range(8):
    if (_candidate / "src" / "pal_found_cli" / "__init__.py").exists():
        _PROJECT_ROOT = str(_candidate)
        break
    if _candidate.parent == _candidate:
        break
    _candidate = _candidate.parent
if _PROJECT_ROOT is None:
    # Last-resort fallback to the historical fixed-depth guess so that the
    # import error surfaces as a normal Python ImportError rather than an
    # unrelated NameError.
    _PROJECT_ROOT = str(_SCRIPT_DIR.parents[4])
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from pal_found_cli.common.config_loader import ConfigLoader
from pal_found_cli.common.async_client_factory import AsyncClientFactory
from pal_found_cli.common.error_serializer import (
    EXIT_SUCCESS, EXIT_USER_INPUT, EXIT_PERMISSION_DENIED,
    EXIT_NOT_FOUND, EXIT_TIMEOUT, EXIT_SERVER_ERROR, EXIT_RATE_LIMIT,
    EXIT_ACCESS_CONTROL, EXIT_CONFIGURATION, ErrorSerializer,
)
from pal_found_cli.common.output_formatter import OutputFormatter
from pal_found_cli.common.log_setup import LogSetup
from pal_found_cli.common.access_control_guard import AccessControlGuard, AccessControlError
from pal_found_cli.common.pagination_helper import PaginationHelper
from pal_found_cli.common.retry import RetryHandler

logger = logging.getLogger(__name__)


def _model_to_dict(obj: Any) -> Any:
    """Convert Pydantic model to serializable dict.

    Handles Pydantic v2 (model_dump), Pydantic v1 (dict), nested collections.
    Checks list/dict before model methods to avoid treating collections as models.
    Uses try/except so MagicMock or objects with dynamic attributes don't corrupt output.
    """
    if obj is None:
        return None
    if isinstance(obj, list):
        return [_model_to_dict(i) for i in obj]
    if isinstance(obj, dict):
        return {k: _model_to_dict(v) for k, v in obj.items()}
    # Try Pydantic v2 first
    try:
        result = obj.model_dump()
        if isinstance(result, dict):
            return result
    except (AttributeError, TypeError):
        pass
    # Fallback to Pydantic v1
    try:
        result = obj.dict()
        if isinstance(result, dict):
            return result
    except (AttributeError, TypeError):
        pass
    return obj


def _get_client(cfg: ConfigLoader, resource: str) -> Any:
    """Get the SDK client for a resource.

    Parameters
    ----------
    cfg : ConfigLoader
        Configuration instance.
    resource : str
        Resource name: dataset, branch, file, transaction, view.

    Returns
    -------
    Any
        SDK client for the requested resource.
    """
    client = AsyncClientFactory.create(cfg).datasets.Dataset
    resource_map = {
        "branch": "Branch",
        "file": "File",
        "transaction": "Transaction",
        "view": "View",
    }
    attr = resource_map.get(resource)
    return getattr(client, attr) if attr else client


async def _invoke(
    resource: str,
    operation: str,
    client: Any,
    args: argparse.Namespace,
    timeout: Optional[int],
) -> Any:
    """Invoke SDK operation (async).

    Parameters
    ----------
    resource : str
        Resource name.
    operation : str
        snake_case operation name.
    client : Any
        SDK client instance.
    args : argparse.Namespace
        Parsed CLI arguments.
    timeout : Optional[int]
        Request timeout in seconds. May be ``None`` to let the SDK decide.

    Returns
    -------
    Any
        SDK response object.

    Raises
    ------
    ValueError
        If the operation is not recognized.
    """
    dr = getattr(args, "dataset_rid", None)
    bn = getattr(args, "branch_name", None)
    tr = getattr(args, "transaction_rid", None)
    ps = getattr(args, "page_size", None)
    pt = getattr(args, "page_token", None)
    fp = getattr(args, "file_path", None)
    vr = getattr(args, "view_dataset_rid", None)
    br = getattr(args, "branch", None)
    nm = getattr(args, "name", None)
    pfr = getattr(args, "parent_folder_rid", None)

    if resource == "dataset":
        if operation == "create":
            return await client.create(name=nm, parent_folder_rid=pfr, request_timeout=timeout)
        if operation == "get":
            return await client.get(dataset_rid=dr, request_timeout=timeout)
        if operation == "get_health_check_reports":
            return await client.get_health_check_reports(dataset_rid=dr, branch_name=bn, request_timeout=timeout)
        if operation == "get_health_checks":
            return await client.get_health_checks(dataset_rid=dr, branch_name=bn, request_timeout=timeout)
        if operation == "get_schedules":
            return await client.get_schedules(dataset_rid=dr, branch_name=bn, page_size=ps, page_token=pt, request_timeout=timeout)
        if operation == "get_schema":
            return await client.get_schema(dataset_rid=dr, branch_name=bn, request_timeout=timeout)
        if operation == "get_schema_batch":
            rids_arg = getattr(args, "dataset_rids", None)
            rids = json.loads(rids_arg) if isinstance(rids_arg, str) else rids_arg
            return await client.get_schema_batch(dataset_rids=rids, request_timeout=timeout)
        if operation == "jobs":
            return await client.jobs(dataset_rid=dr, page_size=ps, page_token=pt, request_timeout=timeout)
        if operation == "put_schema":
            schema_arg = getattr(args, "schema", None)
            schema = json.loads(schema_arg) if isinstance(schema_arg, str) else schema_arg
            return await client.put_schema(dataset_rid=dr, schema=schema, branch_name=bn, request_timeout=timeout)
        if operation == "read_table":
            return await client.read_table(dataset_rid=dr, branch_name=bn, page_size=ps, page_token=pt, request_timeout=timeout)
        if operation == "transactions":
            return await client.transactions(dataset_rid=dr, page_size=ps, page_token=pt, request_timeout=timeout)
    elif resource == "branch":
        if operation == "create":
            return await client.create(dataset_rid=dr, name=nm, transaction_rid=tr, request_timeout=timeout)
        if operation == "delete":
            return await client.delete(dataset_rid=dr, branch_name=bn, request_timeout=timeout)
        if operation == "get":
            return await client.get(dataset_rid=dr, branch_name=bn, request_timeout=timeout)
        if operation == "list":
            return await client.list(dataset_rid=dr, page_size=ps, page_token=pt, request_timeout=timeout)
        if operation == "transactions":
            return await client.transactions(dataset_rid=dr, branch_name=bn, page_size=ps, page_token=pt, request_timeout=timeout)
    elif resource == "file":
        if operation == "content":
            return await client.content(
                dataset_rid=dr, file_path=fp, branch_name=bn,
                end_transaction_rid=getattr(args, "end_transaction_rid", None),
                start_transaction_rid=getattr(args, "start_transaction_rid", None),
                request_timeout=timeout,
            )
        if operation == "delete":
            return await client.delete(dataset_rid=dr, file_path=fp, transaction_rid=tr, request_timeout=timeout)
        if operation == "get":
            return await client.get(dataset_rid=dr, file_path=fp, transaction_rid=tr, request_timeout=timeout)
        if operation == "list":
            return await client.list(dataset_rid=dr, transaction_rid=tr, page_size=ps, page_token=pt, request_timeout=timeout)
        if operation == "upload":
            if fp is None:
                raise ValueError("file_path is required for upload operation")
            with open(fp, "rb") as fobj:
                data = fobj.read()
            return await client.upload(dataset_rid=dr, file_path=fp, content=data, transaction_rid=tr, request_timeout=timeout)
    elif resource == "transaction":
        if operation == "abort":
            return await client.abort(dataset_rid=dr, transaction_rid=tr, request_timeout=timeout)
        if operation == "build":
            return await client.build(dataset_rid=dr, transaction_rid=tr, request_timeout=timeout)
        if operation == "commit":
            return await client.commit(dataset_rid=dr, transaction_rid=tr, request_timeout=timeout)
        if operation == "create":
            return await client.create(dataset_rid=dr, branch_name=bn, request_timeout=timeout)
        if operation == "get":
            return await client.get(dataset_rid=dr, transaction_rid=tr, request_timeout=timeout)
        if operation == "job":
            return await client.job(dataset_rid=dr, transaction_rid=tr, request_timeout=timeout)
    elif resource == "view":
        bd_arg = getattr(args, "backing_datasets", None)
        bd = json.loads(bd_arg) if isinstance(bd_arg, str) else bd_arg
        pk_arg = getattr(args, "primary_key", None)
        pk = json.loads(pk_arg) if isinstance(pk_arg, str) else pk_arg
        if operation == "add_backing_datasets":
            return await client.add_backing_datasets(view_dataset_rid=vr, backing_datasets=bd, branch=br, request_timeout=timeout)
        if operation == "add_primary_key":
            return await client.add_primary_key(view_dataset_rid=vr, primary_key=pk, branch=br, request_timeout=timeout)
        if operation == "create":
            return await client.create(name=nm, parent_folder_rid=pfr, backing_datasets=bd, request_timeout=timeout)
        if operation == "get":
            return await client.get(view_dataset_rid=vr, branch=br, request_timeout=timeout)
        if operation == "remove_backing_datasets":
            return await client.remove_backing_datasets(view_dataset_rid=vr, backing_datasets=bd, branch=br, request_timeout=timeout)
        if operation == "replace_backing_datasets":
            return await client.replace_backing_datasets(view_dataset_rid=vr, backing_datasets=bd, branch=br, request_timeout=timeout)
    raise ValueError(f"Unknown operation: {resource}.{operation}")


# Operations that return a paginated response and accept page_size/page_token
# (FR-PAG-3). For these, the CLI wraps the SDK call with PaginationHelper to
# honour --page-size / --page-token / --batch-pages and emit metadata to stderr.
PAGINATED_OPS = frozenset({
    ("dataset", "get_schedules"),
    ("dataset", "jobs"),
    ("dataset", "read_table"),
    ("dataset", "transactions"),
    ("branch", "list"),
    ("branch", "transactions"),
    ("file", "list"),
    ("transaction", "transactions"),
})


def _is_paginated(resource: str, operation: str) -> bool:
    """Return True if the operation supports pagination (FR-PAG-3)."""
    return (resource, operation) in PAGINATED_OPS


async def _invoke_paginated(
    resource: str,
    operation: str,
    client: Any,
    args: argparse.Namespace,
    timeout: Optional[int],
    helper: PaginationHelper,
) -> Any:
    """Invoke a paginated SDK operation through PaginationHelper.

    Builds a single-page callable that delegates to ``_invoke`` (which already
    forwards page_size/page_token) and feeds it to ``helper.paginate`` so the
    batch aggregation, max-cap enforcement, and token propagation behave per
    FR-PAG-1/2/4/5. The helper's metadata is emitted to stderr by the caller.

    The base pagination kwargs are extracted from the args namespace so they
    are NOT doubly passed (the SDK call receives them inside ``_invoke``).
    """
    dr = getattr(args, "dataset_rid", None)

    async def _single_page(**page_kwargs: Any) -> Any:
        # Materialize a fresh namespace so page tokens from the helper override
        # the CLI-supplied values without mutating the original args.
        paged_args = argparse.Namespace(**vars(args))
        paged_args.page_size = page_kwargs.get("page_size", getattr(args, "page_size", None))
        paged_args.page_token = page_kwargs.get("page_token", None)
        return await _invoke(resource, operation, client, paged_args, timeout)

    return await helper.paginate(_single_page)


OP_MAP = {
    "dataset": {
        "get-health-check-reports": "get_health_check_reports",
        "get-health-checks": "get_health_checks",
        "get-schedules": "get_schedules",
        "get-schema": "get_schema",
        "get-schema-batch": "get_schema_batch",
        "put-schema": "put_schema",
        "read-table": "read_table",
    },
    "view": {
        "add-backing-datasets": "add_backing_datasets",
        "add-primary-key": "add_primary_key",
        "remove-backing-datasets": "remove_backing_datasets",
        "replace-backing-datasets": "replace_backing_datasets",
    },
}


def _resolve(resource: str, op: str) -> str:
    """Resolve kebab-case operation name to snake_case."""
    mapping = OP_MAP.get(resource, {})
    return mapping.get(op, op.replace("-", "_"))


def _common_parser() -> argparse.ArgumentParser:
    """Build the shared argparse parent with global options.

    Every leaf operation subparser inherits these arguments via ``parents``,
    so options like ``--timeout`` may appear after the operation positional.
    """
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--timeout", type=int, default=None)
    common.add_argument("--format", choices=["json", "toon", "auto"], default="auto")
    common.add_argument("--pretty", action="store_true")
    common.add_argument("--page-size", type=int, default=None, dest="page_size")
    common.add_argument("--page-token", type=str, default=None, dest="page_token")
    common.add_argument("--batch-pages", type=int, default=None, dest="batch_pages")
    return common


def build_parser() -> argparse.ArgumentParser:
    """Build argparse parser with all 33 operations."""
    parser = argparse.ArgumentParser(
        prog="pal_found_datasets_cli",
        description="Foundry Datasets CLI - 33 operations across 5 resource clients",
    )
    subparsers = parser.add_subparsers(dest="resource", help="Resource type")

    # --- Dataset (11 operations) ---
    ds = subparsers.add_parser("dataset")
    ds_sub = ds.add_subparsers(dest="operation")
    _p = ds_sub.add_parser("create", parents=[_common_parser()]); _p.add_argument("--name", required=True); _p.add_argument("--parent-folder-rid", required=True, dest="parent_folder_rid")
    _p = ds_sub.add_parser("get", parents=[_common_parser()]); _p.add_argument("dataset_rid")
    _p = ds_sub.add_parser("get-health-check-reports", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--branch-name", default=None, dest="branch_name")
    _p = ds_sub.add_parser("get-health-checks", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--branch-name", default=None, dest="branch_name")
    _p = ds_sub.add_parser("get-schedules", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--branch-name", default=None, dest="branch_name")
    _p = ds_sub.add_parser("get-schema", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--branch-name", default=None, dest="branch_name")
    _p = ds_sub.add_parser("get-schema-batch", parents=[_common_parser()]); _p.add_argument("--dataset-r", required=True, dest="dataset_rids")
    _p = ds_sub.add_parser("jobs", parents=[_common_parser()]); _p.add_argument("dataset_rid")
    _p = ds_sub.add_parser("put-schema", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--schema", required=True); _p.add_argument("--branch-name", default=None, dest="branch_name")
    _p = ds_sub.add_parser("read-table", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--branch-name", default=None, dest="branch_name")
    _p = ds_sub.add_parser("transactions", parents=[_common_parser()]); _p.add_argument("dataset_rid")

    # --- Branch (5 operations) ---
    br = subparsers.add_parser("branch")
    br_sub = br.add_subparsers(dest="operation")
    _p = br_sub.add_parser("create", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--name", required=True); _p.add_argument("--transaction-rid", default=None, dest="transaction_rid")
    _p = br_sub.add_parser("delete", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--branch-name", required=True, dest="branch_name")
    _p = br_sub.add_parser("get", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--branch-name", default=None, dest="branch_name")
    _p = br_sub.add_parser("list", parents=[_common_parser()]); _p.add_argument("dataset_rid")
    _p = br_sub.add_parser("transactions", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--branch-name", default=None, dest="branch_name")

    # --- File (5 operations) ---
    fl = subparsers.add_parser("file")
    fl_sub = fl.add_subparsers(dest="operation")
    _p = fl_sub.add_parser("content", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--file-path", required=True, dest="file_path"); _p.add_argument("--branch-name", default=None, dest="branch_name"); _p.add_argument("--end-transaction-rid", default=None, dest="end_transaction_rid"); _p.add_argument("--start-transaction-rid", default=None, dest="start_transaction_rid")
    _p = fl_sub.add_parser("delete", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--file-path", required=True, dest="file_path"); _p.add_argument("--transaction-rid", default=None, dest="transaction_rid")
    _p = fl_sub.add_parser("get", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--file-path", required=True, dest="file_path"); _p.add_argument("--transaction-rid", default=None, dest="transaction_rid")
    _p = fl_sub.add_parser("list", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--transaction-rid", default=None, dest="transaction_rid")
    _p = fl_sub.add_parser("upload", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--file-path", required=True, dest="file_path"); _p.add_argument("--transaction-rid", default=None, dest="transaction_rid")

    # --- Transaction (6 operations) ---
    tx = subparsers.add_parser("transaction")
    tx_sub = tx.add_subparsers(dest="operation")
    _p = tx_sub.add_parser("abort", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--transaction-rid", required=True, dest="transaction_rid")
    _p = tx_sub.add_parser("build", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--transaction-rid", required=True, dest="transaction_rid")
    _p = tx_sub.add_parser("commit", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--transaction-rid", required=True, dest="transaction_rid")
    _p = tx_sub.add_parser("create", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--branch-name", default=None, dest="branch_name")
    _p = tx_sub.add_parser("get", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--transaction-rid", required=True, dest="transaction_rid")
    _p = tx_sub.add_parser("job", parents=[_common_parser()]); _p.add_argument("dataset_rid"); _p.add_argument("--transaction-rid", required=True, dest="transaction_rid")

    # --- View (6 operations) ---
    vw = subparsers.add_parser("view")
    vw_sub = vw.add_subparsers(dest="operation")
    _p = vw_sub.add_parser("add-backing-datasets", parents=[_common_parser()]); _p.add_argument("--view-dataset-rid", required=True, dest="view_dataset_rid"); _p.add_argument("--backing-datasets", required=True, dest="backing_datasets"); _p.add_argument("--branch", default=None)
    _p = vw_sub.add_parser("add-primary-key", parents=[_common_parser()]); _p.add_argument("--view-dataset-rid", required=True, dest="view_dataset_rid"); _p.add_argument("--primary-key", required=True, dest="primary_key"); _p.add_argument("--branch", default=None)
    _p = vw_sub.add_parser("create", parents=[_common_parser()]); _p.add_argument("--name", required=True); _p.add_argument("--parent-folder-rid", required=True, dest="parent_folder_rid"); _p.add_argument("--backing-datasets", default=None, dest="backing_datasets")
    _p = vw_sub.add_parser("get", parents=[_common_parser()]); _p.add_argument("--view-dataset-rid", required=True, dest="view_dataset_rid"); _p.add_argument("--branch", default=None)
    _p = vw_sub.add_parser("remove-backing-datasets", parents=[_common_parser()]); _p.add_argument("--view-dataset-rid", required=True, dest="view_dataset_rid"); _p.add_argument("--backing-datasets", required=True, dest="backing_datasets"); _p.add_argument("--branch", default=None)
    _p = vw_sub.add_parser("replace-backing-datasets", parents=[_common_parser()]); _p.add_argument("--view-dataset-rid", required=True, dest="view_dataset_rid"); _p.add_argument("--backing-datasets", required=True, dest="backing_datasets"); _p.add_argument("--branch", default=None)

    return parser


async def main() -> int:
    """Main entry point — async, returns exit code."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.resource:
        parser.print_help()
        return EXIT_USER_INPUT

    # WARNING-3 fix: validate operation is provided
    if not getattr(args, "operation", None):
        parser.print_help()
        return EXIT_USER_INPUT

    # Load configuration (ADR-006)
    cfg = ConfigLoader()
    cfg.load()

    # Initialize logging (ADR-005)
    LogSetup.configure(log_level=cfg.log_level)

    # Resolve operation name
    resource = args.resource
    operation = _resolve(resource, args.operation)
    logger.info("Executing operation", extra={"resource": resource, "operation": operation})

    # Access control check (ADR-007)
    guard = AccessControlGuard(cfg, "DATASETS")
    try:
        guard.check(resource, operation)
    except AccessControlError as exc:
        logger.warning("Access control denied", extra={"error": str(exc)})
        serializer = ErrorSerializer()
        serializer.serialize(exc)
        return EXIT_ACCESS_CONTROL

    # Create SDK client
    try:
        client = _get_client(cfg, resource)
    except Exception as exc:
        logger.error("Failed to create client", extra={"error": str(exc)})
        serializer = ErrorSerializer()
        serializer.serialize(exc)
        return EXIT_CONFIGURATION

    # WARNING-2 fix: resolve timeout from CLI flag or config default.
    # cfg.timeout_s is the project-wide default (ADR-002). CLI flag wins.
    timeout = getattr(args, "timeout", None) or getattr(cfg, "timeout_s", None)

    # WARNING-1 fix: apply RetryHandler for transient error recovery (ADR-002).
    retry_handler = RetryHandler()

    # Build PaginationHelper when the operation is paginated (FR-PAG).
    # --page-size / --page-token / --batch-pages are parsed by _common_parser.
    helper: Optional[PaginationHelper] = None
    if _is_paginated(resource, operation):
        helper = PaginationHelper(
            page_size=getattr(args, "page_size", None),
            page_token=getattr(args, "page_token", None),
            batch_pages=getattr(args, "batch_pages", None),
        )

    # Invoke operation
    try:
        if helper is not None:
            result = await retry_handler.execute(
                _invoke_paginated,
                resource, operation, client, args, timeout, helper,
            )
        else:
            result = await retry_handler.execute(
                _invoke, resource, operation, client, args, timeout
            )
        formatter = OutputFormatter(
            format_setting=getattr(args, "format", "auto"),
            pretty=getattr(args, "pretty", False),
        )
        output = formatter.format(_model_to_dict(result))
        print(output)
        # Emit pagination metadata to stderr after stdout (ADR-005, FR-PAG-2).
        if helper is not None:
            helper.emit_metadata()
        return EXIT_SUCCESS
    except AccessControlError as exc:
        logger.warning("Access control denied", extra={"error": str(exc)})
        serializer = ErrorSerializer()
        serializer.serialize(exc)
        return EXIT_ACCESS_CONTROL
    except PermissionError as exc:
        serializer = ErrorSerializer()
        serializer.serialize(exc)
        return EXIT_PERMISSION_DENIED
    except FileNotFoundError as exc:
        serializer = ErrorSerializer()
        serializer.serialize(exc)
        return EXIT_NOT_FOUND
    except TimeoutError as exc:
        serializer = ErrorSerializer()
        serializer.serialize(exc)
        return EXIT_TIMEOUT
    except OSError as exc:
        serializer = ErrorSerializer()
        exit_code = serializer.serialize(exc)
        # Check if it looks like a rate limit (errno 11 or EAGAIN)
        if getattr(exc, "errno", None) in (11, 115):
            return EXIT_RATE_LIMIT
        return exit_code
    except Exception as exc:
        serializer = ErrorSerializer()
        serializer.serialize(exc)
        return EXIT_SERVER_ERROR


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
