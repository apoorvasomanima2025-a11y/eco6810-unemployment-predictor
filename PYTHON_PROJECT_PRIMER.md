# From Colab Notebook To Python Project

This is not a software engineering course.

It is just the minimum shift needed to turn a notebook-based workflow into a clean project workflow.

## The Shortest Honest Explanation

In Colab, one notebook can do everything.

In a project, that gets messy fast.

So we split the work:

- `notebooks/` for exploration and quick experiments
- `project_code/` for reusable Python functions
- `main.py` for the final clean run
- `outputs/` for files your code writes
- `report.md` for the written story

That is the whole idea.

## What To Use, And When

### Use notebooks for:

- opening a new dataset for the first time
- checking variable names and missing values
- trying one cleaning step quickly
- testing a model idea
- making a rough plot
- debugging one step interactively

### Use Python files for:

- any logic you will use more than once
- data-loading functions
- cleaning functions
- metric calculations
- plotting functions for final figures
- API calls or file-reading code
- anything the final project must reproduce reliably

### Use `main.py` for:

- calling the main functions in the right order
- writing the final output files
- printing a short status message

`main.py` should be the clean run, not the place where every line of logic lives.

## The Recommended Workflow

Use this loop:

1. Try the idea in a notebook.
2. Once the code starts working, move the stable part into a helper file in `project_code/`.
3. Import that helper back into the notebook if you still want to explore with it.
4. Call the same helper from `main.py`.
5. Let `main.py` write the final files into `outputs/`.

Good rule:

Explore in notebooks. Keep reusable logic in Python files. Submit through `main.py`.

## Local Setup With `uv`

The cleanest way to run the project is locally from the repo.

Official `uv` docs:

- Installation: https://docs.astral.sh/uv/getting-started/installation/
- Running commands in projects: https://docs.astral.sh/uv/concepts/projects/run/

If one teammate can get the local run working in the first 24 hours, your team is in good shape.

### Basic setup

On macOS or Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

If Python is missing, `uv` can install it:

```bash
uv python install 3.11
```

Then run:

```bash
git clone <your-repo-url>
cd <your-repo-name>
uv sync
uv run main.py
```

If you add a package later, use:

```bash
uv add pandas
```

## A Simple Project Shape

You do not need a complicated structure.

This is enough:

```text
your-project/
  README.md
  main.py
  project_code/
    __init__.py
    data.py
    analysis.py
    plots.py
  notebooks/
  data/
  outputs/
  report.md
```

You do not need all those helper files on day 1.

Start with `main.py`. When the script starts getting crowded, create `project_code/` and move reusable parts there.

## How Imports Work

If your helper code lives in `project_code/`, you can import it from `main.py` like this:

```python
from project_code.data import load_data
from project_code.analysis import compute_primary_metric
```

Then `main.py` can stay short:

```python
from project_code.data import load_data
from project_code.analysis import compute_primary_metric

df = load_data()
result = compute_primary_metric(df)
```

This is better than copying the same code into multiple notebooks.

## How To Use Notebooks And Python Files Together

This is the part that matters most.

Your notebook does not have to disappear.

Instead, let the notebook become a place where you *use* functions, not the only place where those functions exist.

Example notebook pattern:

```python
from project_code.data import load_data
from project_code.analysis import compute_primary_metric

df = load_data()
result = compute_primary_metric(df)
df.head()
```

That way:

- the notebook stays interactive
- the real logic lives in reusable files
- `main.py` can run the same logic later

## If You Want To Keep Using Colab

That is fine.

Two good patterns:

### Pattern A: Colab for exploration only

- use Colab for quick tests
- save the notebook into `notebooks/`
- move stable code into `project_code/`
- run the final pipeline through `main.py`

### Pattern B: Colab notebook that imports project files

If you want a notebook to import `project_code/` files, the repo needs to exist inside the runtime.

In Colab, a clean pattern is:

```python
!git clone <your-repo-url>
%cd <your-repo-name>

from project_code.data import load_data
```

The important idea is simple:

Colab can open a notebook from GitHub, but helper Python files do not magically become available unless the repo is actually present in the runtime.

## When To Move Code Out Of A Notebook

Move code into a Python file when:

- you have used the same code twice
- the step matters for the final result
- the step should run the same way every time
- another teammate needs to reuse it
- you want `main.py` to run it later

Leave code in a notebook when:

- you are still poking around
- the code is temporary
- the chart or table is just exploratory
- you are still deciding whether the idea is worth keeping

## A Good Division Of Labor

For many teams, this works well:

- one notebook for exploration
- one clean `main.py` for the final run
- a few helper files in `project_code/`

You do not need six notebooks and thirteen scripts.

## Common Mistakes

- one giant notebook becomes the whole project
- the same cleaning code is copied into three places
- `main.py` is ignored until the final week
- the final figures exist only inside notebook outputs
- imports break because the helper files are outside the repo or named inconsistently

## The Rule To Remember

Notebook for thinking.

Python files for reusable logic.

`main.py` for the final clean run.
