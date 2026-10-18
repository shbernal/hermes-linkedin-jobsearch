# 006 Personalization

Status: accepted

## Context

The source logic has its owner built in: their first name throughout (including in `ball:`), their city and country in every search string, their tracks and cron times, their model and provider, their messaging platform, and the standing answers in their search-criteria document. Every user has to set all of this for themselves.

## Decision

Everything personal lives in the workspace. The distribution ships defaults and the questions that fill them in.

- **`criteria.md`** holds location and remote rules, contract, level, working languages, title exclusions, target companies, the standing answers and the user's resume preferences. Search strings are built from it.
- **`workspace.yaml`** holds `schema_version`, the `autonomy:` block ([004](004-action-policy.md)), the caps (sends, close-outs, search pages per discovery run, tracks), the ghosting window and the company hold.
- **`ball: user`** replaces the owner's name. The user's name comes from the profile facts, and is used in documents such as the PDF filename.
- **No model in `config.yaml`.** The user's Hermes default applies. The README names the models it was tested with.
- **No shipped cron jobs.** init creates Advance and Tracking, and add-track creates a discovery job and a weekly market job for each track, all with `hermes cron create`. Updates overwrite `deliver` and `workdir` on shipped jobs, so a shipped job would lose the user's delivery target on every update. The prompts name skills, so logic fixes still arrive with the skills.
- **Reports** go to the messaging platform chosen during init, using the `--deliver` targets Hermes supports, or stay `local` when the user picks none.
- **LinkedIn safety:** at most 3 tracks by default, the search pages per discovery run are capped in `workspace.yaml`, and the README warns about LinkedIn's terms. A real limit on call volume belongs in the MCP server.
- **Profile facts** come from the user's LinkedIn profile, read through the MCP, and from a CV if they provide one. A short interview fills the gaps (the `resume-market-fit` approach). Every fact is a file under `profile/`, so the source check on resume lines keeps working.

## Consequences

- The skills read `criteria.md` and `workspace.yaml` and contain no personal values. The scan before the repo goes public ([007](007-distribution-repo.md)) checks this.
- Changing a cron schedule or prompt for existing users needs a migration step, since their jobs are their own.
- Without a CV, the first resume is only as good as the LinkedIn profile and the interview.
