# Resumes

`<track>.yaml`: the base resume for one track, in cratecv's YAML format, cut from `profile/`. Every application in the track starts from a copy of it in `applications/`.

Every detail line carries `source:`, the `profile/` file it comes from, relative to `profile/`:

```yaml
- text: Automated the weekly sales report
  source: experience/acme.md
```

A line with no source, or a source that doesn't back it, doesn't ship. The user's presentation preferences are in the `## Resume` section of `criteria.md`.
