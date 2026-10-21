---
name: jobsearch-advance
description: Take the pipeline entry the agent holds that is furthest along and work it until the ball leaves the agent, through research and preparation to ready, then list what waits to be sent in pipeline/ready.md. Use for the Advance run, or when the user asks to move the pipeline forward.
---

# Advance

First run `uv run ${HERMES_SKILL_DIR}/../jobsearch-init/scripts/preflight.py`, unless it already passed in this session. On any problem, stop and give the user its `problems` as they are.

## Selection

Among the entries with `ball: agent`, finish what's started before opening anything new: furthest along first (`offer`, `interviewing`, `applied`, `ready`, `shortlisted`, then `new`), then highest fit, then oldest `updated`. Skip an entry whose Activity records a step that failed today, so a broken step waits a day instead of repeating each run, and a `ready` entry once today's sends reach `caps.max_sends_per_day`. When the entry stops on such a block, take the next one.

No entry to work on, and `pipeline/ready.md` unchanged: reply `[SILENT]`.

## Steps

Run what the status calls for, then look again, until the entry is no longer the agent's or has ended:

- `new`: the jobsearch-research-company skill.
- `shortlisted`: the jobsearch-prepare-application skill. `ready` only once every draft it lists exists and checks.
- `ready`: the jobsearch-apply skill when `autonomy` sets this entry's kind (`easy_apply` or `external_forms`) to `unattended`. Otherwise it stops here for the user.
- Any other status: the work under `## Next action`, such as interview prep. What would go out to someone is drafted for the user.

A failed step leaves the entry where it was, still the agent's, with an Activity line saying the step failed rather than what it would have found.

## Ready list

Rewrite `pipeline/ready.md` as `pipeline/README.md` gives it: every `ready` entry, highest fit first. Its numbers are what "apply 1 and 3" refers to, so write it even when nothing else changed, and commit it.

## Report

As the jobsearch-scheduled-run skill gives it, for the entry worked:

- `Changed`: the steps done, the drafts produced, a send with its evidence, or why it closed or dropped.
- `Decisions`: what it waits on from the user, the answers resting on a judgment call, the requirement gaps, what to review first.
- `Failed`: every tool, form, renderer or validation failure, and every send refused.
- `Next`: who holds the ball and what they do.

End with the numbered list from `pipeline/ready.md`, and how to answer it: "apply <n>", or "sent <entry>" for one the user sends.
