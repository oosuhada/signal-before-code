# 06 — Heap / Priority Queue

**v0.1 state: scaffold only. Do not treat this chapter as learned or complete.**

No generated heap tutorial lives here yet. There is already better evidence elsewhere for how a heap
works internally.

## Learning question to earn the chapter

When does a problem ask for the **current min/max repeatedly while the candidate set changes**?

The future study session should start from competing approaches:

```text
scan every time
sort once
keep a sorted structure
heap / priority queue
```

and justify the trade-off from update/query frequency.

## Existing evidence bridge

[`beneath-the-stack/include/bts/min_heap.hpp`](https://github.com/oosuhada/beneath-the-stack/blob/main/include/bts/min_heap.hpp)
contains a from-scratch binary min-heap, and
[`labs/heap_scheduler/main.cpp`](https://github.com/oosuhada/beneath-the-stack/blob/main/labs/heap_scheduler/main.cpp)
compares heap selection with repeated linear minimum.

Equally important,
[`elevator-queue-lab/app/dispatch.py`](https://github.com/oosuhada/elevator-queue-lab/blob/main/app/dispatch.py)
evaluates only six state-dependent elevator candidates and intentionally does **not** force a heap.
That is a strong seed for the eventual `When NOT to use it` section.

Practice candidates are in [`../../curriculum/problems.json`](../../curriculum/problems.json).
