# 001 Workspace location

Status: accepted

## Question

Where does a new user's workspace live: inside the agent's Hermes home (`~/.hermes/profiles/jobsearch/workspace/`), or in a directory of its own?

The workspace holds the user's career record: profile facts, resumes, tracks, pipeline, applications, companies, market reports.

## Decision

The workspace goes in a visible directory of its own, always `~/jobsearch`. A setup skill (`/jobsearch-init`) creates it, runs `git init`, and offers a symlink to anyone who wants the data stored elsewhere.

## Why

- **It outlives the agent.** `hermes profile delete` removes the profile directory with `rmtree`, and reinstalling a profile means deleting it first. The career record must survive a broken agent, a reinstall, or a user trying a different agent.
- **The user works in it.** People edit their profile facts, open the resumes and read the reports. A hidden folder under `~/.hermes`, next to sockets and a multi-gigabyte `state.db`, is the wrong place for that.
- **Other tools can use it.** A plain directory with an `AGENTS.md` works with Claude Code, Codex or any other agent. A Hermes profile folder ties the data to Hermes.
- **Git comes for free.** Application history as commits, and a backup by adding a private remote. The profile folder can't be a clean repo.
- **Inside the profile buys almost nothing.** Hermes' local CLI ignores `terminal.cwd` and runs in the shell's current directory (`tests/hermes_cli/test_cwd_env_respect.py`). Only the gateway and cron use the configured cwd. The agent therefore needs an explicit workspace path either way, and `~/jobsearch` is as easy to write down as `~/.hermes/profiles/jobsearch/workspace`.
- **The path is fixed because `SOUL.md` is.** `hermes profile update` replaces `SOUL.md` wholesale, so a path init wrote into it would be lost on the next update. A symlink moves the data without changing the path.

## What we give up

Inside the profile, the workspace would be zero-setup and could never point at a missing directory. The init skill makes up for most of that: SOUL.md checks that the workspace exists and points to `/jobsearch-init` if it doesn't.

## Consequences

- **The path appears in three places**, written as `~/jobsearch`: `terminal.cwd` (expanded by Hermes), `SOUL.md`, and each cron job's `workdir`, which init and add-track set through `hermes cron create` so that Hermes expands it. Cron prompts never name the path. No `/home/<user>`.
- **The workspace holds only data, and the logic ships in the distribution.** The playbooks go into `skills/` so that `hermes profile update` delivers fixes. If they lived in the workspace, every user would keep the version from the day they installed. `/jobsearch-init` writes a short workspace `AGENTS.md` that describes the data layout and points to the skills.
- **The data layout is a contract.** The folder READMEs in the init template are the schema the skills rely on. Changing it needs a migration step in the skill, since updates never touch the workspace.
