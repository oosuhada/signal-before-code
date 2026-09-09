from __future__ import annotations

import unittest

from signal_before_code import (
    bfs_shortest_path,
    dfs_reachable,
    find_pair_with_sum,
    first_duplicate,
    frequency_count,
)


class ArrayHashTests(unittest.TestCase):
    def test_first_duplicate_returns_first_repeated_occurrence(self) -> None:
        self.assertEqual(first_duplicate(["A17", "B04", "C11", "B04", "A17"]), "B04")

    def test_first_duplicate_returns_none_for_unique_input(self) -> None:
        self.assertIsNone(first_duplicate([1, 2, 3]))

    def test_frequency_count_preserves_multiplicity(self) -> None:
        self.assertEqual(frequency_count(["a", "b", "a", "a"]), {"a": 3, "b": 1})


class TwoPointerTests(unittest.TestCase):
    def test_finds_pair_in_sorted_input(self) -> None:
        self.assertEqual(find_pair_with_sum([1, 2, 3, 4, 6, 8, 9], 11), (2, 9))

    def test_returns_none_when_no_pair_exists(self) -> None:
        self.assertIsNone(find_pair_with_sum([1, 3, 5], 20))

    def test_rejects_unsorted_input_because_order_is_the_signal(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-decreasing"):
            find_pair_with_sum([3, 1, 2], 3)


class GraphSearchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["E"],
            "D": ["F"],
            "E": ["F"],
            "F": [],
        }

    def test_bfs_returns_minimum_hop_path(self) -> None:
        path = bfs_shortest_path(self.graph, "A", "F")
        self.assertEqual(path, ["A", "B", "D", "F"])

    def test_bfs_handles_start_equal_target(self) -> None:
        self.assertEqual(bfs_shortest_path(self.graph, "A", "A"), ["A"])

    def test_bfs_returns_none_when_unreachable(self) -> None:
        graph = {**self.graph, "Z": []}
        self.assertIsNone(bfs_shortest_path(graph, "A", "Z"))

    def test_dfs_returns_reachable_component(self) -> None:
        self.assertEqual(dfs_reachable(self.graph, "C"), {"C", "E", "F"})


if __name__ == "__main__":
    unittest.main()
