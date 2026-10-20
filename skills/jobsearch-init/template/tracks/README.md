# Tracks

A track is one role family searched on its own: its keywords, its base resume in `resumes/<track>.yaml`, its market data in `market/<track>/`, a discovery job and a weekly market job. Everything after discovery is shared: one `pipeline/`, one send cap, and a job id belongs to the track that found it first. `workspace.yaml` caps the number of tracks.

`<track>.md`:

- Frontmatter: `track`, `resume`, `discovery` (the cron schedule of its discovery job), `pages` (`max_pages` for each search).
- `## Keywords`: the titles searched, then the ones researched and left out, with why.
- `## Families`: the sub-groups its market report counts. Every posting in `market/<track>/offers/` names one.
- `## Fit`: points in favor on top of those in `criteria.md`.
- `## Positioning`: what the resume argues, and the profile facts behind it.
- `## Interviews`: what interviews for this track have asked, to prepare the next ones. Added after the first.

To pause a track, pause its cron jobs. Its files stay.

## Example

```markdown
---
track: data-analyst              # file name and folder name under market/
resume: resumes/data-analyst.yaml
discovery: "0 9 * * *"           # daily at 9:00
pages: 2
---

# Data analyst

Analytics roles close to the business: dashboards, SQL, experiments.

## Keywords

`data analyst`, `product analyst`, `analytics engineer`

Researched and left out:

- `business intelligence`: mostly consulting firms.

## Families

- `product-analytics`: product usage, funnels, experiments
- `bi`: reporting and dashboards for business teams

## Fit

- The team ships its own dashboards rather than taking tickets

## Positioning

An analyst who builds the pipeline behind the chart. The resume points:

- The reporting automated at the last internship
- The SQL and dbt projects
```
