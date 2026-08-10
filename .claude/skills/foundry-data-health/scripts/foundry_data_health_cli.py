#!/usr/bin/env python3
"""Thin launcher for packaged Foundry Data Health CLI."""

from foundry_cli.data_health.scripts.foundry_data_health_cli import (
    build_parser,
    console_main,
    main,
)

__all__ = ["build_parser", "console_main", "main"]


if __name__ == "__main__":
    raise SystemExit(console_main())
