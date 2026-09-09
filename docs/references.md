# References studied for v0.1

Research date: **2026-09-09**.

This file records what influenced the learning design and, equally importantly, what was **not**
copied. The repository does not import classmates' solution code or mirror copyrighted problem
statements.

## Existing personal learning assets

### `oosuhada/codetest-study`

- Source: https://github.com/oosuhada/codetest-study
- Useful: append-only `run / wrong / correct` history, Python notes, repeated attempts, and the idea
  that failed submissions are learning evidence rather than noise.
- Reused here: only the conceptual bridge to historical attempts.
- Not copied: existing solution files or cheat sheets.
- Why this repo is still needed: the history captures **what I tried**; `signal-before-code` captures
  **why I selected the approach before trying it**.

### `oosuhada/Beakjoon-hub-test`

- Source: https://github.com/oosuhada/Beakjoon-hub-test
- Useful: judge-synchronized practice archive with preserved problem metadata.
- Reused here: link target for future attempt history when relevant.
- Not copied: synchronized problem statements or solutions.

### `oosuhada/codetestlog-extension`

- Source: https://github.com/oosuhada/codetestlog-extension
- Useful: records every submission rather than only the final accepted answer; recognizes that
  iteration history matters.
- Reused here: failure classification complements the captured submission history.
- Not copied: extension code or judge adapters.

### `oosuhada/Lingo`, `javalingo`, `pylingo`

- Sources:
  - https://github.com/oosuhada/Lingo
  - https://github.com/oosuhada/javalingo
  - https://github.com/oosuhada/pylingo
- Useful: short progressive drills and lightweight progress loops work better for syntax repetition
  than passive reading.
- Reused here: the idea of repeated active practice.
- Not copied: frontend, gamification, or drill content. This repository intentionally stays
  Markdown/Python-first instead of becoming another learning application.

### `oosuhada/beneath-the-stack`

- Source: https://github.com/oosuhada/beneath-the-stack
- Useful: from-scratch hash/heap/graph structures, BFS/DFS, scheduler measurements, algorithm-defense
  notes, and an evidence contract that distinguishes explanation from implementation and application.
- Reused here: links to verified artifacts and the habit of defending failure boundaries.
- Not copied: C++ implementations, benchmark code, or measured results.
- Important distinction: `beneath-the-stack` asks **how the abstraction works underneath**;
  `signal-before-code` asks **what problem signal should make it a candidate**.

## Classmate / peer practice repositories

No peer repository below exposed a license during the v0.1 review. Their code is therefore treated as
read-only study evidence and is **not copied**.

### `woovii000/CodingTest`

- Source: https://github.com/woovii000/CodingTest
- Observed shape: auto-pushed Programmers history with many timestamped `run`, `wrong`, and
  `correct` attempts inside level/problem folders.
- Practice signal: repeated work on Level 2 problems such as rescue boats, target number, fatigue,
  and vowel dictionary shows consistency through multiple attempts rather than one final file.
- Useful here: keep attempt history visible and do not pretend AC count equals fluency.
- Limitation of archive form: timestamps show persistence, but do not consistently say which clue
  triggered the algorithm choice or which competing approach was rejected.

### `qqqkyj/algorithm-study`

- Source: https://github.com/qqqkyj/algorithm-study
- Observed shape: Java, BOJ course progression, explicit `2–4 problems/day`, a 200-problem goal,
  commit-after-solving rule, and README progress tracking.
- Progression: basic stack/queue/string/number topics → a substantial DP block → planned brute force,
  DFS/BFS, trees, graphs, greedy, divide-and-conquer, sorting, and binary search.
- Useful here: deliberate topic order and a sustainable daily practice contract.
- Limitation: a curriculum/solved table does not preserve the pre-solution classification decision.

### `Minji6/algolog`

- Source: https://github.com/Minji6/algolog
- Observed shape: Python study repo organized around *This Is Coding Test*, with concept notes,
  solutions, approach notes, troubleshooting, and participant folders.
- Useful here: explanation and troubleshooting belong beside practice rather than in a separate
  retrospective.
- Limitation: topic-guided study makes the pattern visible before the problem; mixed mode is still
  needed to practice classification.

### `Minji6/minji-algolog`

- Source: https://github.com/Minji6/minji-algolog
- Observed shape: personal BaekjoonHub/solution archive synchronized into the shared study repo with
  GitHub Actions.
- Useful here: personal history and group study can remain separate concerns.
- Limitation: automation moves artifacts efficiently but does not add selection reasoning by itself.

### `kennedy0919/baekjoon`

- Source: https://github.com/kennedy0919/baekjoon
- Observed shape: Baekjoon/Programmers solution directories with a deliberately minimal README.
- Useful here: practice repositories do not need infrastructure-heavy presentation.
- Limitation: the archive alone gives little evidence about candidate algorithms or missed clues.

### `josephuk77/Algorithm_Java`

- Source: https://github.com/josephuk77/Algorithm_Java
- Observed shape: Java solution collection spanning SWEA, Baekjoon, Programmers and automated
  LeetHub-style ingestion.
- Useful here: cross-platform repetition can broaden problem exposure.
- Limitation: ingesting more solved files still does not measure pattern-recognition quality.

### `kwongwangjae/java-codingtest`

- Source: https://github.com/kwongwangjae/java-codingtest
- Observed shape: Java practice across LeetCode plus Korean judges; problem folders often contain a
  solution, README and notes.
- Repeated coverage visible from the tree: sliding-window/hash (`Longest Substring`), two pointers
  (`3Sum`), stack (`Valid Parentheses`, `Daily Temperatures`), backtracking, trees, BFS/DFS
  (`Number of Islands`), dependency graphs (`Course Schedule`), heap/top-K, and weighted graph
  (`Network Delay Time`).
- Useful here: a relatively compact set can still cover many interview pattern families.
- Limitation: problem folders are useful after classification; they do not hide the family in a
  mixed interview-like session.

## External learning references

### VisuAlgo

- Source: https://visualgo.net/
- Useful: exposes data-structure state changes and algorithm execution step by step; graph modules
  make frontier/traversal behavior visible and support custom inputs.
- Adopted idea: show tiny state transitions before code with Markdown tables/ASCII/Mermaid.
- Not copied: client-side files, animations, screenshots, quiz system, or explanatory text. VisuAlgo
  explicitly asks others not to rehost/fork its client; this repository links to it instead.

### NeetCode Roadmap / practice lists

- Source: https://neetcode.io/roadmap
- Useful: interview-oriented progression and a compact core vocabulary including Arrays & Hashing,
  Two Pointers, Sliding Window, Stack, Binary Search, Heap / Priority Queue, Graphs, DP, and others.
- Adopted idea: use pattern-based progression before moving to mixed sets, and keep the first
  curriculum narrow.
- Not copied: problem statements, solutions, videos, hints, or proprietary site content.

### Coding Interview University

- Source: https://github.com/jwasham/coding-interview-university
- License observed: **CC BY-SA 4.0**.
- Useful: broad CS/interview study sequence from complexity and data structures through trees,
  sorting, graphs, review and interview practice.
- Adopted idea: fundamentals and interview practice should connect, but a repository can explicitly
  state what it is **not** trying to cover.
- Not copied: study-plan prose, resource lists, or code.

### JavaScript Algorithms

- Source: https://github.com/trekhleb/javascript-algorithms
- License observed: **MIT**.
- Useful: separate data-structure and algorithm organization, approachable explanations, and
  complexity/reference documentation around implementations.
- Adopted idea: explain before implementation and keep complexity beside the mechanism.
- Not copied: JavaScript implementations or README text.

### The Algorithms — Python

- Source: https://github.com/TheAlgorithms/Python
- License observed: **MIT**.
- Useful: broad Python reference catalog and strong emphasis on implementation coverage.
- Adopted idea: tested Python implementations are useful references after understanding.
- Deliberately not adopted: catalog scale. v0.1 should remain small enough that every completed
  chapter corresponds to real study.
- Not copied: implementation code.

### USACO Guide

- Source: https://usaco.guide/
- Useful: module structure that moves from lesson → implementation → practice problems, progression
  from Bronze through advanced topics, and difficulty understood relative to the current module.
- Adopted idea: explanation should lead into carefully selected practice rather than hundreds of
  undifferentiated links.
- Not copied: lesson text, editorials, implementations, problem statements, or site components. The
  guide's own usage notes restrict reproducing/redistributing site content without permission, so
  this repository only links and records the structural lesson.

## Design conclusion from the comparison

Existing solution archives are valuable evidence of consistency and implementation practice. Their
shared blind spot is that a final folder rarely answers:

```text
What did I notice first?
What candidate algorithms did I consider?
Why did I reject the obvious one?
Which assumption made the chosen pattern valid?
What mutation would make it invalid?
```

Those questions are the reason `signal-before-code` exists.
