#!/usr/bin/env python3
"""Thin launcher for packaged Foundry Third-Party Applications CLI."""

from pal_found_cli.third_party_applications.scripts.pal_found_third_party_applications_cli import (  # noqa: E402
    build_parser,
    console_main,
    main,
)

__all__ = ["build_parser", "console_main", "main"]


if __name__ == "__main__":
    raise SystemExit(console_main())
