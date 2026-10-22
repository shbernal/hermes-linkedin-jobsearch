---
name: jobsearch-prepare-application
description: Draft what a shortlisted pipeline entry needs to apply, a tailored resume and an answer to every form question, and take it to ready. Use when an entry is shortlisted, or the user asks to prepare an application.
---

# Prepare application

First run `uv run ${HERMES_SKILL_DIR}/../jobsearch-init/scripts/preflight.py`, unless it already passed in this session. On any problem, stop and give the user its `problems` as they are.

The entry ends at `ready`, and the jobsearch-apply skill sends it. Reading a form never submits it, on LinkedIn or anywhere else.

1. Read the pipeline entry, its posting in `market/<track>/postings/`, the dossier in `companies/`, the family's section of `market/<track>/report.md`, `criteria.md` and `profile/`.
2. An entry without `apply`, or `external` without `apply_url`, gets both from one `get_job_apply_url` call. `applied` or `closed` ends the run: report it. `unknown` on an open external posting is a tool failure, as SOUL.md says.
3. Tailor `applications/<entry>/resume.yaml` and export its PDF with the jobsearch-resume skill. When the export refuses a second page, cut the line that matters least for this posting and retry.
4. Read the form's questions:
   - `easy_apply`: one `get_easy_apply_form` call. With `complete: false`, read the rest by walking the form with `submit_easy_apply` dry runs (no `confirm_submit`): answer the field it stopped on, and each refusal names the next unanswered field, until the walk returns `complete: true`. LinkedIn leaves the mobile phone empty on the contact step, so the walk answers it from `profile/about.md`. Every dry run writes to the account: LinkedIn keeps the answers and preselects an uploaded resume next time.
   - `external`: `uvx --prerelease allow atsfill@latest read <apply_url>`. Each field comes back with an `id`, which `answers.md` records. Then write `answers.json` and dry-run it with `atsfill fill <apply_url> --answers answers.json`, until it ends `ready` with every field reading back `match`. A `blocked: login_required` goes to the user with the command its reason names.
   - atsfill `unsupported`: read the page with the built-in browser, following a job page's apply button to the form. Read label, type, required, options and character limits, stop at a captcha challenge, and never type into it. This form goes to the user. A form behind an account is `Form: account required`.
   - An apply link that ends on a 404 or "no longer available" page means the posting is gone: set `closed` and close it out as `archive/README.md` says.
   - What no tool could read, the user opens or pastes.
5. Write `answers.md` as `applications/README.md` says, from `profile/` and the standing answers in `criteria.md`. Answer every question, including the ones nothing covers, since the send composes nothing of its own. A question that needs the user's call is answered with a proposal and the entry takes `ball: user` with that question under `## Next action`.
6. Set `ready` with its `history` line and `updated`, and add an Activity line naming the PDF and the renderer from `cratecv --version`. A form atsfill doesn't support, or an `autonomy` level of `off` for its kind, makes it the user's (`ball: user`).
7. Report the requirement gaps, the answers resting on a judgment call, and which lines to check first.
