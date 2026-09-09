from __future__ import annotations

import json
import unittest
from datetime import date
from pathlib import Path

from scripts.attempt import build_record, load_answer_key
from scripts.mock import build_mock
from scripts.practice import due_problems, unseen_problems, weakest_problems
from signal_before_code.learning import confidence_calibration, next_review, weakness_score

ROOT = Path(__file__).resolve().parents[1]


class LearningEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.synthetic = json.loads((ROOT / "fixtures/demo-user.json").read_text(encoding="utf-8"))[
            "attempts"
        ]

    def test_success_extends_schedule_and_failure_returns_soon(self) -> None:
        stage, due = next_review("day0", True, date(2026, 1, 1))
        self.assertEqual((stage, due.isoformat()), ("day3", "2026-01-04"))
        stage, due = next_review("day14", False, date(2026, 1, 10))
        self.assertEqual((stage, due.isoformat()), ("day14", "2026-01-13"))

    def test_high_confidence_wrong_scores_as_weakness(self) -> None:
        high_wrong = [{**self.synthetic[0], "confidence": 5}]
        low_wrong = [{**self.synthetic[0], "confidence": 1}]
        today = date(2026, 1, 2)
        self.assertGreater(weakness_score(high_wrong, today), weakness_score(low_wrong, today))

    def test_due_and_weakest_use_synthetic_fixture_without_touching_progress(self) -> None:
        due = due_problems(5, self.synthetic, date(2026, 1, 4), seed=1)
        self.assertEqual({problem["key"] for problem in due}, {"leetcode-217", "leetcode-125"})
        weakest = weakest_problems(1, self.synthetic, date(2026, 1, 4))
        self.assertEqual(weakest[0]["key"], "leetcode-217")

    def test_unseen_excludes_attempted_keys(self) -> None:
        unseen = unseen_problems(20, self.synthetic, seed=3)
        keys = {problem["key"] for problem in unseen}
        self.assertNotIn("leetcode-217", keys)
        self.assertNotIn("leetcode-125", keys)

    def test_confidence_calibration_is_evidence_based(self) -> None:
        calibration = confidence_calibration(self.synthetic)
        self.assertEqual(calibration[5]["accuracy"], 0.0)
        self.assertEqual(calibration[2]["accuracy"], 100.0)

    def test_attempt_record_compares_guess_only_after_input(self) -> None:
        answer_key = load_answer_key()
        record = build_record(
            "leetcode-217",
            "Understand",
            "duplicate check",
            "large N",
            ["01-array-hash", "sorting"],
            "01-array-hash",
            4,
            False,
            True,
            [],
            answer_key,
            date(2026, 1, 1),
        )
        self.assertTrue(record["pattern_correct"])
        self.assertEqual(record["next_revisit_stage"], "day3")

    def test_mock_never_contains_answer_pattern(self) -> None:
        session = build_mock(3, 90, seed=7)
        self.assertFalse(session["answer_key_exposed"])
        for problem in session["problems"]:
            self.assertNotIn("expected_pattern", problem)
            self.assertNotIn("expected_signal", problem)


if __name__ == "__main__":
    unittest.main()
