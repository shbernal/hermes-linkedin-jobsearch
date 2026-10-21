---
name: jobsearch-scheduled-run
description: The rules every scheduled job-search run follows - what it may run, how it commits, where its permissions come from and the shape of its report. Load it with any jobsearch cron job.
---

# Scheduled run

Nobody is there to approve a command or answer a question. Work from the workspace files, never from chat history or an earlier report.

## Tools

`execute_code`, `python -c` and Python heredocs are blocked. Read and enumerate files with the file tools, and call CLIs directly. Never loosen the approval policy to get around a block: report it under `Failed`.

## Permissions

The `autonomy:` and `caps:` blocks of `workspace.yaml` are the only permissions. What they leave at `approval` or `off` waits for the user: the entry takes `ball: user` and the run says what it waits on. Replies, messages and anything else that would go out to someone are drafted, never sent.

## Git

Before writing, record `git status --short` and leave every change already there as it was. Stage the run's files by path, never `git add .` or `-A`. Review the staged diff and commit with a subject that says what changed and doesn't contain `cron`, `run`, `phase` or `step`. No empty commit. A commit that fails goes under `Failed`.

## Report

Exactly four sections: `Changed`, `Decisions`, `Failed`, `Next`. Every opportunity mentioned carries company, title, posted salary or `not disclosed`, fit and status, so the user can decide without opening the workspace. Every line carries news: a change, a question for the user, a failure, or an action someone takes next. Nothing gets a line for not moving. An empty section reads `None`, and when all four are `None` the whole reply is `[SILENT]`.
