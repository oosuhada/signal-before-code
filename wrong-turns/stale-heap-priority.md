# Wrong Turn — trusting every heap entry as current

## Tempting idea

Once `(priority, item)` is in a priority queue, assume the pair remains authoritative until popped.

## Why it looks reasonable

Python's `heapq` has no decrease-key operation, so Dijkstra-style code often pushes a new better
entry rather than modifying the old one. The old tuple still looks structurally valid.

## Smallest counterexample

```text
push (10, X)
later discover X at 4
push (4, X)
```

## Step-by-step failure

`(4, X)` pops and becomes the current/final value. `(10, X)` remains in the heap. If later code
treats it as fresh, it can repeat work or apply stale state.

## Correct signal

The heap is an ordering container, not the source of truth for mutable best-known priority. Compare
the popped value with the authoritative distance/version before processing.

## Better candidates

Lazy stale-entry skipping, an indexed/decrease-key heap where available, or a different maintained
structure when update semantics demand it.

## General lesson

Separate **queue history** from **current state** whenever priorities can improve after insertion.
