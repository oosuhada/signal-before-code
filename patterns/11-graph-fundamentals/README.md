# 11 — Graph Fundamentals

## 1. What problem shape does this solve?

A graph is the model when arbitrary entities are connected by relationships rather than arranged in
one hierarchy or sequence. Before choosing a graph algorithm, identify the graph's **shape and the
query being asked**.

## 2. Signals to notice

```text
nodes / vertices / cities / users / courses
roads / edges / links / dependencies
connected / reachable / route / network
directed? weighted? dynamic?
```

## 3. Naive idea

Jump directly to “BFS” or “DFS” as soon as the statement looks like a graph.

## 4. Why the naive idea breaks

Different graph questions need different invariants. Reachability, dependency order, connectivity
updates, and weighted shortest paths are not the same problem merely because they share nodes/edges.

## 5. Core intuition

Classify first:

```text
directed vs undirected
weighted vs unweighted
sparse vs dense
static vs edges changing
query: reachability? order? distance? connectivity?
```

The algorithm follows the query.

## 6. Invariant

Your representation must preserve the relationships relevant to the query. In an adjacency list,
`graph[u]` is exactly the set/list of outgoing neighbors of `u` under the chosen directedness model.

## 7. Step-by-step walkthrough

Edges `A-B`, `A-C`, `C-D` in an undirected graph become:

```text
A: B, C
B: A
C: A, D
D: C
```

For a directed prerequisite `A → B`, do **not** automatically add `B → A`; direction carries meaning.

## 8. Implementation

```python
from collections import defaultdict


def build_undirected(edges: list[tuple[int, int]]) -> dict[int, list[int]]:
    graph: dict[int, list[int]] = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    return dict(graph)
```

## 9. Complexity

Adjacency-list storage is `O(V + E)` and iterating all neighbors across a traversal is `O(V + E)`.
An adjacency matrix uses `O(V²)` space but supports constant-time edge existence checks.

## 10. Common mistakes

- forgetting reverse edges for an undirected graph;
- adding reverse edges to a directed graph;
- mixing node labels with zero-based array indices;
- overlooking disconnected components;
- choosing adjacency matrix for a huge sparse graph without need.

## 11. When NOT to use it

Do not force graph terminology onto simple arrays or intervals unless relationships truly form the
problem's state. Modeling is useful only when it clarifies queries.

## 12. Neighboring patterns

- **BFS/DFS:** reachability/traversal.
- **Topological sort:** directed dependency order.
- **Union-Find:** repeated undirected component merges/queries.
- **Dijkstra:** non-negative weighted shortest paths.

## 13. Mutation ladder

```text
unweighted undirected graph     → BFS/DFS candidate
directed prerequisites          → topological sort candidate
edge weights added              → weighted shortest-path reasoning
edges added with connectivity Q → Union-Find candidate
graph becomes dense             → representation trade-off changes
```

## 14. Practice ladder

- **Understand:** build adjacency lists, count degrees/components.
- **Recognize:** translate grid/social/prerequisite wording into graph structure.
- **Apply:** choose representation based on query and density.
- **Mixed:** classify graph before naming an algorithm.
