# Pipeline

## `<company-slug>--<role-slug>.md`

One job opportunity.

```yaml
---
company: acme                # matches companies/acme.md
track: data-analyst          # tracks/<track>.md, sets the base resume
role: Data Analyst
status: new
ball: agent                  # agent | user | company, who acts next
fit: 4                       # 1-5, see criteria.md
work_type: remote            # remote | hybrid | on_site
location: Lyon
salary: 45-55k€              # as posted, omit when not shown
source: linkedin             # linkedin | linkedin-inbound | referral | other
linkedin_job_id: "4252026496"
url: https://www.linkedin.com/jobs/view/4252026496/
apply: easy_apply            # easy_apply | external
apply_url: https://job-boards.greenhouse.io/acme/jobs/123  # external only, set when preparing
posted: 2026-09-10
found: 2026-09-13
applied: 2026-09-15          # set when it went out
updated: 2026-09-13
history:                     # one line per status change, oldest first
  - 2026-09-13 new
---
```

Statuses:

- `new`: found by discovery, not reviewed
- `shortlisted`: researched and worth applying
- `ready`: drafts in `applications/` done, waiting to be sent
- `standby`: paused without dropping it. `## Next action` names what must happen before it resumes, and the Activity line that paused it names the status it left. Most often another application at the same company (`company_hold_days` in `workspace.yaml`)
- `applied`
- `interviewing`
- `offer`
- `rejected`: the company said no
- `dropped`: the user or the agent said no, with the reason in the body
- `closed`: the posting stopped taking applications before the user applied
- `ghosted`: no answer `ghosted_after_weeks` after `applied`

`history` dates every status the entry has held, `YYYY-MM-DD <status>`, and its last line matches `status`. Whoever changes `status` appends a line with the date the change happened, not the date it was recorded. Leaving `standby` is a line of its own.

`ball` says who acts next and `## Next action` says what. Whoever changes an entry sets both. By default `new`, `shortlisted` and `ready` are the agent's, and `applied`, `interviewing` and `offer` the company's. A `ready` entry the agent may not or can't send (its `autonomy` level is `off`, or atsfill doesn't support the form) is the user's. A `standby` entry belongs to whoever controls what resumes it. An entry leaves the default when something specific waits: a question only the user can settle, a form the tool refused, a reply to draft, an interview to prepare. An ended entry drops the field.

Body sections: `## Fit` (why this score), `## Next action`, `## Activity` (dated one-liners: drafts ready, applied, interview). A status change names its source: `2026-09-21 rejected, email from the recruiter`.

An entry that becomes `rejected`, `dropped`, `closed` or `ghosted` is closed out by whichever step set the status: see `archive/README.md`.

## `skipped.md`

Jobs discovery fetched and rejected, one table row each, so later runs skip the id without fetching it again. Postings dropped from the search result text alone aren't recorded.

```markdown
# Skipped jobs

| Date | LinkedIn job id | Company | Title | Reason |
|------|-----------------|---------|-------|--------|
| 2026-09-13 | 4466715378 | Acme | Senior Data Analyst | 5+ years |
```

## `ready.md`

The numbered list of entries waiting for the user's go to send. Advance rewrites it whole at the end of each run, and its report ends with the same list. A reply that picks numbers ("apply 1 and 3") refers to this file, so the numbers hold until the next rewrite.

```markdown
# Ready to send

Updated 2026-09-15 09:30

1. acme--data-analyst · Acme, Data Analyst · easy_apply · fit 4 · 45-55k€
2. globex--product-analyst · Globex, Product Analyst · easy_apply · fit 3 · not disclosed
```
