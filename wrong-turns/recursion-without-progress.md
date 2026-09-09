# Wrong Turn — Recursion without a shrinking state

## Tempting idea
Translate “solve the smaller version” into a recursive call without checking that it is actually
smaller.

## Why it looks reasonable
The function name and parameters may look recursive even when the state does not move toward a base.

## Smallest counterexample
`f(n)` calls `f(n)` again for every `n > 0`.

## Step-by-step failure
No measure decreases. The base case is unreachable, so call frames grow until recursion fails.

## Correct signal
Name a well-founded progress measure: smaller index, shorter remaining input, fewer choices, lower
tree depth to a leaf, etc.

## Better candidates
Correct the recursive transition or use an iterative loop with an explicit progress invariant.

## General lesson
Every recursive edge needs a proof that the state approaches termination.
