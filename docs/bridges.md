# Pattern → existing artifact bridges

These links were checked against the repositories' remote default branches on 2026-09-09. A bridge
means “this real artifact raises the same decision question,” not “the production system literally
uses the interview implementation.”

## Array & Hash → AskOosu cache keys

- Artifact: [`AskOosu/src/lib/rag/search-cache.ts`](https://github.com/oosuhada/AskOosu/blob/main/src/lib/rag/search-cache.ts)
- Verified behavior: retrieval parameters are serialized into a stable hash-derived `cache_key`, and
  PostgreSQL queries/upserts cached payloads by that key.
- Selection lesson: repeated exact lookup benefits from preserving a key → result relationship.
- Boundary: PostgreSQL owns the index/storage behavior; this is **not** evidence that an in-process
  Python hash map is the correct production replacement.

## Two Pointers → no forced product bridge yet

No current portfolio artifact was verified as a meaningful two-pointer algorithm use case during the
v0.1 audit.

That absence is intentional evidence too: do not keyword-search a codebase for two indexes and call
it an algorithm application. Add a bridge later only when the same monotonic boundary-elimination
reasoning actually appears.

## Stack & Queue → browser reliability queue ownership

- Artifact: [`browser-reliability-runtime/src/local-llm/queue.ts`](https://github.com/oosuhada/browser-reliability-runtime/blob/main/src/local-llm/queue.ts)
- Backpressure decision: [`docs/ADR-queue-backpressure.md`](https://github.com/oosuhada/browser-reliability-runtime/blob/main/docs/ADR-queue-backpressure.md)
- Verified behavior: file-backed job states, a configurable pending bound, sorted pending filenames,
  atomic state publication, and `rename`-based claim ownership.
- Selection lesson: “queue” in production includes ordering, capacity, ownership, durability, and
  recovery constraints beyond choosing `deque`.
- Boundary: this is not a reason to copy the production queue into coding-test solutions.

## Binary Search → mechanism evidence, product bridge not claimed

`beneath-the-stack` already records binary-search selection reasoning in
[`docs/algorithm-defense.md`](https://github.com/oosuhada/beneath-the-stack/blob/main/docs/algorithm-defense.md).

No v0.1 product artifact is labeled “binary search application” merely because a framework or
database may perform one internally. A future bridge should point to an explicit product decision.

## Heap / Priority Queue → benchmark and counterexample

- Heap implementation: [`beneath-the-stack/include/bts/min_heap.hpp`](https://github.com/oosuhada/beneath-the-stack/blob/main/include/bts/min_heap.hpp)
- Repeated-min benchmark: [`beneath-the-stack/labs/heap_scheduler/main.cpp`](https://github.com/oosuhada/beneath-the-stack/blob/main/labs/heap_scheduler/main.cpp)
- Tiny dynamic candidate set: [`elevator-queue-lab/app/dispatch.py`](https://github.com/oosuhada/elevator-queue-lab/blob/main/app/dispatch.py)

The pair is more useful than either link alone:

```text
many repeated minimum selections
→ heap can preserve useful ordering work

six elevators, rescored from changing live state
→ scan is simple and the heap's maintenance may not buy anything
```

This is the repository's `When NOT to use it` philosophy in real code.

## BFS / DFS → graph internals and a real dependency traversal

- From-scratch graph implementation:
  [`beneath-the-stack/include/bts/graph.hpp`](https://github.com/oosuhada/beneath-the-stack/blob/main/include/bts/graph.hpp)
- Selection/failure reasoning:
  [`beneath-the-stack/docs/algorithm-defense.md`](https://github.com/oosuhada/beneath-the-stack/blob/main/docs/algorithm-defense.md)
- Real PR dependency model:
  [`dev-flow-dashboard/frontend/src/graphModel.ts`](https://github.com/oosuhada/dev-flow-dashboard/blob/main/frontend/src/graphModel.ts)

`dev-flow-dashboard` constructs dependency/downstream adjacency and traverses downstream PRs with a
queue plus a visited set. It is a real graph traversal use case.

Important non-claim: the current artifact is **not** a topological-sort implementation. It models PR
dependencies and downstream reachability; a future Topological Sort chapter may use the same product
domain as a motivating scenario only if ordering/cycle requirements are implemented and verified.

## Future storage bridge → B+ tree

`beneath-the-stack` already has a B+ tree and page/storage experiments, but B+ tree is outside the
v0.1 interview-pattern curriculum. Keep it as a future “internal mechanism ↔ selection” bridge rather
than expanding the current scope.
