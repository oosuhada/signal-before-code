from __future__ import annotations

import unittest

from scripts.practice import learner_view, problems_for_chapter, sample_mixed


class PracticeTests(unittest.TestCase):
    def test_every_chapter_has_six_curated_problems(self) -> None:
        self.assertEqual(len(problems_for_chapter("01-array-hash")), 6)
        self.assertEqual(len(problems_for_chapter("28-bitmask-subsets")), 6)

    def test_mixed_sampling_is_deterministic_with_seed(self) -> None:
        first = [problem["key"] for problem in sample_mixed(5, seed=7)]
        second = [problem["key"] for problem in sample_mixed(5, seed=7)]
        self.assertEqual(first, second)

    def test_learner_view_does_not_reveal_pattern_or_signal_answer(self) -> None:
        problem = problems_for_chapter("15-shortest-path-dijkstra")[0]
        rendered = learner_view(problem)
        self.assertNotIn("15-shortest-path-dijkstra", rendered)
        self.assertNotIn("expected pattern", rendered.lower())
        self.assertNotIn(problem["expected_signal"], rendered)


if __name__ == "__main__":
    unittest.main()
