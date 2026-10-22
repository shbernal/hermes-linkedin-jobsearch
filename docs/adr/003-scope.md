# 003 Scope

Status: accepted

## Context

This agent comes from a personal job-search setup that has been running daily. A later project of the same author takes a different approach to the same problem. This project solves it mainly through LinkedIn: LinkedIn search and Easy Apply, an agent that prepares every application, and atsfill for external forms.

## Decision

hermes-linkedin-jobsearch is a separate product from that later project, not an early version of it.

v1 ships:

| Capability | Skill |
|---|---|
| Find postings for a track and score their fit | discover |
| Weekly report on what a track's postings ask for | analyze-market |
| Company dossier, then shortlist or drop | research-company |
| Tailored resume, answers and form reading | prepare-application |
| Submit Easy Apply and external forms at the level `autonomy` sets, or hand them to the user | apply |
| Statuses from LinkedIn and, if set up, email | update-status |
| Add a role family to search | add-track |
| Resume writing and checks | resume skills |
| Workspace setup | jobsearch-init |

Out of v1:

- **Sending through anything but atsfill.** A form atsfill doesn't support is read with Hermes' browser and goes to the user.
- **Welcome to the Jungle discovery.** WTTJ forms reached from LinkedIn are sent like any atsfill system.
- **A hiring-forms MCP.**
- **outreach**, which was never run, and with it every message or connection request.
- **freehire**, which no workflow uses yet.
- **The third-party dev skills** (grilling, idea-refine, doubt-driven-development).

## Consequences

- External sending is an opt-in ([004](004-action-policy.md)), and atsfill's own `submit` list picks the systems that may receive one.
- apply handles atsfill's result statuses in general. The source's per-system sending notes are dropped: system quirks belong in atsfill.
