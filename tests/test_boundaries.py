import json
import unittest
from pathlib import Path

from scripts.challenge import choose_challenge, hidden_view, reveal_view

ROOT = Path(__file__).resolve().parents[1]


class BoundaryTests(unittest.TestCase):
    def test_mutation_graph_has_twenty_chains(self) -> None:
        data = json.loads((ROOT / "mutations/chains.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data["chains"]), 20)

    def test_counterexample_library_has_twenty_docs(self) -> None:
        docs = list((ROOT / "wrong-turns").glob("*.md"))
        self.assertGreaterEqual(len([path for path in docs if path.name != "README.md"]), 20)

    def test_challenge_hides_counterexample_before_reveal(self) -> None:
        item = choose_challenge("counterexample", "sliding-window", seed=1)
        hidden = hidden_view(item, "counterexample")
        revealed = reveal_view(item, "counterexample")
        self.assertNotIn(str(item["counterexample"]), hidden)
        self.assertIn(str(item["counterexample"]), revealed)

    def test_constraint_and_requirement_modes_exist(self) -> None:
        self.assertIn(
            "Boundary review:", reveal_view(choose_challenge("constraint", seed=1), "constraint")
        )
        self.assertIn(
            "Boundary review:", reveal_view(choose_challenge("requirement", seed=1), "requirement")
        )


if __name__ == "__main__":
    unittest.main()
