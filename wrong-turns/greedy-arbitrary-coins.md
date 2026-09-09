# Wrong Turn — Largest coin first for arbitrary denominations

## Tempting idea
Use the largest coin as much as possible to reduce the remaining amount fastest.

## Why it looks reasonable
Many real currency systems happen to make this greedy rule work on common amounts.

## Smallest counterexample
Coins `{1,3,4}`, target `6`.

## Step-by-step failure
Greedy: `4+1+1` uses three coins. Alternative: `3+3` uses two. The local largest choice blocks the
global optimum.

## Correct signal
Require a proof that the greedy choice can belong to some optimal solution for the given system.

## Better candidates
DP over amounts for arbitrary denominations; BFS over amount states in some formulations.

## General lesson
Examples from one denomination system do not prove a greedy rule for all systems.
