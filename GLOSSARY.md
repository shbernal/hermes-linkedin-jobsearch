# hermes-linkedin-jobsearch

A job-search agent that moves LinkedIn postings through a pipeline, from discovery to an answer from the employer, inside a git workspace owned by the user.

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
The settings in `workspace.yaml` that decide which outside actions the agent takes without the user's go. No skill grants one of its own.
_Avoid_: permissions, policy

**Limits**:
The settings in `workspace.yaml` that bound how much of what autonomy allows happens: sends and close-outs per day, search pages per run, tracks.
_Avoid_: caps, quotas

## Search

**Track**:
One kind of role searched on its own, with its keywords, base resume, market data and scheduled runs.
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
Who acts next on an entry: `agent`, `user` or `employer`.
_Avoid_: owner, assignee

**Employer**:
The organization a posting hires for, which can differ from the account that posted it on LinkedIn.
_Avoid_: company

**Dossier**:
The file in `employers/` describing one employer, shared by all its entries.
_Avoid_: employer profile, research

**Application**:
An entry once it has been sent, from `applied` on.
_Avoid_: submission

**Drafts**:
The folder in `applications/` for one entry: tailored resume, answers, interview prep.
_Avoid_: application (for the folder)

**Ready list**:
`pipeline/ready.md`, the numbered entries waiting for the user's go. Numbers in a reply refer to it.
_Avoid_: queue, shortlist

**Close-out**:
Ending an entry: archiving its files and tidying its LinkedIn job, conversations and emails.
_Avoid_: cleanup

**Employer hold**:
The rule that an employer gets one live application at a time: its other entries wait in `standby` until it answers or `days_before_reapplying_to_unanswered_employer` pass.
_Avoid_: company hold, cooldown

## Sending

**Send**:
Getting an entry's drafts to the employer, through Easy Apply or an external form, which makes it an application. Counted against `max_applications_sent_per_day`.
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
A cron job of the profile, run with nobody there to approve or answer. Its report goes to the `report_delivery_target`.
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

- **Offer** means only the `offer` status, a job offer from the employer. The job ad is a **posting**, stored in `market/<track>/postings/`.
- **Application** is a sent entry. Its folder in `applications/` is its **drafts**, the act of sending is a **send**, and an entry not yet sent is no application.
- **LinkedIn job** is LinkedIn's own record of a posting, the thing saved, archived or dismissed there. In the workspace it is a **posting**.
- **Family** is only the sub-group within a track. A track is a kind of role, not a "role family".
