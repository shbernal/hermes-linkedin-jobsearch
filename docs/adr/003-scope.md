# 003 Scope

Status: accepted

## Context

This agent comes from a personal job-search setup that has been running daily. A later project of the same author takes a different approach to the same problem. This project solves it mainly through LinkedIn: LinkedIn search and Easy Apply, an agent that prepares every application, and a user who submits external forms themselves.

## Decision

hermes-linkedin-jobsearch is a separate product from that later project, not an early version of it.

v1 ships:

| Capability | Skill |
|---|---|
| Find postings for a track and score their fit | discover |
| Weekly report on what a track's postings ask for | analyze-market |
| Company dossier, then shortlist or drop | research-company |
| Tailored resume, answers and form reading | prepare-application |
| Submit Easy Apply, hand external forms to the user | apply |
| Statuses from LinkedIn and, if set up, email | update-status |
| Add a role family to search | add-track |
| Resume writing and checks | resume skills |
| Workspace setup | jobsearch-init |

Out of v1:

- **The agent never fills or submits external forms.** prepare-application reads the form with `atsfill read` and writes the answers, and the user submits. atsfill's `fill` and `send` are blocked ([005](005-dependencies.md)).
- **Welcome to the Jungle**, for both discovery and sending.
- **atsfill `fill` and `send`.**
- **A hiring-forms MCP.**
- **outreach**, which was never run, and with it every message or connection request.
- **freehire**, which no workflow uses yet.
- **The third-party dev skills** (grilling, idea-refine, doubt-driven-development).

## Consequences

- apply is an Easy Apply procedure and a hand-off. The source's per-system sending notes are dropped, and the few quirks needed to read a form go into a reference used by prepare-application.
- The roadmap lists atsfill sending and WTTJ as the next steps, so it's clear they were left out on purpose.
