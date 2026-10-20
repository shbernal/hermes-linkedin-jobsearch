#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Create a job-search workspace from the template: copy it, git init, first commit."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "template"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default="~/jobsearch", help="workspace path (default: ~/jobsearch)")
    target = Path(parser.parse_args().target).expanduser().resolve()

    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        print(json.dumps({"error": "target exists and is not empty", "path": str(target)}))
        return 1
    if subprocess.run(["git", "var", "GIT_COMMITTER_IDENT"], capture_output=True).returncode:
        print(json.dumps({"error": "git has no user.name and user.email to commit with"}))
        return 1

    shutil.copytree(TEMPLATE, target, dirs_exist_ok=True)
    git = ["git", "-C", str(target)]
    subprocess.run([*git, "init", "-q", "-b", "main"], check=True)
    subprocess.run([*git, "add", "-A"], check=True)
    subprocess.run([*git, "commit", "-q", "-m", "Create the job-search workspace"], check=True)
    print(json.dumps({"path": str(target)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
