#!/usr/bin/env python3
"""Run oral algorithm-defense prompts without requiring code."""

from __future__ import annotations

import argparse
import json
import random
from contextlib import suppress
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "interview" / "oral-defense.json"


def load_chapters() -> list[dict[str, object]]:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    return payload["chapters"]


def choose_prompt(chapter: str | None = None, seed: int | None = None) -> dict[str, object]:
    chapters = load_chapters()
    if chapter is not None:
        matches = [item for item in chapters if item["chapter"] == chapter]
        if not matches:
            raise ValueError(f"unknown chapter: {chapter}")
        return matches[0]
    return random.Random(seed).choice(chapters)


def learner_prompt(item: dict[str, object]) -> str:
    follow_ups = item["follow_ups"]
    assert isinstance(follow_ups, list)
    return "\n".join(
        [
            f"Chapter: {item['chapter']}",
            "",
            "Explain when this pattern is the right tool without writing code.",
            (
                "Your answer should include: signal, invariant, complexity, "
                "and one rejection boundary."
            ),
            "",
            f"Follow-up: {follow_ups[0]}",
        ]
    )


def reveal(item: dict[str, object], depth: str) -> str:
    key = "thirty_second" if depth == "30s" else "two_minute"
    follow_ups = item["follow_ups"]
    assert isinstance(follow_ups, list)
    lines = [f"Reference {depth} defense:", str(item[key]), "", "Deep follow-ups:"]
    lines.extend(f"- {question}" for question in follow_ups)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--depth", choices=["30s", "2m"], default="30s")
    parser.add_argument("--reveal", action="store_true")
    parser.add_argument("--step", action="store_true", help="pause before reference answer")
    args = parser.parse_args()

    try:
        item = choose_prompt(args.chapter, args.seed)
    except ValueError as error:
        parser.error(str(error))

    print(learner_prompt(item))
    if args.step and not args.reveal:
        with suppress(EOFError):
            input("\n[Enter to reveal a reference defense] ")
        print()
        print(reveal(item, args.depth))
    elif args.reveal:
        print()
        print(reveal(item, args.depth))
    else:
        print("\nReference answer hidden. Re-run with --reveal after speaking your defense.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
