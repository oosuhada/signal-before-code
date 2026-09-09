"""Deterministic visual traces for reasoning about algorithm state transitions."""

from __future__ import annotations

import heapq
from collections import deque
from collections.abc import Callable
from math import inf
from typing import Any

Trace = dict[str, Any]
Step = dict[str, Any]


def _step(
    number: int,
    state: dict[str, Any],
    decision: str,
    invariant: str,
    visual: str,
    prompt: str,
    eliminated: str = "",
) -> Step:
    return {
        "step": number,
        "state": state,
        "decision": decision,
        "invariant": invariant,
        "eliminated": eliminated,
        "visual": visual,
        "prompt": prompt,
    }


def trace_two_pointers() -> Trace:
    values, target = [1, 2, 4, 6, 8], 10
    left, right, steps = 0, len(values) - 1, []
    number = 0
    while left < right:
        total = values[left] + values[right]
        visual = (
            f"{values}\n{'   ' * left}L{'   ' * max(0, right - left - 1)}R\n"
            f"sum={total} target={target}"
        )
        if total == target:
            decision, eliminated = "pair found; stop", "all remaining pairs are irrelevant"
            steps.append(
                _step(
                    number,
                    {"left": left, "right": right, "sum": total},
                    decision,
                    "Every index outside [left, right] has already been ruled out safely.",
                    visual,
                    "Is the sum too small, too large, or equal?",
                    eliminated,
                )
            )
            break
        if total < target:
            decision = (
                "move left rightward; this left value is too small even with the largest partner"
            )
            eliminated = f"index {left}"
            next_left, next_right = left + 1, right
        else:
            decision = (
                "move right leftward; this right value is too large even with the smallest partner"
            )
            eliminated = f"index {right}"
            next_left, next_right = left, right - 1
        steps.append(
            _step(
                number,
                {"left": left, "right": right, "sum": total},
                decision,
                "Sorted order makes one boundary disposable after each comparison.",
                visual,
                "Which pointer can move without losing a possible target pair?",
                eliminated,
            )
        )
        left, right, number = next_left, next_right, number + 1
    return {
        "algorithm": "two-pointers",
        "input": {"values": values, "target": target},
        "goal": "Find a target-sum pair while proving discarded boundaries cannot help.",
        "steps": steps,
    }


def trace_sliding_window() -> Trace:
    values, limit = [2, 1, 3, 2, 1], 5
    left, total, best, steps = 0, 0, 0, []
    for right, value in enumerate(values):
        total += value
        removed: list[int] = []
        while total > limit:
            removed.append(values[left])
            total -= values[left]
            left += 1
        best = max(best, right - left + 1)
        visual = f"values={values}\nwindow={values[left : right + 1]} sum={total} best={best}"
        decision = "shrink until valid, then record the valid window"
        steps.append(
            _step(
                right,
                {"left": left, "right": right, "sum": total, "best": best},
                decision,
                "All values are positive, so removing from the left can only decrease "
                "the window sum.",
                visual,
                "After adding the new right value, must the left boundary move?",
                f"removed from left: {removed}" if removed else "nothing removed",
            )
        )
    return {
        "algorithm": "sliding-window",
        "input": {"values": values, "max_sum": limit},
        "goal": "Maintain a contiguous window with sum <= 5 without recomputing every interval.",
        "steps": steps,
    }


def trace_binary_search() -> Trace:
    values, target = [1, 4, 7, 10, 13, 17, 23], 17
    left, right, steps, number = 0, len(values) - 1, [], 0
    while left <= right:
        mid = (left + right) // 2
        value = values[mid]
        visual = f"{values}\nL={left}  mid={mid}  R={right}\nnums[mid]={value} target={target}"
        if value == target:
            decision, eliminated = "target found", "search ends"
        elif value < target:
            decision, eliminated = "move left to mid + 1", f"indices {left}..{mid}"
        else:
            decision, eliminated = "move right to mid - 1", f"indices {mid}..{right}"
        steps.append(
            _step(
                number,
                {"left": left, "right": right, "mid": mid, "value": value},
                decision,
                "If the target exists, it remains inside the closed interval [left, right].",
                visual,
                "Which half can be eliminated using sorted order?",
                eliminated,
            )
        )
        if value == target:
            break
        if value < target:
            left = mid + 1
        else:
            right = mid - 1
        number += 1
    return {
        "algorithm": "binary-search",
        "input": {"values": values, "target": target},
        "goal": "Shrink a monotonic search space while preserving the possible-answer interval.",
        "steps": steps,
    }


def trace_heap() -> Trace:
    values = [7, 2, 9, 4, 1]
    heap: list[int] = []
    steps: list[Step] = []
    for number, value in enumerate(values):
        heapq.heappush(heap, value)
        steps.append(
            _step(
                number,
                {"heap": list(heap), "inserted": value},
                f"push {value}",
                "heap[0] is the smallest retained item; the rest is only partially ordered.",
                f"heap-array={heap}\nroot={heap[0]}",
                "After insertion, which value must be at the root?",
            )
        )
    number = len(steps)
    for _ in range(2):
        before = list(heap)
        value = heapq.heappop(heap)
        steps.append(
            _step(
                number,
                {"heap": list(heap), "popped": value},
                f"pop minimum {value}",
                "After repair, heap[0] is again the minimum of all remaining items.",
                f"before={before}\npopped={value}\nafter={heap}",
                "Which value is guaranteed to leave next?",
                f"minimum {value} removed",
            )
        )
        number += 1
    return {
        "algorithm": "heap",
        "input": {"values": values},
        "goal": "Maintain repeated minimum access without fully sorting after each update.",
        "steps": steps,
    }


GRAPH = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": [], "F": []}


def trace_bfs() -> Trace:
    queue = deque(["A"])
    visited = {"A"}
    steps: list[Step] = []
    number = 0
    while queue:
        node = queue.popleft()
        added = []
        for neighbor in GRAPH[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                added.append(neighbor)
        steps.append(
            _step(
                number,
                {"visit": node, "queue": list(queue), "visited": sorted(visited)},
                f"visit {node}; enqueue unseen neighbors {added}",
                "The queue stores the discovered frontier in nondecreasing hop distance.",
                f"visit={node}\nqueue={list(queue)}\nvisited={sorted(visited)}",
                "Which discovered node is visited next, and why?",
            )
        )
        number += 1
    return {
        "algorithm": "bfs",
        "input": {"graph": GRAPH, "start": "A"},
        "goal": "Expose FIFO frontier layers in an unweighted graph.",
        "steps": steps,
    }


def trace_dfs() -> Trace:
    stack, visited, steps, number = ["A"], set(), [], 0
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        pushed = list(reversed(GRAPH[node]))
        stack.extend(pushed)
        steps.append(
            _step(
                number,
                {"visit": node, "stack": list(stack), "visited": sorted(visited)},
                f"visit {node}; push children {pushed}",
                "The stack preserves unfinished branches so one branch is explored deeply "
                "before siblings.",
                f"visit={node}\nstack={stack}\nvisited={sorted(visited)}",
                "Which branch will the LIFO stack explore next?",
            )
        )
        number += 1
    return {
        "algorithm": "dfs",
        "input": {"graph": GRAPH, "start": "A"},
        "goal": "Expose branch depth and the explicit undo point stored by a stack.",
        "steps": steps,
    }


def trace_union_find() -> Trace:
    parent = list(range(6))
    size = [1] * 6
    operations = [(0, 1), (2, 3), (1, 2), (4, 5)]
    steps: list[Step] = []

    def find(x: int) -> int:
        while x != parent[x]:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for number, (a, b) in enumerate(operations):
        ra, rb = find(a), find(b)
        if ra != rb:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
        steps.append(
            _step(
                number,
                {"union": [a, b], "parent": list(parent), "size": list(size)},
                f"merge roots {ra} and {rb}" if ra != rb else "already connected",
                "Every element reaches one representative root for its current component.",
                f"union({a}, {b})\nparent={parent}\nsize={size}",
                "Which representatives should be compared before merging?",
            )
        )
    return {
        "algorithm": "union-find",
        "input": {"nodes": 6, "unions": operations},
        "goal": "Track changing connectivity through component representatives.",
        "steps": steps,
    }


def trace_topological_sort() -> Trace:
    graph = {"A": ["C"], "B": ["C", "D"], "C": ["E"], "D": ["F"], "E": ["F"], "F": []}
    indegree = {node: 0 for node in graph}
    for neighbors in graph.values():
        for neighbor in neighbors:
            indegree[neighbor] += 1
    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    steps: list[Step] = []
    number = 0
    while queue:
        node = queue.popleft()
        released = []
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
                released.append(neighbor)
        steps.append(
            _step(
                number,
                {"take": node, "indegree": dict(indegree), "ready": list(queue)},
                f"emit {node}; release {released}",
                "A node enters the ready queue only after every prerequisite edge has been "
                "removed.",
                f"take={node}\nready={list(queue)}\nindegree={indegree}",
                "Which nodes now have no unfinished prerequisites?",
            )
        )
        number += 1
    return {
        "algorithm": "topological-sort",
        "input": {"graph": graph},
        "goal": "Watch dependency edges disappear until nodes become safe to schedule.",
        "steps": steps,
    }


def trace_dijkstra() -> Trace:
    graph = {"A": [("B", 4), ("C", 1)], "B": [("D", 1)], "C": [("B", 2), ("D", 5)], "D": []}
    distance = {node: inf for node in graph}
    distance["A"] = 0
    heap: list[tuple[float, str]] = [(0, "A")]
    finalized: set[str] = set()
    steps: list[Step] = []
    number = 0
    while heap:
        dist, node = heapq.heappop(heap)
        if node in finalized:
            continue
        finalized.add(node)
        relaxed = []
        for neighbor, weight in graph[node]:
            candidate = dist + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
                relaxed.append(f"{neighbor}={candidate}")
        steps.append(
            _step(
                number,
                {"finalize": node, "distance": dict(distance), "heap": list(heap)},
                f"finalize {node} at {dist}; relax {relaxed}",
                "With nonnegative edges, the smallest tentative distance cannot be improved "
                "through an unfinalized node.",
                f"finalized={sorted(finalized)}\ndist={distance}\nheap={heap}",
                "Why is the minimum tentative node safe to finalize now?",
            )
        )
        number += 1
    return {
        "algorithm": "dijkstra",
        "input": {"graph": graph, "start": "A"},
        "goal": "Separate tentative distances from distances that are safe to finalize.",
        "steps": steps,
    }


def trace_dp() -> Trace:
    n = 6
    dp = [0] * (n + 1)
    dp[1] = 1
    steps = [
        _step(
            0,
            {"dp": list(dp), "defined": [0, 1]},
            "define base states",
            "dp[i] means Fibonacci(i); every filled cell is the final answer for that subproblem.",
            f"dp={dp}",
            "Before transitions, what does each dp index mean?",
        )
    ]
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        steps.append(
            _step(
                i - 1,
                {"index": i, "dp": list(dp)},
                f"dp[{i}] = dp[{i - 1}] + dp[{i - 2}] = {dp[i]}",
                "Every referenced smaller Fibonacci state is already final.",
                f"dp={dp}",
                f"Which previously solved states define dp[{i}]?",
            )
        )
    return {
        "algorithm": "dp",
        "input": {"n": n, "state_definition": "dp[i] = Fibonacci(i)"},
        "goal": "See state meaning before recurrence syntax.",
        "steps": steps,
    }


def trace_dp_grid() -> Trace:
    rows, cols = 3, 3
    dp = [[0] * cols for _ in range(rows)]
    steps: list[Step] = []
    number = 0
    for r in range(rows):
        for c in range(cols):
            if r == 0 and c == 0:
                dp[r][c] = 1
            else:
                up = dp[r - 1][c] if r else 0
                left = dp[r][c - 1] if c else 0
                dp[r][c] = up + left
            visual = "\n".join(" ".join(f"{value:2}" for value in row) for row in dp)
            steps.append(
                _step(
                    number,
                    {"cell": [r, c], "dp": [row[:] for row in dp]},
                    f"fill ({r},{c}) from up + left",
                    "dp[r][c] is the number of right/down paths to that cell.",
                    visual,
                    f"Which already-final neighboring states define cell ({r},{c})?",
                )
            )
            number += 1
    return {
        "algorithm": "dp-grid",
        "input": {
            "rows": rows,
            "cols": cols,
            "state_definition": "dp[r][c] = paths from start to cell (r,c)",
        },
        "goal": "Fill a 2D state table only from states whose meaning is already fixed.",
        "steps": steps,
    }


def trace_monotonic_stack() -> Trace:
    values = [2, 1, 4, 3, 5]
    stack: list[int] = []
    answer = [-1] * len(values)
    steps: list[Step] = []
    for i, value in enumerate(values):
        resolved = []
        while stack and values[stack[-1]] < value:
            index = stack.pop()
            answer[index] = value
            resolved.append(index)
        stack.append(i)
        steps.append(
            _step(
                i,
                {"index": i, "stack_indices": list(stack), "answer": list(answer)},
                f"resolve indices {resolved}; push {i}",
                "Stack values are monotonically decreasing; unresolved indices await a larger "
                "value to the right.",
                f"values={values}\nstack-values={[values[j] for j in stack]}\nanswer={answer}",
                "Which unresolved elements can the current value resolve?",
            )
        )
    return {
        "algorithm": "monotonic-stack",
        "input": {"values": values},
        "goal": "Keep only unresolved candidates that a future larger value could still answer.",
        "steps": steps,
    }


def trace_backtracking() -> Trace:
    values = [1, 2, 3]
    path: list[int] = []
    steps: list[Step] = []
    number = 0

    def visit(index: int) -> None:
        nonlocal number
        if index == len(values):
            steps.append(
                _step(
                    number,
                    {"index": index, "path": list(path)},
                    "emit current subset",
                    "path contains exactly the decisions made along the current root-to-leaf "
                    "branch.",
                    f"leaf {path}",
                    "At a leaf, what result does the current decision path represent?",
                )
            )
            number += 1
            return
        value = values[index]
        path.append(value)
        steps.append(
            _step(
                number,
                {"index": index, "path": list(path)},
                f"choose {value}",
                "Changes belong only to the current branch until they are undone.",
                f"choose → {path}",
                "After choosing, what state must be restored when this branch returns?",
            )
        )
        number += 1
        visit(index + 1)
        path.pop()
        steps.append(
            _step(
                number,
                {"index": index, "path": list(path)},
                f"undo {value}",
                "Undo restores the parent state exactly before exploring the sibling branch.",
                f"undo   → {path}",
                "What sibling decision becomes possible after undo?",
            )
        )
        number += 1
        visit(index + 1)

    visit(0)
    return {
        "algorithm": "backtracking",
        "input": {"values": values},
        "goal": "Make choose → explore → undo visible as a decision-tree state machine.",
        "steps": steps,
    }


TRACE_BUILDERS: dict[str, Callable[[], Trace]] = {
    "two-pointers": trace_two_pointers,
    "sliding-window": trace_sliding_window,
    "binary-search": trace_binary_search,
    "heap": trace_heap,
    "bfs": trace_bfs,
    "dfs": trace_dfs,
    "union-find": trace_union_find,
    "topological-sort": trace_topological_sort,
    "dijkstra": trace_dijkstra,
    "dp": trace_dp,
    "dp-grid": trace_dp_grid,
    "monotonic-stack": trace_monotonic_stack,
    "backtracking": trace_backtracking,
}


def build_trace(algorithm: str) -> Trace:
    try:
        return TRACE_BUILDERS[algorithm]()
    except KeyError as error:
        raise ValueError(f"unknown trace: {algorithm}") from error


def render_step(step: Step, *, reveal: bool = True) -> str:
    lines = [f"Step {step['step']}", step["visual"], "", f"Invariant: {step['invariant']}"]
    if reveal:
        lines.extend([f"Decision: {step['decision']}", f"Eliminated/changed: {step['eliminated']}"])
    else:
        lines.extend(["", f"Predict: {step['prompt']}"])
    return "\n".join(lines)
