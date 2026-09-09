# Heap vs Sorting

## Same-looking problem

“Process items from smallest to largest” can be solved by sorting or by a min-heap.

## What changes?

Ask whether the candidate set changes while you process it.

- Static data, consume everything once → sorting is often simpler: `O(N log N)` once.
- Stream/dynamic insertions, repeatedly need the current minimum → heap supports push/pop in
  `O(log N)` without re-sorting the whole collection.
- Need only top K → a size-K heap can avoid storing/sorting every ordering relationship.

## Deciding signal

**Dynamic repeated selection** favors a heap. **Static total ordering** often favors sort.

Also notice tiny candidate sets: six elevators with state-dependent scores can be clearer as a small
scan than as a heap that becomes stale whenever scores change.
