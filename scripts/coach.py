#!/usr/bin/env python3
"""Run the repository-native AI coach without opening a separate chat application."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from signal_before_code.coach import (  # noqa: E402
    PHASE_POLICIES,
    CoachSession,
    build_context,
    choose_problem_key,
    learner_problem_view,
    load_problem,
    system_instruction,
    user_prompt,
)
from signal_before_code.google_llm import (  # noqa: E402
    GoogleGenAIProvider,
    GoogleProviderConfig,
    doctor,
    load_env_file,
)

SESSION_ROOT = ROOT / ".signal-before-code" / "coach"


def _add_provider_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--backend",
        choices=["vertex-adc", "vertex-api-key", "gemini-api"],
        help="Google backend; defaults to SIGNAL_BEFORE_CODE_GOOGLE_BACKEND or vertex-adc",
    )
    parser.add_argument(
        "--model", help="defaults to SIGNAL_BEFORE_CODE_MODEL, VERTEX_AI_MODEL, or gemini-3.5-flash"
    )
    parser.add_argument("--project", help="Google Cloud project for Vertex ADC")
    parser.add_argument("--location", help="Vertex location; defaults to global")
    parser.add_argument(
        "--env-file",
        type=Path,
        help="optional local env file; only allow-listed Google/coach variables are loaded",
    )


def _config(args: argparse.Namespace) -> GoogleProviderConfig:
    if args.env_file:
        loaded = load_env_file(args.env_file.expanduser())
        print("Loaded config variable names: " + (", ".join(sorted(loaded)) or "none"))
        print("Credential values are never printed.")
    return GoogleProviderConfig.from_env(
        backend=args.backend,
        model=args.model,
        project=args.project,
        location=args.location,
    )


def _safe_problem_line(root: Path, key: str) -> str:
    problem = learner_problem_view(load_problem(root, key))
    return "\n".join(
        [
            f"{problem['key']} — {problem['title']}",
            str(problem.get("abstract", "")),
            str(problem.get("url", "")),
        ]
    )


def _log(path: Path | None, payload: dict[str, object]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _provider(config: GoogleProviderConfig) -> GoogleGenAIProvider:
    return GoogleGenAIProvider(config)


def run_doctor(args: argparse.Namespace) -> int:
    config = _config(args)
    status = doctor(config)
    print("Embedded AI Coach doctor")
    for key, value in status.items():
        print(f"{key}: {value}")
    if config.backend == "vertex-adc":
        print("Authentication: Application Default Credentials; no key value is read or printed.")
        if not status["adc_available"]:
            print("next_step: gcloud auth application-default login")
    else:
        print("Authentication: API key presence only; the key value is never printed.")
        if not status["api_key_present"]:
            print("next_step: export GOOGLE_API_KEY=... or GEMINI_API_KEY=...")
    if args.smoke:
        try:
            provider = _provider(config)
            try:
                reply = provider.generate(
                    "This is a connectivity check. Reply with exactly COACH_OK.",
                    "connectivity check",
                )
            finally:
                provider.close()
        except Exception as error:
            print(f"model_smoke: failed ({type(error).__name__}: {error})")
            return 2
        result = "success" if "COACH_OK" in reply else "unexpected_response"
        print(f"model_smoke: {result}")
        return 0 if result == "success" else 2
    return 0


def run_ask(args: argparse.Namespace) -> int:
    config = _config(args)
    problem_key = choose_problem_key(ROOT, args.problem)
    session = CoachSession(problem_key=problem_key, phase=args.phase)
    if args.pattern_guess:
        session.learner.pattern_guess = args.pattern_guess
    if args.review_unlocked:
        session.review_unlocked = True
    context = build_context(ROOT, session, user_message=args.message)
    provider = _provider(config)
    try:
        print(provider.generate(system_instruction(session.phase), user_prompt(context)))
    finally:
        provider.close()
    return 0


def run_start(args: argparse.Namespace) -> int:
    config = _config(args)
    problem_key = choose_problem_key(ROOT, args.problem)
    session = CoachSession(problem_key=problem_key)
    log_path = None
    if not args.no_log:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_path = SESSION_ROOT / f"{stamp}-{problem_key}.jsonl"

    print("\n" + _safe_problem_line(ROOT, problem_key))
    print("\nAnswer-key metadata is blocked from LLM context before review.")
    print("Coach logs are local-only and never count as solve/mastery evidence.")
    print("Commands: /status, /commit <pattern>, /review, /debug, /oral, /revisit, /quit\n")

    try:
        provider = _provider(config)
    except Exception as error:
        print(f"Coach provider could not start: {type(error).__name__}: {error}")
        print("Run `python3 scripts/coach.py doctor` to inspect safe configuration status.")
        return 2
    conversation: list[dict[str, object]] = []
    try:
        while True:
            try:
                raw = input(f"[{session.phase}] you> ").strip()
            except EOFError:
                break
            if not raw:
                continue
            if raw == "/quit":
                break
            if raw == "/status":
                print(json.dumps(session.to_dict(), ensure_ascii=False, indent=2))
                continue
            if raw.startswith("/commit "):
                guess = raw.removeprefix("/commit ").strip()
                confidence_raw = input("Confidence [1-5, blank to skip]: ").strip()
                try:
                    confidence = int(confidence_raw) if confidence_raw else None
                    session.commit_approach(guess, confidence)
                except ValueError as error:
                    print(f"Cannot commit approach: {error}")
                    continue
                print(
                    "Approach committed. The coach may challenge it but still cannot see "
                    "the answer key."
                )
                continue
            if raw == "/review":
                try:
                    session.mark_submitted()
                except ValueError:
                    print("Commit an approach first; review unlock follows a real attempt.")
                    continue
                print(
                    "Post-submission review unlocked. This does NOT create solved/hint-free "
                    "evidence; record that separately with scripts/attempt.py."
                )
                continue
            if raw == "/oral":
                if not session.review_unlocked:
                    print("Use /review only after a real submission before oral-defense mode.")
                    continue
                session.phase = "oral_defense"
                print("Oral-defense mode: defend the signal, invariant, complexity, and boundary.")
                continue
            if raw == "/debug":
                if session.phase == "pre_attempt":
                    print("Commit an approach first; debugger mode must not become a pattern hint.")
                    continue
                session.phase = "debugger"
                print(
                    "Debugger mode: localize the first broken invariant without replacing "
                    "the solution."
                )
                continue
            if raw == "/revisit":
                session.phase = "revisit"
                print("Revisit mode: previous solution and answer metadata remain hidden.")
                continue

            user_entry = {
                "at": datetime.now().isoformat(timespec="seconds"),
                "role": "user",
                "phase": session.phase,
                "reference_unlocked": session.review_unlocked
                and session.phase in {"post_submission", "debugger"},
                "message": raw,
            }
            context = build_context(
                ROOT,
                session,
                user_message=raw,
                conversation=conversation,
            )
            _log(log_path, user_entry)
            reply = provider.generate(system_instruction(session.phase), user_prompt(context))
            print(f"\ncoach> {reply}\n")
            coach_entry = {
                "at": datetime.now().isoformat(timespec="seconds"),
                "role": "coach",
                "phase": session.phase,
                "reference_unlocked": session.review_unlocked
                and session.phase in {"post_submission", "debugger"},
                "message": reply,
            }
            _log(log_path, coach_entry)
            conversation.extend([user_entry, coach_entry])
    finally:
        provider.close()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    doctor_parser = sub.add_parser("doctor", help="check Google/Vertex configuration safely")
    _add_provider_args(doctor_parser)
    doctor_parser.add_argument("--smoke", action="store_true", help="make one tiny model request")

    start = sub.add_parser("start", help="start an interactive Socratic coaching session")
    _add_provider_args(start)
    start.add_argument("--problem")
    start.add_argument("--no-log", action="store_true")

    ask = sub.add_parser("ask", help="send one phase-controlled coach request")
    _add_provider_args(ask)
    ask.add_argument("--problem")
    ask.add_argument("--phase", choices=sorted(PHASE_POLICIES), default="pre_attempt")
    ask.add_argument("--pattern-guess")
    ask.add_argument(
        "--review-unlocked",
        action="store_true",
        help="allow reference context only in post_submission/debugger after a real submission",
    )
    ask.add_argument("message")

    args = parser.parse_args()
    if args.command == "doctor":
        return run_doctor(args)
    if args.command == "start":
        return run_start(args)
    return run_ask(args)


if __name__ == "__main__":
    raise SystemExit(main())
