`hermes-linkedin-jobsearch`: a [Hermes Agent profile distribution](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions) that installs a job-search agent built on LinkedIn. The agent finds postings, researches companies, tailors resumes, submits Easy Apply with approval and tracks applications. Users install it with `hermes profile install github.com/shbernal/hermes-linkedin-jobsearch --alias`.

- Key commands
  - `hermes profile install ./ --name jobsearch-test --alias -y` installs the working tree as a test profile
  - `hermes profile update jobsearch-test` picks up local changes
  - `uv run skills/jobsearch-init/scripts/sync-config.py --config config.yaml --check` checks that `config.yaml` carries the LinkedIn server the init skill records (also run by CI)
  - A fork bump: tag the fork `jobsearch-v<n>`, update `LINKEDIN` in `sync-config.py` and `config.yaml`, release the distribution

- Key documentation
  - [GLOSSARY.md](GLOSSARY.md): the domain terms. Use them, and avoid the words under `_Avoid_`
  - [docs/adr/](docs/adr/README.md): the architecture decisions this repo implements
  - [CHANGELOG.md](CHANGELOG.md) for version bumps
  - The skills are ported from the author's private job-search setup, which the implementation plan names. Port its logic, never its data.

- Rules
  - Everything personal lives in the user's workspace (`criteria.md`, `workspace.yaml`, `profile/`). The skills contain no names, places, paths or caps.
  - Outside actions follow the `autonomy:` block in `workspace.yaml`. A skill never holds a permission of its own.
  - Only the paths in `distribution_owned` reach a user's profile. Repo files (README, docs, CI) stay in the repo.
  - No symlinks anywhere in the repo: the Hermes installer rejects the whole distribution, even for a link outside `distribution_owned`.

- Iron Laws
  - State of the art AI models/harnesses need minimal guidance. Don't repeat yourself, don't babysit, don't be over-specific.
  - Only document items here when model diverges repeatedly from expected behavior. Don't document behaviors implemented without errors.
  - No journaling: code comments / documentation describe current state, they don't carry a log of their own edit history.
