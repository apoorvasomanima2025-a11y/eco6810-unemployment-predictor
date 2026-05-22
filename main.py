from __future__ import annotations

from pathlib import Path

from project_code.io import write_json
from project_code.template_outputs import (
    build_baseline_metric,
    build_milestone_manifest,
    build_primary_metric,
)

ROOT = Path(__file__).resolve().parent
OUTPUTS_DIR = ROOT / "outputs"


def main() -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    baseline_metric = build_baseline_metric()
    primary_metric = build_primary_metric()
    milestone_manifest = build_milestone_manifest()

    write_json(OUTPUTS_DIR / "baseline_metric.json", baseline_metric)
    write_json(OUTPUTS_DIR / "primary_metric.json", primary_metric)
    write_json(OUTPUTS_DIR / "milestone_manifest.json", milestone_manifest)

    print("Template outputs written to outputs/.")
    print("Replace the placeholder fields before you submit the milestone or the final project.")


if __name__ == "__main__":
    main()
