"""Tests for tracker.formatters — display formatting and TOON encoder."""

from __future__ import annotations

import pytest

from tracker.formatters import (
    format_link,
    format_ticket,
    to_toon,
)


# ── format_ticket / format_link ──────────────────────────────────────────────


class TestDisplayFormatters:
    def test_format_ticket(self) -> None:
        ticket = {
            "id": "TASK-001",
            "status": "New",
            "priority": "High",
            "assignee": "dev",
            "title": "My task",
        }
        line = format_ticket(ticket)
        assert "TASK-001" in line
        assert "New" in line
        assert "High" in line
        assert "dev" in line
        assert "My task" in line

    def test_format_link(self) -> None:
        link = {
            "link_id": "LINK-00001",
            "source_ticket": "TASK-001",
            "target_ticket": "TASK-002",
            "link_type": "Blocks",
            "source_role": "Blocks",
        }
        line = format_link(link)
        assert "LINK-00001" in line
        assert "TASK-001" in line
        assert "->" in line
        assert "TASK-002" in line


# ── TOON encoder ─────────────────────────────────────────────────────────────


class TestToon:
    def test_primitive_string(self) -> None:
        assert to_toon("hello") == "hello\n"

    def test_primitive_int(self) -> None:
        assert to_toon(42) == "42\n"

    def test_primitive_bool(self) -> None:
        assert to_toon(True) == "true\n"

    def test_primitive_none(self) -> None:
        assert to_toon(None) == "null\n"

    def test_flat_dict(self) -> None:
        result = to_toon({"name": "Alice", "age": 30})
        assert "name: Alice" in result
        assert "age: 30" in result

    def test_nested_dict(self) -> None:
        result = to_toon({"outer": {"inner": "value"}})
        assert "outer:" in result
        assert "inner: value" in result

    def test_list_of_primitives(self) -> None:
        result = to_toon({"items": [1, 2, 3]})
        assert "items[3]:" in result

    def test_empty_list(self) -> None:
        result = to_toon({"items": []})
        assert "items[0]:" in result

    def test_list_of_dicts_tabular(self) -> None:
        data = {
            "rows": [
                {"a": 1, "b": 2},
                {"a": 3, "b": 4},
            ]
        }
        result = to_toon(data)
        assert "rows[2]" in result
        assert "{a,b}" in result

    def test_string_quoting_needed(self) -> None:
        result = to_toon({"k": "has:colon"})
        assert '"has:colon"' in result

    def test_string_quoting_true_false(self) -> None:
        result = to_toon({"k": "true"})
        assert '"true"' in result

    def test_string_quoting_numeric(self) -> None:
        result = to_toon({"k": "42"})
        assert '"42"' in result

    def test_string_no_quoting(self) -> None:
        result = to_toon({"k": "simple"})
        assert "k: simple" in result

    def test_list_of_quoted_strings(self) -> None:
        result = to_toon({"items": ["has:colon", "normal"]})
        # Should use expanded list since some items need quoting
        assert "items[2]:" in result

    def test_dict_in_list(self) -> None:
        result = to_toon({"items": [{"x": 1}, {"x": 2}]})
        assert "items[2]" in result

    def test_top_level_list(self) -> None:
        result = to_toon([1, 2, 3])
        assert "[3]:" in result

    def test_nested_list_in_dict(self) -> None:
        result = to_toon({"a": [{"x": [1, 2]}]})
        assert result  # Should not crash

    def test_empty_string_quoted(self) -> None:
        result = to_toon({"k": ""})
        assert '""' in result

    def test_string_with_newline_quoted(self) -> None:
        result = to_toon({"k": "line1\nline2"})
        assert '"line1\\nline2"' in result
