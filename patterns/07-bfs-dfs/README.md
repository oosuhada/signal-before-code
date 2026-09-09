# 07 — BFS / DFS

**v0.1 state:** seed chapter, ready to study — **not a mastery claim**.

BFS and DFS can both visit a graph. The learning target is not memorizing `deque` versus recursion;
it is recognizing what **frontier order** the problem requires.

## 1. The Situation

Suppose every connection between nodes costs exactly one hop. Starting from `A`, find a shortest
route to `F`.

```text
A ─ B ─ D ─ F
│
C ─ E ─ F
```

The requirement is not merely “visit nodes.” It is:

> Visit states in a way that preserves increasing distance from the start.

## 2. First Naive Idea

A natural idea is to walk one path as far as possible and return the first route that reaches `F`.
That is depth-first behavior.

```text
A → B → D → ...
```

DFS is excellent for many reachability and exhaustive-search tasks, so it is a plausible candidate.

## 3. Why It Breaks

For **shortest unweighted path**, “first path found by DFS” can be **incorrect**.

DFS orders work by depth of the current branch, not by distance from the start. It can discover a
long route before a shorter sibling route.

To make the first discovery meaningful for shortest path, the traversal must exhaust distance `d`
before moving to distance `d+1`.

## 4. Signal to Notice

For BFS:

> **Unweighted / equal-cost edges + minimum number of steps/hops** → distance layers → FIFO queue →
> BFS becomes a strong candidate.

For DFS:

> **Reachability, component exploration, cycle/structure discovery, or choice-tree search where
> going deep is natural** → stack/recursion → DFS becomes a strong candidate.

The key distinction is the order in which the frontier should be consumed.

```text
BFS
distance layer 0
→ layer 1
→ layer 2
→ ...

DFS
one branch
→ deeper
→ deeper
→ backtrack
```

## 5. Candidate Approaches

| Candidate | Good at | Problem here |
| --- | --- | --- |
| DFS | reachability, components, recursive choice structure | first found path is not necessarily shortest |
| BFS | unweighted shortest hops, layers, multi-source expansion | may hold a broad frontier in memory |
| Dijkstra | non-negative weighted shortest path | unnecessary machinery when every edge costs 1 |
| repeated path enumeration | can eventually find all paths | potentially explosive and ignores visited-state reuse |

Both BFS and DFS are `O(V+E)` traversals on an adjacency-list graph when each reachable vertex/edge is
processed once. The choice can still affect correctness, memory shape, and what “first discovery”
means.

## 6. Why This Pattern

For the shortest-hop problem, derive the structure in this order:

```text
need closest nodes first
↓
nodes at distance d must be processed before distance d+1
↓
new neighbors discovered later wait behind current layer
↓
first-in-first-out frontier
↓
queue
↓
BFS
```

BFS invariant:

> When a node is first removed from the queue in an unweighted graph, the recorded route uses the
> minimum number of edges from the start.

For DFS reachability, the invariant is different:

> Every node placed on the stack is reachable from an already discovered node; visited-state tracking
> prevents infinite revisits in cyclic graphs.

## 7. Walkthrough

Use this graph:

```text
A: [B, C]
B: [D]
C: [E]
D: [F]
E: [F]
F: []
```

BFS from `A`:

| Step | Queue before | Pop | Newly discovered | Distance |
| ---: | --- | --- | --- | --- |
| 0 | `[A]` | `A` | `B, C` | `B=1, C=1` |
| 1 | `[B, C]` | `B` | `D` | `D=2` |
| 2 | `[C, D]` | `C` | `E` | `E=2` |
| 3 | `[D, E]` | `D` | `F` | `F=3` |

The queue is not an arbitrary implementation detail. Its order encodes the layer promise.

DFS on the same graph might maintain:

```text
stack: [A]
→ [C, B]
→ [C, D]
→ [C, F]
```

That order is perfectly valid for reachability, but the stack itself does not certify minimum hops.

## 8. Implementation

BFS appears only after the distance-layer argument:

```python
from collections import deque


def bfs_shortest_path(graph, start, target):
    queue = deque([start])
    parent = {start: None}

    while queue:
        node = queue.popleft()
        if node == target:
            break
        for neighbor in graph.get(node, ()):
            if neighbor in parent:
                continue
            parent[neighbor] = node
            queue.append(neighbor)

    if target not in parent:
        return None

    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    return list(reversed(path))
```

The tested module
[`../../signal_before_code/graph_search.py`](../../signal_before_code/graph_search.py) includes both
`bfs_shortest_path` and iterative `dfs_reachable` so their frontier policies can be compared without
recursion-limit noise.

## 9. Complexity

With adjacency lists:

- each reachable vertex enters the visited/parent structure at most once;
- each outgoing edge of a visited vertex is inspected at most once;
- therefore BFS and DFS both take `O(V + E)` time over the explored component;
- visited/parent state is `O(V)`;
- BFS queue memory can grow with the graph's maximum frontier width;
- DFS stack memory can grow with traversal depth.

The same Big-O time does **not** make the algorithms interchangeable. Frontier order gives BFS its
shortest-hop property.

## 10. When NOT to Use It

### Do not use plain BFS for arbitrary weighted shortest path

```text
A --100--> F
A --1--> B --1--> F
```

The direct edge uses fewer hops but costs more. Hop layers no longer equal cost layers.

### Do not use recursive DFS blindly on very deep graphs in Python

The algorithm may be conceptually right while recursion depth becomes an implementation hazard.
An explicit stack preserves the traversal family without relying on Python call-stack depth.

### Do not use graph traversal if direct indexing already answers the question

Turning every problem into a graph adds representation cost. The state-transition model should earn
its place.

Systems bridge:
[`beneath-the-stack/include/bts/graph.hpp`](https://github.com/oosuhada/beneath-the-stack/blob/main/include/bts/graph.hpp)
contains from-scratch graph traversal, while
[`docs/algorithm-defense.md`](https://github.com/oosuhada/beneath-the-stack/blob/main/docs/algorithm-defense.md)
records the BFS-vs-weighted-shortest-path failure boundary. The role here is to recognize the signal
before reaching for that implementation.

## 11. Mutation

Shortest-path mutations expose the boundary especially clearly:

### Original — every edge weight is `1`

```text
distance layer
→ FIFO queue
→ BFS
```

### Mutation A — edge weights are only `0` or `1`

Plain BFS no longer orders by total cost. A deque can prioritize zero-cost transitions:

```text
0-weight edge → front
1-weight edge → back
→ 0-1 BFS candidate
```

### Mutation B — all weights are positive but arbitrary

```text
FIFO frontier no longer matches cheapest frontier
→ priority by current distance
→ Dijkstra candidate
```

### Mutation C — a negative edge appears

Dijkstra's “settled minimum cannot improve later” assumption can fail. Dijkstra is no longer a valid
default; algorithms designed for negative edges enter the candidate set.

### Mutation D — there are many starting infection/source cells

Do not run one BFS per source. Initialize the queue with **all sources at distance 0** and expand one
shared frontier: multi-source BFS.

### Mutation E — only “is any path possible?” matters

Shortest-layer ordering is unnecessary. DFS may be simpler and can have a smaller active frontier on
some shapes.

## 12. Practice

### Understand

- [LeetCode 733 — Flood Fill](https://leetcode.com/problems/flood-fill/) — What makes this a
  reachability/component problem rather than a shortest-path problem?
- [Programmers 43165 — 타겟 넘버](https://school.programmers.co.kr/learn/courses/30/lessons/43165)
  — What choice-tree state would a DFS frame represent?

### Recognize

- [LeetCode 200 — Number of Islands](https://leetcode.com/problems/number-of-islands/) — What is the
  graph even though no explicit adjacency list is given?
- [Programmers 43162 — 네트워크](https://school.programmers.co.kr/learn/courses/30/lessons/43162)
  — What does one traversal consume before the component count increases?

### Apply

- [LeetCode 994 — Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) — Why should all
  initially active sources enter the same first layer?
- [LeetCode 1091 — Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/)
  — Which fact makes first discovery a shortest-path certificate?

See [`../../curriculum/problems.json`](../../curriculum/problems.json).
