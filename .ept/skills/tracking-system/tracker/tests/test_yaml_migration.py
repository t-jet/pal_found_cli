"""Parametrised tests that verify the automatic_transitions YAML migration.

Operates purely on YAML file parsing; does NOT initialise the tracker runtime.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

# Path to the ticket YAML files relative to this test file
# test file is at: .ept/skills/tracking-system/tracker/tests/
# tickets dir is: .ept/tracker/.config/tickets/
TICKETS_DIR = (
    Path(__file__).resolve()
    .parent   # tests/
    .parent   # tracker/
    .parent   # tracking-system/
    .parent   # skills/
    .parent   # .ept/
    / "tracker" / ".config" / "tickets"
)

KNOWN_RULE_TYPES = {
    "all_children_reach_status",
    "first_child_reaches_status",
    "linked_ticket_reaches_status",
    "child_blocker_created",
    "all_blockers_cleared",
    "this_ticket_reaches_status",
}

# Files that must have at least one all_blockers_cleared (AT-5) rule
AT5_FILES = {
    "question.yaml",
    "codereview.yaml",
    "epic.yaml",
    "feature.yaml",
    "dev_story.yaml",
    "development.yaml",
    "devops.yaml",
    "design.yaml",
    "unittest.yaml",
    "testcase.yaml",
    "testexec.yaml",
    "bug_subtask.yaml",
    "workitem.yaml",
    "task.yaml",
    "resource_req.yaml",
    "ba_subtask_analysis.yaml",
    "ba_subtask_design.yaml",
    "sa_subtask_analysis.yaml",
    "sa_subtask_design.yaml",
    "ux_subtask_analysis.yaml",
    "ux_subtask_design.yaml",
}

# Files that must have at least one child_blocker_created (AT-4) rule
AT4_FILES = AT5_FILES  # same set

ALL_YAML_FILES = sorted(TICKETS_DIR.glob("*.yaml"))


def _load(filename: str) -> dict:
    path = TICKETS_DIR / filename
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# ── Parametrised: all 22 files ───────────────────────────────────────────────


@pytest.mark.parametrize("yaml_file", [f.name for f in ALL_YAML_FILES])
def test_automatic_transitions_is_list(yaml_file: str):
    data = _load(yaml_file)
    at = data.get("automatic_transitions")
    assert isinstance(at, list), (
        f"{yaml_file}: automatic_transitions must be a list, got {type(at)}"
    )


@pytest.mark.parametrize("yaml_file", [f.name for f in ALL_YAML_FILES])
def test_all_rules_have_known_rule_key(yaml_file: str):
    data = _load(yaml_file)
    for i, rule in enumerate(data.get("automatic_transitions", [])):
        assert isinstance(rule, dict), f"{yaml_file} rule[{i}] must be a dict"
        rt = rule.get("rule")
        assert rt is not None, f"{yaml_file} rule[{i}] missing 'rule' key"
        assert rt in KNOWN_RULE_TYPES, (
            f"{yaml_file} rule[{i}] has unknown rule type '{rt}'"
        )


# ── AT-5 assertions ──────────────────────────────────────────────────────────


@pytest.mark.parametrize("yaml_file", sorted(AT5_FILES))
def test_at5_rule_present(yaml_file: str):
    data = _load(yaml_file)
    rules = data.get("automatic_transitions", [])
    at5_rules = [r for r in rules if r.get("rule") == "all_blockers_cleared"]
    assert len(at5_rules) >= 1, f"{yaml_file}: expected at least one all_blockers_cleared rule"


# ── AT-4 assertions ──────────────────────────────────────────────────────────


@pytest.mark.parametrize("yaml_file", sorted(AT4_FILES))
def test_at4_rule_present(yaml_file: str):
    data = _load(yaml_file)
    rules = data.get("automatic_transitions", [])
    at4_rules = [r for r in rules if r.get("rule") == "child_blocker_created"]
    assert len(at4_rules) >= 1, f"{yaml_file}: expected at least one child_blocker_created rule"


# ── codereview.yaml specific ─────────────────────────────────────────────────


def test_codereview_has_linked_ticket_reaches_status_with_development():
    data = _load("codereview.yaml")
    rules = data.get("automatic_transitions", [])
    matching = [
        r for r in rules
        if r.get("rule") == "linked_ticket_reaches_status"
        and "development" in (r.get("linked_ticket_types") or [])
    ]
    assert len(matching) >= 1, (
        "codereview.yaml: expected linked_ticket_reaches_status rule with "
        "linked_ticket_types containing 'development'"
    )


# ── epic.yaml specific ───────────────────────────────────────────────────────


def test_epic_has_one_first_child_reaches_status():
    data = _load("epic.yaml")
    rules = data.get("automatic_transitions", [])
    count = sum(1 for r in rules if r.get("rule") == "first_child_reaches_status")
    assert count == 1, f"epic.yaml: expected exactly 1 first_child_reaches_status, found {count}"


def test_epic_has_two_all_children_reach_status():
    data = _load("epic.yaml")
    rules = data.get("automatic_transitions", [])
    count = sum(1 for r in rules if r.get("rule") == "all_children_reach_status")
    assert count == 2, f"epic.yaml: expected exactly 2 all_children_reach_status, found {count}"


# ── dev_story.yaml specific ──────────────────────────────────────────────────


def test_dev_story_has_three_all_children_reach_status():
    data = _load("dev_story.yaml")
    rules = data.get("automatic_transitions", [])
    at1_rules = [r for r in rules if r.get("rule") == "all_children_reach_status"]
    assert len(at1_rules) == 3, (
        f"dev_story.yaml: expected 3 all_children_reach_status rules, found {len(at1_rules)}"
    )
    source_statuses = {r.get("source_status") for r in at1_rules}
    assert "Development" in source_statuses, "dev_story.yaml: missing Development source_status"
    assert "QA" in source_statuses, "dev_story.yaml: missing QA source_status"
    assert "Deployment" in source_statuses, "dev_story.yaml: missing Deployment source_status"


# ── bug.yaml specific ────────────────────────────────────────────────────────


def test_bug_yaml_automatic_transitions_is_empty():
    data = _load("bug.yaml")
    at = data.get("automatic_transitions", [])
    assert at == [], f"bug.yaml: automatic_transitions must be [], got {at}"
