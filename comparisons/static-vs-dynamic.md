# Static vs Dynamic State

## Connectivity example

Static graph, one question:

```text
Are A and B connected?
→ BFS/DFS is direct and also gives traversal/path information.
```

Dynamic sequence:

```text
union(A,B)
connected(C,D)?
union(B,C)
connected(A,C)?
...
```

Repeated traversal would rediscover component membership. Union-Find instead maintains a compact
component representative across updates.

## Range-sum example

Static values + many queries → prefix sums are excellent. Add point updates between queries and old
prefix sums become stale; a Fenwick/segment-tree style maintained structure becomes a candidate.

## Decision signal

Ask whether preprocessing remains valid for the whole problem. If input state mutates, a static
precomputation may be the wrong abstraction even when each individual query looks identical.
