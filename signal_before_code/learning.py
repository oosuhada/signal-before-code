"""Small, explainable scheduling and analytics primitives for real learner evidence."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date, timedelta
from typing import Any

FAILURE_TAXONOMY = {
    "constraint_misread",
    "pattern_recognition_failure",
    "wrong_algorithm",
    "correct_algorithm_wrong_complexity",
    "implementation_bug",
    "edge_case_failure",
    "off_by_one",
    "state_definition_failure",
    "invariant_failure",
    "timeout",
    "memory_limit",
}

STAGES = ("day0", "day3", "day14", "day30plus")
SUCCESS_INTERVALS = {"day0": 3, "day3": 11, "day14": 16, "day30plus": 60}


def next_review(stage: str, success: bool, reviewed_on: date) -> tuple[str, date]:
    """Return next stage/date using a deliberately small transparent schedule."""
    if stage not in STAGES:
        raise ValueError(f"unknown revisit stage: {stage}")
    if not success:
        retry_days = 1 if stage in {"day0", "day3"} else 3
        return stage, reviewed_on + timedelta(days=retry_days)
    index = STAGES.index(stage)
    next_stage = STAGES[min(index + 1, len(STAGES) - 1)]
    return next_stage, reviewed_on + timedelta(days=SUCCESS_INTERVALS[stage])


def confidence_mismatch(record: dict[str, Any]) -> float:
    confidence = float(record.get("confidence", 0))
    correct = bool(record.get("pattern_correct"))
    if correct:
        return max(0.0, 3.0 - confidence) * 0.5
    return max(0.0, confidence - 2.0)


def weakness_score(records: list[dict[str, Any]], today: date) -> float:
    """Score one problem's evidence; high means review sooner."""
    if not records:
        return 0.0
    score = 0.0
    revisit_failures = 0
    for record in records:
        failures = set(record.get("failure_modes", []))
        legacy = record.get("failure_mode")
        if legacy:
            failures.add(str(legacy))
        if failures & {"pattern_recognition_failure", "pattern_recognition", "wrong_algorithm"}:
            score += 4.0
        if failures & {"state_definition_failure", "invariant_failure"}:
            score += 3.0
        if failures & {"implementation_bug", "implementation", "off_by_one", "edge_case_failure"}:
            score += 1.5
        score += confidence_mismatch(record)
        if record.get("revisit_stage") != "day0" and not record.get("solved"):
            revisit_failures += 1
    score += min(6.0, revisit_failures * 2.0)

    latest = max(str(record.get("date", "0001-01-01")) for record in records)
    try:
        days_since = max(0, (today - date.fromisoformat(latest)).days)
    except ValueError:
        days_since = 0
    score += min(3.0, days_since / 30)
    return round(score, 2)


def group_by_problem(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        key = record.get("problem_key")
        if key:
            grouped[str(key)].append(record)
    return dict(grouped)


def due_problem_keys(records: list[dict[str, Any]], today: date) -> list[str]:
    latest_by_problem: dict[str, dict[str, Any]] = {}
    for record in records:
        key = str(record.get("problem_key", ""))
        if not key:
            continue
        previous = latest_by_problem.get(key)
        if previous is None or str(record.get("date", "")) >= str(previous.get("date", "")):
            latest_by_problem[key] = record
    due = []
    for key, record in latest_by_problem.items():
        raw_due = record.get("next_review_on")
        if not raw_due:
            continue
        try:
            if date.fromisoformat(str(raw_due)) <= today:
                due.append(key)
        except ValueError:
            continue
    return sorted(due)


def confidence_calibration(records: list[dict[str, Any]]) -> dict[int, dict[str, float | int]]:
    buckets: dict[int, list[bool]] = defaultdict(list)
    for record in records:
        confidence = record.get("confidence")
        if isinstance(confidence, int) and 1 <= confidence <= 5:
            buckets[confidence].append(bool(record.get("pattern_correct")))
    result: dict[int, dict[str, float | int]] = {}
    for confidence, outcomes in sorted(buckets.items()):
        correct = sum(outcomes)
        result[confidence] = {
            "attempts": len(outcomes),
            "correct": correct,
            "accuracy": correct / len(outcomes) * 100,
        }
    return result


def pattern_metrics(
    records: list[dict[str, Any]], answer_key: dict[str, str]
) -> dict[str, dict[str, float | int]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        pattern = answer_key.get(str(record.get("problem_key", "")))
        if pattern:
            grouped[pattern].append(record)
    result: dict[str, dict[str, float | int]] = {}
    for pattern, items in sorted(grouped.items()):
        total = len(items)
        pattern_correct = sum(bool(item.get("pattern_correct")) for item in items)
        solved = sum(bool(item.get("solved")) for item in items)
        hint_free = sum(
            bool(item.get("solved")) and not bool(item.get("used_hint")) for item in items
        )
        result[pattern] = {
            "attempts": total,
            "pattern_recognition_rate": pattern_correct / total * 100,
            "implementation_success_rate": solved / total * 100,
            "hint_free_solve_rate": hint_free / total * 100,
        }
    return result


def failure_counts(records: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for record in records:
        modes = record.get("failure_modes")
        if isinstance(modes, list):
            counts.update(str(mode) for mode in modes)
        elif record.get("failure_mode"):
            counts[str(record["failure_mode"])] += 1
    return counts


def learner_ledger(
    records: list[dict[str, Any]], existing: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Derive achievement counters from real records while preserving manual mastery fields."""
    existing = existing or {}
    failures = failure_counts(records)
    revisits = [record for record in records if record.get("revisit_stage") != "day0"]
    return {
        "version": "0.5",
        "policy": "Only update these values from actual personal problem-solving evidence.",
        "attempted": len(records),
        "solved": sum(bool(record.get("solved")) for record in records),
        "solved_without_hint": sum(
            bool(record.get("solved")) and not bool(record.get("used_hint")) for record in records
        ),
        "correct_pattern_identified": sum(
            bool(record.get("pattern_correct")) for record in records
        ),
        "pattern_recognition_failures": failures["pattern_recognition_failure"]
        + failures["pattern_recognition"],
        "implementation_failures": failures["implementation_bug"] + failures["implementation"],
        "revisit_successes": sum(bool(record.get("solved")) for record in revisits),
        "timed_mocks_completed": int(existing.get("timed_mocks_completed", 0)),
        "mastered_problem_keys": list(existing.get("mastered_problem_keys", [])),
        "chapter_mastery": dict(existing.get("chapter_mastery", {})),
    }
