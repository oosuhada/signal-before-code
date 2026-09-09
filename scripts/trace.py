#!/usr/bin/env python3
"""Run deterministic algorithm traces with optional predict-before-reveal pauses."""

from __future__ import annotations

import argparse
import contextlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from signal_before_code.tracing import TRACE_BUILDERS, build_trace, render_step  # noqa: E402


def load_wrong_traces() -> dict[str, dict[str, object]]:
    data = json.loads((ROOT / "traces/wrong-states.json").read_text(encoding="utf-8"))
    return {item["id"]: item for item in data["traces"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Visualize algorithm state transitions.")
    parser.add_argument("algorithm", nargs="?", choices=sorted(TRACE_BUILDERS))
    parser.add_argument("--step", action="store_true", help="pause between states")
    parser.add_argument("--predict", action="store_true", help="hide the transition until Enter")
    parser.add_argument("--json", action="store_true", help="print the machine-readable trace")
    parser.add_argument(
        "--wrong", metavar="TRACE_ID", help="show a wrong-state counterexample trace"
    )
    args = parser.parse_args()

    if args.wrong:
        wrong = load_wrong_traces()
        if args.wrong not in wrong:
            parser.error(
                f"unknown wrong-state trace: {args.wrong}; choose from {', '.join(sorted(wrong))}"
            )
        print(json.dumps(wrong[args.wrong], indent=2, ensure_ascii=False))
        return 0
    if not args.algorithm:
        parser.error("choose an algorithm or use --wrong TRACE_ID")

    trace = build_trace(args.algorithm)
    if args.json:
        print(json.dumps(trace, indent=2, ensure_ascii=False))
        return 0

    print(f"{trace['algorithm']}: {trace['goal']}\n")
    for index, step in enumerate(trace["steps"]):
        if args.predict:
            print(render_step(step, reveal=False))
            with contextlib.suppress(EOFError):
                input("\n[Enter to reveal] ")
            print(f"\nDecision: {step['decision']}")
            print(f"Eliminated/changed: {step['eliminated']}")
        else:
            print(render_step(step))
        if args.step and not args.predict and index < len(trace["steps"]) - 1:
            with contextlib.suppress(EOFError):
                input("\n[Enter for next state] ")
        if index < len(trace["steps"]) - 1:
            print("\n" + "-" * 60 + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
