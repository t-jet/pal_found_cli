#!/usr/bin/env python3
"""Thin launcher for packaged Foundry SQL Queries CLI."""

from foundry_cli.sql_queries.scripts.foundry_sql_queries_cli import (
    build_parser,
    console_main,
    main,
)

__all__ = ["build_parser", "console_main", "main"]


if __name__ == "__main__":
    raise SystemExit(console_main())
