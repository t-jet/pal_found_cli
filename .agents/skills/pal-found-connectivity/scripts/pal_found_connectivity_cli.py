#!/usr/bin/env python3
"""Thin launcher for packaged Foundry Connectivity CLI."""

from pal_found_cli.connectivity.scripts.pal_found_connectivity_cli import (
    build_parser,
    console_main,
    main,
)

__all__ = ["build_parser", "console_main", "main"]


if __name__ == "__main__":
    raise SystemExit(console_main())
