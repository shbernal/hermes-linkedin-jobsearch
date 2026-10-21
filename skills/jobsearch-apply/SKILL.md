---
name: jobsearch-apply
description: Send a ready application through Easy Apply or atsfill at the level workspace.yaml allows, or hand it to the user, and record what went out. Use when the user says "apply <n>" or "sent <entry>", or an Advance run may send unattended.
---

# Apply

First run `uv run ${HERMES_SKILL_DIR}/../jobsearch-init/scripts/preflight.py`, unless it already passed in this session. On any problem, stop and give the user its `problems` as they are.

A sent application can't be taken back. "apply <n>" names entries by their number in `pipeline/ready.md`: read it and confirm each name with the user if the list looks stale.

## Who sends

`autonomy.easy_apply` and `autonomy.external_forms` in `workspace.yaml` set each kind:

- `off`: hand-off.
- `approval`: send when the user named the entry in this session.
- `unattended`: send, also from Advance with no one asking.

Before any send:

- The applications already sent today, Easy Apply and external, counted from `applied` in `pipeline/` and `archive/pipeline/`, stay under `caps.max_sends_per_day`. Past it, the entry waits for tomorrow.
- Another live entry at the same company within `company_hold_days`: set this one `standby` as `pipeline/README.md` says, and send nothing.
- `applications/<entry>/answers.md` and the PDF named on the Activity line are on disk. Missing either goes back to jobsearch-prepare-application.

## Easy Apply

1. Dry run: `submit_easy_apply` without `confirm_submit`, answers keyed by the labels the form returned, `follow_company: false`. A field answered `Leave unchanged` is left out of the call.
2. The dry run has to show every step reached, `complete: true`, every required field holding its answer, and the resume named on the form. A refusal is fixed in `answers.md`, then step 1 again. A typeahead nothing reaches, or a refusal the answers can't fix, is a hand-off with the refusal under `## Next action`.
3. `submit_easy_apply` with `confirm_submit`, once. Its `confirmation` proves nothing: `get_job_details` reading `apply: applied` confirms the send. An unclear result is checked that way and never retried, since a second call is a second application.

## External forms

The system's `submit_enabled` in `uvx --prerelease allow atsfill@latest status` has to be true, otherwise it's a hand-off. Rebuild `answers.json` from `answers.md`, then `atsfill send <apply_url> --answers answers.json`, once. Never pass `--resend`.

- `submitted`: the result's evidence goes on the Activity line, and a `warning` goes in the report.
- `refused`: a mismatch or invalid answer is fixed in `answers.md`, dry-run with `atsfill fill`, and sent again. `already_sent` means an earlier attempt may have gone: treat it as `unknown`. `submit_not_enabled` is a hand-off.
- `blocked`: nothing was sent. `login_required` goes to the user with the login command its reason names, a captcha, emailed code or score refusal is a hand-off, and `time_budget` can be retried on a later run.
- `unknown`: submit was clicked with no evidence. Never send again. The entry stays `ready` with `ball: user`, counts against the day's sends, and waits for the confirmation email update-status reads.
- `unsupported`: a hand-off.

## Recording a send

Set `status: applied`, `applied` to the send date, its `history` line, `updated`, and an Activity line naming the evidence. Append `## Sent <date>` to `answers.md` with every field filled and the value it holds, from the read-back for an external form: LinkedIn shows a sent Easy Apply nowhere, so this is the only record of what the company read.

## Hand-off

Set `ball: user` with what to do under `## Next action`, then send the user one message with the apply URL, the PDF's absolute path and the path to `answers.md`. "sent <entry>" from the user records the send as above, with the user as the evidence.

## Report

What went out, with its evidence, what was handed off and why, the answers that rested on a judgment call, and every tool failure.
