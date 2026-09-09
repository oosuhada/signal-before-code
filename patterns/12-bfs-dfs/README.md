# 12 — BFS / DFS

## 1. What problem shape does this solve?

BFS and DFS traverse reachable graph state. BFS is special when equal-cost steps make distance
layers meaningful; DFS is natural for deep exploration, recursive structure, components, and many
cycle/backtracking-style tasks.

## 2. Signals to notice

```text
reachable / connected component
unweighted shortest path / minimum moves
explore grid/network
deep recursive structure / cycle reasoning
```

## 3. Naive idea

Follow arbitrary neighbors without a visited structure, or use DFS for every shortest-path question.

## 4. Why the naive idea breaks

Without visited state, cycles repeat forever. DFS can find a path but does not certify the fewest
equal-cost edges because it explores depth before competing paths at the same distance.

## 5. Core intuition

Traversal order determines what first discovery means:

- BFS queue: all distance `d` states leave the frontier before distance `d+1`.
- DFS stack/recursion: pursue one branch until it cannot continue, then backtrack.

## 6. Invariant

BFS: when a node is first enqueued in an unweighted graph, its recorded distance is minimum. Mark it
visited at enqueue time so it enters the queue once.

DFS: every visited node has an active/completed relationship consistent with the chosen cycle or
reachability logic.

## 7. Step-by-step walkthrough

```text
S → A → C
 \→ B → D
```

BFS frontier:

```text
distance 0: S
distance 1: A, B
distance 2: C, D
```

That layering is why first discovery certifies minimum hop count.

## 8. Implementation

```python
from collections import deque


def bfs_distance(graph: dict[int, list[int]], start: int) -> dict[int, int]:
    distance = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph.get(node, []):
            if nxt in distance:
                continue
            distance[nxt] = distance[node] + 1
            queue.append(nxt)
    return distance
```

## 9. Complexity

With adjacency lists, each vertex is discovered once and each edge is inspected a bounded number of
times: `O(V + E)` time and `O(V)` visited/frontier space. DFS recursion additionally uses up to
`O(V)` stack depth in a chain.

## 10. Common mistakes

- marking BFS visited on dequeue instead of enqueue;
- using BFS for arbitrary weighted shortest paths;
- forgetting bounds/visited checks in grid traversal;
- recursive DFS exceeding Python recursion depth;
- assuming traversal reaches disconnected components from one start node.

## 11. When NOT to use it

- Non-negative weighted shortest path → Dijkstra.
- Dependency order → topological sort adds indegree/order invariant.
- Repeated dynamic connectivity → Union-Find may avoid retraversal.

## 12. Neighboring patterns

- **BFS vs DFS:** layer order vs depth order.
- **BFS vs Dijkstra:** equal step cost vs weighted accumulated cost.
- **DFS vs backtracking:** graph traversal vs decision-tree choose/undo.

## 13. Mutation ladder

```text
unweighted shortest path      → BFS
weights 0 or 1                → 0-1 BFS candidate
non-negative arbitrary weight → Dijkstra
negative edge                 → Dijkstra guarantee disappears
need dependency order         → topological sort
```

## Visual Trace / Try Predicting

Compare the FIFO frontier in [`../../visuals/bfs.md`](../../visuals/bfs.md) with the LIFO branch state
in [`../../visuals/dfs.md`](../../visuals/dfs.md). Both can be stepped interactively.

## 14. Practice ladder

- **Understand:** flood fill, connected components.
- **Recognize:** minimum grid moves, island counting.
- **Apply:** multi-source BFS, cycle/color variants.
- **Mixed:** classify weight semantics before choosing BFS.

See [`../../comparisons/bfs-vs-dfs.md`](../../comparisons/bfs-vs-dfs.md) and
[`../../comparisons/bfs-vs-dijkstra.md`](../../comparisons/bfs-vs-dijkstra.md).
