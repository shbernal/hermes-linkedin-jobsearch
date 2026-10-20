#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Checks that every headline, bullet and skill line in a resume YAML cites a file under the
workspace's profile/. Paths are relative to the workspace. With no arguments, checks
resumes/*.yaml and every applications/*/resume.yaml. The layout and the rest of the schema are
checked by cratecv."""

import sys
from pathlib import Path

import yaml

ROOT = Path.home() / "jobsearch"
PROFILE = (ROOT / "profile").resolve()


def lines(resume):
    """Yields (field path, item) for each line that needs a source."""
    if isinstance(resume.get("headline"), dict):
        yield "headline", resume["headline"]
    for s, section in enumerate(resume.get("sections") or []):
        for e, entry in enumerate(section.get("entries") or []):
            for b, bullet in enumerate(entry.get("details") or []):
                yield f"sections[{s}].entries[{e}].details[{b}]", bullet
        for k, skill in enumerate(section.get("skills") or []):
            yield f"sections[{s}].skills[{k}]", skill


def problems(file):
    try:
        resume = yaml.safe_load(file.read_text())
    except (OSError, yaml.YAMLError) as error:
        yield str(error)
        return
    if not isinstance(resume, dict):
        yield "not a mapping"
        return
    for at, item in lines(resume):
        source = item.get("source") if isinstance(item, dict) else None
        if not source:
            yield f"{at}: no source"
            continue
        for path in [source] if isinstance(source, str) else source:
            target = (PROFILE / str(path)).resolve()
            if not target.is_relative_to(PROFILE) or not target.is_file():
                yield f"{at}.source: {path} is not a file in profile/"


def main():
    files = [ROOT / arg for arg in sys.argv[1:]] or sorted(
        [*ROOT.glob("resumes/*.yaml"), *ROOT.glob("applications/*/resume.yaml")]
    )
    failed = False
    for file in files:
        found = list(problems(file))
        if found:
            failed = True
            print(f"{file}:", *(f"  {p}" for p in found), sep="\n", file=sys.stderr)
    if failed:
        sys.exit(1)
    print(f"Sources resolve in {len(files)} resume file(s).")


main()
