# Architecture decisions

- [0001](0001-workspace-location.md): the workspace lives in `~/jobsearch`, outside the Hermes profile, holding data only.
- [0002](0002-workspace-init.md): a script copies the skeleton shipped in the init skill, the agent fills in the personal content.
- [0003](0003-scope.md): LinkedIn-centric and a product of its own. Easy Apply, and external forms through atsfill only.
- [0004](0004-action-policy.md): one `autonomy:` block, approval for Easy Apply and no external sending by default, approval resolved through `pipeline/ready.md`.
- [0005](0005-dependencies.md): a pinned `jobsearch-v<n>` LinkedIn fork kept current by a sync script, unpinned atsfill, no browser MCP.
- [0006](0006-personalization.md): `criteria.md` and `workspace.yaml` hold everything personal, and the user owns every cron job.
- [0007](0007-distribution-repo.md): public from the start, an explicit file allowlist, CI and versions.
