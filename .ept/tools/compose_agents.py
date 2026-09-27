#!/usr/bin/env python3
"""Compose complete agent definitions from centralized skills and agent sources."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[2]
SOURCES_ROOT = ROOT / ".ept" / "resources" / "agent_sources"
INLINE_SKILLS_ROOT = ROOT / ".ept" / "resources" / "skills"
REFERENCE_SKILLS_ROOT = ROOT / ".ept" / "skills"
AGENT_MODELS_PATH = SOURCES_ROOT / "agent-models.yaml"
SKILLS_INTRODUCTION_PATH = Path(__file__).with_name("skills_introduction.txt")


def load_skills_introduction() -> str:
    try:
        return SKILLS_INTRODUCTION_PATH.read_text(encoding="utf-8").rstrip("\n")
    except OSError as error:
        raise CompositionError(f"Unable to read skills introduction {SKILLS_INTRODUCTION_PATH}: {error}") from error


class CompositionError(ValueError):
    """Raised when an agent source cannot be rendered safely."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject YAML mappings that declare a key more than once."""


def construct_unique_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise CompositionError(f"Duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_unique_mapping)


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    path: Path
    body: str


@dataclass(frozen=True)
class AgentSource:
    name: str
    description: str
    agent_instructions: str
    copilot: dict[str, Any]
    claude: dict[str, Any]
    codex: dict[str, Any]


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except (OSError, yaml.YAMLError) as error:
        raise CompositionError(f"Unable to read YAML file {path}: {error}") from error
    if not isinstance(value, dict):
        raise CompositionError(f"{path} must contain a YAML mapping")
    return value


def parse_skill(path: Path) -> Skill:
    content = path.read_text(encoding="utf-8").lstrip("\ufeff").replace("\r\n", "\n")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", content, re.DOTALL)
    if not match:
        raise CompositionError(f"{path} must start with YAML front matter")
    try:
        metadata = yaml.load(match.group(1), Loader=UniqueKeyLoader)
    except yaml.YAMLError as error:
        raise CompositionError(f"Invalid front matter in {path}: {error}") from error
    if not isinstance(metadata, dict):
        raise CompositionError(f"{path} front matter must be a mapping")
    name = metadata.get("name")
    description = metadata.get("description")
    if not isinstance(name, str) or not name or not isinstance(description, str) or not description:
        raise CompositionError(f"{path} must define non-empty name and description fields")
    return Skill(name=name, description=description, path=path, body=match.group(2))


def discover_skills(root: Path) -> list[Skill]:
    if not root.is_dir():
        raise CompositionError(f"Skill root does not exist: {root}")
    resolved_root = root.resolve()
    skills = []
    for path in root.glob("**/SKILL.md"):
        if not path.is_file():
            continue
        try:
            path.resolve().relative_to(resolved_root)
        except ValueError as error:
            raise CompositionError(f"Skill path escapes approved root: {path}") from error
        skills.append(parse_skill(path))
    return sorted(skills, key=lambda skill: skill.name)


def load_agent_source(path: Path) -> AgentSource:
    value = load_yaml(path)
    allowed = {"name", "description", "copilot", "claude", "codex", "agent_instructions"}
    unexpected = set(value) - allowed
    missing = allowed - set(value)
    if unexpected or missing:
        raise CompositionError(f"{path} has unknown fields {sorted(unexpected)} or missing fields {sorted(missing)}")
    for field in ("name", "description", "agent_instructions"):
        if not isinstance(value[field], str) or not value[field].strip():
            raise CompositionError(f"{path} field {field} must be a non-empty string")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value["name"]):
        raise CompositionError(f"{path} field name must be lowercase kebab-case")
    if path.name != "parameters.yaml" or path.parent.name != value["name"]:
        raise CompositionError(f"{path} name must match its source directory")
    mappings = {"copilot": {"tools", "user_invocable"}, "claude": {"tools", "permission_mode"}, "codex": set()}
    for harness, allowed_fields in mappings.items():
        config = value[harness]
        if not isinstance(config, dict):
            raise CompositionError(f"{path} field {harness} must be a mapping")
        invalid = set(config) - allowed_fields
        required = allowed_fields - set(config)
        if invalid or required:
            raise CompositionError(f"{path} {harness} has unknown fields {sorted(invalid)} or missing fields {sorted(required)}")
    if not isinstance(value["copilot"]["tools"], list) or not all(isinstance(tool, str) for tool in value["copilot"]["tools"]):
        raise CompositionError(f"{path} copilot.tools must be a list of strings")
    if not isinstance(value["copilot"]["user_invocable"], bool):
        raise CompositionError(f"{path} copilot.user_invocable must be boolean")
    if not isinstance(value["claude"]["tools"], list) or not all(isinstance(tool, str) for tool in value["claude"]["tools"]):
        raise CompositionError(f"{path} claude.tools must be a list of strings")
    if not isinstance(value["claude"]["permission_mode"], str):
        raise CompositionError(f"{path} claude.permission_mode must be a string")
    return AgentSource(
        name=value["name"], description=value["description"], agent_instructions=value["agent_instructions"],
        copilot=value["copilot"], claude=value["claude"], codex=value["codex"],
    )


def dump_agent_source(source: dict[str, Any]) -> str:
    rendered = dict(source)
    instructions = str(rendered.pop("agent_instructions")).rstrip("\n")
    indented_instructions = "\n".join(f"  {line}" if line else "" for line in instructions.splitlines())
    return f"{yaml.safe_dump(rendered, allow_unicode=False, sort_keys=False)}agent_instructions: |-\n{indented_instructions}\n"


def format_agent_source(path: Path) -> None:
    source = load_yaml(path)
    if "agent_instructions" not in source:
        raise CompositionError(f"{path} must define agent_instructions")
    path.write_text(dump_agent_source(source), encoding="utf-8")


def load_agent_models() -> dict[str, str]:
    models = load_yaml(AGENT_MODELS_PATH)
    required_models = {"copilot", "claude", "codex"}
    unexpected = set(models) - required_models
    missing = required_models - set(models)
    if unexpected or missing:
        raise CompositionError(
            f"{AGENT_MODELS_PATH} has unknown model entries {sorted(unexpected)} or missing entries {sorted(missing)}"
        )
    if not all(isinstance(models[harness], str) and models[harness] for harness in required_models):
        raise CompositionError(f"{AGENT_MODELS_PATH} model entries must be non-empty strings")
    return {harness: models[harness] for harness in required_models}


def render_skills(referenced: list[Skill], inline: list[Skill]) -> str:
    names = [skill.name for skill in referenced + inline]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise CompositionError(f"Duplicate skill names: {duplicates}")
    sections = ["<skills>", load_skills_introduction()]
    for skill in referenced:
        relative_path = skill.path.relative_to(ROOT).as_posix()
        sections.append(f"<skill>\n<name>{skill.name}</name>\n<description>{skill.description}</description>\n<file>{relative_path}</file>\n</skill>")
    for skill in inline:
        sections.append(f"<skill>\n<name>{skill.name}</name>\n<description>{skill.description}</description>\n<instructions>\n{skill.body}</instructions>\n</skill>")
    sections.append("</skills>")
    return "\n".join(sections)


def shared_context(skills: str, agent_instructions: str) -> str:
    return f"{skills}\n\n{agent_instructions}"


def render_copilot(source: AgentSource, skills: str) -> str:
    metadata = {
        "name": source.name,
        "description": source.description,
        "tools": format_copilot_tools(source.copilot["tools"]),
        "model": load_agent_models()["copilot"],
        "user-invocable": source.copilot["user_invocable"],
        "generated-from": f".ept/resources/agent_sources/{source.name}/parameters.yaml",
        "generated-by": f"python .ept/tools/compose_agents.py --agent {source.name}",
    }
    return f"---\n{yaml.safe_dump(metadata, sort_keys=False).rstrip()}\n---\n\n{shared_context(skills, source.agent_instructions)}"


def format_copilot_tools(tools: list[str]) -> str:
    return ", ".join(f"'{tool}'" if "*" in tool else tool for tool in tools)


def render_claude(source: AgentSource, skills: str) -> str:
    metadata = {
        "name": source.name,
        "description": source.description,
        "tools": ", ".join(source.claude["tools"]),
        "permissionMode": source.claude["permission_mode"],
        "model": load_agent_models()["claude"],
        "generated-from": f".ept/resources/agent_sources/{source.name}/parameters.yaml",
        "generated-by": f"python .ept/tools/compose_agents.py --agent {source.name}",
    }
    return f"---\n{yaml.safe_dump(metadata, sort_keys=False).rstrip()}\n---\n\n{shared_context(skills, source.agent_instructions)}"


def render_codex(source: AgentSource, skills: str) -> str:
    description = json_string(source.description)
    name = json_string(source.name)
    prompt = shared_context(skills, source.agent_instructions)
    model = json_string(load_agent_models()["codex"])
    return f"# Generated from .ept/resources/agent_sources/{source.name}/parameters.yaml by python .ept/tools/compose_agents.py --agent {source.name}\nname = {name}\ndescription = {description}\nmodel = {model}\ndeveloper_instructions = {toml_multiline_string(prompt)}\n"


def json_string(value: str) -> str:
    return json.dumps(value)


def toml_multiline_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"""', '\\"""')
    return f'"""\n{escaped}"""'


def output_paths(name: str) -> dict[str, Path]:
    return {
        "copilot": ROOT / ".github" / "agents" / f"{name}.agent.md",
        "claude": ROOT / ".claude" / "agents" / f"{name}.md",
        "codex": ROOT / ".codex" / "agents" / f"{name}.toml",
    }


def write_outputs(outputs: dict[Path, str]) -> list[Path]:
    """Stage every output, then replace them together or restore prior contents."""
    original = {path: path.read_bytes() if path.is_file() else None for path in outputs}
    staged: dict[Path, Path] = {}
    replaced: list[Path] = []
    try:
        for path, content in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as temporary:
                temporary.write(content)
                staged[path] = Path(temporary.name)
        for path, temporary_path in staged.items():
            os.replace(temporary_path, path)
            replaced.append(path)
    except OSError as error:
        for path in reversed(replaced):
            original_content = original[path]
            if original_content is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(original_content)
        raise CompositionError(f"Unable to write generated definitions atomically: {error}") from error
    finally:
        for temporary_path in staged.values():
            temporary_path.unlink(missing_ok=True)
    return list(outputs)


def compose(source_path: Path) -> dict[Path, str]:
    source = load_agent_source(source_path)
    skills = render_skills(discover_skills(REFERENCE_SKILLS_ROOT), discover_skills(INLINE_SKILLS_ROOT))
    return {
        output_paths(source.name)["copilot"]: render_copilot(source, skills),
        output_paths(source.name)["claude"]: render_claude(source, skills),
        output_paths(source.name)["codex"]: render_codex(source, skills),
    }


def migrate(agent_name: str) -> None:
    source_dir = SOURCES_ROOT / agent_name
    source_dir.mkdir(parents=True, exist_ok=True)
    target = source_dir / "parameters.yaml"
    if target.exists() and target.read_text(encoding="utf-8").strip():
        raise CompositionError(f"Migration target already exists: {target}")
    legacy = ROOT / ".ept" / "agents" / f"{agent_name}.md"
    copilot = ROOT / ".github" / "agents" / f"{agent_name}.agent.md"
    if not legacy.is_file() or not copilot.is_file():
        raise CompositionError(f"Missing legacy agent or Copilot definition for {agent_name}")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---", copilot.read_text(encoding="utf-8").lstrip("\ufeff"), re.DOTALL)
    header = match.group(1) if match else ""
    try:
        metadata = yaml.safe_load(header)
    except yaml.YAMLError:
        metadata = {
            key: value.strip()
            for key, value in re.findall(r"^(name|description|tools|user-invocable):\s*(.*)$", header, re.MULTILINE)
        }
    tools = metadata.get("tools") if isinstance(metadata, dict) else None
    if isinstance(tools, str):
        tools = [tool.strip() for tool in tools.split(",") if tool.strip()]
    if not isinstance(metadata, dict) or not isinstance(metadata.get("description"), str) or not isinstance(tools, list):
        raise CompositionError(f"Invalid Copilot front matter for {agent_name}")
    user_invocable = metadata.get("user-invocable", True)
    if isinstance(user_invocable, str) and user_invocable.lower() in {"true", "false"}:
        user_invocable = user_invocable.lower() == "true"
    if not isinstance(user_invocable, bool):
        raise CompositionError(f"Invalid user-invocable value for {agent_name}")
    source = {
        "name": agent_name,
        "description": metadata["description"],
        "copilot": {"tools": tools, "user_invocable": user_invocable},
        "claude": {"tools": ["Read", "Glob", "Grep", "Edit", "Bash", "Agent"], "permission_mode": "bypassPermissions"},
        "codex": {},
        "agent_instructions": legacy.read_text(encoding="utf-8").rstrip("\n"),
    }
    target.write_text(dump_agent_source(source), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render complete Copilot, Claude, and Codex agent definitions from centralized sources.",
        epilog="Use --all to regenerate every agent source below .ept/resources/agent_sources.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--agent", metavar="NAME", help="render all harness definitions for one named agent source")
    group.add_argument("--all", action="store_true", help="regenerate all defined agent sources")
    parser.add_argument("--check", action="store_true", help="report stale or missing generated definitions without writing files")
    parser.add_argument("--migrate-existing", action="store_true", help="create source files from existing legacy agent definitions")
    parser.add_argument("--format-sources", action="store_true", help="rewrite source files using readable YAML literal blocks")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        names = [args.agent] if args.agent else sorted(path.name for path in SOURCES_ROOT.iterdir() if path.is_dir())
        if args.migrate_existing:
            for name in names:
                migrate(name)
            return 0
        if args.format_sources:
            for name in names:
                format_agent_source(SOURCES_ROOT / name / "parameters.yaml")
        all_outputs: dict[Path, str] = {}
        for name in names:
            all_outputs.update(compose(SOURCES_ROOT / name / "parameters.yaml"))
        outdated = {path: content for path, content in all_outputs.items() if not path.is_file() or path.read_text(encoding="utf-8") != content}
        if args.check:
            for path in outdated:
                print(f"Outdated generated definition: {path.relative_to(ROOT)}")
            return 1 if outdated else 0
        if outdated:
            for path in write_outputs(outdated):
                print(f"Wrote {path.relative_to(ROOT)}")
        return 0
    except CompositionError as error:
        print(f"composition error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
