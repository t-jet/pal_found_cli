"""Tests for centralized agent-definition composition."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tomllib

import pytest
import yaml  # type: ignore[import-untyped]


SCRIPT = Path(__file__).parent.parent / ".ept" / "tools" / "compose_agents.py"
SPEC = importlib.util.spec_from_file_location("compose_agents", SCRIPT)
assert SPEC and SPEC.loader
composer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = composer
SPEC.loader.exec_module(composer)


def write_skill(root: Path, name: str, description: str) -> None:
    path = root / name / "SKILL.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        f'---\nname: {name}\ndescription: "{description}"\n---\n# {name}\n',
        encoding="utf-8",
    )


def write_source(root: Path) -> Path:
    source = root / "architect" / "parameters.yaml"
    source.parent.mkdir(parents=True)
    source.write_text(
        """name: architect
description: Architecture agent
copilot:
  tools: [read]
  user_invocable: true
claude:
  tools: [Read]
  permission_mode: default
codex: {}
agent_instructions: |
  Preserve this instruction.
""",
        encoding="utf-8",
    )
    return source


def test_compose_discovers_and_orders_all_skills(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    references = tmp_path / "references"
    inline = tmp_path / "inline"
    write_skill(references, "zebra", "Referenced zebra")
    write_skill(references, "alpha", "Referenced alpha")
    write_skill(inline, "writer", "Inline writer")
    write_skill(inline, "beta", "Inline beta")
    monkeypatch.setattr(composer, "REFERENCE_SKILLS_ROOT", references)
    monkeypatch.setattr(composer, "INLINE_SKILLS_ROOT", inline)
    monkeypatch.setattr(composer, "ROOT", tmp_path)

    rendered = composer.render_skills(composer.discover_skills(references), composer.discover_skills(inline))

    assert rendered.index("<name>alpha</name>") < rendered.index("<name>zebra</name>")
    assert rendered.index("<name>zebra</name>") < rendered.index("<name>beta</name>")
    assert rendered.index("<name>beta</name>") < rendered.index("<name>writer</name>")
    assert "<file>references/alpha/SKILL.md</file>" in rendered
    assert "<instructions>\n# beta\n</instructions>" in rendered


def test_render_skills_loads_introduction_from_sibling_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    introduction = tmp_path / "skills_introduction.txt"
    introduction.write_text("File-backed introduction.\n", encoding="utf-8")
    monkeypatch.setattr(composer, "SKILLS_INTRODUCTION_PATH", introduction)

    assert composer.render_skills([], []) == "<skills>\nFile-backed introduction.\n</skills>"


def test_help_describes_all_regeneration_and_other_options() -> None:
    help_text = composer.build_parser().format_help()

    assert "--help" in help_text
    assert "--all" in help_text
    assert "regenerate all defined agent sources" in help_text
    assert "--check" in help_text
    assert "--migrate-existing" in help_text
    assert "--format-sources" in help_text


def test_compose_writes_three_harnesses_with_fixed_models(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    references = tmp_path / "references"
    inline = tmp_path / "inline"
    write_skill(references, "reference", "Referenced")
    write_skill(inline, "inline", "Inline")
    source_path = write_source(tmp_path / "sources")
    monkeypatch.setattr(composer, "REFERENCE_SKILLS_ROOT", references)
    monkeypatch.setattr(composer, "INLINE_SKILLS_ROOT", inline)
    monkeypatch.setattr(composer, "ROOT", tmp_path)
    monkeypatch.setattr(composer, "load_agent_models", lambda: {"copilot": "copilot-model", "claude": "claude-model", "codex": "codex-model"})

    outputs = composer.compose(source_path)

    assert len(outputs) == 3
    by_name = {path.name: content for path, content in outputs.items()}
    assert 'model: copilot-model' in by_name["architect.agent.md"]
    assert 'model: claude-model' in by_name["architect.md"]
    assert 'model = "codex-model"' in by_name["architect.toml"]
    assert all("Preserve this instruction." in content for content in outputs.values())
    assert tomllib.loads(by_name["architect.toml"])["developer_instructions"]
    assert all("generated-from:" in content or content.startswith("# Generated from") for content in outputs.values())


def test_render_copilot_uses_comma_separated_tools_and_single_quoted_wildcards(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = composer.AgentSource(
        "agent", "desc", "instructions", {"tools": ["read", "github/*", "search"], "user_invocable": True},
        {"tools": [], "permission_mode": "default"}, {},
    )
    monkeypatch.setattr(composer, "load_agent_models", lambda: {"copilot": "copilot-model", "claude": "claude-model", "codex": "codex-model"})

    rendered = composer.render_copilot(source, "<skills></skills>")

    assert "tools: read, 'github/*', search" in rendered
    assert "tools:\n" not in rendered
    assert "'''github/*'''" not in rendered


def test_render_codex_uses_multiline_string_and_escapes_delimiters(monkeypatch: pytest.MonkeyPatch) -> None:
    source = composer.AgentSource("agent", "desc", 'Use `\\` and """.', {"tools": [], "user_invocable": True}, {"tools": [], "permission_mode": "default"}, {})
    monkeypatch.setattr(composer, "load_agent_models", lambda: {"copilot": "copilot-model", "claude": "claude-model", "codex": "codex-model"})

    rendered = composer.render_codex(source, "<skills></skills>")

    assert 'developer_instructions = """\n' in rendered
    assert "\\\"\"\"" in rendered
    assert tomllib.loads(rendered)["developer_instructions"].endswith('Use `\\` and """.')


@pytest.mark.parametrize("agent_instructions", ("Instruction without newline.", "Instruction with newline.\n"))
def test_rendered_shared_context_is_identical_across_harnesses(
    monkeypatch: pytest.MonkeyPatch, agent_instructions: str
) -> None:
    source = composer.AgentSource(
        "agent", "desc", agent_instructions,
        {"tools": [], "user_invocable": True},
        {"tools": [], "permission_mode": "default"},
        {},
    )
    skills = "<skills></skills>"
    monkeypatch.setattr(composer, "load_agent_models", lambda: {"copilot": "copilot-model", "claude": "claude-model", "codex": "codex-model"})

    copilot = composer.render_copilot(source, skills).split("---\n", 2)[2].removeprefix("\n")
    claude = composer.render_claude(source, skills).split("---\n", 2)[2].removeprefix("\n")
    codex = tomllib.loads(composer.render_codex(source, skills))["developer_instructions"]

    expected = f"{skills}\n\n{agent_instructions}"
    assert copilot == expected
    assert claude == expected
    assert codex == expected


def test_skill_discovery_rejects_path_outside_root(tmp_path: Path) -> None:
    root = tmp_path / "skills"
    external = tmp_path / "external" / "SKILL.md"
    external.parent.mkdir(parents=True)
    external.write_text("---\nname: external\ndescription: external\n---\n", encoding="utf-8")
    root.mkdir()
    (root / "SKILL.md").symlink_to(external)

    with pytest.raises(composer.CompositionError, match="escapes approved root"):
        composer.discover_skills(root)


def test_agent_source_rejects_invalid_or_mismatched_name(tmp_path: Path) -> None:
    path = tmp_path / "other" / "parameters.yaml"
    path.parent.mkdir()
    path.write_text("name: ../bad\ndescription: bad\ncopilot: {tools: [], user_invocable: true}\nclaude: {tools: [], permission_mode: default}\ncodex: {}\nagent_instructions: bad\n", encoding="utf-8")

    with pytest.raises(composer.CompositionError, match="lowercase kebab-case"):
        composer.load_agent_source(path)


def test_load_agent_models_rejects_duplicate_model_keys(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    models = tmp_path / "agent-models.yaml"
    models.write_text("copilot: one\ncopilot: two\nclaude: inherit\ncodex: gpt-5.6\n", encoding="utf-8")
    monkeypatch.setattr(composer, "AGENT_MODELS_PATH", models)

    with pytest.raises(composer.CompositionError, match="Duplicate YAML key"):
        composer.load_agent_models()


def test_load_agent_models_reads_all_harness_models(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    models = tmp_path / "agent-models.yaml"
    models.write_text("copilot: local-model\nclaude: inherited-model\ncodex: codex-model\n", encoding="utf-8")
    monkeypatch.setattr(composer, "AGENT_MODELS_PATH", models)

    assert composer.load_agent_models() == {"copilot": "local-model", "claude": "inherited-model", "codex": "codex-model"}


def test_skill_and_instruction_trailing_newlines_are_preserved(tmp_path: Path) -> None:
    skill = tmp_path / "SKILL.md"
    skill.write_text("---\nname: skill\ndescription: desc\n---\nbody\n\n", encoding="utf-8")
    source = tmp_path / "architect" / "parameters.yaml"
    source.parent.mkdir()
    source.write_text("name: architect\ndescription: desc\ncopilot: {tools: [], user_invocable: true}\nclaude: {tools: [], permission_mode: default}\ncodex: {}\nagent_instructions: |+\n  instruction\n\n", encoding="utf-8")

    assert composer.parse_skill(skill).body == "body\n\n"
    assert composer.load_agent_source(source).agent_instructions == "instruction\n\n"


def test_write_outputs_restores_files_when_a_replacement_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    first = tmp_path / "first.md"
    second = tmp_path / "second.md"
    first.write_text("old first", encoding="utf-8")
    second.write_text("old second", encoding="utf-8")
    real_replace = composer.os.replace
    calls = 0

    def fail_second_replace(source: Path, destination: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("simulated replacement failure")
        real_replace(source, destination)

    monkeypatch.setattr(composer.os, "replace", fail_second_replace)

    with pytest.raises(composer.CompositionError, match="atomically"):
        composer.write_outputs({first: "new first", second: "new second"})

    assert first.read_text(encoding="utf-8") == "old first"
    assert second.read_text(encoding="utf-8") == "old second"


def test_agent_source_rejects_missing_mandatory_harness(tmp_path: Path) -> None:
    path = tmp_path / "parameters.yaml"
    path.write_text("name: bad\ndescription: bad\nagent_instructions: bad\ncopilot: {}\nclaude: {}\n", encoding="utf-8")

    with pytest.raises(composer.CompositionError, match="missing fields"):
        composer.load_agent_source(path)


def test_dump_agent_source_uses_literal_block_for_instructions() -> None:
    rendered = composer.dump_agent_source({"name": "agent", "agent_instructions": "First line\nSecond line"})

    assert "agent_instructions: |-\n  First line\n  Second line\n" in rendered


def test_format_agent_source_round_trips_and_requires_instructions(tmp_path: Path) -> None:
    source_path = write_source(tmp_path / "sources")

    composer.format_agent_source(source_path)

    assert "agent_instructions: |-\n  Preserve this instruction.\n" in source_path.read_text(encoding="utf-8")
    assert composer.load_agent_source(source_path).agent_instructions == "Preserve this instruction."

    missing_instructions = tmp_path / "missing" / "parameters.yaml"
    missing_instructions.parent.mkdir()
    missing_instructions.write_text("name: agent\n", encoding="utf-8")

    with pytest.raises(composer.CompositionError, match="must define agent_instructions"):
        composer.format_agent_source(missing_instructions)


def test_migrate_falls_back_to_legacy_header_and_converts_boolean(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    legacy = tmp_path / ".ept" / "agents" / "specialist.md"
    copilot = tmp_path / ".github" / "agents" / "specialist.agent.md"
    legacy.parent.mkdir(parents=True)
    copilot.parent.mkdir(parents=True)
    legacy.write_text("Legacy instructions.\n", encoding="utf-8")
    copilot.write_text(
        "---\nname: specialist\ndescription: Migrated agent\ntools: read, search\nuser-invocable: false\nbroken: [\n---\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(composer, "ROOT", tmp_path)
    monkeypatch.setattr(composer, "SOURCES_ROOT", tmp_path / ".ept" / "resources" / "agent_sources")

    composer.migrate("specialist")

    source = composer.load_agent_source(composer.SOURCES_ROOT / "specialist" / "parameters.yaml")
    assert source.description == "Migrated agent"
    assert source.copilot == {"tools": ["read", "search"], "user_invocable": False}
    assert source.agent_instructions == "Legacy instructions."


@pytest.mark.parametrize(
    "agent_name",
    ("architect", "ba", "tech-lead", "python-developer", "qa-engineer", "devops-engineer"),
)
def test_migrated_agent_instructions_preserve_legacy_bodies(agent_name: str) -> None:
    root = SCRIPT.parent.parent.parent
    source_path = root / ".ept" / "resources" / "agent_sources" / agent_name / "parameters.yaml"
    legacy_path = root / ".ept" / "agents" / f"{agent_name}.md"

    source = yaml.safe_load(source_path.read_text(encoding="utf-8"))

    assert source["agent_instructions"] == legacy_path.read_text(encoding="utf-8").rstrip("\n")
