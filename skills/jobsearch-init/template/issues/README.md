# Issues

## `<slug>.md`

One failure that points at the LinkedIn tools, atsfill or the profile's skills rather than at a posting or the agent's input. Delete it once the failure is fixed.

```yaml
---
repo: shbernal/atsfill   # shbernal/linkedin-mcp-server | shbernal/atsfill | shbernal/hermes-linkedin-jobsearch
status: drafted          # drafted | awaiting-approval | filed
url: https://github.com/shbernal/atsfill/issues/42   # once filed, or the existing issue it was added to
first_seen: 2026-10-23
last_seen: 2026-10-23
occurrences: 1
---
```

Body: `# <title>`, then the issue as it would be filed: the command or tool call, the system and the result. Nothing that identifies the user, the employer or the posting: no names, contact details, profile facts, employer, posting URL or job ID.

- `## Workaround`: what to do instead until the failure is fixed.
- `## File it`: while not filed, a `https://github.com/<repo>/issues/new?title=…&body=…` link with the title and body URL-encoded.

Before filing, search the repo's issues with `gh search issues`. When one matches, comment the new occurrence there instead of opening another.
