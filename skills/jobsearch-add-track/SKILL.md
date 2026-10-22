---
name: jobsearch-add-track
description: Set up a new job-search track, a role family searched on its own. Researches what the role is called on LinkedIn and what postings ask for, settles the keywords and a base resume with the user, writes the track and its first market report, and schedules its discovery and weekly market jobs. Use when the user wants to target a new kind of role, or asks to add or set up a track.
---

# Add a track

First run `uv run ${HERMES_SKILL_DIR}/../jobsearch-init/scripts/preflight.py`, unless it already passed in this session. On any problem, stop and give the user its `problems` as they are.

`tracks/README.md` says what a track is and owns, and gives the file format. This is a conversation: stop at each decision below and let the user make it.

## 1. The role

Count the tracks in `tracks/`, its README aside. At `caps.max_tracks` from `workspace.yaml`, refuse, and say that pausing or removing a track, or raising the cap, makes room.

Get the role family in the user's words and pick a kebab-case slug. Read `criteria.md` and the existing tracks, and say so when the new role overlaps one, since a job id belongs to whichever track finds it first.

## 2. Research on LinkedIn

Find what employers call the role and what they ask for, in about 8 searches and 10 postings read.

- `search_jobs` with each candidate title, built as step 2 of jobsearch-discover builds them from `criteria.md` (place in the keywords, no search filters), with `date_posted: past_month` and `max_pages: 1`. Include titles in every working language `criteria.md` lists. The result titles show which keyword returns the role and which returns noise.
- `get_job_details` on the postings that look like the role: salary, years asked, the tools named, recurring duties, the words employers use.

Report a table of titles: what each covers, examples, whether it's worth a keyword. The user picks the keywords and exclusions.

## 3. The track file

Write `tracks/<track>.md`. Under `## Keywords`, list the titles left out and why, so later analyses don't research them again. Set `discovery` 30 minutes after the latest existing track's, or ask the user for a time when it's the first. Set `pages` so a run's searches fit `caps.max_search_pages_per_run`.

Postings in another track's `market/` can belong here. Name them, and when the user agrees, move them to `market/<track>/postings/` and set `track` on their pipeline entries, in `archive/pipeline/` too.

## 4. The base resume

Write `resumes/<track>.yaml` with the jobsearch-resume skill, from the positioning the research supports, and go through it with the user. It's done when the `resume check` passes. Facts the user gives go into `profile/` first.

## 5. Market

- Postings read in step 2 that fall inside the new scope go through steps 4 and 5 of jobsearch-discover: a posting file, then a pipeline entry or a `skipped.md` row.
- Write `market/<track>/report.md` as a first draft: the titles table, what recurs across postings, gaps against the profile, tailoring per family. Say that the first weekly analysis replaces it.

## 6. The scheduled jobs

Create both jobs with the delivery target in `reports` from `workspace.yaml`. Their prompts name the skill and the track and nothing else, since the rules live in the skills:

```bash
hermes cron create "<discovery>" "Run jobsearch-discover for track <track>." \
  --skill jobsearch-scheduled-run --skill jobsearch-discover --name "Job discovery, <track>" --workdir ~/jobsearch --deliver <reports>
hermes cron create "<schedule>" "Run jobsearch-analyze-market for track <track>." \
  --skill jobsearch-scheduled-run --skill jobsearch-analyze-market --name "Market analysis, <track>" --workdir ~/jobsearch --deliver <reports>
```

The market job runs Fridays, from 21:00 for the first track and 30 minutes after the latest existing one for the next. Check both with `hermes cron list`: schedule, workdir, delivery, enabled. Don't trigger a run without the user's go.

## 7. Report

The keywords and exclusions, the resume and what's open on it, postings moved or created, and the jobs' schedules and first runs.
