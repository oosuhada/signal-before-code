# 14 — Topological Sort

## 1. What problem shape does this solve?

Topological sort orders tasks in a **directed acyclic graph (DAG)** so every prerequisite appears
before what depends on it. It also detects when such an ordering is impossible because of a cycle.

## 2. Signals to notice

```text
prerequisite / dependency
must happen before
course schedule / build order
directed acyclic graph
return any valid ordering
```

## 3. Naive idea

Sort tasks by ID/name or repeatedly pick a task that “looks independent” without tracking incoming
dependencies.

## 4. Why the naive idea breaks

Ordinary sort knows nothing about edges. A valid ordering is constrained by graph relationships, and
a cycle can make every linear order invalid.

## 5. Core intuition

Kahn's algorithm repeatedly removes nodes whose prerequisites are already satisfied. Indegree is the
count of unresolved prerequisites.

## 6. Invariant

Every node in the queue has indegree zero **with respect to the remaining graph**. Removing such a
node cannot violate any prerequisite because nothing unresolved points into it.

## 7. Step-by-step walkthrough

Dependencies `A→C`, `B→C`, `C→D`:

```text
indegree: A=0 B=0 C=2 D=1
queue=[A,B]
remove A → C becomes 1
remove B → C becomes 0 → enqueue C
remove C → D becomes 0 → enqueue D
order: A,B,C,D
```

If processed count is less than node count, remaining nodes participate in a cycle.

## 8. Implementation

```python
from collections import deque


def topo_order(n: int, edges: list[tuple[int, int]]) -> list[int] | None:
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for before, after in edges:
        graph[before].append(after)
        indegree[after] += 1

    queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == n else None
```

## 9. Complexity

Building indegrees touches every edge once. Each node enters the queue once and each edge decrements
one indegree once, giving `O(V + E)` time and `O(V + E)` adjacency storage.

## 10. Common mistakes

- reversing prerequisite edge direction;
- forgetting isolated nodes with indegree zero;
- returning a partial order despite a cycle;
- decrementing indegree more than once per edge;
- assuming topological order is unique.

## 11. When NOT to use it

- Undirected graphs do not have prerequisite direction in this sense.
- Reachability alone does not require a topological order.
- Cyclic workflow constraints may need cycle reporting rather than pretending an order exists.

## 12. Neighboring patterns

- **Topological sort vs BFS:** Kahn uses a queue, but the invariant is indegree zero, not distance.
- **Topological sort vs DFS:** DFS postorder can also produce a topo order if cycles are handled.
- **Topological sort + DP:** DAG order often makes DP transitions safe in dependency order.

## 13. Mutation ladder

```text
directed prerequisites, DAG → topological sort
cycle introduced           → no valid order
need lexicographically min  → zero-indegree min-heap
need longest DAG path       → topo order + DP
undirected dependencies     → rethink model
```

## 14. Practice ladder

- **Understand:** course schedule feasibility/order.
- **Recognize:** build systems, alien ordering, dependency workflows.
- **Apply:** heap-based deterministic topo order, DAG DP.
- **Mixed:** separate generic graph traversal from dependency ordering.
