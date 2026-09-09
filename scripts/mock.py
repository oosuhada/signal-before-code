#!/usr/bin/env python3
"""Generate answer-hidden timed mocks and record reviews only when the learner runs them."""

from __future__ import annotations

import argparse
import contextlib
import json
import random
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESSION_DIR = ROOT / "mocks" / "sessions"


def load_catalog() -> list[dict[str, object]]:
    return json.loads((ROOT / "curriculum/problems.json").read_text(encoding="utf-8"))["problems"]


def build_mock(problem_count: int, duration: int, seed: int | None = None) -> dict[str, object]:
    if problem_count < 1:
        raise ValueError("problem count must be positive")
    problems = load_catalog()
    if problem_count > len(problems):
        raise ValueError("problem count exceeds catalog size")
    chosen = random.Random(seed).sample(problems, problem_count)
    return {
        "started_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "duration_minutes": duration,
        "answer_key_exposed": False,
        "problems": [
            {
                "key": problem["key"],
                "title": problem["title"],
                "url": problem["url"],
                "abstract": problem["abstract"],
            }
            for problem in chosen
        ],
    }


def save_mock(session: dict[str, object]) -> Path:
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    stamp = str(session["started_at"]).replace(":", "-")
    path = SESSION_DIR / f"mock-{stamp}.json"
    path.write_text(json.dumps(session, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def review_session(path: Path) -> Path:
    session = json.loads(path.read_text(encoding="utf-8"))
    reviews = []
    for problem in session["problems"]:
        print(f"\n{problem['key']} — {problem['title']}")
        identified = -1
        with contextlib.suppress(ValueError):
            identified = int(input("Seconds to identify pattern (blank=unknown): ") or "-1")
        implemented = -1
        with contextlib.suppress(ValueError):
            implemented = int(input("Seconds to implement (blank=unknown): ") or "-1")
        reviews.append(
            {
                "problem_key": problem["key"],
                "solved": input("Solved? [y/N]: ").strip().lower() == "y",
                "pattern_identified": input("Pattern identified? [y/N]: ").strip().lower() == "y",
                "time_to_identify_seconds": None if identified < 0 else identified,
                "time_to_implement_seconds": None if implemented < 0 else implemented,
                "wrong_turns": input("Wrong turns: ").strip(),
                "used_hint": input("Used hint? [y/N]: ").strip().lower() == "y",
            }
        )
    review = {"synthetic": False, "session": path.name, "reviews": reviews}
    output = path.with_name(path.stem + "-review.json")
    first_review = not output.exists()
    output.write_text(json.dumps(review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if first_review:
        status_path = ROOT / "progress" / "learner-status.json"
        status = json.loads(status_path.read_text(encoding="utf-8"))
        status["timed_mocks_completed"] = int(status.get("timed_mocks_completed", 0)) + 1
        status_path.write_text(
            json.dumps(status, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=int, default=90)
    parser.add_argument("--problems", type=int, default=3)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--review", type=Path)
    args = parser.parse_args()

    if args.review:
        output = review_session(args.review)
        print(f"Review saved to {output.relative_to(ROOT)}")
        return 0
    try:
        session = build_mock(args.problems, args.duration, args.seed)
    except ValueError as error:
        parser.error(str(error))
    path = save_mock(session)
    print(f"Timed mock: {session['duration_minutes']} minutes")
    for index, problem in enumerate(session["problems"], start=1):
        print(f"\n[{index}] {problem['title']}\n{problem['url']}\n{problem['abstract']}")
    print(f"\nSession metadata: {path.relative_to(ROOT)}")
    print("Answer labels are not included. Review only after the timer ends.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
