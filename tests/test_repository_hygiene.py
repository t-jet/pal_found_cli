"""Regression checks for local credential ignore rules."""

from pathlib import Path
import subprocess
import sys
import tomllib


ROOT = Path(__file__).parent.parent
IGNORED_CREDENTIAL_PATHS = (
    ".env",
    ".env.local",
    ".env.production",
    "qa-private-key.pem",
    "qa-private.key",
    "qa-certificate.p12",
    "qa-certificate.pfx",
)
TRACKABLE_ENV_PATHS = (".env.example", ".env.template")


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ("git", "-C", str(ROOT), *args),
        check=False,
        capture_output=True,
        text=True,
    )


def test_local_credential_paths_are_ignored() -> None:
    for path in IGNORED_CREDENTIAL_PATHS:
        result = _git("check-ignore", "--quiet", "--", path)
        assert result.returncode == 0, f"expected {path} to be ignored: {result.stderr}"


def test_placeholder_environment_files_remain_trackable() -> None:
    for path in TRACKABLE_ENV_PATHS:
        result = _git("check-ignore", "--quiet", "--", path)
        assert result.returncode == 1, f"expected {path} to remain trackable"


def test_no_live_credential_pattern_is_tracked() -> None:
    result = _git("ls-files")
    assert result.returncode == 0, result.stderr

    unsafe = []
    for tracked_path in result.stdout.splitlines():
        name = Path(tracked_path).name
        is_live_env = name == ".env" or (
            name.startswith(".env.") and name not in TRACKABLE_ENV_PATHS
        )
        if is_live_env or Path(name).suffix.lower() in {".pem", ".key", ".p12", ".pfx"}:
            unsafe.append(tracked_path)

    assert not unsafe, f"tracked credential-pattern files: {unsafe}"


def test_generated_agent_definitions_are_current() -> None:
    result = subprocess.run(
        (sys.executable, ".ept/tools/compose_agents.py", "--all", "--check"),
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_generated_codex_definitions_are_valid_toml() -> None:
    for path in (ROOT / ".codex" / "agents").glob("*.toml"):
        tomllib.loads(path.read_text(encoding="utf-8"))
