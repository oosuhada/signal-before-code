# Wrong Turn: Sliding Window with Negative Values

## Temptation

For “shortest subarray with sum at least K,” expand right until the sum is big enough, then shrink
left while it stays big enough.

## The missing assumption

That logic assumes moving right cannot decrease the sum and moving left cannot increase it. Negative
values break both directions.

```text
[2, -5, 10], K = 7
```

The window sum does not change monotonically with its boundaries.

## Repair

Re-express the condition using prefix sums; for some variants, a monotonic deque over prefix sums is
the correct advanced pattern.
