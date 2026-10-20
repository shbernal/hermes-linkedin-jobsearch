---
name: jobsearch-discover
description: Find new LinkedIn postings for one job-search track, score their fit and add them to the pipeline. Use when a discovery run names a track, or the user asks to look for new jobs.
---

# Discover jobs

First run `uv run ${HERMES_SKILL_DIR}/../jobsearch-init/scripts/preflight.py`, unless it already passed in this session. On any problem, stop and give the user its `problems` as they are.

The run names one track. `tracks/<track>.md` gives its keywords, families, fit points and `pages`, `criteria.md` the rules every track shares, and the workspace READMEs every file format.

1. Collect the `linkedin_job_id`s already in `pipeline/`, `archive/pipeline/` and `pipeline/skipped.md`, whatever their track.
2. Run `search_jobs` once per keyword with `date_posted: past_week` and `max_pages` set to the track's `pages`. Build each query from `criteria.md`'s location and remote rules, one pass per arrangement it accepts, with the place and work type inside the keywords: `remote <keyword> in <country>`, `<keyword> in <city>`.
   - LinkedIn's redesigned search keeps only the keywords, the date and paging. Leave `location`, `work_type`, `job_type` and `experience_level` off (a `filters_dropped` error means one was passed), and don't quote keywords. A query with no match returns unrelated postings, which step 3 drops.
   - The track's `pages` limits each query, continuations included. A search that stops on `pagination.reason: time_budget` before reading them has more behind it: call again with the same keywords, `start` set to its `next_offset` and `max_pages` set to the pages left, until the query reads its `pages`, stops on `complete`, or brings no unknown id.
   - The pages read across the run stay within `caps.max_search_pages_per_run` in `workspace.yaml`. Past it, stop searching and say which keywords went unsearched.
   - Only when `autonomy.dismiss_known_jobs` is true, pass the known ids as `dismiss_ids`. It hides them from search for good, at most ten per call.
3. Drop known ids, and drop obvious misses from the result text before fetching anything: off the keyword, outside the accepted locations, companies `criteria.md` rules out, titles carrying its title exclusions. A continued search can repeat ids already seen.
4. `get_job_details` for the rest. The company LinkedIn shows can be an account that posted for the employer (an incubator, a recruiting tool): take the employer from the body. Every posting inside the track's scope gets a `market/<track>/offers/` file, whatever its fit. Then apply `criteria.md`'s hard filters and score.
5. Fit 3 or higher gets a `pipeline/` entry at `new`, `ball: agent`, with the track and `apply: easy_apply` when the button reads Easy Apply, `external` when it reads Apply. An entry at a company another entry holds (see `standby` in `pipeline/README.md`, and `company_hold_days`) starts at `standby` instead. Everything else gets a row in `pipeline/skipped.md` with the reason.
6. Report the new entries sorted by fit, the number skipped, the number dismissed if any, and every MCP failure.

Discovery stops at `new`: it doesn't research companies or shortlist.
