# Visual Trace — Heap

A heap maintains just enough order for the current extremum.

```text
push 7 → [7]
push 2 → [2, 7]
push 9 → [2, 7, 9]
push 1 → root becomes 1 after local repair

pop → guaranteed minimum leaves
repair → new root is the next minimum
```

Invariant: `heap[0]` is the smallest retained item. The rest of the array is **not globally sorted**.
That weaker guarantee is exactly why repeated push/pop can be cheaper than sorting after every
update.

```bash
python3 scripts/trace.py heap --step
python3 scripts/trace.py --wrong stale-heap-entry
```
