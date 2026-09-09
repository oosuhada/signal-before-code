#!/usr/bin/env python3
"""Select textbook practice without leaking mixed-mode answer labels by default."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_catalog() -> list[dict[str, str]]:
    return json.loads((ROOT / "curriculum/problems.json").read_text(encoding="utf-8"))["problems"]


def load_answer_key() -> dict[str, str]:
    return json.loads((ROOT / "curriculum/answer-key.json").read_text(encoding="utf-8"))[
        "expected_pattern"
    ]


def sample_mixed(count: int, seed: int | None = None) -> list[dict[str, str]]:
    problems = load_catalog()
    if count < 1 or count > len(problems):
        raise ValueError(f"count must be between 1 and {len(problems)}")
    rng = random.Random(seed)
    return rng.sample(problems, count)


def problems_for_chapter(chapter: str) -> list[dict[str, str]]:
    key = load_answer_key()
    return [problem for problem in load_catalog() if key[problem["key"]] == chapter]


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
    parser.add_argument("--seed", type=int)
    parser.add_argument("--reveal", action="store_true")
    args = parser.parse_args()

    if args.mixed is not None:
        problems = sample_mixed(args.mixed, args.seed)
    else:
        problems = problems_for_chapter(args.chapter)
        if not problems:
            parser.error(f"unknown chapter: {args.chapter}")

    answer_key = load_answer_key()
    for index, problem in enumerate(problems, start=1):
        print(f"\n[{index}]")
        if args.reveal:
            print(review_view(problem, answer_key))
        else:
            print(learner_view(problem))

    if not args.reveal:
        print("\nAnswer labels hidden. Re-run with --reveal only after classification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
