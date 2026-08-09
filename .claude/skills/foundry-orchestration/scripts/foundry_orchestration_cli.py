#!/usr/bin/env python3
"""Thin launcher for packaged Foundry Orchestration CLI."""

from foundry_cli.orchestration.scripts.foundry_orchestration_cli import (
    build_parser,
    console_main,
    main,
)

__all__ = ["build_parser", "console_main", "main"]


if __name__ == "__main__":
    raise SystemExit(console_main())
