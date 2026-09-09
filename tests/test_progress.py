from __future__ import annotations

import unittest

from scripts.progress import format_percentage, summarize


class ProgressSummaryTests(unittest.TestCase):
    def test_empty_summary_uses_none_for_rates(self) -> None:
        summary = summarize([])
        self.assertEqual(summary["attempted"], 0)
        self.assertIsNone(summary["pattern_recognition_rate"])
        self.assertEqual(format_percentage(None), "n/a")

    def test_summary_separates_recognition_and_implementation_failures(self) -> None:
        records = [
            {
                "solved": True,
                "used_hint": False,
                "pattern_correct": True,
                "failure_mode": None,
                "revisit_stage": "day0",
            },
            {
                "solved": False,
                "used_hint": True,
                "pattern_correct": False,
                "failure_mode": "pattern_recognition",
                "revisit_stage": "day0",
            },
            {
                "solved": False,
                "used_hint": False,
                "pattern_correct": True,
                "failure_mode": "implementation",
                "revisit_stage": "day3",
            },
            {
                "solved": True,
                "used_hint": False,
                "pattern_correct": True,
                "failure_mode": None,
                "revisit_stage": "day14",
            },
        ]

        summary = summarize(records)
        self.assertEqual(summary["attempted"], 4)
        self.assertEqual(summary["solved_without_hint"], 2)
        self.assertEqual(summary["correct_pattern"], 3)
        self.assertEqual(summary["implementation_failures"], 1)
        self.assertEqual(summary["recognition_failures"], 1)
        self.assertEqual(summary["pattern_recognition_rate"], 75.0)
        self.assertEqual(summary["hint_free_solve_rate"], 50.0)
        self.assertEqual(summary["revisit_success_rate"], 50.0)


if __name__ == "__main__":
    unittest.main()
