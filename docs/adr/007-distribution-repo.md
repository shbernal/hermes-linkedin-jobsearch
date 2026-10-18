# 007 Distribution repo

Status: accepted

## Decision

- **Identity:** `shbernal/hermes-linkedin-jobsearch`, public, MIT. The manifest's `name: jobsearch` gives users a `jobsearch` command. Tests install it next to an existing profile with `--name jobsearch-test`.
- **Hermes:** `hermes_requires: ">=0.22"`, tested on the current release.
- **What gets installed:** `distribution.yaml` lists `distribution_owned` explicitly: `SOUL.md`, `config.yaml`, `skills/`, `distribution.yaml`. `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `LICENSE`, `docs/` and `.github/` stay in the repo and never reach a profile. No `mcp.json` ([005](005-dependencies.md)) and no `cron/` ([006](006-personalization.md)).
- **Scripts** live in the skills that run them, under each skill's `scripts/`, and run with `uv run`. The workspace holds no code.
- **Public early:** the repo goes public as soon as the skeleton installs, and CI runs from the first push. Before that push, a one-time scan covers the tree and the full history: the owner's names, `/home/` paths, email addresses, the old cookie and profile paths, a named owner in `ball:`, real company names and salary figures. Anything found is fixed and the history rewritten. The scan isn't a CI check, because a green check would promise more than a pattern match can.
- **CI** installs the distribution into a throwaway `HERMES_HOME` with `hermes profile install ./ -y` on every push, and checks that only the allowlisted paths arrive.
- **Roadmap:** `ROADMAP.md`, linked at the top of the README. It lists what is tested (LinkedIn, together with the pinned MCP) and what is next (atsfill for external forms, Welcome to the Jungle, other job sources).
- **Versions:** `v0.1.0` is tagged once a fresh install has run a full day of cron. The 0.x number says it isn't stable, with no separate preview label. `1.0.0` comes after a real setup has moved onto the distribution and run on it. `CHANGELOG.md` records the bumps. Distribution versions are independent of the fork's tags.
- **These ADRs** live in `docs/adr/`.
