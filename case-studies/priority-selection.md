# Case Study — Priority Selection: Heap vs Scan

## Textbook question

Do we repeatedly need the current minimum/maximum from a changing candidate set?

That signal makes a heap a **candidate**, not an automatic answer.

## Verified artifacts

- `beneath-the-stack/include/bts/min_heap.hpp` — remote-main blob
  `fcb674c76c2a1de42374a46094bf474dc9dd436d`.
- `elevator-queue-lab/app/dispatch.py` — remote-main blob
  `e7404f94dac5a8bba78819f85adedfc6356aa3cd`.

The first implements heap mechanics directly. The second computes state-dependent scores for six
elevators and selects the minimum eligible evaluation with a direct `min(...)` scan.

## Why the choices differ

```text
large candidate set
+ many repeated min extractions
+ priorities remain meaningful between operations
→ heap may preserve useful ordering work

six candidate cars
+ score depends on changing live state
+ every decision already recomputes candidate scores
→ scanning the six current scores is direct and easy to audit
```

## Why not sort every time?

Sorting establishes far more order than “which candidate is smallest?” requires. For repeated
extremum selection over many items, `O(n log n)` re-sorts can be unnecessary work.

## Why not force a heap into the elevator dispatcher?

A heap only pays off if maintained priorities remain useful. If every dispatch event rescored every
car from changing position, direction, capacity, and queue state, rebuilding/repairing a heap over
six elements adds state-management complexity with little selection benefit.

## Interview defense

Say: “Repeated minimum makes me consider a heap. Before choosing it, I also ask how many candidates
exist and whether priorities persist between decisions.”
