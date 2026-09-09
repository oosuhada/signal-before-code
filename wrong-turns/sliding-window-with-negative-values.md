# Wrong Turn — Sliding Window with negative values

## Tempting idea

For a contiguous sum condition, expand right and move left whenever the sum is too large.

## Why it looks reasonable

With nonnegative values, adding on the right cannot decrease the sum and removing on the left cannot
increase it. That directional behavior makes discarded starts safe.

## Smallest counterexample

```text
values = [2, -5, 10]
target >= 7
```

## Step-by-step failure

The sum can decrease when right expands (`2 → -3`) and increase when a negative left value is
removed. A local “too small/too large” condition no longer tells one boundary which way repairs it.

## Correct signal

Sliding window needs a boundary movement whose effect on validity is predictable. Contiguity alone is
not enough.

## Better candidates

Prefix Sum + Hash for exact-sum style variants; Monotonic Queue over prefix sums for some shortest
threshold variants; problem-specific DP/search elsewhere.

## General lesson

Name the monotonic boundary effect before writing a sliding-window loop.
