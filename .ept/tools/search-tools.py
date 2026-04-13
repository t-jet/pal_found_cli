#!/usr/bin/env python3
"""Search the tools index for tools relevant to a free-text description.

Usage:
  search-tools.py <query>         # fuzzy-search and print top-N matches
  search-tools.py --all           # print all tools
  search-tools.py --help          # print this help

Examples:
  search-tools.py "create a ticket"
  search-tools.py "show workflow transitions"
  search-tools.py --all
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path
from typing import Any

import yaml

# ── Configuration ─────────────────────────────────────────────────────────────

# Maximum number of results to display.
TOP_N: int = 5

# Minimum combined score [0.0 – 1.0] for a tool to appear in results.
MIN_SCORE: float = 0.15

# Path to the index file, relative to this script.
_INDEX_PATH: Path = Path(__file__).resolve().parent / ".tools-index.yaml"


# ── Scoring ───────────────────────────────────────────────────────────────────

_STOP_WORDS: frozenset[str] = frozenset(
    {
        # articles / prepositions / conjunctions
        "a", "an", "the", "to", "of", "in", "for", "and", "or", "with",
        "by", "at", "from", "on", "into", "via", "per",
        # pronouns / determiners
        "it", "its", "this", "that", "these", "those", "which", "who",
        "what", "any", "all", "each", "both", "either",
        # verbs (high-frequency, low-signal)
        "is", "are", "be", "been", "was", "were", "do", "does", "did",
        "has", "have", "had", "can", "may", "will", "would", "should",
        "use", "used",
        # negation / modifiers (generic, appear everywhere)
        "not", "no", "nor",
        # other low-signal words
        "as", "if", "then", "when", "where", "so", "also", "only",
        "same", "new", "one", "two", "every", "more"
    }
)


def _tokenize(text: str) -> list[str]:
    """Lower-case, split on non-alphanumeric characters, drop stop-words."""
    raw = re.split(r"[^a-z0-9]+", text.lower())
    return [t for t in raw if t and t not in _STOP_WORDS]


def _score(query: str, tool: dict[str, Any]) -> float:
    """Return a relevance score in [0.0, 1.0] for *tool* against *query*.

    The score is a weighted combination of two signals:

    - **Token recall** (weight 0.7): fraction of query tokens found anywhere in
      the combined description + full_description + path text.  Using recall
      rather than Jaccard means adding more text to a document can only *help*
      the score, never hurt it.
    - **Sequence-match ratio** (weight 0.3): ``difflib`` character-level
      similarity between the query and the *short* description + path only,
      keeping the target string short to avoid length-dilution of the ratio.
    """
    description: str = tool.get("description", "")
    full_description: str = tool.get("full_description", "")
    path: str = tool.get("path", "")

    # Token recall over the full searchable corpus (description + full_description + path)
    full_searchable: str = f"{description} {full_description} {path}"
    q_tokens = set(_tokenize(query))
    d_tokens = set(_tokenize(full_searchable))
    recall: float = len(q_tokens & d_tokens) / len(q_tokens) if q_tokens else 0.0

    # Sequence similarity against the concise description + path only
    short_target: str = f"{description} {path}"
    seq_ratio: float = difflib.SequenceMatcher(
        None, query.lower(), short_target.lower(), autojunk=False
    ).ratio()

    return 0.7 * recall + 0.3 * seq_ratio


# ── Index loading ─────────────────────────────────────────────────────────────


def _load_tools() -> list[dict[str, Any]]:
    """Load and return the tools list from the YAML index."""
    if not _INDEX_PATH.exists():
        print(f"Error: tools index not found at {_INDEX_PATH}", file=sys.stderr)
        sys.exit(1)
    with _INDEX_PATH.open(encoding="utf-8") as fh:
        data: dict[str, Any] = yaml.safe_load(fh) or {}
    tools: list[dict[str, Any]] = data.get("tools", [])
    if not tools:
        print("Error: tools index is empty.", file=sys.stderr)
        sys.exit(1)
    return tools


# ── Output ────────────────────────────────────────────────────────────────────


def _dump(tools: list[dict[str, Any]]) -> None:
    """Print *tools* as a YAML document, omitting the full_description field."""
    output = [
        {k: v for k, v in tool.items() if k != "full_description"}
        for tool in tools
    ]
    print(yaml.dump({"tools": output}, default_flow_style=False, allow_unicode=True, sort_keys=False), end="")


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        prog=Path(__file__).name,
        description="Fuzzy-search the tools index for a free-text action description.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "query",
        nargs="?",
        default=None,
        metavar="QUERY",
        help="Free-text description of the action you want to perform.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="show_all",
        help="Print all available tools and exit.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=TOP_N,
        metavar="N",
        help=f"Maximum number of results to show (default: {TOP_N}).",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=MIN_SCORE,
        metavar="SCORE",
        help=f"Minimum relevance score 0..1 (default: {MIN_SCORE}).",
    )

    args = parser.parse_args()

    tools = _load_tools()

    if args.show_all:
        _dump(tools)
        return 0

    if not args.query:
        parser.print_help()
        return 0

    scored: list[tuple[float, dict[str, Any]]] = [
        (_score(args.query, tool), tool) for tool in tools
    ]
    scored.sort(key=lambda x: x[0], reverse=True)

    results = [
        tool for score, tool in scored[: args.top] if score >= args.min_score
    ]

    if not results:
        print("No relevant tools found.")
        return 0

    _dump(results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
