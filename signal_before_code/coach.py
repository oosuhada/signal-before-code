"""Repository-native AI coaching policy and context construction.

The coach controls what repository data can reach an LLM at each learning phase,
so provider code cannot accidentally leak answer metadata before review.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

CoachPhase = Literal[
    "pre_attempt",
    "approach_committed",
    "post_submission",
    "revisit",
    "oral_defense",
    "debugger",
]

SAFE_PROBLEM_FIELDS = (
    "key",
    "platform",
    "id",
    "title",
    "url",
    "difficulty",
    "stage",
    "abstract",
)

REFERENCE_PHASES = {"post_submission", "debugger", "oral_defense"}
FORBIDDEN_REFERENCE_KEYS = {
    "expected_pattern",
    "expected_signal",
    "chapter_reference",
    "reference_solution",
}

REVIEW_SECTIONS = (
    "## 2. Signals to notice",
    "## 6. Invariant",
    "## 10. Common mistakes",
    "## 11. When NOT to use it",
    "## 12. Neighboring patterns",
    "## 13. Mutation ladder",
)

PHASE_POLICIES: dict[str, dict[str, Any]] = {
    "pre_attempt": {
        "role": "Socratic coach",
        "allowed": [
            "clarify wording or input/output",
            "ask which constraints matter",
            "ask for a brute-force baseline",
            "ask the learner to name candidate approaches",
        ],
        "forbidden": [
            "name the expected pattern",
            "rank candidate algorithms",
            "state the key invariant",
            "provide solution code or pseudocode",
            "reveal the repository expected signal",
        ],
        "response_style": "Ask one or two short questions. Do not teach the answer yet.",
    },
    "approach_committed": {
        "role": "Adversarial interviewer",
        "allowed": [
            "challenge the learner's chosen approach",
            "ask for complexity derived from operations",
            "ask for a correctness argument",
            "ask for a counterexample or mutation",
        ],
        "forbidden": [
            "confirm whether the chosen pattern matches the answer key",
            "replace the learner's approach with the reference solution",
            "state the repository expected signal",
        ],
        "response_style": "Challenge before correcting. Prefer questions over declarations.",
    },
    "post_submission": {
        "role": "Reviewer and algorithm-defense interviewer",
        "allowed": [
            "reveal the expected pattern and signal",
            "review correctness and complexity",
            "explain the invariant",
            "compare neighboring approaches",
            "generate counterexamples and mutations",
        ],
        "forbidden": [
            "fabricate solved, hint-free, mastery, or revisit evidence",
        ],
        "response_style": "Derive the answer from constraints and failure boundaries before code.",
    },
    "revisit": {
        "role": "Recall examiner",
        "allowed": [
            "ask for signals, invariant, complexity, and a mutation",
            "probe reconstruction without previous solution code",
        ],
        "forbidden": [
            "reveal previous solution code before the learner attempts reconstruction",
            "mark the revisit successful on the learner's behalf",
        ],
        "response_style": (
            "Test retrieval. Keep the answer hidden until the learner explicitly reviews."
        ),
    },
    "oral_defense": {
        "role": "Technical interviewer",
        "allowed": [
            "ask 30-second, 2-minute, and deep follow-up questions",
            "challenge complexity and applicability boundaries",
        ],
        "forbidden": ["claim the learner passed an interview"],
        "response_style": "Ask one follow-up at a time and press on unsupported claims.",
    },
    "debugger": {
        "role": "Invariant debugger",
        "allowed": [
            "ask for the first state where expected and actual behavior diverge",
            "ask about boundary conventions, visited timing, stale state, and base cases",
        ],
        "forbidden": [
            "replace debugging with a full correct solution",
            "reveal answer-key metadata before post-submission review",
        ],
        "response_style": "Localize the first broken invariant; do not rewrite the whole solution.",
    },
}


@dataclass(slots=True)
class LearnerContext:
    first_impression: str = ""
    constraints: str = ""
    candidates: list[str] = field(default_factory=list)
    pattern_guess: str = ""
    confidence: int | None = None
    notes: str = ""


@dataclass(slots=True)
class CoachSession:
    problem_key: str
    phase: CoachPhase = "pre_attempt"
    learner: LearnerContext = field(default_factory=LearnerContext)
    review_unlocked: bool = False

    def commit_approach(
        self,
        pattern_guess: str,
        confidence: int | None = None,
        candidates: list[str] | None = None,
    ) -> None:
        if self.phase != "pre_attempt":
            raise ValueError("approach can only be committed from pre_attempt")
        if confidence is not None and not 1 <= confidence <= 5:
            raise ValueError("confidence must be between 1 and 5")
        self.learner.pattern_guess = pattern_guess.strip()
        self.learner.confidence = confidence
        if candidates is not None:
            self.learner.candidates = list(candidates)
        self.phase = "approach_committed"

    def mark_submitted(self) -> None:
        if self.phase not in {"approach_committed", "debugger"}:
            raise ValueError("submission review requires a committed approach")
        self.review_unlocked = True
        self.phase = "post_submission"

    def to_dict(self) -> dict[str, Any]:
        return {
            "problem_key": self.problem_key,
            "phase": self.phase,
            "learner": asdict(self.learner),
            "review_unlocked": self.review_unlocked,
        }


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return value


def load_problem(root: Path, problem_key: str) -> dict[str, Any]:
    problems = _read_json(root / "curriculum" / "problems.json").get("problems", [])
    for problem in problems:
        if isinstance(problem, dict) and problem.get("key") == problem_key:
            return problem
    raise ValueError(f"unknown problem key: {problem_key}")


def learner_problem_view(problem: dict[str, Any]) -> dict[str, Any]:
    """Return only fields that are safe before pattern classification."""
    return {key: problem[key] for key in SAFE_PROBLEM_FIELDS if key in problem}


def _extract_sections(markdown: str, headings: tuple[str, ...] = REVIEW_SECTIONS) -> dict[str, str]:
    lines = markdown.splitlines()
    wanted = set(headings)
    result: dict[str, list[str]] = {}
    active: str | None = None
    for line in lines:
        if line.startswith("## "):
            active = line if line in wanted else None
            if active:
                result.setdefault(active, [])
            continue
        if active is not None:
            result[active].append(line)
    return {
        heading.removeprefix("## "): "\n".join(section_lines).strip()
        for heading, section_lines in result.items()
    }


def _review_reference(root: Path, problem: dict[str, Any]) -> dict[str, Any]:
    answer_key = _read_json(root / "curriculum" / "answer-key.json").get("expected_pattern", {})
    expected_pattern = answer_key.get(problem["key"])
    if not isinstance(expected_pattern, str):
        raise ValueError(f"answer key missing for {problem['key']}")
    chapter_path = root / "patterns" / expected_pattern / "README.md"
    chapter_sections = _extract_sections(chapter_path.read_text(encoding="utf-8"))
    return {
        "expected_pattern": expected_pattern,
        "expected_signal": problem.get("expected_signal", ""),
        "chapter_reference": chapter_sections,
    }


def build_context(
    root: Path,
    session: CoachSession,
    *,
    user_message: str = "",
    conversation: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    problem = load_problem(root, session.problem_key)
    history = list(conversation or [])[-8:]
    if not (session.review_unlocked and session.phase in REFERENCE_PHASES):
        history = [entry for entry in history if not entry.get("reference_unlocked")]
    context: dict[str, Any] = {
        "phase": session.phase,
        "policy": PHASE_POLICIES[session.phase],
        "problem": learner_problem_view(problem),
        "learner": asdict(session.learner),
        "conversation": history,
        "user_message": user_message,
    }
    if session.review_unlocked and session.phase in REFERENCE_PHASES:
        context["reference"] = _review_reference(root, problem)
    assert_context_policy(context)
    return context


def assert_context_policy(context: dict[str, Any]) -> None:
    phase = context.get("phase")
    reference = context.get("reference")
    if reference is not None and phase in REFERENCE_PHASES:
        return
    if reference is not None:
        raise ValueError(f"reference context is forbidden during {phase}")
    problem = context.get("problem", {})
    if isinstance(problem, dict):
        leaked = FORBIDDEN_REFERENCE_KEYS & set(problem)
        if leaked:
            raise ValueError(f"learner problem view leaked fields: {sorted(leaked)}")
        if "expected_signal" in problem:
            raise ValueError("expected_signal is forbidden before review")


def system_instruction(phase: CoachPhase) -> str:
    policy = PHASE_POLICIES[phase]
    allowed = "\n".join(f"- {item}" for item in policy["allowed"])
    forbidden = "\n".join(f"- {item}" for item in policy["forbidden"])
    return f"""You are the embedded Signal Before Code coach.

Your job is to train algorithm selection, not to maximize answer speed.
The learner's actual achievements are written only by explicit learner evidence;
never infer mastery.

Current phase: {phase}
Role: {policy["role"]}

Allowed:
{allowed}

Forbidden:
{forbidden}

Style: {policy["response_style"]}

Never mention hidden repository fields that are not present in the supplied context.
If the learner directly asks for a forbidden answer, keep the boundary and ask a useful
question instead.
Reply in the same language as the learner's latest message unless they ask for another language.
""".strip()


def user_prompt(context: dict[str, Any]) -> str:
    assert_context_policy(context)
    return (
        "Use only the following repository context plus the learner's message. "
        "Do not infer hidden answer-key data.\n\n"
        + json.dumps(context, ensure_ascii=False, indent=2)
    )


def attempted_problem_keys(root: Path) -> set[str]:
    path = root / "progress" / "attempts.jsonl"
    if not path.exists():
        return set()
    keys: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if isinstance(record, dict) and record.get("problem_key"):
            keys.add(str(record["problem_key"]))
    return keys


def choose_problem_key(root: Path, requested: str | None = None) -> str:
    if requested:
        load_problem(root, requested)
        return requested
    attempted = attempted_problem_keys(root)
    problems = _read_json(root / "curriculum" / "problems.json").get("problems", [])
    for problem in problems:
        if isinstance(problem, dict) and problem.get("key") not in attempted:
            return str(problem["key"])
    raise ValueError("all curated problems have attempts; pass --problem explicitly")
