# 005 Dependencies

Status: accepted

## Context

The source setup runs the LinkedIn MCP from a local checkout of a fork. It uses four or five browser MCPs, each with its own login or profile, to read and fill external forms. Email goes through the Himalaya CLI, and resumes go through cratecv, built from source. A distribution can't install anything: it copies files, and setup happens in a skill the user runs.

## Decision

| Dependency | How it is used | How it gets installed |
|---|---|---|
| LinkedIn MCP | `shbernal/linkedin-mcp-server`, pinned to a tag `jobsearch-v<n>` on its `jobsearch` branch, run as `uvx --from git+https://github.com/shbernal/linkedin-mcp-server@<tag> mcp-server-linkedin` | `uv`. Init runs the same command with `--login` and keeps the server's default profile location |
| Forms | atsfill, the newest dev release, run as `uvx --prerelease allow atsfill@latest <command>`. No browser MCP ships | `uv`. Some systems are read over HTTP. The others need atsfill's pinned Camoufox, which init offers (`atsfill install-browser`, 1.3 GB), and some an account (`atsfill login <system>`) |
| Email (optional) | Himalaya CLI, read-only unless archiving is enabled ([004](004-action-policy.md)) | binary offered by init; skill via `npx skills` |
| Resumes | cratecv | GitHub release binaries; skill via `npx skills` |

- **Why no browser MCP:** a CLI that prints one JSON document costs fewer tokens than page snapshots, keeps no process or browser profile, and runs through `uvx`. A system atsfill returns `unsupported` for is read with Hermes' built-in browser, which runs a fresh session per task.
- **Why atsfill is unpinned:** hiring systems and their bot detection change fast, and so does atsfill. A pin would hold users on adapters that have stopped working. No version is recorded or checked anywhere. Fixes come from upstream: when a result points at atsfill rather than the form or the answers, the agent drafts an issue for github.com/shbernal/atsfill/issues without the user's data, and the user files it. LinkedIn tool failures get the same treatment on the fork, which stays pinned.
- **Sending:** atsfill's `submit` list in its own config picks the systems that may receive a send, and `autonomy.external_forms` decides whether the agent sends ([004](004-action-policy.md)). Neither stops an agent that ignores its skills, since it can write both files. The pre-run check reports a non-empty `submit` list while `external_forms` is off.
- **Why the fork:** discover, prepare, apply and update-status depend on fork-only tools, for example `submit_easy_apply`, `get_easy_apply_form`, `unsave_job`, `archive_job`, and the `start` and `dismiss_ids` parameters on `search_jobs`. The upstream package would break them.
- **Fork releases:** the `jobsearch` branch is upstream `main` plus the fork's topic branches. A `jobsearch-v<n>` tag and a GitHub release mark each build the distribution needs, and the release notes record the upstream base commit and the branches it contains. The number has its own sequence because a build carries unreleased upstream commits, and a `v<upstream>-…` name would misstate that.
- **Where the servers are configured:** `mcp_servers` in the shipped `config.yaml`, with `tools.exclude` on the LinkedIn server and `${userHome}` where a path is needed (Hermes doesn't expand `~` in MCP args). A profile-root `mcp.json` is copied by the installer but never read. An agent plugin's `mcp.json` is read and updated with the distribution, but it can't filter tools, which [004](004-action-policy.md) relies on.
- **Keeping them current:** `hermes profile update` keeps the user's `config.yaml` whole, and `--force-config` would erase the user's other settings. `skills/jobsearch-init/scripts/sync-config.py` rewrites only the `linkedin` server entry to what the skill records. The skills' pre-run check (`preflight.py`) compares the installed version with the recorded one and points to the sync script when they differ. A fork bump is: tag the fork, record the tag in the init skill, release the distribution.
- **Skills from other repos** go into the profile with `HERMES_HOME=<profile> npx skills add <repo> --skill <name> -g -a hermes-agent --copy`. That covers `shbernal/skills` (himalaya) and `shbernal/cratecv` (cratecv). Updates merge `skills/` one entry at a time, so these survive `hermes profile update`. Hermes seeds its own himalaya skill, for Himalaya 1.x, on its first update or session in the profile, and a second skill with the same name makes both unloadable by name. init lists `himalaya` in `skills/.curator_suppressed`, the file Hermes reads to skip seeding a built-in.
- **Tools on the user's machine** (uv, node for `npx skills`, cratecv, himalaya): init checks PATH and offers what is missing. With mise present, it offers `mise use -g <tool>` (`himalaya`, `github:shbernal/cratecv`). Otherwise it prints the release or package-manager command. It never installs without asking. Without Himalaya, init skips the email step, and tracking uses LinkedIn only.

## Consequences

- A release of this distribution depends on a tagged fork release. Bringing the fork's features upstream would remove that dependency. That is open, not planned.
- `mise use -g github:shbernal/cratecv` has to be tested on a clean machine before the README promises it.
