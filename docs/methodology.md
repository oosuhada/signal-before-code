# Learning methodology

The repository optimizes for one question:

> Given a problem I have not seen before, can I identify and defend an appropriate algorithm before
> implementation begins?

That is a different skill from remembering code, recognizing a famous problem title, or knowing how
a data structure works internally.

## 1. Read for constraints before patterns

On the first pass, do not ask “which algorithm is this?” Ask what the problem permits and forbids.

Capture at least:

- input size and value range;
- whether the data is sorted, bounded, unique, weighted, mutable, or streaming;
- whether the result is one value, all values, an ordering, or a shortest/cheapest path;
- whether the same operation is repeated;
- whether order matters;
- time and memory limits when they are provided.

These facts are stronger evidence than keywords. “Shortest” alone does not imply BFS; equal edge
cost is what makes BFS layers correspond to path length.

## 2. Write the naive idea first

The naive approach is useful because it reveals what work is being repeated.

Examples:

```text
check every pair
→ repeated pair work
→ O(n²)

scan the entire list for the minimum every time
→ repeated selection work
→ O(n) per extraction

explore every path and remember the first path found
→ traversal order is not distance order
→ may be incorrect for shortest path
```

Do not skip this step just because a familiar pattern is obvious. The goal is to practice deriving
the better approach rather than naming it from memory.

## 3. Diagnose exactly how the naive idea breaks

Use one of these labels:

- **incorrect** — it can return a wrong result;
- **too slow** — operation count exceeds what the constraints can tolerate;
- **too much memory** — retained state grows beyond the useful bound;
- **works, but simpler exists** — the sophisticated structure has no payoff at this scale.

The fourth case matters. `elevator-queue-lab`, for example, scores only six changing elevator cars.
A heap would add maintenance complexity without creating a meaningful asymptotic advantage for that
tiny dynamic candidate set.

## 4. Identify the signal

A signal is a fact that eliminates or promotes candidates.

| Signal | Candidate it should make me consider | Why |
| --- | --- | --- |
| repeated membership / frequency lookup | set / hash map | store knowledge instead of rescanning |
| sorted data + pair relation moves monotonically | two pointers | one comparison can eliminate one boundary |
| reusable contiguous interval | sliding window | update state instead of rebuilding each interval |
| first-in-first-out distance layers | queue / BFS | frontier order matches hop distance |
| repeated current min/max | heap | maintain an extremum under updates |
| sorted data or monotonic predicate | binary search | discard half the search space |
| nested/undo structure | stack | most recent unresolved state is next |

This table is a starting vocabulary, not a lookup table that replaces reasoning.

## 5. Keep at least two candidates alive

For interview training, “I know the answer” is weaker than “I compared these options.”

Record:

```text
Candidate A
- correctness argument
- time
- memory
- implementation risk

Candidate B
- correctness argument
- time
- memory
- implementation risk
```

Then state why one wins for **this** input shape.

## 6. State the invariant before code

The chosen pattern should have one sentence that remains true while it runs.

Examples:

- Two pointers: every discarded boundary can no longer participate in a valid target pair.
- Sliding window: the window state summarizes exactly the current interval.
- BFS: when a node is first dequeued in an unweighted graph, no later undiscovered route can use
  fewer edges.
- Heap: the root represents the current extremum under the heap ordering invariant.

If the invariant cannot be stated, implementation is premature.

## 7. Walk a tiny input by hand

Use four to eight values, not a production-size example. Record state transitions explicitly.

```text
state before
→ decision
→ state after
→ fact that remains true
```

Visually exposing state changes is more useful here than building a frontend. Markdown tables,
ASCII diagrams, and Mermaid are enough for v0.1.

## 8. Implement only after the choice is defended

Python is primary because the training target is reasoning rather than syntax. The reusable example
implementations are intentionally small and tested. They are not a claim that every judge solution
should be copied from a template.

After an approach is understood, selected problems can be reimplemented in Java:

```text
Python
→ understand and defend the algorithm

Java
→ reproduce it under stricter syntax, types, and library choices
```

## 9. Explain complexity from the operations

Do not stop at a Big-O label.

Bad:

```text
O(n)
```

Better:

```text
Each pointer only moves inward and never moves back.
Across the entire run, left advances at most n times and right retreats at most n times.
Therefore the total pointer movement is linear: O(n).
```

For hash-based approaches, state when expected/amortized behavior depends on the implementation.

## 10. Mutation defines the applicability boundary

After solving, change one assumption and ask whether the chosen algorithm survives.

Shortest-path example:

```text
all edge weights = 1
→ BFS

weights are only 0 or 1
→ 0-1 BFS becomes a candidate

positive arbitrary weights
→ Dijkstra becomes a candidate

negative edge
→ Dijkstra's settled-distance assumption is no longer valid
```

The mutation is often more educational than another near-identical problem because it explains why
an algorithm stops applying.

## 11. Always write “When NOT to use it”

Patterns are not achievements to force into problems.

Examples:

- Heap: one minimum query over a static list usually needs only a scan.
- Binary search: arbitrary unordered membership search has no monotonic half to discard.
- BFS: arbitrary positive edge weights do not preserve hop-count distance.
- Hash map: sorted iteration or range queries may need a different structure.

## 12. Practice in three modes

### Understand

The structure is visible. The goal is to internalize the invariant.

### Recognize

The pattern label is hidden. The goal is to identify the signal before coding.

### Apply

The problem combines patterns or offers an attractive competing approach. The goal is to defend the
choice under ambiguity.

## 13. Move from labeled to mixed practice

Pattern folders help create a mental vocabulary, but they create a classification hint. Once a
chapter feels familiar, use `mixed/` where pattern labels are hidden until review.

For a mixed problem, the first written line should not be an algorithm name. It should be the facts
that drive the choice.

## 14. One AC is not mastery

Use the default revisit rhythm unless a problem needs a shorter interval:

| Stage | Goal |
| --- | --- |
| Day 0 | first defended solve |
| Day 3 | reconstruct without previous code |
| Day 14 | identify it inside a mixed set |
| Day 30+ | explain selection and implement from scratch |

Revisit success counts only when the previous solution is not opened first.

## 15. Record failure by layer

An incorrect submission is not one category.

Use the smallest accurate failure label:

- `pattern_recognition` — chose the wrong family of approach;
- `complexity` — correct idea but ignored the constraint scale;
- `implementation` — pattern was correct but code was wrong;
- `edge_case` — invariant was correct but a boundary condition was missed;
- `explanation` — solution worked but could not be defended clearly.

The point of metrics is to decide what to practice next, not to make a leaderboard.
