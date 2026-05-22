from __future__ import annotations


def build_baseline_metric() -> dict:
    return {
        "metric_name": "replace_me_baseline",
        "value": 0.0,
        "unit": "replace_me_unit",
        "notes": "Template value. Replace this with your real baseline before the milestone.",
        "is_template": True,
    }


def build_primary_metric() -> dict:
    return {
        "metric_name": "replace_me_primary",
        "value": 0.0,
        "threshold": 0.0,
        "passed": False,
        "notes": "Template value. Replace this with your real project metric before the final submission.",
        "is_template": True,
    }


def build_milestone_manifest() -> dict:
    return {
        "charter_locked": False,
        "sources": [
            {
                "name": "replace_me_source",
                "status": "blocked",
                "probe_artifact": "artifacts/probes/replace_me_probe.md",
                "note": "Replace this with a real one-row or one-response source probe.",
            }
        ],
        "baseline_ready": False,
        "primary_metric_schema_ready": True,
        "run_command": "uv run main.py",
        "template_warning": "This scaffold runs, but it is not submission-ready until you replace the placeholders.",
    }
