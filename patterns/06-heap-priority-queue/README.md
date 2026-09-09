# 06 — Heap / Priority Queue

## 1. What problem shape does this solve?

Heaps fit a changing set where you repeatedly need the current minimum/maximum, next deadline,
cheapest frontier item, or top-K boundary without maintaining a complete sorted order.

## 2. Signals to notice

```text
repeated smallest / largest
top K
priority / deadline / cheapest next
streaming candidates
merge K sorted sources
```

## 3. Naive idea

Scan every candidate to find the minimum each time, or re-sort after every insertion.

## 4. Why the naive idea breaks

Repeated linear minimum selection over `N` changing items can approach `O(N²)`; repeated full sorts
maintain far more ordering information than “what is best next?” requires.

## 5. Core intuition

A heap maintains **partial order**: the root is best, while the rest only satisfies parent/child heap
relationships. That is enough for fast best-item access without paying for total order.

## 6. Invariant

In a min-heap, every parent key is `<=` its children. After push/pop, local swaps restore this
property. The array is not globally sorted.

## 7. Step-by-step walkthrough

Insert priorities `5, 2, 7, 1`:

```text
[5]
[2,5]        2 bubbles above 5
[2,5,7]
[1,2,7,5]    1 bubbles toward root
pop → 1      remaining heap repairs root path
```

## 8. Implementation

```python
from heapq import heappop, heappush


def k_smallest(values: list[int], k: int) -> list[int]:
    heap: list[int] = []
    for value in values:
        heappush(heap, value)
    return [heappop(heap) for _ in range(min(k, len(heap)))]
```

Interview code often uses `heapq`; implementing the heap itself is a different learning objective.

## 9. Complexity

Heap push/pop touch only one root-to-leaf path, whose height is `O(log N)`. Peeking at the root is
`O(1)`. Building a heap with repeated pushes is `O(N log N)`; `heapify` can do it in `O(N)`.

## 10. Common mistakes

- assuming the entire heap array is sorted;
- forgetting Python `heapq` is a min-heap;
- popping from an empty heap;
- failing to discard stale entries when priorities are updated lazily;
- using a heap for one minimum query where `min()`/scan is simpler.

## 11. When NOT to use it

- Static data consumed completely in sorted order → sort once.
- One min/max → linear scan.
- Tiny, constantly rescored candidate sets may favor direct scan.

## 12. Neighboring patterns

- **Heap vs sort:** dynamic repeated selection vs static total ordering.
- **Heap vs queue:** priority order vs arrival order.
- **Heap vs Dijkstra:** heap is the frontier mechanism; Dijkstra adds shortest-path invariants.

## 13. Mutation ladder

```text
one minimum                 → scan
consume all sorted          → sort
dynamic insert + extract    → heap
top K from stream           → size-K heap
priority values mutate      → lazy entries + stale check / redesign
```

## 14. Practice ladder

- **Understand:** kth largest, last-stone style selection.
- **Recognize:** task scheduling, merge sorted sources.
- **Apply:** top-K frequency, Dijkstra frontier.
- **Mixed:** defend heap against sort or a tiny linear scan.

See [`../../comparisons/heap-vs-sort.md`](../../comparisons/heap-vs-sort.md) and the verified bridge in
[`../../docs/bridges.md`](../../docs/bridges.md).
