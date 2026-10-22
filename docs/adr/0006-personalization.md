# Everything personal lives in the workspace, and the user owns every cron job

The source logic had its owner built in: name, city, tracks, cron times, model, messaging platform and standing answers. The distribution ships only defaults and the questions that fill them in: `criteria.md` holds what the user looks for and their standing answers, `workspace.yaml` holds `autonomy:` ([0004](0004-action-policy.md)), the caps, the ghosting window and the company hold, and `ball: user` replaces the owner's name.

## Considered options

- **Shipping cron jobs**: updates overwrite `deliver` and `workdir` on shipped jobs, so the user's delivery target would be lost on every update. Init creates Advance and Tracking, add-track creates a discovery and a weekly market job per track, all through `hermes cron create`. The prompts name skills, so logic fixes still arrive.
- **A model in `config.yaml`**: an installed profile doesn't inherit the default profile's model, so init checks one is set and points to `jobsearch model`. The README names the tested models.

## Consequences

- Reports go to the platform chosen at init (`reports` in `workspace.yaml`, read by every `hermes cron create`), or stay `local`.
- Profile facts come from the user's LinkedIn profile, a CV if given, and a short interview, one file each under `profile/`. Without a CV, the first resume is only as good as the profile and the interview.
- LinkedIn safety relies on defaults: at most 3 tracks, capped search pages per discovery run, and a warning in the README. A real limit on call volume belongs in the MCP server.
- Skills contain no personal values, which the scan before going public ([0007](0007-distribution-repo.md)) checked.
- Changing a cron schedule or prompt for existing users needs a migration, since their jobs are their own.
