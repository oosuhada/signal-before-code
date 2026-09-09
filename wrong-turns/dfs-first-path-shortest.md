# Wrong Turn — Taking DFS's first path as shortest

## Tempting idea
DFS finds a route quickly; stop at the target and call that route shortest.

## Why it looks reasonable
The first target hit feels like progress, and DFS is a valid reachability algorithm.

## Smallest counterexample
`A→B→C→T` and `A→T`. If DFS explores `B` first, its first target route has three edges instead of one.

## Step-by-step failure
DFS orders work by branch depth, not hop count. A deeper branch can reach the target before an
unexplored shallow sibling.

## Correct signal
Unweighted shortest hops require frontier layers ordered by distance.

## Better candidates
BFS for minimum hops; DFS when reachability/component/path existence is sufficient.

## General lesson
Traversal order becomes a correctness property when “first found” is used as the answer.
