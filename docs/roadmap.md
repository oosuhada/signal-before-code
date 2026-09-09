# Roadmap

The roadmap is intentionally smaller than a complete algorithm catalog. A chapter advances because
real solving sessions create evidence, not because a generator can write plausible prose.

## v0.1 — selection scaffold

- repository concept and naming;
- learning methodology;
- AI interviewer/reviewer contract;
- progress and revisit schema;
- seven-pattern curriculum surface;
- full seed chapters for Array & Hash, Two Pointers, and BFS / DFS;
- curated 30–50 problem pool without copied statements;
- mixed-practice foundation;
- timed-mock template;
- small tested Python reference implementations for seed chapters;
- lightweight CI and repository validation.

## v0.2 candidates

Only promote these when actual study reaches them:

- Trees;
- Backtracking;
- Graph patterns beyond basic BFS / DFS;
- Union-Find;
- Topological Sort;
- Shortest Path;
- Greedy;
- Dynamic Programming.

Existing artifacts can provide bridges when relevant:

- `beneath-the-stack` already has union-find, heap, BFS/DFS, B+ tree, scheduler, and algorithm-defense
  evidence;
- `dev-flow-dashboard` contains a real PR dependency graph;
- `browser-reliability-runtime` contains queue ownership/backpressure behavior;
- `elevator-queue-lab` is useful both as a scheduling example and as evidence for when a heap is not
  automatically worthwhile.

Those artifacts should be linked, not recopied.

## Later: mixed and timed interview mode

After the first pattern set has real attempt history:

```text
90 minutes
3 problems
no AI
no pattern labels
explain before code
```

The first version needs only Markdown records. Build an app only if repeated use demonstrates a real
workflow problem that files and scripts cannot solve.

## Language progression

```text
first ~100 selected problems
→ Python for reasoning speed

representative solved problems
→ Java reimplementation for syntax/type discipline
```

Do not duplicate every solution in both languages by default.
