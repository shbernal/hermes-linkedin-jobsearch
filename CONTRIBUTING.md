# Contributing

Issues and pull requests are welcome, including ones written entirely by an AI agent.

## Working on the distribution

Install your working tree as a separate profile, so an existing `jobsearch` profile stays untouched:

```bash
hermes profile install ./ --name jobsearch-test --alias -y
```

After a change, pick it up with:

```bash
hermes profile update jobsearch-test
```

The [architecture decisions](docs/adr/README.md) are the reference for what the skills do. [AGENTS.md](AGENTS.md) holds the rules every change follows.

CI installs the distribution into a throwaway Hermes home on every push and checks that only the paths in `distribution_owned` reach the profile.

## Bugs in the tools

A LinkedIn tool that fails or misreads a page belongs to [linkedin-mcp-server](https://github.com/shbernal/linkedin-mcp-server/issues). A hiring form atsfill can't read, fill or send belongs to [atsfill](https://github.com/shbernal/atsfill/issues). Leave out your personal data, the company and the posting URL.

## Pull requests

State in the PR body whether an AI wrote the change, with the harness and the model. Commit messages carry no AI attribution.
