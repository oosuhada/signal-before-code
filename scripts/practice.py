#!/usr/bin/env python3
"""Select practice from the textbook while respecting real learner evidence."""

from __future__ import annotations

import argparse
import json
import random
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from signal_before_code.learning import (  # noqa: E402
    due_problem_keys,
    group_by_problem,
    weakness_score,
)

ATTEMPTS = ROOT / "progress" / "attempts.jsonl"


def load_catalog() -> list[dict[str, str]]:
    return json.loads((ROOT / "curriculum/problems.json").read_text(encoding="utf-8"))["problems"]


def load_answer_key() -> dict[str, str]:
    return json.loads((ROOT / "curriculum/answer-key.json").read_text(encoding="utf-8"))[
        "expected_pattern"
    ]


def load_attempts(path: Path = ATTEMPTS) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def _sample(items: list[dict[str, str]], count: int, seed: int | None) -> list[dict[str, str]]:
    if count < 1:
        raise ValueError("count must be positive")
    if count > len(items):
        count = len(items)
    return random.Random(seed).sample(items, count)


def sample_mixed(count: int, seed: int | None = None) -> list[dict[str, str]]:
    problems = load_catalog()
    if count > len(problems):
        raise ValueError(f"count must be between 1 and {len(problems)}")
    return _sample(problems, count, seed)


def problems_for_chapter(chapter: str) -> list[dict[str, str]]:
    key = load_answer_key()
    return [problem for problem in load_catalog() if key[problem["key"]] == chapter]


def unseen_problems(
    count: int, records: list[dict[str, Any]], seed: int | None = None
) -> list[dict[str, str]]:
    seen = {str(record.get("problem_key")) for record in records}
    items = [problem for problem in load_catalog() if problem["key"] not in seen]
    return _sample(items, count, seed)


def due_problems(
    count: int, records: list[dict[str, Any]], today: date, seed: int | None = None
) -> list[dict[str, str]]:
    due = set(due_problem_keys(records, today))
    items = [problem for problem in load_catalog() if problem["key"] in due]
    return _sample(items, count, seed) if items else []


def weakest_problems(
    count: int, records: list[dict[str, Any]], today: date
) -> list[dict[str, str]]:
    grouped = group_by_problem(records)
    ranked = sorted(
        grouped,
        key=lambda key: (weakness_score(grouped[key], today), key),
        reverse=True,
    )
    wanted = set(ranked[:count])
    catalog_by_key = {problem["key"]: problem for problem in load_catalog()}
    return [
        catalog_by_key[key] for key in ranked[:count] if key in wanted and key in catalog_by_key
    ]


def implementation_retries(count: int, records: list[dict[str, Any]]) -> list[dict[str, str]]:
    wanted = []
    seen = set()
    for record in reversed(records):
        key = str(record.get("problem_key", ""))
        modes = set(record.get("failure_modes", []))
        if (
            record.get("pattern_correct")
            and not record.get("solved")
            and modes
            & {
                "implementation_bug",
                "off_by_one",
                "edge_case_failure",
            }
            and key
            and key not in seen
        ):
            wanted.append(key)
            seen.add(key)
        if len(wanted) == count:
            break
    catalog = {problem["key"]: problem for problem in load_catalog()}
    return [catalog[key] for key in wanted if key in catalog]


def recognition_problems(count: int, seed: int | None = None) -> list[dict[str, str]]:
    items = [problem for problem in load_catalog() if problem["stage"] == "Recognize"]
    return _sample(items, count, seed)


def learner_view(problem: dict[str, str]) -> str:
    return "\n".join(
        [
            f"{problem['key']} — {problem['title']}",
            f"stage: {problem['stage']} | difficulty: {problem['difficulty']}",
            problem["abstract"],
            problem["url"],
        ]
    )


def review_view(problem: dict[str, str], answer_key: dict[str, str]) -> str:
    return "\n".join(
        [
            learner_view(problem),
            f"expected pattern: {answer_key[problem['key']]}",
            f"signal to review: {problem['expected_signal']}",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mixed", type=int, metavar="COUNT")
    group.add_argument("--chapter")
    group.add_argument("--weakest", type=int, metavar="COUNT")
    group.add_argument("--due", type=int, metavar="COUNT")
    group.add_argument("--unseen", type=int, metavar="COUNT")
    group.add_argument("--recognition-only", type=int, metavar="COUNT")
    group.add_argument("--implementation", type=int, metavar="COUNT")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--reveal", action="store_true")
    parser.add_argument("--attempts", type=Path, default=ATTEMPTS)
    args = parser.parse_args()

    records = load_attempts(args.attempts)
    try:
        if args.mixed is not None:
            problems = sample_mixed(args.mixed, args.seed)
        elif args.chapter:
            problems = problems_for_chapter(args.chapter)
            if not problems:
                parser.error(f"unknown chapter: {args.chapter}")
        elif args.unseen is not None:
            problems = unseen_problems(args.unseen, records, args.seed)
        elif args.recognition_only is not None:
            problems = recognition_problems(args.recognition_only, args.seed)
        elif args.due is not None:
            problems = due_problems(args.due, records, date.today(), args.seed)
        elif args.weakest is not None:
            problems = weakest_problems(args.weakest, records, date.today())
        else:
            problems = implementation_retries(args.implementation, records)
    except ValueError as error:
        parser.error(str(error))

    evidence_mode = (
        args.due is not None or args.weakest is not None or args.implementation is not None
    )
    if evidence_mode and not records:
        print("No real learner attempts recorded yet.")
        return 0
    if not problems:
        print("No matching practice items are currently available.")
        return 0

    answer_key = load_answer_key()
    for index, problem in enumerate(problems, start=1):
        print(f"\n[{index}]")
        print(review_view(problem, answer_key) if args.reveal else learner_view(problem))

    if not args.reveal:
        print("\nAnswer labels hidden. Re-run with --reveal only after classification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
