#!/usr/bin/env python3
"""Attack algorithm claims with counterexamples and mutation drills."""

from __future__ import annotations

import argparse
import contextlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = {
    "counterexample": ROOT / "challenges/counterexamples.json",
    "constraint": ROOT / "challenges/constraint-mutations.json",
    "requirement": ROOT / "challenges/requirement-mutations.json",
}


def load_challenges(mode: str) -> list[dict[str, object]]:
    data = json.loads(DATA[mode].read_text(encoding="utf-8"))
    key = "challenges"
    return data[key]


def choose_challenge(
    mode: str, topic: str | None = None, seed: int | None = None
) -> dict[str, object]:
    items = load_challenges(mode)
    if topic:
        query = topic.lower()
        items = [
            item
            for item in items
            if query in str(item.get("algorithm", "")).lower()
            or query in str(item.get("id", "")).lower()
        ]
    if not items:
        raise ValueError(f"no {mode} challenge matches {topic!r}")
    return random.Random(seed).choice(items)


def hidden_view(item: dict[str, object], mode: str) -> str:
    if mode == "counterexample":
        return f"Claim:\n{item['claim']}\n\nFind the smallest counterexample you can."
    return f"Mutation:\n{item['prompt']}\n\nWhat candidate would you reject or promote, and why?"


def reveal_view(item: dict[str, object], mode: str) -> str:
    if mode == "counterexample":
        candidates = ", ".join(str(value) for value in item["better_candidates"])
        return (
            f"Counterexample: {item['counterexample']}\n"
            f"Why it breaks: {item['failure']}\n"
            f"Better candidates: {candidates}"
        )
    return f"Boundary review: {item['reveal']}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Practice algorithm boundaries, not answer labels."
    )
    parser.add_argument("topic", nargs="?", help="algorithm or challenge id filter")
    parser.add_argument(
        "--mode", choices=sorted(DATA), default="counterexample", help="type of boundary drill"
    )
    parser.add_argument("--seed", type=int)
    parser.add_argument("--reveal", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    if args.list:
        for mode in sorted(DATA):
            print(f"[{mode}]")
            for item in load_challenges(mode):
                print(f"- {item['id']}")
        return 0

    try:
        item = choose_challenge(args.mode, args.topic, args.seed)
    except ValueError as error:
        parser.error(str(error))
    print(hidden_view(item, args.mode))
    if not args.reveal:
        with contextlib.suppress(EOFError):
            input("\n[Enter to reveal] ")
    print("\n" + reveal_view(item, args.mode))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
