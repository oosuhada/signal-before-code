# Backtracking vs DP

## Same-looking problem

Both may start from a recursive decision tree.

## What changes?

Backtracking cares about constructing/enumerating valid choices and pruning invalid prefixes. DP
cares about repeated subproblems where only a compact state affects the future.

## Deciding signal

- Need all permutations/configurations or one valid construction → backtracking.
- Many recursion branches reach the same `(index, remaining, ...)` state and only the best/count is
  needed → memoization/DP can collapse repeated work.
- If the full path/history affects future legality, state compression may be difficult; backtracking
  can remain the honest model.

The bridge is often: write recursion first, observe repeated states, then decide whether memoization
changes exponential repeated work into a bounded state graph.
