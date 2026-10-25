#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Create a job-search workspace from the template: copy it, git init, first commit.

On an existing workspace, copy only the template files it lacks and commit them, never touching a file it has.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "template"


def missing(target: Path) -> list[Path]:
    """Template files, relative to the template, that the workspace doesn't have."""
    files = (p.relative_to(TEMPLATE) for p in TEMPLATE.rglob("*") if p.is_file())
    return sorted(p for p in files if not (target / p).exists())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default="~/jobsearch", help="workspace path (default: ~/jobsearch)")
    target = Path(parser.parse_args().target).expanduser().resolve()

    existing = (target / "workspace.yaml").exists()
    if not existing and target.exists() and (not target.is_dir() or any(target.iterdir())):
        print(json.dumps({"error": "target exists and is not empty", "path": str(target)}))
        return 1
    if subprocess.run(["git", "var", "GIT_COMMITTER_IDENT"], capture_output=True).returncode:
        print(json.dumps({"error": "git has no user.name and user.email to commit with"}))
        return 1

    git = ["git", "-C", str(target)]
    if not existing:
        shutil.copytree(TEMPLATE, target, dirs_exist_ok=True)
        subprocess.run([*git, "init", "-q", "-b", "main"], check=True)
        subprocess.run([*git, "add", "-A"], check=True)
        subprocess.run([*git, "commit", "-q", "-m", "Create the job-search workspace"], check=True)
        print(json.dumps({"path": str(target)}))
        return 0

    added = missing(target)
    for path in added:
        (target / path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TEMPLATE / path, target / path)
    if added:
        paths = [str(p) for p in added]
        subprocess.run([*git, "add", "--", *paths], check=True)
        subprocess.run([*git, "commit", "-q", "-m", "Add the template files the workspace lacks", "--", *paths], check=True)
    print(json.dumps({"path": str(target), "added": [str(p) for p in added]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
