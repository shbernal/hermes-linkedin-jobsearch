# hermes-linkedin-jobsearch

A job-search agent that moves LinkedIn postings through a pipeline, from discovery to an answer from the company, inside a git workspace owned by the user.

## Workspace

**Workspace**:
The user's `~/jobsearch` git repository, holding every piece of personal data and state. The distribution never writes it on update.
_Avoid_: profile folder, data dir

**Profile**:
The installed Hermes profile: skills, `SOUL.md` and `config.yaml`, no personal data.
_Avoid_: agent, install

**Profile facts**:
The files under `profile/`, the only source a resume line or form answer may draw from.
_Avoid_: candidate data, background

**Criteria**:
`criteria.md`: what the user looks for, their standing answers and how fit is scored.
_Avoid_: preferences, filters

**Autonomy**:
The `autonomy:` block of `workspace.yaml`, the only place an outside action gets its permission.
_Avoid_: permissions, policy

## Search

**Track**:
One role family searched on its own, with its keywords, base resume, market data and cron jobs.
_Avoid_: search, role, campaign

**Family**:
A sub-group within a track that its market report counts separately.
_Avoid_: category, cluster

**Posting**:
A job ad as published on LinkedIn or a hiring system.
_Avoid_: offer, job, listing

**Market report**:
The weekly analysis of a track's fetched postings: what they ask for and how the resume should answer.
_Avoid_: market analysis

## Pipeline

**Entry**:
One file in `pipeline/`: a posting the agent is pursuing, with its status, ball and history.
_Avoid_: opportunity, application, job

**Status**:
Where an entry stands: `new`, `shortlisted`, `ready`, `standby`, `applied`, `interviewing`, `offer`, or one of the ended statuses `rejected`, `dropped`, `closed`, `ghosted`.
_Avoid_: stage, state

**Ball**:
Who acts next on an entry: `agent`, `user` or `company`.
_Avoid_: owner, assignee

**Dossier**:
The file in `companies/` describing one company, shared by all its entries.
_Avoid_: company profile, research

**Application**:
The drafts folder in `applications/` for one entry: tailored resume, answers, interview prep.
_Avoid_: submission

**Ready list**:
`pipeline/ready.md`, the numbered entries waiting for the user's go. Numbers in a reply refer to it.
_Avoid_: queue, shortlist

**Close-out**:
Ending an entry: archiving its files and tidying its LinkedIn job, conversations and emails.
_Avoid_: cleanup

**Company hold**:
The rule that one live application per company pauses the others in `standby`.
_Avoid_: cooldown

## Sending

**Send**:
Submitting an application to the company, through Easy Apply or an external form. Counted against `max_sends_per_day`.
_Avoid_: apply (as a verb for the act itself), submit

**Easy Apply**:
LinkedIn's in-site application form, sent through the fork's `submit_easy_apply`.

**External form**:
A hiring-system form outside LinkedIn, read, filled and sent through atsfill.
_Avoid_: ATS form, career page

**Dry run**:
Filling a form without sending it. It can still save answers and the resume on the hiring system.
_Avoid_: test run, preview

## Runs

**Scheduled run**:
A cron job of the profile, run with nobody there to approve or answer. Its report goes to the `reports` target.
_Avoid_: cron, job

**Advance**:
The scheduled run that works the agent's furthest-along entry until the ball leaves the agent, then rewrites the ready list.

**Tracking**:
The scheduled run that updates statuses from LinkedIn and, if set up, email.
_Avoid_: sync, status check

**Pre-run check**:
`preflight.py`, run before each skill: workspace schema version and the LinkedIn server config.
_Avoid_: preflight (in prose), health check

## Flagged ambiguities

- **Offer** means only the `offer` status, a job offer from the company. The job ad is a **posting**, even though the `market/<track>/offers/` folder keeps the older word.
- **Application** is the drafts folder, not the act of sending it, which is a **send**, nor the pipeline file, which is an **entry**.
