# A script copies the workspace skeleton, the agent fills it in

`/jobsearch-init` creates the workspace ([0001](0001-workspace-location.md)) in two halves: `scripts/init.py` copies a skeleton shipped under `skills/jobsearch-init/template/`, runs `git init` and commits, then the skill's conversation fills in what is personal (`criteria.md`, profile facts, the first track and its resume, see [0006](0006-personalization.md)). A script lays out the same structure every time at no token cost, while the personal content can only come from talking to the user.

## Considered options

- **The agent generates the folder**: a dozen READMEs written by the model give a slightly different workspace on every install.
- **A top-level `workspace/` in the repo**: dropped by the installer, which excludes `workspace` (`USER_OWNED_EXCLUDE` in `hermes_cli/profile_distribution.py`). Under `skills/jobsearch-init/template/` the skeleton travels with `skills/` and is versioned with the playbooks.
- **A separate template repo**: a second thing to version and fetch, whose layout would drift from the playbooks, and init would need network access.

## Consequences

- `init.py` refuses a target that exists and isn't empty.
- `workspace.yaml` records `schema_version`. Skills check it before running and point an outdated workspace to a migration, shipped with each layout change. A CI check that the template and the skills agree arrives with the first migration.
- Every empty folder carries a README saying what goes in it and in which format: the schema documentation, and what lets git track the folder.
- The layout comes from the author's source setup, with its data stripped and its data rules kept. Its playbook rules moved into the skills.
