---
name: jobsearch-analyze-market
description: Work out what one track's postings ask for and how its base resume should change to match, rewriting market/<track>/report.md. Use for the weekly market run of a track, or when the user asks what a role's postings want.
---

# Analyze market

First run `uv run ${HERMES_SKILL_DIR}/../jobsearch-init/scripts/preflight.py`. On any problem, stop and give the user its `problems` as they are.

Suggestions only use experience that is on the resume or recorded in `profile/`, never invented.

1. Load every file in `market/<track>/offers/`. The main sample is postings at the level and contract `criteria.md` targets. More senior postings go into a short separate note on what the role asks for later in a career.
2. If a family has fewer than 15 offers in the main sample, run the jobsearch-discover skill for the track with `date_posted: past_month`, capped at 15 `get_job_details` calls. Skip it when a discovery run happened in the last few days, and say so in the report.
3. Count tags per family from the frontmatter: the share of offers listing each `must_have` and `nice_to_have` tag, years required, languages. Read the requirement and responsibility text for recurring duties and the exact words employers use.
4. Compare with `resumes/<track>.yaml` and `profile/`. Put each frequent tag in one bucket:
   - covered: on the resume or in the profile, citing the line or file
   - worded differently: the resume says "automated flows", offers say "workflow automation"
   - unconfirmed: likely true but written nowhere. Ask the user, and record what they confirm in `profile/`
   - gap: missing. Say whether a small project could close it
5. Rewrite `market/<track>/report.md`:
   - Sample: offers per family, posting date range
   - One section per family: top requirements with shares, years asked, languages, recurring responsibilities, phrases worth reusing
   - Resume match: the four buckets
   - Tailoring per family: a summary line, which lines to lead with and which to cut, the skills line in the offers' vocabulary

Report the families whose tailoring moved, the unconfirmed facts and closable gaps, and whether the track's resume needs rework.
