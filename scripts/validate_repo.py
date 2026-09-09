#!/usr/bin/env python3
"""Validate the textbook contract and keep learner evidence separate from generated content."""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from signal_before_code.learning import FAILURE_TAXONOMY, learner_ledger  # noqa: E402
from signal_before_code.tracing import TRACE_BUILDERS, build_trace  # noqa: E402

REQUIRED_CHAPTER_HEADINGS = [
    "## 1. What problem shape does this solve?",
    "## 2. Signals to notice",
    "## 3. Naive idea",
    "## 4. Why the naive idea breaks",
    "## 5. Core intuition",
    "## 6. Invariant",
    "## 7. Step-by-step walkthrough",
    "## 8. Implementation",
    "## 9. Complexity",
    "## 10. Common mistakes",
    "## 11. When NOT to use it",
    "## 12. Neighboring patterns",
    "## 13. Mutation ladder",
    "## 14. Practice ladder",
]

ALLOWED_STAGES = {"Understand", "Recognize", "Apply"}
ALLOWED_DIFFICULTIES = {"intro", "intermediate", "advanced"}
EXPECTED_HOSTS = {
    "LeetCode": "leetcode.com",
    "Programmers": "school.programmers.co.kr",
    "Baekjoon": "www.acmicpc.net",
}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PYTHON_FENCE = re.compile(r"```python\n(.*?)```", re.DOTALL)

REQUIRED_TRACES = {
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

COUNTEREXAMPLE_HEADINGS = [
    "## Tempting idea",
    "## Why it looks reasonable",
    "## Smallest counterexample",
    "## Step-by-step failure",
    "## Correct signal",
    "## Better candidates",
    "## General lesson",
]


def read_json(relative: str, errors: list[str]) -> dict[str, object] | None:
    path = ROOT / relative
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{relative}: invalid JSON: {error}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{relative}: root must be an object")
        return None
    return value


def load_chapters(errors: list[str]) -> list[dict[str, str]]:
    data = read_json("curriculum/chapters.json", errors)
    if data is None:
        return []
    chapters = data.get("chapters")
    if not isinstance(chapters, list):
        errors.append("curriculum/chapters.json: chapters must be a list")
        return []
    if len(chapters) != 28:
        errors.append(f"expected 28 textbook chapters, found {len(chapters)}")

    ids: set[str] = set()
    typed: list[dict[str, str]] = []
    for index, chapter in enumerate(chapters):
        if not isinstance(chapter, dict):
            errors.append(f"chapter[{index}] must be an object")
            continue
        chapter_id = chapter.get("id")
        if not isinstance(chapter_id, str) or not chapter_id:
            errors.append(f"chapter[{index}] missing id")
            continue
        if chapter_id in ids:
            errors.append(f"duplicate chapter id: {chapter_id}")
        ids.add(chapter_id)
        if chapter.get("chapter_status") != "textbook_complete":
            errors.append(f"{chapter_id}: chapter_status must be textbook_complete")
        if chapter.get("learner_status") not in {
            "not_started",
            "in_progress",
            "revisiting",
            "mastered",
        }:
            errors.append(f"{chapter_id}: invalid learner_status")
        typed.append({key: str(value) for key, value in chapter.items()})
    return typed


def validate_chapters(chapters: list[dict[str, str]], errors: list[str]) -> None:
    chapter_ids = {chapter["id"] for chapter in chapters}
    found_dirs = {
        path.parent.name for path in (ROOT / "patterns").glob("*/README.md") if path.is_file()
    }
    if found_dirs != chapter_ids:
        missing = sorted(chapter_ids - found_dirs)
        extra = sorted(found_dirs - chapter_ids)
        if missing:
            errors.append(f"pattern directories missing: {missing}")
        if extra:
            errors.append(f"unregistered pattern directories: {extra}")

    for chapter_id in sorted(chapter_ids):
        path = ROOT / "patterns" / chapter_id / "README.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for heading in REQUIRED_CHAPTER_HEADINGS:
            if heading not in text:
                errors.append(f"{path.relative_to(ROOT)} missing heading {heading!r}")
        if "scaffold only" in text.lower():
            errors.append(f"{path.relative_to(ROOT)} still claims scaffold-only state")
        if len(text.splitlines()) < 70:
            errors.append(f"{path.relative_to(ROOT)} is too thin for textbook_complete")


def validate_python_fences(errors: list[str]) -> int:
    compiled = 0
    for markdown in sorted((ROOT / "patterns").glob("*/README.md")):
        text = markdown.read_text(encoding="utf-8")
        for index, snippet in enumerate(PYTHON_FENCE.findall(text), start=1):
            try:
                compile(snippet, f"{markdown.relative_to(ROOT)}#python-{index}", "exec")
            except SyntaxError as error:
                errors.append(
                    f"{markdown.relative_to(ROOT)} python fence {index} has syntax error: {error}"
                )
            compiled += 1
    return compiled


def validate_problem_catalog(
    chapter_ids: set[str], errors: list[str]
) -> tuple[int, dict[str, str], dict[str, list[str]]]:
    catalog = read_json("curriculum/problems.json", errors)
    answers = read_json("curriculum/answer-key.json", errors)
    if catalog is None or answers is None:
        return 0, {}, {}

    problems = catalog.get("problems")
    mapping = answers.get("expected_pattern")
    if not isinstance(problems, list):
        errors.append("curriculum/problems.json: problems must be a list")
        return 0, {}, {}
    if not isinstance(mapping, dict):
        errors.append("curriculum/answer-key.json: expected_pattern must be an object")
        return len(problems), {}, {}

    if not 150 <= len(problems) <= 200:
        errors.append(f"curated roadmap should contain 150-200 problems, found {len(problems)}")

    required = {
        "key",
        "platform",
        "id",
        "title",
        "url",
        "difficulty",
        "stage",
        "abstract",
        "expected_signal",
    }
    forbidden = {"pattern", "expected_pattern", "chapter"}
    seen_keys: set[str] = set()
    seen_problem_ids: set[tuple[str, str]] = set()
    stages_by_chapter: dict[str, list[str]] = defaultdict(list)

    for index, problem in enumerate(problems):
        label = f"problem[{index}]"
        if not isinstance(problem, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = required - problem.keys()
        if missing:
            errors.append(f"{label} missing keys: {sorted(missing)}")
            continue
        leaked = forbidden & problem.keys()
        if leaked:
            errors.append(f"{label} leaks review-only fields: {sorted(leaked)}")

        key = str(problem["key"])
        if key in seen_keys:
            errors.append(f"duplicate problem key: {key}")
        seen_keys.add(key)

        platform = str(problem["platform"])
        problem_id = str(problem["id"])
        pair = (platform, problem_id)
        if pair in seen_problem_ids:
            errors.append(f"duplicate problem id: {platform} {problem_id}")
        seen_problem_ids.add(pair)

        stage = problem["stage"]
        if stage not in ALLOWED_STAGES:
            errors.append(f"{key}: invalid stage {stage}")
        if problem["difficulty"] not in ALLOWED_DIFFICULTIES:
            errors.append(f"{key}: invalid difficulty {problem['difficulty']}")

        expected_host = EXPECTED_HOSTS.get(platform)
        actual_host = urlparse(str(problem["url"])).netloc
        if expected_host is None:
            errors.append(f"{key}: unsupported platform {platform}")
        elif actual_host != expected_host:
            errors.append(f"{key}: URL host {actual_host} does not match {expected_host}")

        if len(str(problem["abstract"])) > 240:
            errors.append(f"{key}: abstract is too long; keep learner-facing summaries compact")

        chapter = mapping.get(key)
        if chapter not in chapter_ids:
            errors.append(f"{key}: answer key points to unknown chapter {chapter!r}")
        elif isinstance(stage, str):
            stages_by_chapter[str(chapter)].append(stage)

    answer_keys = set(mapping)
    if answer_keys != seen_keys:
        missing_answers = sorted(seen_keys - answer_keys)
        extra_answers = sorted(answer_keys - seen_keys)
        if missing_answers:
            errors.append(f"problem keys missing answer metadata: {missing_answers}")
        if extra_answers:
            errors.append(f"answer metadata without learner-facing problem: {extra_answers}")

    for chapter_id in sorted(chapter_ids):
        stages = stages_by_chapter.get(chapter_id, [])
        if len(stages) < 6:
            errors.append(
                f"{chapter_id}: expected at least 6 curated problems, found {len(stages)}"
            )
        counts = Counter(stages)
        for stage in ALLOWED_STAGES:
            if counts[stage] < 2:
                errors.append(f"{chapter_id}: expected at least 2 {stage} problems")

    typed_mapping = {str(key): str(value) for key, value in mapping.items()}
    return len(problems), typed_mapping, stages_by_chapter


def validate_learner_status(chapter_ids: set[str], errors: list[str]) -> None:
    data = read_json("progress/learner-status.json", errors)
    if data is None:
        return
    counters = [
        "attempted",
        "solved",
        "solved_without_hint",
        "correct_pattern_identified",
        "pattern_recognition_failures",
        "implementation_failures",
        "revisit_successes",
        "timed_mocks_completed",
    ]
    for name in counters:
        value = data.get(name)
        if not isinstance(value, int) or value < 0:
            errors.append(f"progress/learner-status.json: {name} must be a non-negative integer")

    attempted = data.get("attempted", 0)
    solved = data.get("solved", 0)
    hint_free = data.get("solved_without_hint", 0)
    if isinstance(attempted, int) and isinstance(solved, int) and solved > attempted:
        errors.append("learner status cannot have solved > attempted")
    if isinstance(solved, int) and isinstance(hint_free, int) and hint_free > solved:
        errors.append("learner status cannot have solved_without_hint > solved")

    mastered = data.get("mastered_problem_keys")
    if not isinstance(mastered, list):
        errors.append("learner status mastered_problem_keys must be a list")
    chapter_mastery = data.get("chapter_mastery")
    if not isinstance(chapter_mastery, dict):
        errors.append("learner status chapter_mastery must be an object")
    elif set(chapter_mastery) - chapter_ids:
        errors.append("learner status contains unknown chapter mastery keys")

    if attempted == 0:
        nonzero = [name for name in counters[1:] if data.get(name) != 0]
        if nonzero:
            errors.append(f"zero-attempt ledger cannot contain achievement counters: {nonzero}")
        if mastered:
            errors.append("zero-attempt ledger cannot contain mastered problems")
        if chapter_mastery:
            errors.append("zero-attempt ledger cannot contain chapter mastery claims")


def validate_revisit_csv(errors: list[str]) -> None:
    path = ROOT / "progress/revisits.csv"
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            header = next(csv.reader(handle), [])
    except OSError as error:
        errors.append(f"cannot read progress/revisits.csv: {error}")
        return
    expected = ["problem_key", "first_solved_on", "due_on", "stage", "status"]
    if header != expected:
        errors.append(f"progress/revisits.csv header must be {expected}, found {header}")


def validate_personal_templates(errors: list[str]) -> None:
    required = [
        "attempts/TEMPLATE.md",
        "revisits/TEMPLATE.md",
        "mixed/TEMPLATE.md",
        "mocks/TEMPLATE.md",
    ]
    for relative in required:
        path = ROOT / relative
        if not path.exists():
            errors.append(f"missing personal learning template: {relative}")


def validate_visual_traces(errors: list[str]) -> None:
    missing = REQUIRED_TRACES - TRACE_BUILDERS.keys()
    if missing:
        errors.append(f"missing required visual traces: {sorted(missing)}")
    for name in sorted(REQUIRED_TRACES & TRACE_BUILDERS.keys()):
        trace = build_trace(name)
        if trace.get("algorithm") != name:
            errors.append(f"trace {name}: algorithm field mismatch")
        steps = trace.get("steps")
        if not isinstance(steps, list) or not steps:
            errors.append(f"trace {name}: steps must be a non-empty list")
            continue
        for index, step in enumerate(steps):
            if step.get("step") != index:
                errors.append(f"trace {name}: expected step number {index}")
            for field in ["state", "decision", "invariant", "visual", "prompt"]:
                if not step.get(field):
                    errors.append(f"trace {name} step {index}: missing {field}")

    wrong = read_json("traces/wrong-states.json", errors)
    if wrong is not None:
        traces = wrong.get("traces")
        if not isinstance(traces, list) or len(traces) < 5:
            errors.append("traces/wrong-states.json must contain at least 5 wrong-state traces")


def validate_boundaries(errors: list[str]) -> tuple[int, int, int]:
    mutations = read_json("mutations/chains.json", errors)
    chains: list[object] = []
    if mutations is not None:
        value = mutations.get("chains")
        if isinstance(value, list):
            chains = value
        else:
            errors.append("mutations/chains.json: chains must be a list")
    if len(chains) < 20:
        errors.append(f"expected at least 20 mutation chains, found {len(chains)}")
    for index, chain in enumerate(chains):
        if not isinstance(chain, dict) or not chain.get("id") or not chain.get("transitions"):
            errors.append(f"mutation chain {index} needs id and non-empty transitions")

    wrong_turns = sorted((ROOT / "wrong-turns").glob("*.md"))
    wrong_turns = [path for path in wrong_turns if path.name != "README.md"]
    if len(wrong_turns) < 20:
        errors.append(f"expected at least 20 counterexample docs, found {len(wrong_turns)}")
    for path in wrong_turns:
        text = path.read_text(encoding="utf-8")
        for heading in COUNTEREXAMPLE_HEADINGS:
            if heading not in text:
                errors.append(
                    f"{path.relative_to(ROOT)} missing counterexample heading {heading!r}"
                )

    counterexamples = read_json("challenges/counterexamples.json", errors)
    if counterexamples is not None:
        items = counterexamples.get("challenges")
        if not isinstance(items, list) or len(items) < 20:
            errors.append("challenges/counterexamples.json must contain at least 20 challenges")

    adversarial = read_json("practice-guides/adversarial-recognition.json", errors)
    prompts: list[object] = []
    if adversarial is not None:
        value = adversarial.get("prompts")
        if isinstance(value, list):
            prompts = value
        else:
            errors.append("adversarial-recognition.json: prompts must be a list")
    if not 50 <= len(prompts) <= 100:
        errors.append(
            f"adversarial recognition set should contain 50-100 prompts, found {len(prompts)}"
        )
    prompt_ids = [item.get("id") for item in prompts if isinstance(item, dict)]
    if len(prompt_ids) != len(set(prompt_ids)):
        errors.append("adversarial recognition prompt ids must be unique")
    return len(chains), len(wrong_turns), len(prompts)


def validate_learning_engine(errors: list[str]) -> None:
    taxonomy = read_json("progress/failure-taxonomy.json", errors)
    if taxonomy is not None:
        modes = taxonomy.get("failure_modes")
        if not isinstance(modes, list) or set(modes) != FAILURE_TAXONOMY:
            errors.append("progress/failure-taxonomy.json does not match the learning engine")

    fixture = read_json("fixtures/demo-user.json", errors)
    if fixture is not None and fixture.get("synthetic") is not True:
        errors.append("fixtures/demo-user.json must be explicitly marked synthetic")

    for relative in [
        "scripts/attempt.py",
        "scripts/mock.py",
        "scripts/practice.py",
        "scripts/progress.py",
    ]:
        if not (ROOT / relative).exists():
            errors.append(f"missing learning engine CLI: {relative}")

    attempts_path = ROOT / "progress" / "attempts.jsonl"
    status = read_json("progress/learner-status.json", errors)
    if status is None:
        return
    records: list[dict[str, object]] = []
    if attempts_path.exists():
        for line_number, line in enumerate(
            attempts_path.read_text(encoding="utf-8").splitlines(), 1
        ):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                errors.append(f"progress/attempts.jsonl:{line_number}: invalid JSON: {error.msg}")
                continue
            if isinstance(record, dict):
                records.append(record)
            else:
                errors.append(f"progress/attempts.jsonl:{line_number}: record must be an object")

    derived = learner_ledger(records, status)
    counters = [
        "attempted",
        "solved",
        "solved_without_hint",
        "correct_pattern_identified",
        "pattern_recognition_failures",
        "implementation_failures",
        "revisit_successes",
    ]
    for counter in counters:
        if status.get(counter) != derived[counter]:
            errors.append(
                f"learner-status {counter}={status.get(counter)!r} disagrees with real attempts "
                f"({derived[counter]})"
            )


def validate_local_markdown_links(errors: list[str]) -> None:
    for markdown in ROOT.rglob("*.md"):
        if ".git" in markdown.parts:
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (markdown.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(
                    f"{markdown.relative_to(ROOT)}: local link escapes repository: {raw_target}"
                )
                continue
            if not resolved.exists():
                errors.append(f"{markdown.relative_to(ROOT)}: broken local link: {raw_target}")


def main() -> int:
    errors: list[str] = []
    chapters = load_chapters(errors)
    chapter_ids = {chapter["id"] for chapter in chapters}
    validate_chapters(chapters, errors)
    python_fences = validate_python_fences(errors)
    problem_count, _, _ = validate_problem_catalog(chapter_ids, errors)
    validate_learner_status(chapter_ids, errors)
    read_json("progress/schema.json", errors)
    validate_revisit_csv(errors)
    validate_personal_templates(errors)
    validate_visual_traces(errors)
    mutation_count, wrong_turn_count, adversarial_count = validate_boundaries(errors)
    validate_learning_engine(errors)
    validate_local_markdown_links(errors)

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Repository validation passed: "
        f"{len(chapters)} textbook-complete chapters, "
        f"{problem_count} curated problems, "
        f"{python_fences} chapter Python examples compiled, "
        f"{len(REQUIRED_TRACES)} core visual traces, "
        f"{mutation_count} mutation chains, {wrong_turn_count} counterexamples, "
        f"{adversarial_count} adversarial prompts, "
        "learning engine/evidence contract and local links OK."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
