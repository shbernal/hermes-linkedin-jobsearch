---
name: jobsearch-resume-market-fit
description: Talk through a track's market report with the user, presenting the qualities postings ask for most and prompting their memory for experiences that could back them better. Use when the user wants to strengthen a track's resume against its market, or to fill gaps in their profile facts.
---

# Resume market fit

First run `uv run ${HERMES_SKILL_DIR}/../jobsearch-init/scripts/preflight.py`, unless it already passed in this session. On any problem, stop and give the user its `problems` as they are.

A conversation, not a report. It uses `market/<track>/report.md` to find experiences worth adding to `profile/`, and better ways to present the ones already there.

## Prepare

Ask which track when the user doesn't name one. Read the report, `tracks/<track>.md`, its resume and `profile/`. Say so when the report is more than a week old.

Rank the qualities by how often postings ask for them, then by how weak the evidence is: gaps and unconfirmed items first, then thin coverage (one line, a course, a side project where offers want real work). Well-covered qualities get only a quick check on wording.

## Discuss

One quality at a time:

- Say what postings ask for, with the share and the words employers use, and what currently backs it.
- Ask concrete questions that jog memory, not "do you have X?". Name situations from the user's own files where it might have happened, and ask what they did, for whom, with what tools, what came of it, and any numbers.
- Look past the obvious file: schoolwork, associations, favors, personal tooling and things too small to mention often hold the evidence.
- When an experience already recorded fits better under another angle, say how the report's vocabulary would describe it.

Two or three questions per turn, then wait. Drop a quality when the user says there's nothing there.

## Record

Facts go into the matching `profile/` file as `profile/README.md` says, dated and attributed to the user, including answers to open questions. Presentation choices go into `## Resume` in `criteria.md`. Resumes aren't edited here: the jobsearch-resume skill does that when the user asks.

## Close

What was added to the profile, which gaps closed or narrowed, which remain, and the resume changes the new facts support.
