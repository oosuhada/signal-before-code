# Wrong Turn — BFS on an arbitrary weighted graph

## Tempting idea

“Shortest path” sounds like BFS because BFS is the first shortest-path algorithm many people learn.

## Why it looks reasonable

BFS does finalize nodes in increasing distance **when every edge contributes the same cost**. The
mistake is remembering the result while forgetting the equal-cost assumption that proves it.

## Smallest counterexample

```text
A --10--> B
A --1--> C --1--> B
```

## Step-by-step failure

BFS sees `B` one edge away and `C` one edge away. If it treats edge count as cost, it accepts the
direct route `A→B` although its weight is 10. The two-edge route through `C` costs only 2.

## Correct signal

The question is not “shortest?” but “what makes path cost increase?” Equal edge costs permit BFS
layers; arbitrary nonnegative weights require a cost-ordered frontier.

## Better candidates

Dijkstra for nonnegative weights; 0-1 BFS when weights are exactly 0/1; other methods when negative
weights invalidate Dijkstra's finalization proof.

## General lesson

Always attach an algorithm to the assumption that makes its invariant true.
