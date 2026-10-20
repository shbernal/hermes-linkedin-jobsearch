# Market

What a track's postings ask for, so its resume can answer it.

## `<track>/offers/<company-slug>--<role-slug>.md`

One posting, as fetched. Discovery writes one for every posting inside the track's scope, skipped ones included. A posting with a pipeline entry shares its filename.

```yaml
---
company: acme
title: Data Analyst
family: product-analytics    # one of the track's families
level: entry                 # internship | entry | associate | mid_senior | director | unknown
contract: full_time          # full_time | internship | apprenticeship | freelance | other
work_type: remote
salary: 45-55k€              # as posted, omit when not shown
linkedin_job_id: "4252026496"
posted: 2026-09-10
fetched: 2026-09-13
years_required: 1            # minimum asked, 0 when not stated
languages: [english]
must_have: [sql, python, dashboards]
nice_to_have: [dbt, ownership]
---
```

- Level and contract come from the posting body, not LinkedIn's metadata, which is often wrong. `unknown` levels count as target level.
- Tags are lowercase kebab-case English, whatever the posting's language. Reuse an existing tag before creating one (`grep -h must_have market/*/offers/*.md`). Soft requirements get tags too (`ownership`, `startup-experience`).
- Body: `## Responsibilities` and `## Requirements`, copied from the posting in its original language, so a later analysis with different tags needs no new fetch.

## `<track>/report.md`

The weekly analysis of `offers/`: the sample per family, the leading requirements with their share, recurring responsibilities, phrases worth reusing, and how the track's resume should be tailored per family.
