# A public distribution with an explicit file allowlist

The distribution is `shbernal/hermes-linkedin-jobsearch`, public under MIT from the moment the skeleton installed, with `name: jobsearch` and `hermes_requires: ">=0.22.2"`. `distribution_owned` lists exactly `SOUL.md`, `config.yaml`, `skills/` and `distribution.yaml`, so repo files never reach a profile and no `mcp.json` ([0005](0005-dependencies.md)) or `cron/` ([0006](0006-personalization.md)) ships.

## Consequences

- Scripts live in the skill that runs them, under its `scripts/`, run with `uv run`. The workspace holds no code.
- Before the first push, a one-time scan of the tree and full history looked for the owner's names, `/home/` paths, emails, old cookie and profile paths, a named `ball:` owner, real company names and salaries, and the history was rewritten. It isn't a CI check, because a green check would promise more than a pattern match can.
- CI installs the distribution into a throwaway `HERMES_HOME` on every push and checks that only the allowlisted paths arrive.
- `v0.1.0` is tagged once a fresh install has run every scheduled job, and 0.x alone says it isn't stable. `1.0.0` comes after a real setup has moved onto the distribution. `CHANGELOG.md` records bumps, independent of the fork's tags.
