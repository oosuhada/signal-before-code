# Wrong Turn — Full Backtracking after N outgrows the tree

## Tempting idea
The problem asks for a subset/arrangement, so enumerate every choice tree and check leaves.

## Why it looks reasonable
Backtracking is the most direct correctness baseline and works beautifully for small `N`.

## Smallest counterexample
Binary include/exclude choices at `N=50` imply about `2^50` leaves before pruning.

## Step-by-step failure
Even tiny per-node work cannot compensate for the exponential tree. The issue appears before Python
syntax or micro-optimization matters.

## Correct signal
Read `N` before committing to exhaustive branching; look for repeated state, separability, or strong
pruning structure.

## Better candidates
DP, meet-in-the-middle, greedy if provable, branch-and-bound with a meaningful bound, or reformulation.

## General lesson
Backtracking's correctness is cheap; its state-space size is the real algorithmic cost.
