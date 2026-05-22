# ECO 6810 Final Project

One project. Two checkpoints. Fifty percent of the course.

- Project milestone: 20%
- Final submission: 30%

This is not a presentation contest, and it is not a "pick a cool topic and see what happens" assignment. Your team is building one clear economics project that someone else should be able to understand and run.

Start here. Then use the [charter template](./CHARTER.md). For exact milestone and final submission steps, read the [submission flow](./SUBMISSION_FLOW.md).

## At a Glance

| Item | Requirement |
|---|---|
| Team size | 2-3 students |
| Project types | Predictive, causal, or descriptive |
| First gate | Approved charter |
| Core standard | One main question, one main metric, one simple baseline, one reproducible run |
| Final expectation | A GitHub repo that runs cleanly and contains the required files |

## Spring 2026 Dates

- Project milestone due: **Wednesday, May 6, 2026, 11:59 PM IST**
- Final project due: **Friday, May 15, 2026, 11:59 PM IST**
- Your charter should be approved before the milestone. If you wait until the milestone week to start the charter, you are taking an unnecessary risk.

## One Important Workflow Rule

As soon as your team and provisional project title are set:

- create a GitHub repo from the template
- rename it clearly
- if the repo is private, add the instructor GitHub account `chitagni` as a collaborator
- start filling `CHARTER.md` inside that repo

That repo should become the home of the project immediately.

Do not wait until the charter is approved, the milestone, or the final deadline to share the repo for the first time.

## GitHub And Colab

This repo is the home of the project.

If GitHub is new to you, start with [GITHUB_PRIMER.md](./GITHUB_PRIMER.md). If moving from notebooks to a small Python project is new, also read [PYTHON_PROJECT_PRIMER.md](./PYTHON_PROJECT_PRIMER.md). The course template repo is public, but your team should normally create a **private** repo from it and add teammates as collaborators. If you prefer working in Colab for exploration, that is fine. Use Colab when it helps, then move the important work back here. The final project should not live in one person's browser tab. GitHub is the shared source of truth. Colab is just one place to run code.

## What You Are Actually Building

Your team will pick one economic question and answer it with data.

Good projects are narrow. They have:

- a clear question
- data you can actually access
- one main number you are trying to estimate, predict, or compare
- a simple baseline to compare against
- a result that someone else can reproduce from your repo

If you want to see what strong finished charters look like, read the [peer samples](./peer-samples/README.md). If you want a few starter ideas that your team could still choose and narrow down, read the [starter ideas](./starter-ideas/README.md).

Examples:

- Predictive: forecast district-level inflation, rainfall shocks, demand, or program uptake
- Causal: estimate the effect of a policy, subsidy, intervention, or treatment
- Descriptive: measure disparities, trends, or patterns across groups, places, or time

## What A Good Project Looks Like

- The question matters to a real person, institution, or policy choice.
- The main outcome is concrete and measurable.
- You can name the exact source of the data now, not later.
- You can compute a simple baseline before you build anything fancy.
- The scope fits one semester and a 2-3 person team.
- The final result can be reproduced from a clean run.

## What Usually Goes Wrong

- The question is too broad: "study inflation in India"
- The outcome is vague: "understand impact" or "analyze trends"
- The team wants to make a causal claim with data that only supports description
- The key dataset is inaccessible, dirty beyond repair, or arrives too late
- The project quietly changes direction after the charter is approved
- The work becomes a dashboard, app, or slide deck with no clear quantitative answer

## The Flow

### Step 1: Lock the charter

Before you build, create your team repo from the template and start the charter in [CHARTER.md](./CHARTER.md).

Think of the charter as your short project plan. It tells us:

- what question you are answering
- who cares about the answer
- what your main metric is
- what baseline you will compare against
- what success would look like numerically
- what data you will use
- what you are not claiming

The charter is reviewed in that repo and comes back as `approved` or `needs_revision`. You can revise and update it there before the deadline. Once it is approved, that becomes the plan we will use to grade both the milestone and the final submission.

### Step 2: Submit the milestone

The milestone is worth 20 points. At this stage, you are proving that the project is real and underway.

You must submit:

- your approved charter
- a repo link or repo snapshot
- a tiny proof that you can access each main data source
- `outputs/baseline_metric.json`
- `outputs/milestone_manifest.json`
- a short `README.md` with the exact milestone run command

What we are asking at the milestone:

| What we check | Points | In plain English |
|---|---:|---|
| Did you stay with the approved plan? | 4 | The question, project type, main metric, and baseline still match the approved charter |
| Can you get the data? | 4 | For each main source, show a small proof that it works, or ask early to replace it with a different source |
| Did you build the simple version first? | 4 | You computed a baseline and saved it in `outputs/baseline_metric.json` |
| Does the repo run? | 4 | The command in your `README.md` runs and writes the milestone files |
| Are the final outputs taking shape? | 4 | `outputs/milestone_manifest.json` shows that your final metric file is already taking the right shape |

### Step 3: Submit the final project

The final submission is worth 30 points. Now we grade execution.

You must submit:

- your approved charter
- the final repo
- `outputs/primary_metric.json`
- `outputs/baseline_metric.json`
- the final report as PDF or Markdown
- the tables and figures promised in the charter
- a short AI usage log

What we are asking at the final submission:

| What we check | Points | In plain English |
|---|---:|---|
| Did you stick to the approved project? | 5 | You did not quietly change the question, main metric, baseline, or project type |
| Does the repo run cleanly? | 5 | The repo runs, the outputs are stable, and the `README.md` matches what is really needed |
| Is the evidence actually there? | 8 | The promised figures, tables, checks, and output files are present and easy to inspect |
| Does the report make the result useful? | 12 | Your report explains what the result means, who it matters for, and where the evidence stops |

The 12-point report bucket is where your economics reasoning matters most. A strong final report:

- answers the approved question directly, using the main metric and baseline
- explains the size and direction of the result in plain economics language
- connects tables and figures to a claim, instead of leaving them as decoration
- compares against the threshold, baseline, groups, places, or time periods that matter for your project
- separates descriptive, predictive, and causal claims
- names the main data limits and says what extra evidence would change your mind

## How Grading Works In Practice

This project is not graded by whether the topic sounds fancy. It is graded against the approved plan in your charter.

In practice, we mainly check three things:

- did you follow the approved plan
- does the repo run and produce the required files
- does the report match what the code actually produced

Some of these checks can be automated. I will step in when human judgment is needed, especially for:

- privacy or ethics concerns
- unsupported advanced methods
- repeated unresolved ambiguity
- serious mismatch between the submitted files and the written claims

## Important Grading Principle

You are not being graded on whether the world gives you a pretty result.

A null result can still earn a strong grade. A messy overclaim cannot.

If your project is well-scoped, reproducible, and honest, you can still do well even if the effect is small, the forecast is hard, or the hypothesis fails. But if you never produce a valid main metric, that is a serious problem, because the whole point of the project is to define and deliver one.

## Required Repo Shape

Use this as the default layout unless you have a good reason not to:

```text
your-project/
  README.md
  main.py
  data/
  outputs/
    baseline_metric.json
    primary_metric.json
    milestone_manifest.json
  report.md
```

Rules:

- `uv run main.py` should run end-to-end on a clean machine
- no manual clicking or hidden setup steps
- data should be fetched in code or stored with a licence note
- the README should be short and exact

If your project needs a different run command, clear it with the instructor early. Do not surprise us at the final submission stage.

## Required Output Files

### `outputs/baseline_metric.json`

This is your simple benchmark result. It answers: what is the basic thing we compare against?

Minimum shape:

```json
{
  "metric_name": "string",
  "value": 0.0,
  "unit": "string"
}
```

### `outputs/primary_metric.json`

This is your main project result. It answers: what is the final number this project is about?

Minimum shape:

```json
{
  "metric_name": "string",
  "value": 0.0,
  "threshold": 0.0,
  "passed": false
}
```

### `outputs/milestone_manifest.json`

This is a short status file for the milestone. It shows that the project is set up properly and moving in the right direction.

Minimum shape:

```json
{
  "charter_locked": true,
  "sources": [
    {
      "name": "string",
      "status": "ok | fallback | blocked",
      "probe_artifact": "relative/path"
    }
  ],
  "baseline_ready": true,
  "primary_metric_schema_ready": true,
  "run_command": "uv run main.py"
}
```

You can add more fields if they help, but these fields must exist.

## What "Data Probe" And "Fallback" Mean

Students often get stuck on this, so here is the simple version:

- A `data probe` is a tiny proof that you can access a source.
- Examples: one row from a CSV, one successful API call, one screenshot of a cleaned sample, one exported response from a form or portal.
- A `fallback` is your backup source or backup plan if the original source stops working.
- If a source breaks, do not hide it. Tell me early and get the fallback approved.

## Rules Of The Game

- Better a small clean project than a sprawling broken one.
- If you want to change the main metric, baseline, or project type after charter approval, ask first.
- You may use AI. Log where you used it and what you checked yourself.
- Every team member should understand the core pipeline and be able to explain it.
- Honesty helps you. Bluffing does not.

## Submission Checklist

### Milestone Checklist: due Wednesday, May 6, 2026, 11:59 PM IST

- the charter is approved
- the GitHub repo link is ready
- each main data source has a small proof that it works
- `outputs/baseline_metric.json` is real, not placeholder text
- `outputs/milestone_manifest.json` is real, not placeholder text
- the run command in `README.md` works

### Final Checklist: due Friday, May 15, 2026, 11:59 PM IST

- the final GitHub repo link is ready
- `outputs/baseline_metric.json` is real
- `outputs/primary_metric.json` is real
- the report matches what the code actually produced
- the promised tables and figures are present
- the AI usage log is honest and complete
- the repo is clean enough that someone else can inspect it without guessing

## How To Pick A Project Quickly

If you are stuck, start with this sequence:

1. Pick a stakeholder.
2. Pick one decision that stakeholder cares about.
3. Pick one outcome you can measure.
4. Check that the data exists and is accessible now.
5. Write the dumb baseline first.
6. Only then decide whether the project is predictive, causal, or descriptive.

That order saves a lot of pain.

## One Last Thing

Ambition is good. Scope control is better.

The strongest projects in this course will usually look a bit boring at first glance: one sharp question, one clean baseline, one honest result, one repo that just works.
