# Wrong Turn: Trusting Stale Heap Entries

Python's `heapq` has no decrease-key operation. A common technique is to push a new `(priority,
item)` pair and leave the old one in the heap.

That works only if pop-time code checks whether the entry still matches the current best state.

```python
distance, node = heappop(heap)
if distance != dist[node]:
    continue
```

Without that stale-entry guard, Dijkstra or dynamic-priority code can process obsolete priorities
as if they were current truth.
