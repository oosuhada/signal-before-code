# signal-before-code

**An intuition-first algorithm selection textbook + a separate personal practice system.**

I already build web, AI, backend, and systems software with queues, caches, graphs, schedulers,
indexes, retries, and state machines. What I want to train here is a different skill: reading an
unfamiliar problem and deciding **which algorithm deserves to be considered, why it fits, and where
its assumptions stop being valid**.

```text
Problem
  ↓
Constraints
  ↓
Signals
  ↓
Naive candidates
  ↓
Why they fail
  ↓
Candidate patterns
  ↓
Invariant / key insight
  ↓
Algorithm choice
  ↓
Implementation
  ↓
Complexity + boundaries
  ↓
Mutation
```

The repository has two deliberately different layers.

```text
TEXTBOOK LAYER                         PERSONAL LEARNING LAYER
AI-assisted + source-referenced        only actual attempts

patterns/                              attempts/
concepts/                              revisits/
comparisons/                           mixed/
wrong-turns/                           mocks/
practice-guides/                       progress/
mutations/
        ↓                                      ↓
learn signals and trade-offs            prove what I can do unaided
```

The textbook may be complete before I solve the problems. The personal layer may not claim
`solved`, `hint_free`, or `mastered` until a real learning session produces that evidence.

> **Textbook completion is not learner mastery.**

## How to use the book

1. Read [`concepts/reading-constraints.md`](concepts/reading-constraints.md) and
   [`concepts/complexity-intuition.md`](concepts/complexity-intuition.md).
2. Use [`docs/algorithm-selection-map.md`](docs/algorithm-selection-map.md) to generate candidates,
   not to jump directly to an answer.
3. Work through a pattern chapter. Every chapter starts with problem shape and signals before code.
4. Compare neighboring patterns in [`comparisons/`](comparisons/README.md).
5. Study failure cases in [`wrong-turns/`](wrong-turns/README.md).
6. Use [`practice-guides/recognition-quiz.md`](practice-guides/recognition-quiz.md) and
   [`practice-guides/flash-recognition.md`](practice-guides/flash-recognition.md) for fast recall.
7. Then solve problems without hints and record only real evidence in the personal layer.

## Curriculum

The progression intentionally moves from local sequence state, to search/order, to recursive and
graph state, then to optimization/state compression.

### Foundation

1. [Array & Hash](patterns/01-array-hash/README.md)
2. [Two Pointers](patterns/02-two-pointers/README.md)
3. [Sliding Window](patterns/03-sliding-window/README.md)
4. [Stack & Queue](patterns/04-stack-queue/README.md)
5. [Binary Search](patterns/05-binary-search/README.md)
6. [Heap / Priority Queue](patterns/06-heap-priority-queue/README.md)

### Recursive structures and graphs

7. [Linked List](patterns/07-linked-list/README.md)
8. [Tree / BST](patterns/08-tree-bst/README.md)
9. [Recursion](patterns/09-recursion/README.md)
10. [Backtracking](patterns/10-backtracking/README.md)
11. [Graph Fundamentals](patterns/11-graph-fundamentals/README.md)
12. [BFS / DFS](patterns/12-bfs-dfs/README.md)
13. [Union-Find](patterns/13-union-find/README.md)
14. [Topological Sort](patterns/14-topological-sort/README.md)
15. [Shortest Path / Dijkstra](patterns/15-shortest-path-dijkstra/README.md)

### Range, ordering, and optimization

16. [Greedy](patterns/16-greedy/README.md)
17. [Prefix Sum](patterns/17-prefix-sum/README.md)
18. [Interval Problems](patterns/18-interval-problems/README.md)
19. [DP Fundamentals](patterns/19-dp-fundamentals/README.md)
20. [1D DP](patterns/20-1d-dp/README.md)
21. [2D DP](patterns/21-2d-dp/README.md)
22. [Knapsack-style DP](patterns/22-knapsack-dp/README.md)
23. [LIS-style DP](patterns/23-lis-dp/README.md)

### Useful interview patterns

24. [Monotonic Stack](patterns/24-monotonic-stack/README.md)
25. [Monotonic Queue](patterns/25-monotonic-queue/README.md)
26. [Trie](patterns/26-trie/README.md)
27. [Bit Manipulation](patterns/27-bit-manipulation/README.md)
28. [Bitmask / Subset Enumeration](patterns/28-bitmask-subsets/README.md)

The canonical machine-readable chapter status is in
[`curriculum/chapters.json`](curriculum/chapters.json). All 28 chapters are textbook-complete; their
learner status starts at `not_started` until my own attempts say otherwise.

## What every chapter teaches

Each chapter follows the same reasoning contract:

```text
What problem shape does this solve?
Signals to notice
Naive idea
Why the naive idea breaks
Core intuition
Invariant
Step-by-step walkthrough
Implementation
Complexity
Common mistakes
When NOT to use it
Neighboring patterns
Mutation ladder
Practice ladder
```

The purpose is not to memorize those headings. Repetition makes the selection questions habitual:

- Which constraint actually matters?
- What work would the naive solution repeat?
- What property lets me eliminate candidates safely?
- Which invariant must remain true after every operation?
- Which small mutation would invalidate my chosen algorithm?

## Practice roadmap

[`curriculum/problems.json`](curriculum/problems.json) is the learner-facing catalog. It stores
platform, problem ID, title, URL, difficulty, a short original abstract, expected signal, and stage.
It does **not** expose the answer pattern as an `expected_pattern` field.

The separate [`curriculum/answer-key.json`](curriculum/answer-key.json) is review/reference metadata.
Mixed-mode material should present the learner-facing record first and reveal the answer key only
after a classification attempt.

Problem statements from Baekjoon, Programmers, and LeetCode are not copied into this repository.

## See the algorithm move

The visual layer turns the same reasoning into explicit state transitions without adding a frontend.
Start at [`visuals/README.md`](visuals/README.md) or run a trace directly:

```bash
python3 scripts/trace.py binary-search
python3 scripts/trace.py bfs --step
python3 scripts/trace.py dijkstra --predict
python3 scripts/trace.py dp-grid
```

`--predict` is the preferred mode after the first walkthrough. It shows current state + invariant,
hides the transition, and asks what should happen next before reveal. Machine-readable traces use
[`traces/schema.json`](traces/schema.json); wrong-state traces live in
[`traces/wrong-states.json`](traces/wrong-states.json).

The visualized set focuses on algorithms where state movement carries the proof: Two Pointers,
Sliding Window, Binary Search, Heap, BFS, DFS, Union-Find, Topological Sort, Dijkstra, DP,
Monotonic Stack, and Backtracking.

## Break the algorithm at its boundary

After seeing a correct trace, change one assumption. [`mutations/chains.json`](mutations/chains.json)
contains 20+ explicit transitions such as unweighted → 0/1 → nonnegative weighted → negative-edge
shortest path. [`docs/decision-boundaries.md`](docs/decision-boundaries.md) is the compact question
map; [`comparisons/online-vs-offline.md`](comparisons/online-vs-offline.md) and
[`comparisons/static-vs-dynamic.md`](comparisons/static-vs-dynamic.md) cover engineering-flavored
boundaries.

The [`wrong-turns/`](wrong-turns/README.md) library uses the smallest counterexample possible. Attack
the claims before reading the reveal:

```bash
python3 scripts/challenge.py sliding-window
python3 scripts/challenge.py --mode constraint --seed 3
python3 scripts/challenge.py --mode requirement
```

For rapid ambiguous classification, use the 56 synthetic prompts in
[`practice-guides/adversarial-recognition.json`](practice-guides/adversarial-recognition.json).

## Personal learning loop

The textbook is ready in advance. Evidence is earned later:

```text
textbook knowledge
  ↓
no-AI first attempt
  ↓
first impression + constraints + candidates
  ↓
implementation + judge result
  ↓
wrong-choice review
  ↓
Day 3 revisit
  ↓
Day 14 mixed recognition
  ↓
Day 30+ reconstruction / timed mock
```

Templates live in [`attempts/`](attempts/TEMPLATE.md), [`revisits/`](revisits/TEMPLATE.md),
[`mixed/`](mixed/README.md), and [`mocks/`](mocks/README.md). The learner ledger lives in
[`progress/learner-status.json`](progress/learner-status.json) and contains no fabricated wins.

## AI usage and transparency

The **textbook layer is AI-assisted educational content** informed by the references documented in
[`docs/references.md`](docs/references.md). Explanations, examples, diagrams, and Python code are
written for this repository rather than copied from those sources.

The **personal learning layer is different**: it is created only from actual problem-solving
sessions. Before a first attempt, AI may clarify wording but must not reveal the pattern. After an
attempt it may act as interviewer, reviewer, adversary, counterexample generator, or problem mutator.
See [`docs/ai-usage.md`](docs/ai-usage.md).

## Existing project bridges

This textbook connects abstract selection rules to verified source artifacts where the analogy is
real:

- hash/cache lookup → [`AskOosu`](https://github.com/oosuhada/AskOosu)
- queue ownership/backpressure →
  [`browser-reliability-runtime`](https://github.com/oosuhada/browser-reliability-runtime)
- graph dependencies → [`dev-flow-dashboard`](https://github.com/oosuhada/dev-flow-dashboard)
- heap internals and BFS/DFS → [`beneath-the-stack`](https://github.com/oosuhada/beneath-the-stack)
- small dynamically rescored candidate sets where a heap is *not* automatically best →
  [`elevator-queue-lab`](https://github.com/oosuhada/elevator-queue-lab)

Exact verified files and non-claims are recorded in [`docs/bridges.md`](docs/bridges.md).

## Why this is not another solution archive

My existing repositories already preserve judge submissions and repeated attempts. This repository
answers a different question: **what should I notice before I write the solution?**

```text
signal-before-code             → selection reasoning textbook + evidence system
codetest-study                 → long-running coding-test attempt history
Beakjoon-hub-test              → judge-synchronized solution archive
codetestlog-extension          → captures submission history
Lingo / pylingo / javalingo    → syntax and short drills
beneath-the-stack              → implement and measure abstractions internally
```

## Quality

The repository deliberately avoids frontend/dashboard infrastructure. CI validates the educational
contract and the small set of executable Python examples:

```bash
ruff format --check .
ruff check .
python -m compileall -q signal_before_code scripts tests
python -m unittest discover -s tests -v
python scripts/validate_repo.py
```

The validator checks chapter sections, internal Markdown links, curriculum metadata, duplicate
problem IDs, textbook/learner status separation, JSON schemas, and personal-learning templates.

Start with [`docs/algorithm-selection-map.md`](docs/algorithm-selection-map.md), then pick the first
chapter whose signals you cannot yet explain without looking.
