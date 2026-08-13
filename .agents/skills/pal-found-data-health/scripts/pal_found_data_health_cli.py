#!/usr/bin/env python3
"""Thin launcher for packaged Foundry Data Health CLI."""

from pal_found_cli.data_health.scripts.pal_found_data_health_cli import (
    build_parser,
    console_main,
    main,
)

__all__ = ["build_parser", "console_main", "main"]


if __name__ == "__main__":
    raise SystemExit(console_main())
