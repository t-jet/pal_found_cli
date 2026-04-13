"""Display formatting and TOON (Token-Oriented Object Notation) encoder."""

from __future__ import annotations

import re
from typing import Any


def format_ticket(ticket: dict[str, str]) -> str:
    """Format a ticket row for tabular display."""
    return (
        f"{ticket['id']:<15} {ticket['status']:<15} "
        f"{ticket['priority']:<10} {ticket['assignee']:<20} {ticket['title']}"
    )


def format_link(link: dict[str, str]) -> str:
    """Format a link row for tabular display."""
    return (
        f"{link['link_id']:<15} {link['source_ticket']:<15} -> "
        f"{link['target_ticket']:<15} {link['link_type']:<15} "
        f"({link['source_role']})"
    )


# ── TOON encoder ─────────────────────────────────────────────────────────────
# Spec: https://toonformat.dev/guide/format-overview

_TOON_NUMBER_RE = re.compile(
    r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?$",
)


def _toon_str_needs_quote(s: str) -> bool:
    """Return ``True`` when *s* must be quoted in TOON output."""
    if not s:
        return True
    if s != s.strip():
        return True
    if s in ("true", "false", "null"):
        return True
    if _TOON_NUMBER_RE.fullmatch(s):
        return True
    if re.match(r"^-?0[0-9]", s):
        return True
    if s[0] == "-":
        return True
    for ch in (":", '"', "\\", "[", "]", "{", "}", "\n", "\r", "\t", ","):
        if ch in s:
            return True
    return False


def _toon_quote_str(s: str) -> str:
    """Return *s* double-quoted with all required escapes applied."""
    s = (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    return f'"{s}"'


def _toon_prim(value: Any) -> str:
    """Encode a Python primitive as a TOON token."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    return _toon_quote_str(s) if _toon_str_needs_quote(s) else s


def _toon_key(key: Any) -> str:
    """Encode a dict key as a TOON key token."""
    s = str(key)
    return _toon_quote_str(s) if _toon_str_needs_quote(s) else s


def _toon_encode_fields(
    obj: dict[str, Any],
    indent: int,
    out: list[str],
) -> None:
    """Emit TOON lines for all key/value pairs in *obj*."""
    pad = " " * indent
    for key, value in obj.items():
        k = _toon_key(key)
        if value is None or isinstance(value, (bool, int, float, str)):
            out.append(f"{pad}{k}: {_toon_prim(value)}")
        elif isinstance(value, dict):
            out.append(f"{pad}{k}:")
            if value:
                _toon_encode_fields(value, indent + 2, out)
        elif isinstance(value, list):
            _toon_encode_array(k, value, indent, out)


def _toon_encode_array(
    key_tok: str,
    arr: list[Any],
    indent: int,
    out: list[str],
) -> None:
    """Emit TOON lines for an array field."""
    pad = " " * indent
    n = len(arr)

    if n == 0:
        out.append(f"{pad}{key_tok}[0]:")
        return

    # All-primitive array
    all_prim = all(
        v is None or isinstance(v, (bool, int, float, str)) for v in arr
    )
    if all_prim:
        tokens = [_toon_prim(v) for v in arr]
        if all(not t.startswith('"') for t in tokens):
            out.append(f'{pad}{key_tok}[{n}]: {",".join(tokens)}')
        else:
            ip = " " * (indent + 2)
            out.append(f"{pad}{key_tok}[{n}]:")
            for t in tokens:
                out.append(f"{ip}- {t}")
        return

    # Tabular: all objects with identical primitive-valued keys
    if all(isinstance(v, dict) for v in arr):
        key_sets = [frozenset(v.keys()) for v in arr]
        if len(set(key_sets)) == 1:
            fields = list(arr[0].keys())
            only_prim = all(
                v is None or isinstance(v, (bool, int, float, str))
                for row in arr
                for v in row.values()
            )
            if only_prim:
                field_header = "{" + ",".join(fields) + "}"
                ip = " " * (indent + 2)
                out.append(f"{pad}{key_tok}[{n}]{field_header}:")
                for row in arr:
                    out.append(
                        ip + ",".join(_toon_prim(row[f]) for f in fields),
                    )
                return

    # Non-uniform / mixed → list format
    out.append(f"{pad}{key_tok}[{n}]:")
    for item in arr:
        _toon_encode_list_item(item, indent + 2, out)


def _toon_encode_list_item(
    item: Any,
    indent: int,
    out: list[str],
) -> None:
    """Emit a single TOON list item prefixed with ``- ``."""
    pad = " " * indent
    if item is None or isinstance(item, (bool, int, float, str)):
        out.append(f"{pad}- {_toon_prim(item)}")
    elif isinstance(item, list):
        n = len(item)
        tokens = [_toon_prim(v) for v in item]
        if all(not t.startswith('"') for t in tokens):
            out.append(f'{pad}- [{n}]: {",".join(tokens)}')
        else:
            ip = " " * (indent + 2)
            out.append(f"{pad}- [{n}]:")
            for t in tokens:
                out.append(f"{ip}  {t}")
    elif isinstance(item, dict):
        if not item:
            out.append(f"{pad}-")
            return
        sub: list[str] = []
        _toon_encode_fields(item, indent + 4, sub)
        if sub:
            out.append(f"{pad}- {sub[0].lstrip()}")
            for line in sub[1:]:
                out.append(line)


def to_toon(data: Any) -> str:
    """Serialise *data* to Token-Oriented Object Notation (TOON).

    Format specification: https://toonformat.dev/guide/format-overview
    """
    out: list[str] = []
    if isinstance(data, dict):
        _toon_encode_fields(data, indent=0, out=out)
    elif isinstance(data, list):
        _toon_encode_array("", data, indent=0, out=out)
    else:
        out.append(_toon_prim(data))
    return "\n".join(out) + "\n" if out else ""
