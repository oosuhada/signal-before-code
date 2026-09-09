# 13 — Union-Find

## 1. What problem shape does this solve?

Union-Find, or Disjoint Set Union (DSU), is built for repeated **merge components** and **ask whether
two items belong to the same component** operations.

## 2. Signals to notice

```text
connect / merge groups
same component?
edges added over time
cycle detection in undirected edges
Kruskal-style connectivity
```

## 3. Naive idea

After each new edge, run BFS/DFS from one endpoint to answer connectivity queries.

## 4. Why the naive idea breaks

Traversal repeatedly rediscovers component membership that changes only when components merge. With
many updates and queries, that repeated graph walk dominates the work.

## 5. Core intuition

Give every component a representative. `find(x)` follows parent links to that representative;
`union(a,b)` makes two representatives share one root. Path compression remembers what earlier
finds learned.

## 6. Invariant

Two nodes are connected exactly when `find(a) == find(b)`. Every parent chain must end at a root that
represents one disjoint component.

## 7. Step-by-step walkthrough

```text
start: {1} {2} {3} {4}
union(1,2) → {1,2} {3} {4}
union(3,4) → {1,2} {3,4}
union(2,3) → {1,2,3,4}
find(1) == find(4) → connected
```

The structure does not store the actual connecting path; only component identity.

## 8. Implementation

```python
class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True
```

## 9. Complexity

With path compression plus union by size/rank, a long sequence of operations costs almost constant
amortized time: `O(α(N))` per operation, where the inverse Ackermann function grows extraordinarily
slowly. Space is `O(N)`.

## 10. Common mistakes

- unioning raw nodes instead of roots;
- forgetting path compression or union by rank/size in large workloads;
- using DSU for directed reachability;
- expecting DSU to reconstruct a path;
- mishandling one-based versus zero-based node labels.

## 11. When NOT to use it

- Need shortest paths or actual routes → traversal/path algorithms.
- Directed connectivity/order → DSU usually does not model it.
- Edge deletions make ordinary DSU much harder; offline/dynamic-connectivity techniques may be needed.

## 12. Neighboring patterns

- **Union-Find vs DFS/BFS:** persistent component memory vs retraversal.
- **Union-Find vs topological sort:** undirected membership vs directed dependency order.
- **Union-Find + greedy:** Kruskal combines cheapest-edge ordering with DSU cycle checks.

## 13. Mutation ladder

```text
one connectivity query         → BFS/DFS may be simplest
many union + connected queries → DSU
need path itself               → graph traversal
directed edges                 → DSU no longer answers reachability
edge deletions                 → ordinary DSU boundary reached
```

## 14. Practice ladder

- **Understand:** basic set merge/connectivity.
- **Recognize:** redundant connection / undirected cycle.
- **Apply:** Kruskal support, account/group merging.
- **Mixed:** decide whether the query needs path information or only identity.

See [`../../comparisons/union-find-vs-dfs.md`](../../comparisons/union-find-vs-dfs.md).
