# Sliding Window vs Prefix Sum

## Same-looking problem

Both are common when the statement says “subarray,” “substring,” or “range.”

## What changes?

Prefix sums answer an aggregate for a *given* static range quickly:

```text
sum(l..r) = prefix[r + 1] - prefix[l]
```

Sliding window searches among ranges by moving boundaries while maintaining validity.

## Deciding signal

- many range sum queries → prefix sum;
- longest/shortest contiguous range satisfying a monotonic condition → sliding window;
- arbitrary negative values can destroy “expand makes sum larger / shrink makes sum smaller,” so a
  sum-constrained sliding window may become invalid while prefix sums still work as range queries.

The difference is **querying a known range** versus **discovering the right range**.
