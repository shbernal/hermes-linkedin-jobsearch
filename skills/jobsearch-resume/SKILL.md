---
name: jobsearch-resume
description: Write, tailor, review and export the user's resumes, the cratecv YAML files in resumes/ and applications/<entry>/resume.yaml. Use whenever a resume line is written, cut, reordered or reworded, when an application needs a resume, or to render one to PDF. Covers what earns a line, sources, wording, filling the page and exporting. The YAML format and layout report belong to the cratecv skill.
---

# Resume

First run `uv run ${HERMES_SKILL_DIR}/../jobsearch-init/scripts/preflight.py`. On any problem, stop and give the user its `problems` as they are.

You are on the user's side. The resume exists to get them an interview: find what in `profile/` makes them worth one and put it on a full page, in words a recruiter for that role understands.

| What | Where |
| --- | --- |
| Every fact about the user | `profile/`, as its README says |
| One base resume per track | `resumes/<track>.yaml` |
| The tailored copy | `applications/<entry>/resume.yaml`, a copy of the track's base |
| How the user likes their resumes | `## Resume` in `criteria.md` |
| What a track's postings want | `market/<track>/report.md` |

The preferences in `criteria.md` are followed unless an offer makes another choice better, and then the report says so. A preference the user states goes there, with its date.

## The loop

1. Read the `profile/` files behind the entries you keep, the offer when there is one, and the preferences.
2. Draft or edit the YAML.
3. Run the value check below on every line.
4. Run the layout check and fix what it finds, as the cratecv skill says.
5. Fill the page, then report.

## Sources

Every line carries `source:`, a path relative to `profile/` or a list of them. The check is about traceability, not proof.

- The user's word is a source. A fact they give, or a line they ask to keep that nothing documents, goes into the matching profile file first, dated and attributed to them, and the line cites that file.
- Never drop a line for lack of evidence without saying so. Small jobs leave no records: ask, take the answer, record it.
- Don't invent. No number, tool, client, title or result that nobody stated. What the offer asks for and the profile lacks is reported as a gap.
- Earlier resume wording in a profile file is usable, but prefer what the user did. If you reuse a quote, confirm it with the user and move it into the body.

## Every line earns its place

For each line, answer: what does a recruiter for this role now believe about the user that they didn't before? A line that names a task given and stops there fails. Rewrite it around what they built, decided, ran or changed, and what came of it. Keep the answers to yourself unless asked.

- A number counts only when the reader can place it: "elected to a team of 18" means nothing without the size of the class it was picked from. With no reference point, ask, or write the line without the number.
- Counts of a project's internals (migrations, tests, entries flagged) mean nothing to an outsider. Drop them. A number that reads on its own stays.
- Say what the work proves through the verb, the order and the framing: who they dealt with, what they owned, what shipped, the scale. Never state a soft skill outright: "Ran 36 hours of interviews with the security and IT leads" already says it.
- An interpretation is not a fact. Reading the interviews as senior stakeholder work is fair. Writing that the client praised the work is not, unless someone said so. Every interpretation goes in the report.

## Writing the lines

- Neighbouring bullets start with different verbs.
- Spell a name out once on the page, abbreviate after: TypeScript then TS. Names only ever read as initials (API, LLM) need no expansion. Never "TypeScript (TS)".
- `label` names the client, project or event a bullet is about.
- Related small projects share one line that says what they do. No repository lists, issue numbers or download counts.
- A confidential client is described by sector until the user allows its name.

## Fill the page

One page, and empty space at the bottom is an argument not made. Aim for the last line within a line or two of the margin (`remainingMm`).

- Fill with the next most valuable line from the profile, or a result an existing bullet is missing. Never filler, never layout changes.
- Over a page, the export refuses. Cut the single line that matters least for this role and name it in the report.
- A line the user asked to keep stays. If space forces the choice, they decide.

## Tailoring and export

To tailor for an offer, copy the track's base resume to `applications/<entry>/resume.yaml` and rework it for the offer and the track's market report.

Every cratecv command goes through the wrapper, which checks the sources first and resolves paths from the workspace:

```bash
${HERMES_SKILL_DIR}/scripts/resume check <resume.yaml> --json
${HERMES_SKILL_DIR}/scripts/resume build <resume.yaml> -o "<dir>/<PDF name>.pdf"
```

`uv run ${HERMES_SKILL_DIR}/scripts/check-resume.py` with no arguments checks every resume. The PDF name rule is in `applications/README.md`, with the name from `profile/about.md`.

## Report

- the interpretations made, so the user can strike them
- the lines resting on the user's word alone, and what was recorded in `profile/`
- what the offer or market asks for that the profile doesn't cover
- what was cut, and why
- the questions that would most improve the page, ranked, five at most
