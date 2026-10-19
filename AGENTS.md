`hermes-linkedin-jobsearch`: a [Hermes Agent profile distribution](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions) that installs a job-search agent built on LinkedIn. The agent finds postings, researches companies, tailors resumes, submits Easy Apply with approval and tracks applications. Users install it with `hermes profile install github.com/shbernal/hermes-linkedin-jobsearch --alias`.

- Key commands
  - `hermes profile install ./ --name jobsearch-test --alias -y` installs the working tree as a test profile
  - `hermes profile update jobsearch-test` picks up local changes

- Key documentation
  - [docs/adr/](docs/adr/README.md): the architecture decisions this repo implements
  - The skills are ported from the author's private job-search setup, which the implementation plan names. Port its logic, never its data.

- Rules
  - Everything personal lives in the user's workspace (`criteria.md`, `workspace.yaml`, `profile/`). The skills contain no names, places, paths or caps.
  - Outside actions follow the `autonomy:` block in `workspace.yaml`. A skill never holds a permission of its own.
  - Only the paths in `distribution_owned` reach a user's profile. Repo files (README, docs, CI) stay in the repo.

- Iron Laws
  - Tokens are expensive, state of the art models need minimal guidance, don't repeat yourself, don't babysit, don't be over-specific.
  - AI-native project. All code is AI-generated.
  - Minimal attention when model implements without errors, we document in more detail when model struggles.
  - Do not expect the user to have read each line, don't lose him on the internals, give visibility on a higher-architectural level.
  - No journaling: code comments / documentation describe current state, they don't carry a log of their own edit history.
