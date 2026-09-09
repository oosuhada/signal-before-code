# Pattern → existing artifact bridges

These links were checked against the repositories' remote default branches on 2026-09-09. A bridge
means “this real artifact raises the same decision question,” not “the production system literally
uses the interview implementation.”

For the v0.6 interview-oriented case studies, including explicit “Why not another algorithm?”
defenses, see [`../case-studies/README.md`](../case-studies/README.md).

Verification snapshot (remote `main`, checked with authenticated `gh api`):

| Artifact | Blob SHA |
| --- | --- |
| `beneath-the-stack/include/bts/min_heap.hpp` | `fcb674c76c2a1de42374a46094bf474dc9dd436d` |
| `beneath-the-stack/include/bts/graph.hpp` | `f65aa3c4f0feea62c8ea56616635bdf08079c6a1` |
| `elevator-queue-lab/app/dispatch.py` | `e7404f94dac5a8bba78819f85adedfc6356aa3cd` |
| `dev-flow-dashboard/frontend/src/graphModel.ts` | `f44bf41727de15d8816b1df666b6a7c3118a7f37` |
| `browser-reliability-runtime/src/local-llm/queue.ts` | `4cabba6324b5c67d936a119d72e8958f782951d4` |
| `AskOosu/src/lib/rag/search-cache.ts` | `0f5f71059d6ab16f810d853551e5909eb77369fd` |
| `source-archive/search-worker.js` | `9a48df9dd43da65430a3c9657c0bdcc2a2343a7a` |

## Array & Hash → AskOosu cache keys

- Artifact: [`AskOosu/src/lib/rag/search-cache.ts`](https://github.com/oosuhada/AskOosu/blob/main/src/lib/rag/search-cache.ts)
- Verified behavior: retrieval parameters are serialized into a stable hash-derived `cache_key`, and
  PostgreSQL queries/upserts cached payloads by that key.
- Selection lesson: repeated exact lookup benefits from preserving a key → result relationship.
- Boundary: PostgreSQL owns the index/storage behavior; this is **not** evidence that an in-process
  Python hash map is the correct production replacement.

## Two Pointers → no forced product bridge yet

No current portfolio artifact was verified as a meaningful two-pointer algorithm use case during the
v0.2 audit.

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

No product artifact is labeled “binary search application” merely because a framework or
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

Important non-claim: the current artifact is **not** a topological-sort implementation. The textbook
Topological Sort chapter uses the same dependency domain as a conceptual bridge, but this file does
not claim the production project currently performs Kahn's algorithm.

## Topological Sort → PR dependency domain, not implementation claim

- Artifact: [`dev-flow-dashboard/frontend/src/graphModel.ts`](https://github.com/oosuhada/dev-flow-dashboard/blob/main/frontend/src/graphModel.ts)
- Verified behavior: builds directed dependency/downstream relationships and traverses downstream
  nodes.
- Selection lesson: dependency direction is real product state; if the product needed a valid merge
  sequence over a DAG, topological ordering would be the relevant algorithm family.
- Boundary: current source is traversal/ranking logic, **not** evidence that topo sort is deployed.

## Graph / queue state → browser reliability runtime

The file-backed queue in
[`browser-reliability-runtime/src/local-llm/queue.ts`](https://github.com/oosuhada/browser-reliability-runtime/blob/main/src/local-llm/queue.ts)
also demonstrates why algorithm names do not fully specify production semantics: queue order is only
one concern alongside bounded capacity, atomic ownership, durability, and recovery.

## Storage bridge → B+ tree remains outside interview curriculum

`beneath-the-stack` already has a B+ tree and page/storage experiments, but B+ tree is outside the
current 28-chapter interview-pattern curriculum. Keep it as an “internal mechanism ↔ selection”
bridge rather than expanding this textbook into a database-internals catalog.

## Ranked search → full sorting vs top-K mutation

- Artifact: [`source-archive/search-worker.js`](https://github.com/oosuhada/source-archive/blob/main/search-worker.js)
- Verified behavior: score each document, filter zero-score matches, then sort the complete match set
  by score and tie-break before returning all ranked IDs.
- Selection lesson: complete ranked output gives full sorting real value. If the requirement mutates
  to a tiny top-K over a much larger corpus, a bounded heap becomes a candidate instead.
- Boundary: an exact-key hash table does not replace relevance scoring; the query is ranking, not
  direct ID lookup.

## Agentic ontology dashboard → local-only topological-order observation

The local `agentic-ontology-dashboard` snapshot at commit
`35dc61aa625301cef1daa5b6cdb9b7783cc5927d` contains a Kahn-style `_topological_order` in
`api/ontology_dashboard/analysis_service.py`, including indegree accounting, a zero-indegree deque,
and cycle rejection.

This is deliberately **not** linked as a verified GitHub-main artifact: the local branch is heavily
diverged from `origin/main`, and the GitHub contents API currently reports that path absent from the
default branch. The observation is useful evidence from local source, not a remote-main claim.
