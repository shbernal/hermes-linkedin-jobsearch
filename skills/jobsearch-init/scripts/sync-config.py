#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["ruamel.yaml>=0.18"]
# ///
"""Keep the profile's config.yaml on the LinkedIn server this distribution expects.

Rewrites only the `linkedin` server's command, args and tool exclusions. Every other key stays.
`--check` reports without writing.
"""

import argparse
import json
import os
import sys
from pathlib import Path

from ruamel.yaml import YAML

LINKEDIN = {
    "command": "uvx",
    "args": [
        "--from",
        "git+https://github.com/shbernal/linkedin-mcp-server@jobsearch-v1",
        "mcp-server-linkedin",
        "--transport",
        "stdio",
    ],
    "exclude": ["send_message", "connect_with_person", "reply_to_conversation"],
}


def find_config(arg: str | None) -> Path:
    if arg:
        return Path(arg).expanduser()
    if home := os.environ.get("HERMES_HOME"):
        return Path(home) / "config.yaml"
    for parent in Path(__file__).resolve().parents:
        if (parent / "distribution.yaml").exists():
            return parent / "config.yaml"
    sys.exit("no profile found: pass --config")


def mismatches(config: dict) -> list[str]:
    server = (config.get("mcp_servers") or {}).get("linkedin") or {}
    found = []
    if server.get("command") != LINKEDIN["command"] or list(server.get("args") or []) != LINKEDIN["args"]:
        found.append("mcp_servers.linkedin command or args")
    if list((server.get("tools") or {}).get("exclude") or []) != LINKEDIN["exclude"]:
        found.append("mcp_servers.linkedin tools.exclude")
    return found


def sync(config: dict) -> None:
    server = config.setdefault("mcp_servers", {}).setdefault("linkedin", {})
    server["command"] = LINKEDIN["command"]
    server["args"] = LINKEDIN["args"]
    server.setdefault("tools", {})["exclude"] = LINKEDIN["exclude"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", help="config.yaml to sync (default: the profile this script is installed in)")
    parser.add_argument("--check", action="store_true", help="report mismatches, write nothing")
    args = parser.parse_args()

    path = find_config(args.config)
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    config = (yaml.load(path) if path.exists() else None) or {}
    found = mismatches(config)
    report = {"config": str(path), "mismatches": found}

    if args.check:
        print(json.dumps(report, indent=2))
        return int(bool(found))
    if found:
        sync(config)
        yaml.dump(config, path)
    report["updated"] = bool(found)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
