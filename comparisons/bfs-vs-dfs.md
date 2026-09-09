# BFS vs DFS

## Same-looking problem

“Starting from node A, explore a graph and find node B.” Both algorithms can reach B.

## What changes?

If the question becomes “find the path with the fewest **unweighted edges**,” traversal order now
matters. BFS explores distance layers; DFS commits deeply before exploring siblings.

```text
A
├─ B ─ D ─ E
└─ C ─ E

BFS: A → {B,C} → E     shortest edge count is certified at first discovery
DFS: A → B → D → E     valid path, not necessarily shortest
```

## Deciding signal

- shortest number of equal-cost steps → BFS;
- reachability/components → either;
- recursive structure, cycle detection, backtracking-like exploration → DFS often feels natural;
- very wide graph → DFS may use less frontier memory, though recursion depth can become its own risk.

The data structure—queue vs stack—is a consequence of the exploration order you need.
