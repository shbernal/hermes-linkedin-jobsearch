#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["ruamel.yaml>=0.18"]
# ///
"""Keep the profile's config.yaml on the LinkedIn server and atsfill rules this distribution expects.

Rewrites only the `linkedin` server's command, args and tool exclusions, and the atsfill rules in
`approvals.deny`. Every other key, and the user's other deny rules, stay. `--check` reports without
writing, and also reports signs that atsfill sent something, which no config rule can prevent.
"""

import argparse
import json
import os
import platform
import sys
import tomllib
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
ATSFILL_DENY = ["*atsfill* send", "*atsfill* send *", "*atsfill* fill", "*atsfill* fill *"]


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
    deny = (config.get("approvals") or {}).get("deny") or []
    if [rule for rule in deny if "atsfill" in rule] != ATSFILL_DENY:
        found.append("approvals.deny atsfill rules")
    return found


def sync(config: dict) -> None:
    server = config.setdefault("mcp_servers", {}).setdefault("linkedin", {})
    server["command"] = LINKEDIN["command"]
    server["args"] = LINKEDIN["args"]
    server.setdefault("tools", {})["exclude"] = LINKEDIN["exclude"]
    approvals = config.setdefault("approvals", {})
    approvals["deny"] = [rule for rule in approvals.get("deny") or [] if "atsfill" not in rule] + ATSFILL_DENY


def atsfill_findings() -> list[str]:
    """atsfill's own paths (atsfill core/paths.py): a submit list, or any logged send attempt."""
    linux = platform.system() == "Linux"
    if xdg := os.environ.get("XDG_CONFIG_HOME"):
        config_file = Path(xdg) / "atsfill/config.toml"
    else:
        config_file = Path.home() / (".config/atsfill/config.toml" if linux else ".atsfill/config.toml")
    if env := os.environ.get("ATSFILL_DATA_DIR"):
        data_dir = Path(env)
    elif linux:
        data_dir = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state") / "atsfill"
    else:
        data_dir = Path.home() / ".atsfill"

    found = []
    if config_file.exists():
        try:
            submit = tomllib.loads(config_file.read_text()).get("submit")
        except tomllib.TOMLDecodeError as e:
            found.append(f"{config_file} doesn't parse: {e}")
        else:
            if submit:
                found.append(f"{config_file} enables sending: submit = {submit}")
    attempts = data_dir / "attempts.jsonl"
    if attempts.exists() and (lines := [line for line in attempts.read_text().splitlines() if line.strip()]):
        found.append(f"{attempts} records {len(lines)} send attempt(s)")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", help="config.yaml to sync (default: the profile this script is installed in)")
    parser.add_argument("--check", action="store_true", help="report mismatches and atsfill findings, write nothing")
    args = parser.parse_args()

    path = find_config(args.config)
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    config = (yaml.load(path) if path.exists() else None) or {}
    found = mismatches(config)
    report = {"config": str(path), "mismatches": found}

    if args.check:
        report["atsfill"] = atsfill_findings()
        print(json.dumps(report, indent=2))
        return int(bool(found or report["atsfill"]))
    if found:
        sync(config)
        yaml.dump(config, path)
    report["updated"] = bool(found)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
