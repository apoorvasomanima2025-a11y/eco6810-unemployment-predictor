# ECO6810 Final Project Starter Repo

This repo is the home for your team's final project.

Use it to keep the charter, code, report, outputs, and team history in one place. If you like working in Colab, that is fine. Run notebooks there if you want, but push the important work back here. GitHub is the source of truth. Colab is just one place to run code.

This public repo is the starter. Your actual team repo should usually be private.

## Start Here

1. Click `Use this template` on GitHub to create your team's own **private** repo.
2. Rename the repo to something clear and short.
3. Add teammates as collaborators.
4. Add the instructor as collaborator if the repo is private.
5. If GitHub is new, read [GITHUB_PRIMER.md](./GITHUB_PRIMER.md).
6. If moving from notebooks to scripts is new, read [PYTHON_PROJECT_PRIMER.md](./PYTHON_PROJECT_PRIMER.md).
7. Read [FINAL_PROJECT.md](./FINAL_PROJECT.md).
8. Read [SUBMISSION_FLOW.md](./SUBMISSION_FLOW.md).
9. Start filling [CHARTER.md](./CHARTER.md) in this repo.
10. Replace the placeholder fields in `main.py`, `report.md`, and `AI_USAGE_LOG.md`.
11. Run `uv sync && uv run main.py`.
12. Commit early. Commit often. Keep the repo readable.

## Why GitHub For The Project

For assignments, plain Colab was enough. For a team project, it starts to break down.

GitHub helps because:

- everyone sees the same current version
- code, report, figures, and outputs live in one place
- you can tell what changed and when
- reproducibility gets much easier
- handing the project to the instructor is just sharing the repo

The goal is not to turn you into software engineers overnight. The goal is to make team coordination simple and keep the project organized.

## What This Repo Already Gives You

- a fast primer in [GITHUB_PRIMER.md](./GITHUB_PRIMER.md)
- a notebook-to-project guide in [PYTHON_PROJECT_PRIMER.md](./PYTHON_PROJECT_PRIMER.md)
- the full project brief in [FINAL_PROJECT.md](./FINAL_PROJECT.md)
- an exact submission guide in [SUBMISSION_FLOW.md](./SUBMISSION_FLOW.md)
- the project plan template in [CHARTER.md](./CHARTER.md)
- a runnable `main.py` that writes the required JSON outputs
- a `project_code/` folder for reusable Python functions
- a report template in [report.md](./report.md)
- an AI usage log template in [AI_USAGE_LOG.md](./AI_USAGE_LOG.md)
- a `notebooks/` folder for Colab-first exploration
- probe and output folders in the right shape
- peer samples in [`peer-samples/README.md`](./peer-samples/README.md)
- starter ideas in [`starter-ideas/README.md`](./starter-ideas/README.md)

## The Working Rule

One repo. One main metric. One baseline. One documented run command.

If your team remembers only one thing, remember that.

## Repo Map

| Path | What it is for |
|---|---|
| `GITHUB_PRIMER.md` | Fast GitHub onboarding for students coming from Colab |
| `PYTHON_PROJECT_PRIMER.md` | How to combine notebooks, Python files, and `main.py` |
| `FINAL_PROJECT.md` | Full project requirements and grading |
| `SUBMISSION_FLOW.md` | Exact milestone and final submission steps |
| `CHARTER.md` | The short project plan you submit first |
| `main.py` | Your main reproducible run |
| `project_code/` | Reusable helper functions imported by notebooks or `main.py` |
| `notebooks/` | Colab notebooks and exploratory work |
| `data/` | Data files or licence notes |
| `artifacts/probes/` | Small proofs that your data sources work |
| `outputs/` | Required JSON outputs plus tables and figures |
| `report.md` | Final written report |
| `AI_USAGE_LOG.md` | What you used AI for and what you verified yourself |
| `peer-samples/` | Strong sample charters based on earlier student project ideas |
| `starter-ideas/` | Course-proposed project ideas you can adopt and narrow down |

## Quick Setup

```bash
uv sync
uv run main.py
```

That first run is only a scaffold check. It writes placeholder outputs so you can see the required file shapes. Replace those placeholders before you submit anything.

Add project-specific packages in `pyproject.toml` as your work evolves. The starter environment is intentionally light.

## How To Work As A Team

- put the project question and stakeholder in the charter first
- assign clear ownership for data, analysis, writing, and cleanup
- keep commits small enough that teammates can understand them
- do not let the report drift away from what the code actually produced
- if you use a notebook, export the important logic into scripts before the end

## If You Prefer Colab

You can still use it.

Good pattern:

- explore in Colab if that is faster
- save the notebook in `notebooks/`
- move stable logic into `project_code/` or helper scripts
- keep the final reproducible run inside the repo

Bad pattern:

- one teammate has the "real" notebook
- figures exist only in Colab outputs
- no one knows which version is current
- the final result depends on hidden notebook state

## What Will Be Graded

You are not submitting a random folder of files. You are showing that your project works and that your team can explain it clearly.

For the milestone, we mainly ask:

- is the project real?
- can you access the data?
- does the repo run?

For the final submission, we mainly ask:

- did you stick to the approved plan?
- does the repo still run cleanly?
- does the report match the code and outputs?

The full details are in [FINAL_PROJECT.md](./FINAL_PROJECT.md).

## Before You Submit

For the milestone:

- the charter is approved
- the run command in `README.md` is accurate
- each main data source has a small proof that it works
- `outputs/baseline_metric.json` is real
- `outputs/milestone_manifest.json` is real

For the final submission:

- `outputs/baseline_metric.json` is real
- `outputs/primary_metric.json` is real
- the report matches the code
- the AI usage log is honest

## One Good Habit

Do not wait until the final week to make the repo clean.

Messy projects do not usually fail because the idea was bad. They fail because the structure never became stable enough to trust.
