# 002 Workspace init

Status: accepted

## Question

How does `/jobsearch-init` create `~/jobsearch` (see [001](001-workspace-location.md))? The options are to ship a starting folder in the distribution repo and copy it, to have the agent generate the folder, or to clone a separate template repo.

## Decision

The workspace starts as a skeleton copied by a script, and the agent then fills in the personal content by talking to the user.

The skeleton ships inside the init skill:

```
skills/jobsearch-init/
├── SKILL.md              # the onboarding conversation
├── scripts/init.py       # copies the skeleton, git init, first commit
├── scripts/sync-config.py  # keeps the MCP entries of config.yaml current (005)
└── template/             # the skeleton
    ├── AGENTS.md         # data layout, and where the playbooks live (the skills)
    ├── .gitignore
    ├── workspace.yaml    # schema_version: 1
    ├── criteria.md
    ├── profile/README.md
    ├── resumes/README.md
    ├── tracks/README.md  # plus one commented example track
    ├── pipeline/README.md
    ├── applications/README.md
    ├── companies/README.md
    └── market/README.md
```

1. `init.py` copies `template/` to `~/jobsearch`. It refuses if the target exists and is not empty. Then it runs `git init` and makes a first commit. If the user wants the data elsewhere, the skill creates it there and links `~/jobsearch` to it.
2. The skill's conversation fills in what is personal: `criteria.md`, the profile facts, the first track and its resume. It commits again at the end. [006](006-personalization.md) covers the sources and order, [005](005-dependencies.md) the tool checks that come first.

## Why

- **The structure comes from a script and the content from the agent.** A script copies the layout the same way every time, and costs no tokens. Having the agent write a dozen READMEs would give a slightly different workspace each time. Tracks, profile facts and resumes are personal, so they come from a conversation and not from a file.
- **The skeleton lives inside the skill so it is versioned with the playbooks.** `hermes profile update` replaces the skill, so a new init always uses the layout the current playbooks expect, and a migration can compare a workspace with the current template.
- **The installer copies it as it is.** A top-level `workspace/` in the repo would be dropped: `workspace` is on the installer's fixed exclusion list (`hermes_cli/profile_distribution.py`, `USER_OWNED_EXCLUDE`). Under `skills/jobsearch-init/template/` the skeleton travels with `skills/`.
- **A separate template repo adds a second thing to version and fetch.** Its layout and the playbooks would drift apart, and init would need network access and a clone.

## Consequences

- **`workspace.yaml` records `schema_version`.** When the data layout changes, the skills bump it and ship a migration. The skills check the version before they run, and point an outdated workspace to the migration. A CI check that the template and the skills agree on the layout arrives with the first migration, not before.
- **Empty folders carry a README** that says what goes in them and in which format. That doubles as the schema documentation and lets git track the folders.
- **The source setup gives the template its layout.** We take that layout, strip the data, and keep the rules from its `AGENTS.md` that are about data. The playbook rules move into the skills.
