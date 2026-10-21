---
name: jobsearch-update-status
description: Bring every open application up to date from LinkedIn, the user's email when it's set up, and what the user says, then close out the entries that ended. Use for the Tracking run, or when the user reports news on an application ("I got rejected from Acme").
---

# Update status

First run `uv run ${HERMES_SKILL_DIR}/../jobsearch-init/scripts/preflight.py`, unless it already passed in this session. On any problem, stop and give the user its `problems` as they are.

Open means `ready`, `applied`, `interviewing`, `offer` or `standby` in `pipeline/`.

## Evidence

A status changes only on evidence, and its Activity line names the source: `2026-09-21 applied, Greenhouse confirmation email`.

- The user saying so is enough.
- `applied` also takes a confirmation email, the job in `get_saved_jobs` at `stage: applied`, or `get_job_details` reading `apply: applied`. Never presume a `ready` entry went out.

## Steps

1. Email, only when the himalaya skill is loaded and `himalaya account list` shows an account. Otherwise this run is LinkedIn only, and the report says so once. Following the himalaya skill, one `envelope search` over the inbox per open entry, since its drafts were ready, matching the company across `subject`, `body` and `from`: hiring systems send from their own domains with the company in the subject or body. Read the matches.
2. LinkedIn:
   - `get_saved_jobs` with `stage: applied`, once, for the `ready` entries. Raise `max_pages` when an old application is missing from the first pages.
   - `get_inbox`, then `get_conversation` on threads with recruiters, tracked companies or people from the dossiers. A new inbound opportunity gets a pipeline entry with `source: linkedin-inbound` at `new`.
   - `get_job_details` only for `ready` entries still without evidence: its `apply` field reads `applied` or `closed`. Not `get_job_apply_url`, which leaves a "did you apply?" prompt on the posting.
3. Update each entry as `pipeline/README.md` says: `status` and its `history` line, `ball`, `applied`, `updated`, an Activity line per event.
   - A closed posting with no evidence of applying becomes `closed`.
   - `applied` for `ghosted_after_weeks` with no answer becomes `ghosted`.
   - A `standby` entry whose company is free again under `company_hold_days` goes back to the status it left, `ball: agent`, with the reason. When several wait at one company, only the highest fit.
   - Small work an event asks of the user, such as a reply, is drafted here and the entry goes to `ball: user`. Heavier work, such as interview prep, goes to `ball: agent` under `## Next action` for jobsearch-advance.
4. Close out every entry that ended as `archive/README.md` says. On LinkedIn: `unsave_job` for a saved job, `archive_job` for one in the Applied tab, `archive_conversation` for a thread whose outcome is settled, with or without a pipeline entry. A thread that still expects a reply from the user stays. Count today's close-outs from the Activity lines against `caps.max_close_outs_per_day`. Past it, they wait for the next run.
5. Archive email only when `autonomy.archive_email` is true: what needs nothing more from the user, such as receipts, rejections and automated updates. Anything that asks the user something stays in the inbox.

## Report

- Status changes, each with its source.
- Emails and LinkedIn threads waiting on the user, each with a draft reply. Nothing is ever sent.
- `ready` entries with no evidence 3 days after their drafts: ask whether the user applied or wants to drop them.
- The day's first report lists every entry at `ball: user`, with what it waits on and since when.
- Close-outs that failed, and every LinkedIn or himalaya failure.
