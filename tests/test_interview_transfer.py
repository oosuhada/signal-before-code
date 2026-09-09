from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.interview import choose_prompt, learner_prompt, load_chapters, reveal

ROOT = Path(__file__).resolve().parents[1]


class InterviewTransferTests(unittest.TestCase):
    def test_oral_defense_covers_all_chapters(self) -> None:
        chapters = load_chapters()
        self.assertEqual(len(chapters), 28)
        self.assertEqual(len({item["chapter"] for item in chapters}), 28)
        for item in chapters:
            self.assertGreaterEqual(len(item["follow_ups"]), 3)

    def test_prompt_hides_reference_defense(self) -> None:
        item = choose_prompt("15-shortest-path-dijkstra")
        prompt = learner_prompt(item)
        self.assertNotIn(str(item["thirty_second"]), prompt)
        self.assertIn("Follow-up:", prompt)
        self.assertIn("priority queue", reveal(item, "2m").lower())

    def test_java_catalog_covers_all_chapters(self) -> None:
        catalog = json.loads((ROOT / "languages/java/catalog.json").read_text(encoding="utf-8"))[
            "implementations"
        ]
        chapter_ids = {
            item["id"]
            for item in json.loads((ROOT / "curriculum/chapters.json").read_text(encoding="utf-8"))[
                "chapters"
            ]
        }
        self.assertGreaterEqual(len(catalog), 25)
        self.assertLessEqual(len(catalog), 40)
        self.assertEqual({item["chapter"] for item in catalog}, chapter_ids)


if __name__ == "__main__":
    unittest.main()
