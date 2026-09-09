# 15 — Shortest Path / Dijkstra

## 1. What problem shape does this solve?

Dijkstra solves single-source shortest paths when edge weights are **non-negative**. It generalizes
BFS's frontier idea from equal-cost layers to accumulated-cost priority.

## 2. Signals to notice

```text
minimum total cost / distance / time
weighted graph
non-negative edge costs
many possible routes
```

## 3. Naive idea

Use BFS because the question says “shortest,” or enumerate all paths.

## 4. Why the naive idea breaks

BFS minimizes edge count, not total weight. Enumerating paths is exponential because cycles and
branching produce many route combinations.

## 5. Core intuition

Always expand the unsettled node with the smallest known distance. With non-negative edges, any
alternative path reaching that node later cannot become cheaper by first taking an even more
expensive unsettled prefix.

## 6. Invariant

When a node is popped with distance equal to the current best `dist[node]`, that distance is final.
Relaxation maintains the best known upper bound for every discovered node.

## 7. Step-by-step walkthrough

```text
S --2--> A --2--> T
 \--7------------> T
```

Start `dist[S]=0`. Relax to `A=2`, `T=7`. Pop A next because 2 is smallest; relax T to 4. The heap
now contains a stale `(7,T)` entry, which must be ignored later.

## 8. Implementation

```python
from heapq import heappop, heappush


def dijkstra(graph: list[list[tuple[int, int]]], start: int) -> list[float]:
    dist = [float("inf")] * len(graph)
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        cost, node = heappop(heap)
        if cost != dist[node]:
            continue
        for nxt, weight in graph[node]:
            candidate = cost + weight
            if candidate < dist[nxt]:
                dist[nxt] = candidate
                heappush(heap, (candidate, nxt))
    return dist
```

## 9. Complexity

With an adjacency list and binary heap, each successful relaxation can push a heap entry, giving the
standard `O((V + E) log V)`-style bound (often written `O(E log V)` for connected sparse graphs).
Space is `O(V + E)` plus heap entries.

## 10. Common mistakes

- using Dijkstra with negative edges;
- forgetting the stale-entry check;
- reversing `(neighbor, weight)` tuple meaning;
- using BFS just because all weights are integers;
- overflowing fixed-width numeric types in other languages.

## 11. When NOT to use it

- Equal weights → BFS is simpler.
- 0/1 weights → 0-1 BFS may be simpler/faster.
- Negative edges → Dijkstra's settled-distance proof fails.

## 12. Neighboring patterns

- **Dijkstra vs BFS:** priority by cost vs FIFO by hop layer.
- **Dijkstra vs heap:** heap is only the frontier structure; relaxation gives algorithm meaning.
- **Dijkstra vs DP:** shortest path on a DAG can be solved in topological order without a heap.

## 13. Mutation ladder

```text
all weights 1              → BFS
weights 0/1                → 0-1 BFS
weights non-negative       → Dijkstra
negative edge              → choose another shortest-path method
DAG with weights           → topo order + relaxation candidate
```

## Visual Trace / Try Predicting

Separate tentative from finalized distance in [`../../visuals/dijkstra.md`](../../visuals/dijkstra.md),
then compare the negative-edge wrong-state trace.

## 14. Practice ladder

- **Understand:** network delay / weighted source distances.
- **Recognize:** cheapest route in weighted grids/networks.
- **Apply:** state-augmented Dijkstra, path reconstruction.
- **Mixed:** classify edge weight assumptions first.

See [`../../wrong-turns/bfs-on-weighted-graph.md`](../../wrong-turns/bfs-on-weighted-graph.md).
