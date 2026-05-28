# Final Project Submission Flow

This page answers one question:

What exactly do we need to do to count as submitted?

## The Short Answer

For both the milestone and the final project, submission has **two parts**:

1. your GitHub repo is updated and ready
2. your Classroom submission is uploaded before the deadline

You need both.

## The Version That Gets Graded

The version that gets graded is:

- the latest version visible in your GitHub repo at the deadline
- together with the files or links you submitted in Classroom by the deadline

Do not upload something to Classroom and then quietly keep changing the repo afterward.

If you make a meaningful change after the deadline, it does not count unless the instructor explicitly allows it.

## Before Either Deadline

Make sure all of this is already true:

- your team repo exists on GitHub
- the repo is the same one you shared when the team formed
- the repo has a short `README.md` with the run command
- the important project files are pushed to GitHub
- the repo is not depending on one teammate's unsaved local state

## Create And Share The Repo Early

Do this as soon as your team and provisional project title are set:

- create the repo from the template
- rename it clearly
- if the repo is private, add the instructor GitHub account `chitagni` as a collaborator
- start `CHARTER.md` in that repo
- keep using that same repo for the rest of the project

This is important.

The repo should not first appear at charter approval, the milestone, or the final deadline. It should already be the home of the project by then.

## After Charter Approval

Once the charter is approved:

- make sure `CHARTER.md` in the repo matches the approved version
- optionally freeze it as `charter_approved.pdf`
- if you want that locked PDF, one teammate can run:

```bash
pandoc CHARTER.md -o charter_approved.pdf
```

- commit the PDF to the repo

## Why This Helps Everyone

This makes the process simpler for students and for grading:

- students have one clear first action after class
- the charter and the project live in one place
- the repo link does not keep changing
- project tracking becomes one stable list of team repos
- grading is easier because the same repo is used from start to finish

## Milestone Submission

### Deadline

**Wednesday, May 6, 2026, 11:59 PM IST**

### What must be in GitHub before the deadline

- approved charter
- working team repo
- `README.md` with the exact milestone run command
- `outputs/baseline_metric.json`
- `outputs/milestone_manifest.json`
- small proof that each main data source works

Good places for those small proofs:

- `artifacts/probes/`
- `notebooks/`
- a short markdown note in the repo

### What to submit in Classroom

Upload one short submission that contains:

- the GitHub repo link
- a short note saying where the source proofs live if they are not obvious

No separate charter PDF is needed if the approved charter is already in the repo.

If your team created `charter_approved.pdf`, that is fine to keep in the repo too.

### What "submitted" means for the milestone

Your milestone counts as submitted only if:

- the GitHub repo is accessible by the instructor
- the milestone files are already in the repo
- the Classroom submission is turned in before the deadline

## Final Project Submission

### Deadline

**Friday, May 15, 2026, 11:59 PM IST**

### What must be in GitHub before the deadline

- final version of the team repo
- `README.md` with the exact final run command
- `outputs/baseline_metric.json`
- `outputs/primary_metric.json`
- final report as `report.md` or PDF
- promised figures and tables
- `AI_USAGE_LOG.md`

### What to submit in Classroom

Upload one short submission that contains:

- the GitHub repo link
- the final report PDF if your report in the repo is Markdown
- a one-line note if anything important is stored in a non-obvious folder

### What "submitted" means for the final project

Your final project counts as submitted only if:

- the GitHub repo is accessible by the instructor
- the final files are already in the repo
- the Classroom submission is turned in before the deadline

## If You Are Using Colab

That is fine.

But before either deadline:

- push the notebook back into the repo
- move stable logic into `main.py` or `project_code/`
- make sure the final figures, tables, and outputs are in the repo

The repo is the submission home. Colab is not the submission home.

## A Good Final 30-Minute Check

Before you click submit, one teammate should verify:

- the repo link opens
- the right branch is pushed
- the latest changes are visible on GitHub
- the required JSON files are present
- the `README.md` run command is accurate
- the Classroom submission includes the correct repo link

## One Common Mistake To Avoid

Do not assume that "we worked on it" means "we submitted it."

For this project, submitted means:

- pushed to GitHub
- visible to the instructor
- turned in on Classroom
