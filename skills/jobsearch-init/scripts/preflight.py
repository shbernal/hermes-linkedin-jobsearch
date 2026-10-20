#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""The check every jobsearch skill runs first: the workspace exists at the schema the skills expect,
the profile's config matches this release (sync-config.py --check), and atsfill can't send while
`autonomy.external_forms` is off.

Prints JSON with `problems`, each with a `fix`, and exits 1 when there is any.
"""

import json
import os
import platform
import subprocess
import sys
import tomllib
from pathlib import Path

import yaml

SCHEMA_VERSION = 1
WORKSPACE = Path.home() / "jobsearch"
SYNC = Path(__file__).resolve().parent / "sync-config.py"


def load_workspace() -> tuple[dict, list[dict]]:
    path = WORKSPACE / "workspace.yaml"
    if not path.exists():
        return {}, [{"problem": f"{path} is missing", "fix": "run /jobsearch-init"}]
    try:
        workspace = yaml.safe_load(path.read_text()) or {}
    except yaml.YAMLError as e:
        return {}, [{"problem": f"{path} doesn't parse: {e}", "fix": "repair the file"}]
    if (version := workspace.get("schema_version")) != SCHEMA_VERSION:
        return workspace, [{"problem": f"schema_version is {version}, the skills expect {SCHEMA_VERSION}", "fix": "run /jobsearch-init"}]
    return workspace, []


def config_problems() -> list[dict]:
    run = subprocess.run(["uv", "run", "-q", str(SYNC), "--check"], capture_output=True, text=True)
    try:
        report = json.loads(run.stdout)
    except json.JSONDecodeError:
        return [{"problem": f"sync-config.py --check failed: {run.stderr.strip()}", "fix": "tell the user"}]
    return [{"problem": m, "fix": f"uv run {SYNC}"} for m in report["mismatches"]]


def atsfill_config() -> Path:
    """atsfill's own config path (atsfill core/paths.py)."""
    if xdg := os.environ.get("XDG_CONFIG_HOME"):
        return Path(xdg) / "atsfill/config.toml"
    return Path.home() / (".config/atsfill/config.toml" if platform.system() == "Linux" else ".atsfill/config.toml")


def atsfill_problems(workspace: dict) -> list[dict]:
    if ((workspace.get("autonomy") or {}).get("external_forms") or "off") != "off":
        return []
    path = atsfill_config()
    if not path.exists():
        return []
    try:
        submit = tomllib.loads(path.read_text()).get("submit")
    except tomllib.TOMLDecodeError as e:
        return [{"problem": f"{path} doesn't parse: {e}", "fix": "tell the user"}]
    if not submit:
        return []
    return [{
        "problem": f"{path} lets atsfill send to {submit} while autonomy.external_forms is off",
        "fix": "tell the user: empty the submit list, or opt in to external sending in workspace.yaml",
    }]


def main() -> int:
    workspace, problems = load_workspace()
    problems += config_problems() + atsfill_problems(workspace)
    print(json.dumps({"workspace": str(WORKSPACE), "problems": problems}, indent=2))
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
