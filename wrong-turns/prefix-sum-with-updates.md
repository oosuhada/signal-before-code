# Wrong Turn — Static Prefix Sum with online updates

## Tempting idea
Prefix sums make range sums `O(1)`, so precompute once and answer forever.

## Why it looks reasonable
For immutable arrays the preprocessing is exactly right.

## Smallest counterexample
Values `[1,2,3]`; query sum `[0,2]`; update index 0 to 10; query `[0,2]` again.

## Step-by-step failure
The old prefix array still encodes the original `1`. Updating one base value invalidates every later
prefix entry unless they are recomputed.

## Correct signal
Ask whether updates occur between queries and whether preprocessing remains valid.

## Better candidates
Fenwick Tree or Segment Tree for common update/range-query mixes; recomputation only at tiny scale.

## General lesson
Preprocessing is useful only while its assumptions remain static.
