"""Tests for tracker.utils — sanitization, escapes, frontmatter, extra fields."""

from __future__ import annotations

import pytest

from tracker.exceptions import ValidationError
from tracker.utils import (
    build_frontmatter_text,
    decode_escape_sequences,
    now_date,
    now_timestamp,
    parse_extra_fields,
    sanitize_author,
)


# ── sanitize_author ──────────────────────────────────────────────────────────


class TestSanitizeAuthor:
    @pytest.mark.parametrize(
        "raw, expected",
        [
            ("John Doe", "John-Doe"),
            ("  alice  ", "alice"),
            ("bob_smith", "bob_smith"),
            ("a@b!c#d", "a-b-c-d"),
            ("", "unknown"),
            ("   ", "unknown"),
            ("---", "unknown"),
        ],
    )
    def test_sanitize(self, raw: str, expected: str) -> None:
        assert sanitize_author(raw) == expected


# ── decode_escape_sequences ──────────────────────────────────────────────────


class TestDecodeEscapeSequences:
    @pytest.mark.parametrize(
        "raw, expected",
        [
            ("hello\\nworld", "hello\nworld"),
            ("line1\\r\\nline2", "line1\nline2"),
            ("tab\\there", "tab\there"),
            ("no escapes", "no escapes"),
        ],
    )
    def test_decode(self, raw: str, expected: str) -> None:
        assert decode_escape_sequences(raw) == expected


# ── now_date / now_timestamp ─────────────────────────────────────────────────


class TestTimestamps:
    def test_now_date_format(self) -> None:
        d = now_date()
        assert len(d) == 10
        assert d[4] == "-" and d[7] == "-"

    def test_now_timestamp_format(self) -> None:
        ts = now_timestamp()
        assert "T" in ts
        assert len(ts) == 19


# ── build_frontmatter_text ───────────────────────────────────────────────────


class TestBuildFrontmatter:
    def test_basic(self) -> None:
        fields = {"title": "Hello", "status": "New", "priority": "High"}
        ordered = ["title", "status", "priority"]
        text = build_frontmatter_text(fields, ordered)
        assert "title: Hello" in text
        assert "status: New" in text
        assert "priority: High" in text

    def test_respects_order(self) -> None:
        fields = {"b": "2", "a": "1", "c": "3"}
        text = build_frontmatter_text(fields, ["a", "b", "c"])
        lines = text.strip().splitlines()
        assert lines[0].startswith("a:")
        assert lines[1].startswith("b:")
        assert lines[2].startswith("c:")

    def test_skips_missing_keys(self) -> None:
        fields = {"a": "1"}
        text = build_frontmatter_text(fields, ["a", "b"])
        assert "b:" not in text

    def test_bool_lowercase(self) -> None:
        text = build_frontmatter_text({"flag": True}, ["flag"])
        assert "flag: true" in text

    def test_int_no_quotes(self) -> None:
        text = build_frontmatter_text({"count": 42}, ["count"])
        assert "count: 42" in text

    def test_string_with_colon_quoted(self) -> None:
        text = build_frontmatter_text({"k": "a: b"}, ["k"])
        assert "k:" in text
        # Value should be quoted to prevent YAML misparse
        assert "a: b" in text


# ── parse_extra_fields ───────────────────────────────────────────────────────


class TestParseExtraFields:
    def test_basic_kv(self) -> None:
        result = parse_extra_fields(["foo=bar", "baz=qux"])
        assert result == {"foo": "bar", "baz": "qux"}

    def test_none_returns_empty(self) -> None:
        assert parse_extra_fields(None) == {}

    def test_empty_returns_empty(self) -> None:
        assert parse_extra_fields([]) == {}

    def test_missing_equals_raises(self) -> None:
        with pytest.raises(ValidationError, match="Expected format"):
            parse_extra_fields(["no_equals"])

    def test_empty_key_raises(self) -> None:
        with pytest.raises(ValidationError, match="cannot be empty"):
            parse_extra_fields(["=value"])
