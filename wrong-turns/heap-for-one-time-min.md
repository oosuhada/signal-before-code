# Wrong Turn — Heap for a one-time minimum

## Tempting idea
The problem says “minimum,” and heaps are the minimum data structure.

## Why it looks reasonable
`heappop` exposes the minimum cleanly, so the API appears to match the noun in the requirement.

## Smallest counterexample
Find the minimum of `[7, 2, 9, 1]` exactly once.

## Step-by-step failure
Building a heap spends `O(N)` construction plus extra representation machinery. A scan keeps one
running best value and touches each item once with `O(1)` auxiliary state.

## Correct signal
Ask whether minimum selection repeats under updates, not whether the word “minimum” appears.

## Better candidates
Linear scan for one min/max; sort if full ordering is required; heap for repeated online extrema.

## General lesson
Choose a data structure for the operation sequence, not the operation name.
