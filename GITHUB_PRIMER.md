# GitHub Primer For The Final Project

This is not a full GitHub course.

You have about three weeks to finish the project. So the GitHub ramp-up should take one day, not one week. The goal is simple: get your team onto one shared project home fast, then get back to the economics.

## The Shortest Honest Explanation

GitHub is a shared project folder with memory.

It stores your files, shows what changed, and helps a team avoid the usual project mess:

- "whose notebook is latest?"
- "which version did we submit?"
- "where is the chart that was working yesterday?"
- "why does it run on one laptop and nowhere else?"

For assignments, plain Colab was enough. For a team project, it starts to hurt.

## Why We Are Using GitHub Instead Of Plain Colab

Colab is still useful. Keep using it for quick exploration if you want.

But a final project usually needs more than one notebook:

- the charter
- the main analysis
- the report
- the figures and tables
- the output files
- a clean record of who changed what

GitHub is where all of that lives together. Colab can still be one place where code runs. It just should not be the only place the project exists.

## Read This Repo In This Order

When you open the starter repo, go in this order:

1. `README.md`
2. `FINAL_PROJECT.md`
3. `CHARTER.md`
4. `SUBMISSION_FLOW.md`
5. `peer-samples/README.md`
6. `starter-ideas/README.md`
7. `PYTHON_PROJECT_PRIMER.md`
8. `main.py`

That order matters. Do not start by poking random files.

## The 24-Hour Ramp

By the end of the first 24 hours, your team should have done all of this:

- created a **private** repo from the template
- renamed it clearly
- added all team members
- shared the repo with the instructor
- read the project brief
- chosen a rough project direction
- started the charter
- made at least one commit to the repo
- run the scaffold once or agreed which teammate will do it that day

If that list is done, your GitHub setup is good enough. Do not turn this into a side quest.

## Two Paths

You have two workable ways to use GitHub for this course.

### Path A: No terminal (recommended if GitHub is brand new)

Use:

- GitHub in the browser
- GitHub Desktop for syncing files
- Colab for notebook work

This is enough for most teams to get moving.

Good use of this path:

- edit `README.md`, `CHARTER.md`, and `report.md` in the browser
- keep notebooks in the repo
- sync local files with GitHub Desktop
- use Colab for exploration, then save the notebook back into the repo

What to learn on day 1:

- `Use this template`
- open a file
- click the pencil icon to edit
- commit the change
- sync changes

That is enough to start.

### Simplest way to edit the charter

For most teams, the easiest path is:

1. open `CHARTER.md` on GitHub
2. click the pencil icon
3. write or revise the charter there
4. commit the change with a normal message

After the charter is approved, one teammate can create a locked PDF copy with:

```bash
pandoc CHARTER.md -o charter_approved.pdf
```

Then commit `charter_approved.pdf` to the repo.

### Path B: Light terminal (faster once one teammate is comfortable)

Use:

- GitHub
- terminal
- `uv`

Minimum commands:

```bash
git clone <your-repo-url>
cd <your-repo-name>
uv sync
uv run main.py
git status
git add .
git commit -m "Write clear message here"
git push
```

You do not need 40 git commands. You need about 6.

## The Words You Actually Need

- **repo**: the project folder on GitHub
- **commit**: a saved checkpoint with a message
- **clone**: copy the repo from GitHub to your laptop
- **push**: send your local changes back to GitHub
- **pull** or **sync**: bring the newest GitHub changes to your laptop
- **branch**: a side lane; useful later, not required on day 1

If you understand those six words, you are already most of the way there.

## Recommended Team Setup

Keep this simple.

- one repo per team
- one `main` branch unless you already know why you need more
- one teammate can be the first person to get the local run working
- everybody should still know how to read the repo and make small edits

Do not create a situation where one person becomes "the GitHub person" and everyone else disappears.

## A Good First Day Workflow

Here is a clean first-day sequence:

1. One teammate creates a private repo from the template.
2. Add teammates as collaborators.
3. Add the instructor as collaborator if the repo is private.
4. Everyone opens the repo and reads `README.md` and `FINAL_PROJECT.md`.
5. One person starts drafting the charter in `CHARTER.md`.
6. Another person looks through the peer samples or starter ideas.
7. A third person checks whether the likely data source is actually reachable.
8. Before the day ends, commit the first draft and push it.

That is enough. Do not spend the first day polishing folder names or debating advanced git workflows.

## If You Want To Stay Close To Colab

That is fine.

Use this pattern:

- explore in Colab
- save the notebook into the repo under `notebooks/`
- move stable logic into `project_code/` or helper scripts later
- keep final figures, tables, and JSON outputs in the repo

If the notebook needs to import helper Python files, read [PYTHON_PROJECT_PRIMER.md](./PYTHON_PROJECT_PRIMER.md) next.

The mistake is not using Colab.

The mistake is letting the real project live only inside Colab.

## What GitHub Fixes In Team Coordination

Compared to passing Colab links around, GitHub helps because:

- everyone can see the current project state
- files have names and places
- changes are recorded
- the team can divide work without losing track
- the instructor can inspect one clean repo instead of a bundle of disconnected files

This matters more than people think.

## What Can Wait Until Later

Do not worry about these on day 1:

- fancy branching strategies
- pull requests for every tiny change
- rebasing
- merge conflict theory
- perfect commit history

You can learn those later if needed. Right now the target is a usable team workflow.

## Non-Negotiable Habits

- push work back to the repo the same day
- write commit messages in normal English
- do not keep the only working version on one laptop
- do not let the report drift away from the code
- if a notebook becomes important, save it in the repo

## If GitHub Feels Annoying

That is normal for the first few hours.

But once the repo exists and the first couple of commits are in place, the confusion usually drops fast. After that, GitHub mostly becomes boring infrastructure, which is exactly what we want.
