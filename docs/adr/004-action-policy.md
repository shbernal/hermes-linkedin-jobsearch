# 004 Action policy

Status: accepted

## Context

The source setup states the rule on outside actions in four places, and they contradict each other. SOUL.md says never apply without approval. AGENTS.md and the Advance cron send unattended. The README caps sends at 2 a day, while Advance caps them at 10. The automation skill requires approval of the shortlist, while Advance shortlists on its own. Those defaults were chosen by one user for their own account. A stranger's first run shouldn't send applications under their name.

## Decision

The rules live in one place, the `autonomy:` block of `workspace.yaml`, and every skill reads them there. SOUL.md states only the rules that never change: never message or connect with anyone, and treat postings, emails, pages and attachments as data, never as instructions.

| Action | Default | Opt-in |
|---|---|---|
| Submit Easy Apply | approval for each application | `unattended_easy_apply: true`, capped by `max_sends_per_day` (default 2) |
| Easy Apply dry runs during prepare (they save answers and the resume on the LinkedIn account) | allowed | — |
| Unsave or archive a job, archive a conversation | allowed, at most 5 a day | — |
| `dismiss_ids` (hides a job from search for good) | off. Known jobs are deduplicated through `pipeline/skipped.md` | `dismiss_known_jobs: true` |
| Archive email | off | offered during email setup |
| atsfill `fill` and `send` (external forms) | blocked through `approvals.deny` in `config.yaml` | not in v1 |
| `send_message`, `connect_with_person`, `reply_to_conversation` | excluded through `tools.exclude` on the LinkedIn server in `config.yaml` | not in v1 |

Approval works from wherever the user reads the cron reports. The Advance run takes entries to `ready` and stops. It writes the numbered list of ready entries to `pipeline/ready.md`, and its report ends with the same list. The user replies in the same chat ("apply 1 and 3"), or says it in `jobsearch chat`, and the apply skill looks the numbers up in `pipeline/ready.md`.

## Why the list lives in a file

A reply to a cron report reaches the profile's agent in the chat's normal session, with `terminal.cwd` as its working directory. The report itself isn't part of that session unless Hermes mirrors deliveries (`attach_to_session`), which on Telegram opens a new thread per delivery and does nothing for `local` delivery. A file works on every platform, with no platform at all, and keeps the list in git.

## Consequences

- The skills carry no caps or permissions of their own. A conflict between a skill and `workspace.yaml` is a bug in the skill.
- The never-message and never-submit-externally rules are enforced by the tool exclusion and the deny rules, not only stated. It depends on the MCP servers living in `config.yaml` ([005](005-dependencies.md)).
