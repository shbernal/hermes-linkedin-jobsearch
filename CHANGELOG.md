# Changelog

## 0.2.0

- Workspace `schema_version: 2`: self-explanatory `workspace.yaml` keys in autonomy, limits and timings sections, `employers/` for `companies/`, `market/<track>/postings/` for `offers/`, and `employer` for the `company` field and ball value. `/jobsearch-init` migrates a version 1 workspace.
- Tool and skill failures are recorded in `issues/` and filed upstream as `file_github_issues` allows.
- LinkedIn server pinned to `jobsearch-v3-rc1`. Run `/jobsearch-init` after updating, since an update keeps your `config.yaml`.
- Follows atsfill's `submit-allowed` config key, one-line results and newer result codes.
- A closed posting is checked for a live repost, a status the user names is where Advance stops, and a confirmed answer is kept in `answers.md`.

## 0.1.0

First release: discovery, company research, application preparation, Easy Apply and atsfill sending, status tracking and market reports on LinkedIn, set up by `/jobsearch-init`.
