# The workspace lives in ~/jobsearch, outside the Hermes profile

The workspace holds the user's career record, which must survive `hermes profile delete` (an `rmtree`, and the first step of every reinstall), stay easy to open and edit, work with other agents, and be a clean git repo. So it always lives in `~/jobsearch`, created by `/jobsearch-init`, with a symlink for anyone who wants the data elsewhere, never inside `~/.hermes/profiles/jobsearch/`.

## Considered options

- **Inside the profile** (`~/.hermes/profiles/jobsearch/workspace/`): zero setup and never missing, but deleted with the profile, hidden next to sockets and a multi-gigabyte `state.db`, and tied to Hermes. It saves no configuration either: Hermes' local CLI ignores `terminal.cwd` (`tests/hermes_cli/test_cwd_env_respect.py`), so the agent needs an explicit path anyway.
- **A path chosen at init**: `hermes profile update` replaces `SOUL.md` wholesale, so a path written into it would be lost on the next update. A symlink moves the data without changing the path.

## Consequences

- The path appears as `~/jobsearch` in `terminal.cwd`, `SOUL.md`, and each cron job's `workdir`, which init and add-track set through `hermes cron create` so Hermes expands it. Cron prompts never name it, and nothing names `/home/<user>`.
- `SOUL.md` points to `/jobsearch-init` when the workspace is missing.
- The workspace holds only data. The playbooks ship in `skills/` so `hermes profile update` delivers fixes, and the workspace `AGENTS.md` only describes the layout and names the skills.
- The data layout is a contract: the template's folder READMEs are the schema the skills rely on, and changing it needs a migration, since updates never touch the workspace.
