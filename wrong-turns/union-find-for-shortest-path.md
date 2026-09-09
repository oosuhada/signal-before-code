# Wrong Turn — Union-Find for shortest path

## Tempting idea
Union-Find answers whether two nodes are connected, so perhaps it can also help find how to travel.

## Why it looks reasonable
Both tasks use components and edges, and Union-Find compresses connectivity efficiently.

## Smallest counterexample
`A-B-C` and `A-D-C` are one component, but connectivity alone does not say which route is shorter.

## Step-by-step failure
After unions, `A`, `B`, `C`, `D` may share one root. Parent pointers describe a DSU forest chosen for
efficiency, not graph edges or path length. Route information has been discarded.

## Correct signal
Union-Find answers repeated **same component?** questions under merges; shortest path needs traversal
or distance state.

## Better candidates
BFS for unweighted shortest path; Dijkstra for nonnegative weighted shortest path.

## General lesson
A compressed summary cannot answer information it intentionally threw away.
