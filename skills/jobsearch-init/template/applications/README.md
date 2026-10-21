# Applications

## `<company-slug>--<role-slug>/`

Drafts for one application, named like its pipeline file.

- `resume.yaml`: a full copy of the track's base resume from `resumes/`, tailored to the offer.
- The exported PDF, gitignored. The pipeline Activity line records how it was rendered, so it can be rebuilt.
- `answers.md`: every question on the form, answered.
- `answers.json`: atsfill's `{field id: value}` map, external forms only, written from `answers.md` before each fill or send.
- `fit-interview-prep.md`: the HR or motivation round, for a non-technical interviewer: motivation and plain-language stories, no jargon.
- `technical-interview-prep.md`: the role itself, its tools and concepts, technical evidence and gaps.
- `interviews/YYYY-MM-DD-<round>.srt`: the user's transcript of one interview. `<round>` is `recruiter`, `hiring-manager`, `technical`, `case` or `founder`, with a suffix (`-2`) for a second round the same day. The next round's prep reads it.

PDF name: `<First> <LAST> - Resume.pdf`, or `<First> <LAST> - Resume - <Company>.pdf` with `name` from `companies/<slug>.md`, the name taken from `profile/about.md`. Another name when the form, the company or the user asks for one. A file upload is answered with the PDF's absolute path.

## `answers.md`

```markdown
# Acme, Data Analyst
Form: <easy apply | hiring system + URL | account required + URL | pasted by the user> · read YYYY-MM-DD
<LinkedIn job URL, easy apply only>

## <question, verbatim>
<field type> · <required | optional> · <options or character limit> · <atsfill field id, external forms only>
Answer:
<the answer, one line>
<justification, one line, only when the answer is a judgment call>
Source: <profile files, criteria.md, company dossier, offer>
```

- `Answer:` is alone on its line and the answer is the next line, so the user can copy it by line number.
- An answer is one line with no line breaks. Several short sentences are fine.
- Select and radio fields: one of the options, verbatim.
- A field that should keep what the form already holds is answered `Leave unchanged`, with the reason below. The resume radios take it: uploading a resume already selects it.
- No placeholders. Always propose an answer, and put the reasoning on the justification line when it's uncertain.
- Easy Apply steps the form reader couldn't read go last, under `## Unread steps`: which step blocked and on which field.
- A sent application appends `## Sent <date>` with every field filled and the value it holds. LinkedIn shows a sent Easy Apply nowhere, so this is the only record of what the company read.
- Facts come from `profile/`, recurring answers from `criteria.md`. A requirement the user doesn't meet is said plainly in the justification.
