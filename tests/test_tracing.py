import json
import unittest
from pathlib import Path

from signal_before_code.tracing import TRACE_BUILDERS, build_trace, render_step

ROOT = Path(__file__).resolve().parents[1]


class TraceTests(unittest.TestCase):
    def test_required_visual_algorithms_exist(self) -> None:
        required = {
            "two-pointers",
            "sliding-window",
            "binary-search",
            "heap",
            "bfs",
            "dfs",
            "union-find",
            "topological-sort",
            "dijkstra",
            "dp",
            "monotonic-stack",
            "backtracking",
        }
        self.assertTrue(required <= TRACE_BUILDERS.keys())

    def test_trace_steps_have_reasoning_fields(self) -> None:
        for name in TRACE_BUILDERS:
            trace = build_trace(name)
            self.assertGreater(len(trace["steps"]), 0, name)
            for index, step in enumerate(trace["steps"]):
                self.assertEqual(index, step["step"], name)
                self.assertTrue(step["invariant"], name)
                self.assertTrue(step["prompt"], name)
                self.assertTrue(step["visual"], name)

    def test_predict_view_hides_decision(self) -> None:
        step = build_trace("binary-search")["steps"][0]
        hidden = render_step(step, reveal=False)
        self.assertIn("Predict:", hidden)
        self.assertNotIn(step["decision"], hidden)

    def test_wrong_state_library_has_five_examples(self) -> None:
        data = json.loads((ROOT / "traces/wrong-states.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data["traces"]), 5)
        self.assertTrue(all(item["broken_invariant"] for item in data["traces"]))


if __name__ == "__main__":
    unittest.main()
