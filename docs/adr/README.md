# Architecture decisions

- [001 Workspace location](001-workspace-location.md): always `~/jobsearch`, outside the Hermes profile, holding data only.
- [002 Workspace init](002-workspace-init.md): a skeleton shipped in the init skill and copied by a script, with personal content filled in by talking to the user.
- [003 Scope](003-scope.md): LinkedIn-centric and a product of its own. Easy Apply yes, external submission no.
- [004 Action policy](004-action-policy.md): one `autonomy:` block, approval by default, and approval by replying to the cron report, resolved through `pipeline/ready.md`.
- [005 Dependencies](005-dependencies.md): a `jobsearch-v<n>` fork tag configured in `config.yaml` and kept current by a sync script, atsfill read only and no browser MCP, optional Himalaya, and cratecv binaries.
- [006 Personalization](006-personalization.md): `criteria.md` and `workspace.yaml` hold everything personal, and the user owns every cron job.
- [007 Distribution repo](007-distribution-repo.md): identity, file allowlist, public early after a scan, CI, roadmap and versions.
