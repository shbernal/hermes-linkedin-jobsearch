# A pinned LinkedIn fork, unpinned atsfill, no browser MCP

A distribution only copies files, so every dependency is either run through `uvx` or offered by the init skill. The LinkedIn MCP is the `shbernal/linkedin-mcp-server` fork pinned to a `jobsearch-v<n>` tag, because discover, prepare, apply and update-status need fork-only tools; forms go through atsfill's newest dev release with no browser MCP; email (Himalaya) is optional, and resumes use cratecv.

| Dependency | Run as | Installed by |
|---|---|---|
| LinkedIn MCP | `uvx --from git+https://github.com/shbernal/linkedin-mcp-server@<tag> mcp-server-linkedin` | `uv`; init runs it with `--login` |
| Forms | `uvx --prerelease allow atsfill@latest <command>` | `uv`; init offers `atsfill install-browser` (1.3 GB) and `atsfill login <system>` where needed |
| Email (optional) | Himalaya CLI, read-only unless archiving is enabled ([0004](0004-action-policy.md)) | binary offered by init, skill via `npx skills` |
| Resumes | cratecv | release binaries, skill via `npx skills` |

## Considered options

- **Browser MCPs** (the source setup ran four or five): a CLI printing one JSON document costs fewer tokens than page snapshots and keeps no process or browser profile. A system atsfill returns `unsupported` for is read with Hermes' built-in browser.
- **Pinning atsfill**: hiring systems and their bot detection change fast, and a pin would hold users on adapters that stopped working. Tool failures are fixed upstream instead: the agent drafts an issue without the user's data and the user files it.
- **The upstream LinkedIn package**: lacks `submit_easy_apply`, `get_easy_apply_form`, `unsave_job`, `archive_job`, and the `start` and `dismiss_ids` parameters of `search_jobs`.
- **A profile-root or plugin `mcp.json`**: the first is copied but never read, the second can't filter tools, which [0004](0004-action-policy.md) relies on. The servers live in `mcp_servers` of the shipped `config.yaml`, with `${userHome}` where a path is needed (Hermes doesn't expand `~` in MCP args).

## Consequences

- The `jobsearch` branch is upstream `main` plus the fork's topic branches. Each `jobsearch-v<n>` tag has a GitHub release recording the upstream base and the branches it contains, with its own number since a build carries unreleased upstream commits.
- `hermes profile update` keeps the user's `config.yaml` whole, so `sync-config.py` rewrites only the `linkedin` entry and the pre-run check points to it when the installed version differs. A fork bump is: tag the fork, record the tag in the init skill, release the distribution.
- A release of this distribution depends on a tagged fork release, until the fork's features land upstream (open, not planned).
- Skills from other repos (himalaya from `shbernal/skills`, cratecv from `shbernal/cratecv`) go in with `HERMES_HOME=<profile> npx skills add <repo> --skill <name> -g -a hermes-agent --copy`, and survive updates because `skills/` is merged one entry at a time.
- Init checks PATH for uv, node, cratecv and himalaya and offers what is missing (`mise use -g` when mise is present), never installing without asking. Without Himalaya, tracking uses LinkedIn only.
- `mise use -g github:shbernal/cratecv` has to be tested on a clean machine before the README promises it.
