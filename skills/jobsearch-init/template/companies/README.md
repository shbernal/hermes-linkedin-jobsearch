# Companies

## `<slug>.md`

One dossier per company, shared by every pipeline entry at it.

```yaml
---
name: Acme
linkedin: acme               # company_name for get_company_profile
website: https://acme.example
stage: seed                  # pre-seed | seed | series-a | series-b | series-c+ | public | acquired | unknown
headcount: 11-50
hq: Lyon
remote_policy: remote-first  # remote-first | hybrid | on-site | unknown
updated: 2026-09-13
---
```

Body sections: `## Product`, `## Funding` (with source URLs), `## Team` (founders and relevant people, with LinkedIn URLs and connection degree), `## Hiring signals`, `## Notes`.
