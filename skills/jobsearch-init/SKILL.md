---
name: jobsearch-init
description: Set up the job-search agent for a new user, or finish a setup that stopped partway. Checks the model and tools, creates the ~/jobsearch workspace, logs in to LinkedIn, builds the profile facts and criteria by interview, sets what may be sent without asking, creates the first track and schedules the jobs. Use when ~/jobsearch is missing, or when the user asks to set up, onboard or resume setup.
---

# Set up the job search

A conversation, run once. Every step first checks whether it's already done and skips if so, so a second run picks up where the first stopped. Never install a tool or open a login without the user's yes. `<profile>` below is this profile's home, `$HERMES_HOME`.

## 1. Model

`hermes config get model.default`. When it's empty, cron jobs have nothing to run on: tell the user to run `jobsearch model` (the profile's alias) and stop here.

## 2. Tools

Check PATH for `uv`, `node` with `npx`, `git` and `cratecv`, and ask whether the user wants email tracking, which needs `himalaya`. For each missing tool, offer one install command and run it on a yes: `mise use -g <tool>` when `mise` is on PATH (`github:shbernal/cratecv` for cratecv), otherwise the official release or the system package manager. `git` also needs `user.name` and `user.email` to commit.

## 3. Config

`uv run ${HERMES_SKILL_DIR}/scripts/sync-config.py`, so the LinkedIn server entry matches this release.

## 4. Workspace

Skip when `~/jobsearch/workspace.yaml` exists. Ask where the data should live. For `~/jobsearch`, run `uv run ${HERMES_SKILL_DIR}/scripts/init.py`. Elsewhere, run it with that path and then `ln -s <path> ~/jobsearch`. The skills always use `~/jobsearch`.

## 5. Skills

Skip when `<profile>/skills/cratecv` exists:

```bash
HERMES_HOME=<profile> npx skills add shbernal/cratecv --skill cratecv -g -a hermes-agent --copy
```

## 6. LinkedIn

Run the `linkedin` server's command and args from `<profile>/config.yaml` with `--transport stdio` replaced by `--status`. When the session isn't valid, the same command with `--login` opens a browser where the user signs in. If it can't open a window from here, give the user that command to run in their own terminal. Then call `get_person_profile` on the user. It works when it returns their profile, and that output feeds step 8.

## 7. Reports

Ask which messaging platform gets the scheduled reports, among the `--deliver` targets in `hermes cron create --help`. None means `local`. A platform needs the gateway: point to `hermes gateway setup` for the connection and `hermes gateway install` so jobs run in the background, then check `hermes gateway status`. Write the choice to `reports` in `workspace.yaml`.

## 8. Profile facts

Skip what `profile/` already holds. Sources, in order: the LinkedIn profile from step 6, a CV if the user gives one (copy it to `profile/sources/`), then a short interview for the gaps: dates, scope, results, tools, anything the CV and LinkedIn disagree on. Write the files as `profile/README.md` specifies, each fact with its source.

## 9. Criteria

Fill every section of `criteria.md` by interview, `## Resume` included, offering what the profile facts already suggest. Remove the template's placeholder prose as each section is filled. Dated answers carry today's date.

## 10. Sending

Explain each `autonomy` and `caps` setting in `workspace.yaml` in a line and ask:

- `easy_apply` and `external_forms`: `off`, `approval` or `unattended`, and `max_sends_per_day`.
- When `external_forms` isn't `off`: run `uvx --prerelease allow atsfill@latest status`, offer every system it supports, and mark those only dry-run verified. Write the chosen systems to the `submit` list in atsfill's config (`status` prints its path). Offer `atsfill install-browser` (1.3 GB) when a chosen system needs the browser, and `atsfill login <system>` for each one that needs an account.
- `dismiss_known_jobs`, and whether the defaults for the other caps fit.

## 11. First track

Skip when `tracks/` holds a track. Otherwise run the jobsearch-add-track skill. It writes the track, the base resume and the first market report, and creates the track's two jobs.

## 12. Email (optional)

When the user wants it and `himalaya` is installed: `HERMES_HOME=<profile> npx skills add shbernal/skills --skill himalaya -g -a hermes-agent --copy`, then the account setup the himalaya skill documents, with an app password or OAuth. Check that listing the inbox works. Ask whether tracking may archive application email once handled, and set `archive_email` to match.

## 13. Advance and Tracking

Skip a job `hermes cron list` already shows. Create both with the `reports` target:

```bash
hermes cron create "0 10-20/2 * * *" "Run jobsearch-advance." \
  --skill jobsearch-scheduled-run --skill jobsearch-advance --name "Advance" --workdir ~/jobsearch --deliver <reports>
hermes cron create "30 6,14,22 * * *" "Run jobsearch-update-status for every open application." \
  --skill jobsearch-scheduled-run --skill jobsearch-update-status --name "Tracking" --workdir ~/jobsearch --deliver <reports>
```

Add `--skill himalaya` to Tracking when email is set up. Check all four jobs in `hermes cron list`. Don't trigger a run without the user's go.

## 14. Commit and report

Commit the workspace. Report what was set up, what was skipped and why, the jobs and their next runs, and anything still open, such as an atsfill login the user postponed.
