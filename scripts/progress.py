#!/usr/bin/env python3
"""Summarize real learner evidence; remain explicit when no attempts exist."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from signal_before_code.learning import (  # noqa: E402
    confidence_calibration,
    failure_counts,
    pattern_metrics,
)

DEFAULT_ATTEMPTS = ROOT / "progress" / "attempts.jsonl"


def load_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {error.msg}") from error
        if not isinstance(record, dict):
            raise ValueError(f"{path}:{line_number}: each JSONL record must be an object")
        records.append(record)
    return records


def load_answer_key() -> dict[str, str]:
    return json.loads((ROOT / "curriculum/answer-key.json").read_text(encoding="utf-8"))[
        "expected_pattern"
    ]


def percentage(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator * 100


def summarize(records: list[dict[str, Any]]) -> dict[str, int | float | None]:
    attempted = len(records)
    solved_without_hint = sum(
        bool(record.get("solved")) and not bool(record.get("used_hint")) for record in records
    )
    correct_pattern = sum(bool(record.get("pattern_correct")) for record in records)
    implementation_failures = sum(
        record.get("failure_mode") in {"implementation", "implementation_bug"}
        or "implementation_bug" in record.get("failure_modes", [])
        for record in records
    )
    recognition_failures = sum(
        record.get("failure_mode") in {"pattern_recognition", "pattern_recognition_failure"}
        or "pattern_recognition_failure" in record.get("failure_modes", [])
        for record in records
    )
    revisits = [record for record in records if record.get("revisit_stage") != "day0"]
    revisit_successes = sum(bool(record.get("solved")) for record in revisits)
    return {
        "attempted": attempted,
        "solved_without_hint": solved_without_hint,
        "correct_pattern": correct_pattern,
        "implementation_failures": implementation_failures,
        "recognition_failures": recognition_failures,
        "pattern_recognition_rate": percentage(correct_pattern, attempted),
        "hint_free_solve_rate": percentage(solved_without_hint, attempted),
        "revisit_success_rate": percentage(revisit_successes, len(revisits)),
    }


def format_percentage(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.1f}%"


def render_summary(summary: dict[str, int | float | None]) -> str:
    return "\n".join(
        [
            f"Attempted: {summary['attempted']}",
            f"Solved without hint: {summary['solved_without_hint']}",
            f"Correct pattern identified: {summary['correct_pattern']}",
            f"Implementation failure: {summary['implementation_failures']}",
            f"Pattern recognition failure: {summary['recognition_failures']}",
            "",
            f"Pattern recognition rate: {format_percentage(summary['pattern_recognition_rate'])}",
            f"Hint-free solve rate: {format_percentage(summary['hint_free_solve_rate'])}",
            f"Revisit success rate: {format_percentage(summary['revisit_success_rate'])}",
        ]
    )


def render_extended(records: list[dict[str, Any]]) -> str:
    lines = [render_summary(summarize(records))]
    counts = failure_counts(records)
    if counts:
        lines.extend(["", "Failure modes:"])
        lines.extend(f"- {name}: {count}" for name, count in counts.most_common())
    calibration = confidence_calibration(records)
    if calibration:
        lines.extend(["", "Confidence calibration:"])
        for confidence, bucket in calibration.items():
            lines.append(
                f"- {confidence}/5: {bucket['accuracy']:.1f}% correct "
                f"({bucket['correct']}/{bucket['attempts']})"
            )
    metrics = pattern_metrics(records, load_answer_key())
    if metrics:
        lines.extend(["", "Pattern metrics:"])
        for pattern, values in metrics.items():
            lines.append(
                f"- {pattern}: recognition {values['pattern_recognition_rate']:.1f}% | "
                f"implementation {values['implementation_success_rate']:.1f}% | "
                f"hint-free {values['hint_free_solve_rate']:.1f}%"
            )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_ATTEMPTS)
    args = parser.parse_args()
    try:
        records = load_records(args.path)
    except ValueError as error:
        parser.error(str(error))
    if not records:
        print("No real learner attempts recorded yet.")
        print(render_summary(summarize(records)))
        return 0
    print(render_extended(records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
