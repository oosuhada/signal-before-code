# 04 — Stack & Queue

## 1. What problem shape does this solve?

Stacks and queues encode **which pending item must be handled next**. Use a stack when the most recent
unfinished context matters; use a queue when work must be processed in arrival/layer order.

## 2. Signals to notice

```text
nested / matching / undo / previous unfinished → stack
first come first served / layer / frontier       → queue
evaluate expression / parsing                    → stack
process tasks in arrival order                    → queue
```

## 3. Naive idea

Use a general list and repeatedly search for the relevant unfinished item or remove from the wrong
end.

## 4. Why the naive idea breaks

The problem already specifies an order discipline. Ignoring it introduces unnecessary scans or
expensive front removals from Python lists.

## 5. Core intuition

The data structure is a statement about **ownership of the next action**: LIFO means the newest open
context closes first; FIFO means older frontier work cannot be skipped by newer arrivals.

## 6. Invariant

- Stack: the top is the most recent unresolved item.
- Queue: the front is the oldest discovered but unprocessed item.

Every push/pop or enqueue/dequeue should preserve that ordering contract.

## 7. Step-by-step walkthrough

Balanced brackets `([])`:

```text
(  stack=[(]
[  stack=[(, []
]  must match top [  → pop
)  must match top (  → pop
empty stack → balanced
```

Matching against anything except the top would violate nesting.

## 8. Implementation

```python
def balanced(text: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for char in text:
        if char in "([{":
            stack.append(char)
        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
    return not stack
```

For FIFO queues in Python, prefer `collections.deque` rather than `list.pop(0)`.

## 9. Complexity

Each symbol is pushed/popped at most once, so bracket validation is `O(N)` time and `O(N)` worst-case
stack space. `deque.popleft()` is `O(1)`; list front deletion shifts remaining elements.

## 10. Common mistakes

- popping an empty stack;
- ignoring mismatched bracket types;
- using `list.pop(0)` for large FIFO workloads;
- confusing “visited” state with “processed” queue state in BFS;
- reaching for a stack when a monotonic stack invariant is actually required.

## 11. When NOT to use it

- Repeated best-priority item → heap, not ordinary queue.
- Random membership lookup → hash set/map.
- Next greater/smaller queries need a monotonic stack, not just any stack.

## 12. Neighboring patterns

- **Queue vs heap:** arrival order vs priority order.
- **Queue vs BFS:** queue is the mechanism; BFS is the graph-search invariant built on it.
- **Stack vs recursion:** recursion uses an implicit call stack.

## 13. Mutation ladder

```text
matching brackets       → stack
need minimum item next  → heap
graph distance layers   → queue + BFS
next greater element    → monotonic stack
bounded producer queue  → queue + capacity/backpressure concerns
```

## 14. Practice ladder

- **Understand:** valid parentheses, basic queue simulation.
- **Recognize:** expression evaluation, task ordering.
- **Apply:** queue-based graph frontier or stack-based parsing.
- **Mixed:** distinguish ordinary stack/queue from monotonic or priority structures.
