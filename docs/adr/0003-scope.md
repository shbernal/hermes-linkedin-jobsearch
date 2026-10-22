# A LinkedIn-centric product, sending only through Easy Apply and atsfill

The agent comes from a personal setup that ran daily, and a later project by the same author takes a different approach to the same problem. hermes-linkedin-jobsearch is a separate product, not an early version of that project: it works through LinkedIn search and Easy Apply, an agent that prepares every application, and atsfill for external forms.

## Consequences

v1 ships discover, analyze-market, research-company, prepare-application, apply, update-status, add-track, the resume skills and jobsearch-init. Left out on purpose:

- Sending through anything but atsfill. A form atsfill doesn't support is read with Hermes' browser and goes to the user.
- Welcome to the Jungle discovery. WTTJ forms reached from LinkedIn are sent like any atsfill system.
- A hiring-forms MCP, outreach (and with it every message or connection request), freehire, and the third-party dev skills.

External sending is an opt-in ([0004](0004-action-policy.md)), and atsfill's own `submit` list picks the systems that may receive one. apply handles atsfill's result statuses in general: system quirks belong in atsfill, not in per-system notes here.
