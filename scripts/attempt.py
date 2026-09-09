#!/usr/bin/env python3
"""Record one real learner attempt without pre-revealing the expected pattern."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from signal_before_code.learning import FAILURE_TAXONOMY, learner_ledger, next_review  # noqa: E402

ATTEMPTS = ROOT / "progress" / "attempts.jsonl"


def load_catalog() -> list[dict[str, object]]:
    return json.loads((ROOT / "curriculum/problems.json").read_text(encoding="utf-8"))["problems"]


def load_answer_key() -> dict[str, str]:
    return json.loads((ROOT / "curriculum/answer-key.json").read_text(encoding="utf-8"))[
        "expected_pattern"
    ]


def attempted_keys(path: Path = ATTEMPTS) -> set[str]:
    if not path.exists():
        return set()
    keys = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            keys.add(str(json.loads(line)["problem_key"]))
    return keys


def choose_problem(problem_key: str | None = None) -> dict[str, object]:
    catalog = load_catalog()
    if problem_key:
        for problem in catalog:
            if problem["key"] == problem_key:
                return problem
        raise ValueError(f"unknown problem key: {problem_key}")
    seen = attempted_keys()
    for problem in catalog:
        if problem["key"] not in seen:
            return problem
    raise ValueError("all curated problems already have an attempt; choose --problem explicitly")


def ask_bool(label: str) -> bool:
    while True:
        value = input(f"{label} [y/n]: ").strip().lower()
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("Enter y or n.")


def ask_confidence() -> int:
    while True:
        raw = input("Pattern confidence [1-5]: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= 5:
            return int(raw)
        print("Enter an integer from 1 to 5.")


def parse_failures(raw: str) -> list[str]:
    values = [value.strip() for value in raw.split(",") if value.strip()]
    invalid = set(values) - FAILURE_TAXONOMY
    if invalid:
        raise ValueError(f"unknown failure modes: {sorted(invalid)}")
    return values


def build_record(
    problem_key: str,
    level: str,
    first_impression: str,
    constraints: str,
    candidates: list[str],
    guess: str,
    confidence: int,
    used_hint: bool,
    solved: bool,
    failures: list[str],
    answer_key: dict[str, str],
    attempted_on: date,
    notes: str = "",
) -> dict[str, object]:
    pattern_correct = guess == answer_key[problem_key]
    review_success = solved and pattern_correct
    next_stage, due = next_review("day0", review_success, attempted_on)
    return {
        "problem_key": problem_key,
        "date": attempted_on.isoformat(),
        "level": level,
        "first_impression": first_impression,
        "constraints": constraints,
        "candidate_patterns": candidates,
        "pattern_guess": guess,
        "confidence": confidence,
        "pattern_correct": pattern_correct,
        "solved": solved,
        "used_hint": used_hint,
        "failure_modes": failures,
        "failure_mode": failures[0] if failures else None,
        "revisit_stage": "day0",
        "next_revisit_stage": next_stage,
        "next_review_on": due.isoformat(),
        "notes": notes,
    }


def append_record(record: dict[str, object], path: Path = ATTEMPTS) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    if path == ATTEMPTS:
        records = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        status_path = ROOT / "progress" / "learner-status.json"
        existing = json.loads(status_path.read_text(encoding="utf-8"))
        status_path.write_text(
            json.dumps(learner_ledger(records, existing), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["start"])
    parser.add_argument("--problem")
    args = parser.parse_args()

    try:
        problem = choose_problem(args.problem)
    except ValueError as error:
        parser.error(str(error))

    print(f"\n{problem['key']} — {problem['title']}")
    print(problem["abstract"])
    print(problem["url"])
    print("\nExpected pattern remains hidden until you commit your own guess.\n")

    first_impression = input("First impression: ").strip()
    constraints = input("Important constraints: ").strip()
    candidates = [
        value.strip()
        for value in input("Candidate patterns (comma-separated): ").split(",")
        if value.strip()
    ]
    guess = input("Chosen pattern: ").strip()
    confidence = ask_confidence()
    used_hint = ask_bool("Used a hint?")
    solved = ask_bool("Solved?")
    print("Failure taxonomy (comma-separated, blank if none):")
    print(", ".join(sorted(FAILURE_TAXONOMY)))
    while True:
        try:
            failures = parse_failures(input("Failures: ").strip())
            break
        except ValueError as error:
            print(error)
    notes = input("Notes / wrong turns: ").strip()

    record = build_record(
        str(problem["key"]),
        str(problem["stage"]),
        first_impression,
        constraints,
        candidates,
        guess,
        confidence,
        used_hint,
        solved,
        failures,
        load_answer_key(),
        date.today(),
        notes,
    )
    append_record(record)
    print(f"\nRecorded real attempt in {ATTEMPTS.relative_to(ROOT)}")
    print(f"Pattern correct: {record['pattern_correct']}")
    print(f"Next review: {record['next_review_on']} ({record['next_revisit_stage']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
