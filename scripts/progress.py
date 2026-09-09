#!/usr/bin/env python3
"""Summarize algorithm-selection metrics from progress/attempts.jsonl."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
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
        record.get("failure_mode") == "implementation" for record in records
    )
    recognition_failures = sum(
        record.get("failure_mode") == "pattern_recognition" for record in records
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_ATTEMPTS)
    args = parser.parse_args()

    records = load_records(args.path)
    if not records and not args.path.exists():
        print(f"No attempt records yet: {args.path.relative_to(ROOT)}")
        print(render_summary(summarize(records)))
        return 0

    print(render_summary(summarize(records)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
