#!/usr/bin/env python3
"""Validate the lightweight learning-repository contract without external services."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

PATTERNS = {
    "01-array-hash": "seed",
    "02-two-pointers": "seed",
    "03-sliding-window": "scaffold",
    "04-stack-queue": "scaffold",
    "05-binary-search": "scaffold",
    "06-heap-priority-queue": "scaffold",
    "07-bfs-dfs": "seed",
}

REQUIRED_SEED_HEADINGS = [
    "## 1. The Situation",
    "## 2. First Naive Idea",
    "## 3. Why It Breaks",
    "## 4. Signal to Notice",
    "## 5. Candidate Approaches",
    "## 6. Why This Pattern",
    "## 7. Walkthrough",
    "## 8. Implementation",
    "## 9. Complexity",
    "## 10. When NOT to Use It",
    "## 11. Mutation",
    "## 12. Practice",
]

ALLOWED_LEVELS = {"Understand", "Recognize", "Apply"}
EXPECTED_HOSTS = {
    "LeetCode": "leetcode.com",
    "Programmers": "school.programmers.co.kr",
    "Baekjoon": "www.acmicpc.net",
}

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def validate_chapters(errors: list[str]) -> None:
    for pattern, state in PATTERNS.items():
        chapter = ROOT / "patterns" / pattern / "README.md"
        if not chapter.exists():
            errors.append(f"missing chapter: {chapter.relative_to(ROOT)}")
            continue
        text = chapter.read_text(encoding="utf-8")
        if state == "seed":
            for heading in REQUIRED_SEED_HEADINGS:
                if heading not in text:
                    errors.append(f"{chapter.relative_to(ROOT)} missing heading {heading!r}")
        elif "scaffold only" not in text.lower():
            errors.append(f"{chapter.relative_to(ROOT)} must explicitly remain scaffold only")


def validate_problem_catalog(errors: list[str]) -> int:
    path = ROOT / "curriculum" / "problems.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"cannot parse curriculum/problems.json: {error}")
        return 0

    problems = data.get("problems")
    if not isinstance(problems, list):
        errors.append("curriculum/problems.json: problems must be a list")
        return 0

    if not 30 <= len(problems) <= 50:
        errors.append(f"v0.1 problem pool should contain 30-50 entries, found {len(problems)}")

    keys: set[str] = set()
    counts: Counter[str] = Counter()
    required = {
        "key",
        "platform",
        "id",
        "title",
        "url",
        "pattern",
        "level",
        "abstract",
        "selection_question",
    }

    for index, problem in enumerate(problems):
        label = f"problem[{index}]"
        if not isinstance(problem, dict):
            errors.append(f"{label} must be an object")
            continue

        missing = required - problem.keys()
        if missing:
            errors.append(f"{label} missing keys: {sorted(missing)}")
            continue

        key = problem["key"]
        if key in keys:
            errors.append(f"duplicate problem key: {key}")
        keys.add(key)

        pattern = problem["pattern"]
        if pattern not in PATTERNS:
            errors.append(f"{key}: unknown pattern {pattern}")
        counts[pattern] += 1

        if problem["level"] not in ALLOWED_LEVELS:
            errors.append(f"{key}: invalid level {problem['level']}")

        platform = problem["platform"]
        expected_host = EXPECTED_HOSTS.get(platform)
        actual_host = urlparse(problem["url"]).netloc
        if expected_host is None:
            errors.append(f"{key}: unsupported platform {platform}")
        elif actual_host != expected_host:
            errors.append(f"{key}: URL host {actual_host} does not match {expected_host}")

        if len(problem["abstract"]) > 240:
            errors.append(f"{key}: abstract is too long; keep it original and compact")

    for pattern in PATTERNS:
        if counts[pattern] < 5:
            errors.append(
                f"{pattern}: expected at least 5 curated problems, found {counts[pattern]}"
            )

    return len(problems)


def validate_json_files(errors: list[str]) -> None:
    for relative in ["progress/schema.json", "curriculum/problems.json"]:
        path = ROOT / relative
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"{relative}: invalid JSON: {error}")


def validate_revisit_csv(errors: list[str]) -> None:
    path = ROOT / "progress" / "revisits.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
    expected = ["problem_key", "first_solved_on", "due_on", "stage", "status"]
    if header != expected:
        errors.append(f"progress/revisits.csv header must be {expected}, found {header}")


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
    validate_chapters(errors)
    problem_count = validate_problem_catalog(errors)
    validate_json_files(errors)
    validate_revisit_csv(errors)
    validate_local_markdown_links(errors)

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Repository validation passed: "
        f"{len(PATTERNS)} pattern chapters, {problem_count} curated problems, local links OK."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
