---
name: jobsearch-research-company
description: Create or refresh a company dossier for a company with a new pipeline entry, then settle the entry as shortlisted, dropped or closed. Use when a new entry needs research, or the user asks about a company in the pipeline.
---

# Research company

First run `uv run ${HERMES_SKILL_DIR}/../jobsearch-init/scripts/preflight.py`, unless it already passed in this session. On any problem, stop and give the user its `problems` as they are.

A dossier refreshed in the last few days is reused as is.

1. Find the LinkedIn company name with `search_companies` if needed, then `get_company_profile` with `sections: posts,jobs`.
2. `get_company_employees` for headcount by function and location.
3. Founders and people in the functions the track works with, through `search_people` with the company URN from the profile as `current_company`. A second pass with `network: [1st, 2nd]` shows who could refer. This is reading only: nobody is contacted.
4. Funding stage and recent rounds on the web when LinkedIn doesn't show them, keeping the source URLs.
5. Write `companies/<slug>.md` as `companies/README.md` says.
6. Settle each `new` entry at this company, with the reason on its Activity line and the dossier as the source:
   - The posting stopped taking applications: `closed`. Check this first, since nothing else matters once it's gone.
   - A hard filter from `criteria.md` that the dossier disproves: `dropped`.
   - Otherwise `shortlisted`. A doubt the hard filters don't settle shortlists the entry and is reported, since an entry nobody acts on is worse than an application the user cancels.

   `closed` and `dropped` entries are closed out right away as `archive/README.md` says, LinkedIn close-outs within `caps.max_close_outs_per_day` and email archiving only when `autonomy.archive_email` allows it. When the research itself fails, the entry stays `new` and its Activity line says the run failed, so a later run can tell it from a settled one.
