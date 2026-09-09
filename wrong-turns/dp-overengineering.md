# Wrong Turn — DP before a repeated state exists

## Tempting idea

Create `dp[i]` or `dp[i][j]` whenever a problem asks for a maximum/minimum.

## Why it looks reasonable

Optimization problems and DP often appear together, so adding a table feels sophisticated and safe.

## Smallest counterexample

Find the maximum element in `[3, 8, 2]`.

## Step-by-step failure

A table `dp[i] = max of prefix 0..i` works, but if only the final maximum is requested, every old
cell is dead state. One running variable preserves exactly the needed information.

## Correct signal

Before DP, identify repeated subproblems and define what one state means. Then ask whether multiple
states must remain available for future transitions.

## Better candidates

Linear scan for one aggregate; greedy or another direct invariant when no overlapping subproblem
structure exists.

## General lesson

DP is justified by reusable state dependencies, not by the presence of “best,” “count,” or “ways.”
