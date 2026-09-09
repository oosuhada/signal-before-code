from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from signal_before_code.coach import (
    CoachSession,
    assert_context_policy,
    build_context,
    system_instruction,
)
from signal_before_code.google_llm import GoogleProviderConfig, load_env_file


class CoachPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / "curriculum").mkdir()
        (self.root / "patterns" / "05-binary-search").mkdir(parents=True)
        (self.root / "curriculum" / "problems.json").write_text(
            json.dumps(
                {
                    "problems": [
                        {
                            "key": "demo-1",
                            "platform": "Demo",
                            "id": "1",
                            "title": "Boundary",
                            "url": "https://example.invalid/1",
                            "difficulty": "intro",
                            "stage": "Recognize",
                            "abstract": "Find a target in ordered values.",
                            "expected_signal": "Sorted order permits half elimination.",
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        (self.root / "curriculum" / "answer-key.json").write_text(
            json.dumps({"expected_pattern": {"demo-1": "05-binary-search"}}),
            encoding="utf-8",
        )
        chapter = """# Binary Search

## 2. Signals to notice
sorted and monotonic

## 6. Invariant
answer remains in [left, right]

## 10. Common mistakes
off by one

## 11. When NOT to use it
no monotonicity

## 12. Neighboring patterns
two pointers

## 13. Mutation ladder
answer search
"""
        (self.root / "patterns" / "05-binary-search" / "README.md").write_text(
            chapter, encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_pre_attempt_does_not_load_answer_metadata(self) -> None:
        context = build_context(self.root, CoachSession("demo-1"), user_message="What matters?")
        serialized = json.dumps(context)
        self.assertNotIn("expected_pattern", serialized)
        self.assertNotIn("expected_signal", serialized)
        self.assertNotIn("05-binary-search", serialized)
        self.assertNotIn("half elimination", serialized)

    def test_committed_phase_still_hides_answer_key(self) -> None:
        session = CoachSession("demo-1")
        session.commit_approach("two-pointers", confidence=4)
        context = build_context(self.root, session, user_message="Does this work?")
        self.assertEqual(context["learner"]["pattern_guess"], "two-pointers")
        self.assertNotIn("reference", context)

    def test_post_submission_unlocks_reference(self) -> None:
        session = CoachSession("demo-1")
        session.commit_approach("two-pointers", confidence=4)
        session.mark_submitted()
        self.assertTrue(session.review_unlocked)
        context = build_context(self.root, session)
        self.assertEqual(context["reference"]["expected_pattern"], "05-binary-search")
        self.assertIn("Sorted order", context["reference"]["expected_signal"])
        self.assertIn("6. Invariant", context["reference"]["chapter_reference"])

    def test_oral_defense_can_use_reference_only_after_review(self) -> None:
        session = CoachSession("demo-1")
        session.commit_approach("two-pointers", confidence=3)
        session.phase = "oral_defense"
        self.assertNotIn("reference", build_context(self.root, session))
        session.phase = "approach_committed"
        session.mark_submitted()
        session.phase = "oral_defense"
        self.assertIn("reference", build_context(self.root, session))

    def test_debugger_only_sees_reference_after_review_unlock(self) -> None:
        session = CoachSession("demo-1")
        session.commit_approach("two-pointers", confidence=3)
        session.phase = "debugger"
        self.assertNotIn("reference", build_context(self.root, session))
        session.mark_submitted()
        session.phase = "debugger"
        self.assertIn("reference", build_context(self.root, session))

    def test_policy_rejects_reference_in_locked_phase(self) -> None:
        with self.assertRaises(ValueError):
            assert_context_policy(
                {
                    "phase": "pre_attempt",
                    "problem": {},
                    "reference": {"expected_pattern": "05-binary-search"},
                }
            )

    def test_revisit_filters_review_unlocked_history(self) -> None:
        session = CoachSession("demo-1")
        session.commit_approach("two-pointers", confidence=3)
        session.mark_submitted()
        session.phase = "revisit"
        context = build_context(
            self.root,
            session,
            conversation=[
                {
                    "role": "coach",
                    "message": "The reference pattern is binary search.",
                    "reference_unlocked": True,
                },
                {
                    "role": "user",
                    "message": "I originally guessed two pointers.",
                    "reference_unlocked": False,
                },
            ],
        )
        self.assertEqual(len(context["conversation"]), 1)
        self.assertNotIn("binary search", json.dumps(context))

    def test_system_instruction_preserves_socratic_boundary(self) -> None:
        instruction = system_instruction("pre_attempt")
        self.assertIn("Socratic", instruction)
        self.assertIn("Forbidden", instruction)
        self.assertIn("solution code", instruction)

    def test_google_provider_defaults_to_vertex_adc(self) -> None:
        config = GoogleProviderConfig.from_env(
            backend="vertex-adc",
            project="demo-project",
            location="global",
            model="gemini-3.5-flash",
        )
        self.assertEqual(config.backend, "vertex-adc")
        self.assertEqual(config.project, "demo-project")

    def test_env_file_loads_only_allowlisted_config(self) -> None:
        env = self.root / "coach.env"
        env.write_text(
            "GOOGLE_CLOUD_PROJECT=demo-project\n"
            "SIGNAL_BEFORE_CODE_MODEL=gemini-3.5-flash\n"
            "UNRELATED_VALUE=ignore-me\n",
            encoding="utf-8",
        )
        old_project = os.environ.pop("GOOGLE_CLOUD_PROJECT", None)
        old_model = os.environ.pop("SIGNAL_BEFORE_CODE_MODEL", None)
        old_unrelated = os.environ.pop("UNRELATED_VALUE", None)
        try:
            loaded = load_env_file(env)
            self.assertEqual(set(loaded), {"GOOGLE_CLOUD_PROJECT", "SIGNAL_BEFORE_CODE_MODEL"})
            self.assertNotIn("UNRELATED_VALUE", os.environ)
        finally:
            for name, value in [
                ("GOOGLE_CLOUD_PROJECT", old_project),
                ("SIGNAL_BEFORE_CODE_MODEL", old_model),
                ("UNRELATED_VALUE", old_unrelated),
            ]:
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value


if __name__ == "__main__":
    unittest.main()
