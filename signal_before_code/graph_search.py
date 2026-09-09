"""Reference BFS/DFS implementations for the graph-search seed chapter."""

from collections import deque
from collections.abc import Hashable, Iterable, Mapping


def bfs_shortest_path[T: Hashable](
    graph: Mapping[T, Iterable[T]], start: T, target: T
) -> list[T] | None:
    """Return a minimum-hop path in an unweighted graph, or None when unreachable."""

    queue: deque[T] = deque([start])
    parent: dict[T, T | None] = {start: None}

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

    path: list[T] = []
    node: T | None = target
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path


def dfs_reachable[T: Hashable](graph: Mapping[T, Iterable[T]], start: T) -> set[T]:
    """Return all nodes reachable from start using an explicit LIFO frontier."""

    visited: set[T] = set()
    stack: list[T] = [start]

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)

        # Reverse a materialized neighbor list so a list-like adjacency order is explored naturally
        # when pushed onto a LIFO stack. Reachability correctness does not depend on this order.
        neighbors = tuple(graph.get(node, ()))
        stack.extend(reversed(neighbors))

    return visited
