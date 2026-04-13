"""Utility functions: sanitisation, escape-sequence decoding, timestamps, frontmatter."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

import yaml

from .exceptions import ValidationError


def sanitize_author(author: str) -> str:
    """Sanitise *author* to filesystem-safe characters (``[a-zA-Z0-9._-]``)."""
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", author.strip())
    return cleaned.strip("-") or "unknown"


def decode_escape_sequences(text: str) -> str:
    r"""Decode common backslash escape sequences from CLI input.

    Shells such as PowerShell do not expand ``\n`` inside double-quoted
    strings, so the literal two-character sequence ``\`` + ``n`` arrives
    unchanged.  This function converts the most common sequences so that
    multi-line values work as expected with ``--text`` / ``--description``.
    """
    return (
        text
        .replace("\\r\\n", "\n")   # CRLF first (most specific)
        .replace("\\r", "\n")      # bare CR → newline
        .replace("\\n", "\n")      # bare LF escape → newline
        .replace("\\t", "\t")      # tab
    )


def now_date() -> str:
    """Return the current date as ``YYYY-MM-DD``."""
    return datetime.now().strftime("%Y-%m-%d")


def now_timestamp() -> str:
    """Return the current timestamp as ``YYYY-MM-DDTHH:MM:SS``."""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def build_frontmatter_text(
    fields: dict[str, Any],
    ordered_fields: list[str],
) -> str:
    """Build YAML frontmatter from *fields* in the given order.

    Handles date objects, numeric scalars, booleans, and strings with
    special YAML characters to prevent ``yaml.safe_dump`` from appending
    a document-end marker (``...``).
    """
    lines: list[str] = []
    for field in ordered_fields:
        if field not in fields:
            continue
        value = fields[field]

        # Convert date/datetime to ISO string first
        if hasattr(value, "isoformat"):
            value = value.isoformat()

        if isinstance(value, bool):
            value_str = str(value).lower()
        elif isinstance(value, (int, float)):
            value_str = str(value)
        elif isinstance(value, str):
            if any(ch in value for ch in (":", '"')) or value.strip() != value:
                value_str = yaml.safe_dump(
                    value, default_flow_style=True, allow_unicode=True,
                ).strip()
            else:
                value_str = value
        else:
            value_str = yaml.safe_dump(
                value, default_flow_style=True, allow_unicode=True,
            ).strip()

        lines.append(f"{field}: {value_str}")
    return "\n".join(lines)


def parse_extra_fields(extra_fields: list[str] | None) -> dict[str, str]:
    """Parse ``--field key=value`` items into a dictionary.

    Raises :class:`~tracker.exceptions.ValidationError` on malformed input.
    """
    parsed: dict[str, str] = {}
    for item in extra_fields or []:
        if "=" not in item:
            raise ValidationError(
                f"Invalid --field value: '{item}'. Expected format: --field key=value"
            )
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValidationError(
                f"Invalid --field value: '{item}'. Field name cannot be empty"
            )
        parsed[key] = value
    return parsed
