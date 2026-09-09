# signal-before-code

**A repository for training algorithm selection, not memorizing algorithm solutions.**

I already spend most of my engineering time building web/AI products and, separately, going below
the abstractions I use through systems programming. I use queues, caches, graphs, schedulers,
indexes, retries, and state machines in real products, and I have implemented several of them from
scratch in [`beneath-the-stack`](https://github.com/oosuhada/beneath-the-stack).

But knowing how a heap works is not the same skill as reading an unfamiliar interview problem and
realizing, under time pressure, **why a heap should be one of the candidates**.

That second skill is what this repository trains.

```text
Problem
  ↓
Constraint / clue
  ↓
Candidate approaches
  ↓
Trade-off
  ↓
Pattern recognition
  ↓
Implementation
  ↓
Defense: why this choice, and when does it stop being valid?
```

The code is deliberately late in the process. The useful artifact is the reasoning that came first:
the naive idea, the clue hidden in the input or constraints, the alternatives considered, the wrong
turn, and the reason one approach wins.

> **Do not memorize the solution. Recognize the signal. Compare the options. Choose the tool.
> Defend the choice.**

## Why this is a separate repository

My existing learning repositories already preserve other parts of the story:

| Repository | What it is for | What this repository does instead |
| --- | --- | --- |
| [`codetest-study`](https://github.com/oosuhada/codetest-study) | Append-only coding-test attempts, failed submissions, notes, and Python practice history | Trains the reasoning that should happen **before** another solution is added to the history |
| [`Beakjoon-hub-test`](https://github.com/oosuhada/Beakjoon-hub-test) | Judge-synchronized submission archive | Links to selected practice without becoming another submission mirror |
| [`codetestlog-extension`](https://github.com/oosuhada/codetestlog-extension) | Captures the full submission workflow automatically | Adds structured reflection fields for pattern recognition, not another ingestion layer |
| [`Lingo`](https://github.com/oosuhada/Lingo), [`pylingo`](https://github.com/oosuhada/pylingo), [`javalingo`](https://github.com/oosuhada/javalingo) | Short syntax and programming-fundamental drills | Assumes syntax is secondary and focuses on algorithm choice |
| [`beneath-the-stack`](https://github.com/oosuhada/beneath-the-stack) | Implements and measures abstractions below the stack | Asks when an unfamiliar problem should make me reach for those abstractions |

The intended bridge is:

```text
algorithm intuition
        ↕
existing solution history
        ↕
beneath-the-stack implementation / benchmark
        ↕
real product usage
```

No solved-problem history is copied here just to make this repository look larger.

## The learning contract

Every mature pattern chapter uses the same sequence:

```text
Problem
↓
First naive idea
↓
Why it fails / becomes slow
↓
Hidden clue
↓
Candidate approaches
↓
Chosen pattern
↓
Walkthrough
↓
Implementation
↓
Complexity
↓
Mutation
↓
When NOT to use it
↓
Practice: Understand → Recognize → Apply
```

The chapter is not successful if it merely says “use BFS” or “use a hash map.” It must explain what
fact about the problem made that choice defensible.

Read [`docs/methodology.md`](docs/methodology.md) for the full workflow.

## v0.1 curriculum

Only three chapters are intentionally seeded with full reasoning content in v0.1. The other four
exist as **scaffolds**, not as AI-generated lessons pretending I have already learned them.

| # | Pattern | v0.1 state | Focus |
| --- | --- | --- | --- |
| 01 | [Array & Hash](patterns/01-array-hash/README.md) | Seed chapter | Repeated membership, counting, key → value lookup |
| 02 | [Two Pointers](patterns/02-two-pointers/README.md) | Seed chapter | Monotonic movement over ordered structure |
| 03 | [Sliding Window](patterns/03-sliding-window/README.md) | Scaffold only | Reusable interval state |
| 04 | [Stack & Queue](patterns/04-stack-queue/README.md) | Scaffold only | Order of removal, nested state, frontiers |
| 05 | [Binary Search](patterns/05-binary-search/README.md) | Scaffold only | Sorted data and monotonic answer spaces |
| 06 | [Heap / Priority Queue](patterns/06-heap-priority-queue/README.md) | Scaffold only | Repeated min/max and dynamic priority |
| 07 | [BFS / DFS](patterns/07-bfs-dfs/README.md) | Seed chapter | Frontier order, reachability, unweighted distance |

“Seed chapter” means **ready for a learning session**, not mastered. Mastery is earned by solving and
revisiting problems without hints; it is never inferred from generated documentation.

## Practice is only three levels

- **Understand** — the pattern is almost visible; practice the invariant and mechanics.
- **Recognize** — the algorithm name is hidden; identify it from constraints and problem language.
- **Apply** — combine the pattern with another idea, or distinguish it from a tempting alternative.

The curated v0.1 pool lives in [`curriculum/problems.json`](curriculum/problems.json). It keeps only
problem identifiers, links, short original abstracts, and the learning question. Copyrighted problem
statements are not mirrored.

## How to solve a problem here

1. Pick one problem from a chapter or an unlabeled [`mixed/`](mixed/README.md) set.
2. Do a **no-AI first attempt**. Write constraints, first impression, candidate approaches, and the
   pattern guess before writing solution code.
3. Record the attempt using [`attempts/TEMPLATE.md`](attempts/TEMPLATE.md).
4. Submit through the normal judge workflow. The actual submission history can continue living in
   the existing coding-test repositories.
5. After the first attempt, use AI only as an interviewer/reviewer: challenge assumptions, ask for a
   counterexample, or request a mutation. See [`docs/ai-usage.md`](docs/ai-usage.md).
6. Add one mutation that changes the applicability boundary.
7. Schedule a revisit instead of treating one AC as mastery.

```text
Day 0   first solve
Day 3   reconstruct without previous code
Day 14  solve inside a mixed set
Day 30+ explain the selection from scratch, then implement
```

## What progress means here

The important metrics are not a giant solved count. They are signals about selection quality:

```text
Attempted
Solved without hint
Correct pattern identified
Implementation failure
Pattern recognition failure

pattern recognition rate
hint-free solve rate
revisit success rate
```

[`progress/schema.json`](progress/schema.json) defines the compact machine-readable record, while the
Markdown attempt template keeps the richer reasoning. `python scripts/progress.py` summarizes real
records once they exist. v0.1 ships with **no fake attempts**.

## Mixed mode and timed mocks

Pattern folders are training wheels. Real interviews do not label a question “heap” before I see it.

[`mixed/`](mixed/README.md) therefore hides categories until review. [`mocks/`](mocks/README.md)
contains only lightweight infrastructure for later `90 minutes / 3 problems / no AI / no category`
sessions. No dashboard or database is required.

## Connections to real systems

These links are evidence bridges, not claims that interview algorithms and production systems are
identical:

- **Hash / cache lookup:** [`AskOosu`](https://github.com/oosuhada/AskOosu) has a query-hash keyed RAG
  search cache. That is a real key-based lookup use case, though PostgreSQL owns the actual index
  implementation.
- **Heap selection:** [`beneath-the-stack`](https://github.com/oosuhada/beneath-the-stack) measures a
  binary min-heap against repeated linear minimum selection. In contrast,
  [`elevator-queue-lab`](https://github.com/oosuhada/elevator-queue-lab) intentionally scores only six
  changing elevator candidates with a scan. That is a concrete reminder that “priority” does not
  automatically mean “heap.”
- **Queue / ownership:** [`browser-reliability-runtime`](https://github.com/oosuhada/browser-reliability-runtime)
  uses a bounded file-backed queue with explicit claim/ownership transitions.
- **Graph dependencies:** [`dev-flow-dashboard`](https://github.com/oosuhada/dev-flow-dashboard)
  builds PR dependency/downstream relationships and traverses them to rank bottlenecks. Future graph
  chapters can connect to that artifact without copying it here.
- **Graph internals:** `beneath-the-stack` already contains from-scratch BFS/DFS and graph traversal
  evidence. This repository focuses on recognizing when those traversals are the right choice.

The exact verified files and the non-claims around them are recorded in
[`docs/bridges.md`](docs/bridges.md).

## AI is not the solver

Before the first attempt, AI may clarify wording but must not reveal the pattern. After the first
attempt it may challenge the approach. After submission it may review complexity, generate
counterexamples, compare alternatives, and mutate the problem.

The ready-to-use interviewer prompt is in [`prompts/interviewer.md`](prompts/interviewer.md).

## Quality without infrastructure theater

Python is the primary language for the first ~100 problems so syntax does not dominate the learning
loop. Representative problems can later be reimplemented in Java to practice stricter
implementation constraints.

The small CI surface checks only what supports the repository's purpose:

```bash
python -m unittest discover -s tests -v
python -m compileall -q signal_before_code scripts tests
python scripts/validate_repo.py
ruff format --check .
ruff check .
```

The reusable Python implementations exist to validate the three seed chapters. The repository is not
trying to become another all-algorithms catalog.

## References and attribution

The learning design was informed by VisuAlgo, NeetCode, Coding Interview University,
`javascript-algorithms`, The Algorithms — Python, USACO Guide, and several classmates' public
practice repositories. What was useful, license status where relevant, and what was deliberately not
copied are recorded in [`docs/references.md`](docs/references.md).

The naming review is in [`docs/naming.md`](docs/naming.md), and the deliberately incomplete roadmap is
in [`docs/roadmap.md`](docs/roadmap.md).
