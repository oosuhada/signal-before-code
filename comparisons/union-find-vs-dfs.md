# Union-Find vs DFS/BFS

## Same-looking problem

“Are A and B connected?” can be answered by traversal or by a Disjoint Set Union structure.

## What changes?

- One/few queries on a static graph → BFS/DFS is straightforward and can also recover paths.
- Many edge additions plus repeated connectivity queries → Union-Find remembers components and
  avoids retraversing the graph every time.

## Deciding signal

Union-Find is excellent for **merge + connectivity**. It is not a general graph query engine: it does
not tell you the actual path, shortest distance, or directed reachability.
