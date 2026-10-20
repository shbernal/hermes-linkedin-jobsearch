#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""The check every jobsearch skill runs first: the workspace exists at the schema the skills expect,
and the profile's config matches this release (sync-config.py --check, atsfill findings included).

Prints JSON with `problems`, each with a `fix`, and exits 1 when there is any.
"""

import json
import subprocess
import sys
from pathlib import Path

import yaml

SCHEMA_VERSION = 1
WORKSPACE = Path.home() / "jobsearch"
SYNC = Path(__file__).resolve().parent / "sync-config.py"


def workspace_problems() -> list[dict]:
    path = WORKSPACE / "workspace.yaml"
    if not path.exists():
        return [{"problem": f"{path} is missing", "fix": "run /jobsearch-init"}]
    try:
        version = (yaml.safe_load(path.read_text()) or {}).get("schema_version")
    except yaml.YAMLError as e:
        return [{"problem": f"{path} doesn't parse: {e}", "fix": "repair the file"}]
    if version != SCHEMA_VERSION:
        return [{"problem": f"schema_version is {version}, the skills expect {SCHEMA_VERSION}", "fix": "run /jobsearch-init"}]
    return []


def config_problems() -> list[dict]:
    run = subprocess.run(["uv", "run", "-q", str(SYNC), "--check"], capture_output=True, text=True)
    try:
        report = json.loads(run.stdout)
    except json.JSONDecodeError:
        return [{"problem": f"sync-config.py --check failed: {run.stderr.strip()}", "fix": "tell the user"}]
    found = [{"problem": m, "fix": f"uv run {SYNC}"} for m in report["mismatches"]]
    found += [{"problem": a, "fix": "stop and tell the user: atsfill may have sent an application"} for a in report["atsfill"]]
    return found


def main() -> int:
    problems = workspace_problems() + config_problems()
    print(json.dumps({"workspace": str(WORKSPACE), "problems": problems}, indent=2))
    return int(bool(problems))


if __name__ == "__main__":
    sys.exit(main())
