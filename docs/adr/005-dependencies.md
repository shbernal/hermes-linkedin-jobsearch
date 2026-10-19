# 005 Dependencies

Status: accepted

## Context

The source setup runs the LinkedIn MCP from a local checkout of a fork. It uses four or five browser MCPs, each with its own login or profile, to read and fill external forms. Email goes through the Himalaya CLI, and resumes go through cratecv, built from source. A distribution can't install anything: it copies files, and setup happens in a skill the user runs.

## Decision

| Dependency | How it is used | How it gets installed |
|---|---|---|
| LinkedIn MCP | `shbernal/linkedin-mcp-server`, pinned to a tag `jobsearch-v<n>` on its `jobsearch` branch, run as `uvx --from git+https://github.com/shbernal/linkedin-mcp-server@<tag> mcp-server-linkedin` | `uv`. Init runs the same command with `--login` and keeps the server's default profile location |
| Forms | atsfill, pinned to an exact dev release and run as `uvx --from atsfill==<version> atsfill read <url>`. Read only: no browser MCP ships | `uv`. Ashby and Greenhouse are read over HTTP. Teamtailor needs atsfill's pinned Camoufox, which init offers (`atsfill install-browser`, 1.3 GB) |
| Email (optional) | Himalaya CLI, read-only unless archiving is enabled ([004](004-action-policy.md)) | binary offered by init; skill via `npx skills` |
| Resumes | cratecv | GitHub release binaries; skill via `npx skills` |

- **Why no browser MCP:** v1 only reads forms ([003](003-scope.md)). A CLI that prints one JSON document costs fewer tokens than page snapshots, keeps no process or browser profile, and pins through `uvx`. A system atsfill returns `unsupported` for is read with Hermes' built-in browser, which runs a fresh session per task.
- **Read only:** `config.yaml` sets `approvals.deny` on `atsfill … send` and `atsfill … fill`, which Hermes blocks before any approval mode or YOLO is consulted. `fill` is blocked too because some systems save answers as they are typed. atsfill's own gate (no `submit` list in the user's atsfill config) is a second barrier. The deny rule matches command text, so it stops an agent that follows its skills, not a hostile one.
- **Why the fork:** discover, prepare, apply and update-status depend on fork-only tools, for example `submit_easy_apply`, `get_easy_apply_form`, `unsave_job`, `archive_job`, and the `start` and `dismiss_ids` parameters on `search_jobs`. The upstream package would break them.
- **Fork releases:** the `jobsearch` branch is upstream `main` plus the fork's topic branches. A `jobsearch-v<n>` tag and a GitHub release mark each build the distribution needs, and the release notes record the upstream base commit and the branches it contains. The number has its own sequence because a build carries unreleased upstream commits, and a `v<upstream>-…` name would misstate that.
- **Where the servers are configured:** `mcp_servers` in the shipped `config.yaml`, with `tools.exclude` on the LinkedIn server and `${userHome}` where a path is needed (Hermes doesn't expand `~` in MCP args). A profile-root `mcp.json` is copied by the installer but never read. An agent plugin's `mcp.json` is read and updated with the distribution, but it can't filter tools, which [004](004-action-policy.md) relies on.
- **Keeping them current:** `hermes profile update` keeps the user's `config.yaml` whole, and `--force-config` would erase the user's other settings. `skills/jobsearch-init/scripts/sync-config.py` rewrites only the `linkedin` server entry and the atsfill rules in `approvals.deny` to what the skill records, keeping the user's other deny rules. The skills' pre-run check compares the installed version with the recorded one and points to the sync script when they differ. A fork bump is: tag the fork, record the tag in the init skill, release the distribution.
- **Skills from other repos** go into the profile with `HERMES_HOME=<profile> npx skills add <repo> --skill <name> -g -a hermes-agent --copy`. That covers `shbernal/skills` (himalaya) and `shbernal/cratecv` (cratecv). Updates merge `skills/` one entry at a time, so these survive `hermes profile update`.
- **Tools on the user's machine** (uv, node for `npx skills`, cratecv, himalaya): init checks PATH and offers what is missing. With mise present, it offers `mise use -g <tool>` (`himalaya`, `github:shbernal/cratecv`). Otherwise it prints the release or package-manager command. It never installs without asking. Without Himalaya, init skips the email step, and tracking uses LinkedIn only.

## Consequences

- A release of this distribution depends on a tagged fork release. Bringing the fork's features upstream would remove that dependency. That is open, not planned.
- `mise use -g github:shbernal/cratecv` has to be tested on a clean machine before the README promises it.
- The himalaya skill was written for Himalaya 2.1.x, and mise currently installs 2.2.1.
