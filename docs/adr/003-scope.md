# 003 Scope

Status: accepted

## Context

This agent comes from a personal job-search setup that has been running daily. `hermes-careers`, a later project, takes a different approach to the same problem. This project solves it mainly through LinkedIn: LinkedIn search and Easy Apply, an agent that prepares every application, and a user who submits external forms themselves.

## Decision

hermes-linkedin-jobsearch is a separate product from hermes-careers, not an early version of it.

v1 ships:

| Capability | Skill | From |
|---|---|---|
| Find postings for a track and score their fit | discover | `workflows/discover-jobs.md` |
| Weekly report on what a track's postings ask for | analyze-market | `workflows/analyze-market.md` |
| Company dossier, then shortlist or drop | research-company | `workflows/research-company.md` |
| Tailored resume, answers and form reading | prepare-application | `workflows/prepare-application.md` |
| Submit Easy Apply, hand external forms to the user | apply | `workflows/apply.md`, revised |
| Statuses from LinkedIn and, if set up, email | update-status | `workflows/update-status.md` |
| Add a role family to search | add-track | `create-job-track` skill |
| Resume writing and checks | resume skills | `resume-management`, `write-resume`, `resume-market-fit` |
| Workspace setup | jobsearch-init | new, [002](002-workspace-init.md) |

Out of v1:

- **The agent never fills or submits external forms.** prepare-application reads the form with `atsfill read` and writes the answers, and the user submits. atsfill's `fill` and `send` are blocked ([005](005-dependencies.md)).
- **Welcome to the Jungle**, for both discovery and sending.
- **atsfill `fill` and `send`.**
- **The hiring-forms MCP** from NEXT-ARCHITECTURE.
- **outreach**, which was never run, and with it every message or connection request.
- **freehire**, which no workflow uses yet.
- **The third-party dev skills** (grilling, idea-refine, doubt-driven-development).

## Consequences

- `apply.md` is reduced to an Easy Apply procedure and a hand-off. Its per-system sending notes are dropped. The few quirks needed to read a form go into a reference used by prepare-application.
- The roadmap lists atsfill sending and WTTJ as the next steps, so it's clear they were left out on purpose.
