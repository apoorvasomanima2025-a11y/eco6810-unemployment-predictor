# Notebooks Folder

If you use Colab, save the notebook back into this folder.

Good use of notebooks here:

- quick exploration
- data probes
- first-pass visual checks
- trying model ideas before you clean them up

Once something becomes central to the project, move the stable logic into `project_code/` and let `main.py` call it.

Good mixed workflow:

- notebook for exploration
- `project_code/` for reusable logic
- `main.py` for the final clean run

Example import from a notebook:

```python
from project_code.template_outputs import build_baseline_metric
```

The notebook can stay. It just should not be the only place where the real analysis lives.

If this workflow is new, read [PYTHON_PROJECT_PRIMER.md](../PYTHON_PROJECT_PRIMER.md).
