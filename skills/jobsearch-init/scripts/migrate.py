#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Bring a schema_version 1 workspace to the layout the skills expect, and commit it.

Moves companies/ to employers/ and market/<track>/offers/ to postings/, renames the `company`
field and ball value to `employer`, rewrites workspace.yaml on the template with the user's values,
rewrites paths to them in the user's files,
and replaces the template's READMEs and AGENTS.md. Prints the READMEs it replaced: their git diff
shows any lines the user had added. Refuses a workspace with uncommitted changes.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

TEMPLATE = Path(__file__).resolve().parent.parent / "template"
SCHEMA_VERSION = 2

RENAMED_KEYS = {
    "easy_apply": "linkedin_easy_apply",
    "dismiss_known_jobs": "hide_known_jobs_from_linkedin_search",
    "archive_email": "archive_handled_emails",
    "max_sends_per_day": "max_applications_sent_per_day",
    "max_close_outs_per_day": "max_linkedin_close_outs_per_day",
    "max_search_pages_per_run": "max_search_pages_per_discovery_run",
    "ghosted_after_weeks": "weeks_without_answer_until_ghosted",
    "company_hold_days": "days_before_reapplying_to_unanswered_employer",
    "reports": "report_delivery_target",
}
SECTIONS = ("autonomy", "caps", "limits", "timings")


def settings(old: dict) -> dict:
    """The user's values under the current key names, sections flattened."""
    flat = {}
    for key, value in old.items():
        if key in SECTIONS and isinstance(value, dict):
            flat.update(value)
        else:
            flat[key] = value
    return {RENAMED_KEYS.get(k, k): v for k, v in flat.items()}


def aligned(value: str, old: str) -> str:
    """The value, padded so a comment after it keeps its column."""
    return value if old == old.rstrip() else value.ljust(len(old) - 1) + " "


def workspace_yaml(old: dict) -> tuple[str, list[str]]:
    """The template's workspace.yaml holding the user's values, and the keys it had no place for."""
    values = settings(old)
    values["schema_version"] = str(SCHEMA_VERSION)
    text, placed = (TEMPLATE / "workspace.yaml").read_text(), set()
    for key, value in values.items():
        pattern = re.compile(rf"^({re.escape(key)}:[ \t]*)(\S+)([ \t]*)", re.MULTILINE)
        if pattern.search(text):
            text = pattern.sub(lambda m: m.group(1) + aligned(value, m.group(2) + m.group(3)), text, count=1)
            placed.add(key)
    return text, sorted(set(values) - placed)


def rename_field(path: Path) -> bool:
    """`company:` to `employer:` in the frontmatter, and `ball: company` to `ball: employer`."""
    text = path.read_text()
    match = re.match(r"---\n.*?\n---\n", text, re.DOTALL)
    if not match:
        return False
    front = re.sub(r"^company:", "employer:", match.group(0), flags=re.MULTILINE)
    front = re.sub(r"^ball:(\s*)company\b", r"ball:\1employer", front, flags=re.MULTILINE)
    if front == match.group(0):
        return False
    path.write_text(front + text[match.end():])
    return True


OLD_PATHS = (
    (re.compile(r"(?<![\w/.])companies/(?=[a-z0-9-]+\.md)"), "employers/"),
    (re.compile(r"\b(market/[a-z0-9-]+)/offers/"), r"\1/postings/"),
)


def rewrite_paths(ws: Path) -> int:
    """Paths to companies/ and offers/ inside the user's files, URLs left alone. Returns the files changed."""
    changed = 0
    for path in [*ws.rglob("*.md"), *ws.rglob("*.yaml")]:
        if ".git" in path.relative_to(ws).parts:
            continue
        text = new = path.read_text()
        for pattern, repl in OLD_PATHS:
            new = pattern.sub(repl, new)
        if new != text:
            path.write_text(new)
            changed += 1
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default="~/jobsearch", help="workspace path (default: ~/jobsearch)")
    ws = Path(parser.parse_args().target).expanduser().resolve()
    git = ["git", "-C", str(ws)]

    old = yaml.load((ws / "workspace.yaml").read_text(), Loader=yaml.BaseLoader) or {}  # values as written: `off` stays off
    if old.get("schema_version") != "1":
        print(json.dumps({"error": f"schema_version is {old.get('schema_version')}, this migrates 1"}))
        return 1
    if subprocess.run([*git, "status", "--porcelain"], capture_output=True, text=True, check=True).stdout:
        print(json.dumps({"error": "the workspace has uncommitted changes: commit them first"}))
        return 1

    for src, dst in [(ws / "companies", ws / "employers"), *((d / "offers", d / "postings") for d in (ws / "market").glob("*/"))]:
        if src.is_dir() and not dst.exists():
            subprocess.run([*git, "mv", str(src), str(dst)], check=True)

    renamed = [
        str(p.relative_to(ws))
        for pattern in ("pipeline/*.md", "archive/pipeline/*.md", "market/*/postings/*.md")
        for p in ws.glob(pattern)
        if p.name != "README.md" and rename_field(p)
    ]

    paths = rewrite_paths(ws)
    if (skipped := ws / "pipeline/skipped.md").exists():
        text = skipped.read_text().replace("# Skipped jobs", "# Skipped postings", 1)
        skipped.write_text(re.sub(r"^(\|[^|\n]*\|[^|\n]*\|\s*)Company(\s*\|)", r"\1Employer\2", text, count=1, flags=re.MULTILINE))
    if (criteria := ws / "criteria.md").exists():
        criteria.write_text(re.sub(r"^## Companies$", "## Employers", criteria.read_text(), count=1, flags=re.MULTILINE))

    text, unplaced = workspace_yaml(old)
    (ws / "workspace.yaml").write_text(text)

    replaced = []
    for src in sorted(TEMPLATE.rglob("*")):
        rel = src.relative_to(TEMPLATE)
        if src.is_file() and (src.name == "README.md" or str(rel) == "AGENTS.md"):
            dst = ws / rel
            if not dst.exists() or dst.read_bytes() != src.read_bytes():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                replaced.append(str(rel))

    subprocess.run([*git, "add", "-A"], check=True)
    subprocess.run([*git, "commit", "-q", "-m", f"Migrate the workspace to schema_version {SCHEMA_VERSION}"], check=True)
    commit = subprocess.run([*git, "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    print(json.dumps({
        "path": str(ws),
        "commit": commit,
        "frontmatter_renamed": len(renamed),
        "files_with_paths_rewritten": paths,
        "readmes_replaced": replaced,
        "settings_without_a_place": unplaced,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
