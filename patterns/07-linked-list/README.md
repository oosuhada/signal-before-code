# 07 — Linked List

## 1. What problem shape does this solve?

Linked-list problems are usually not about “using a linked list” from scratch. The structure is
already given, and the task tests pointer ownership: reverse links, detect cycles, find middle nodes,
merge chains, or rearrange without random indexing.

## 2. Signals to notice

```text
singly / doubly linked nodes
reverse in-place
cycle
middle / kth from end
merge sorted lists
O(1) extra space requested
```

## 3. Naive idea

Copy every value into an array, solve there, then rebuild the list.

## 4. Why the naive idea breaks

It may violate `O(1)` extra-space requirements and hides the pointer reasoning the problem is testing.
It also cannot preserve node identity if the output must reuse original nodes.

## 5. Core intuition

A linked list trades random access for cheap local rewiring. Before changing `current.next`, save any
pointer you will still need. Most bugs are ownership bugs: you lose the rest of the chain.

## 6. Invariant

During iterative reversal:

```text
prev    = already reversed prefix
current = first node not yet reversed
```

The union of those two parts must always equal the original list, with no lost nodes.

## 7. Step-by-step walkthrough

Reverse `1 → 2 → 3 → None`:

```text
prev=None, cur=1
save next=2; 1.next=None; prev=1; cur=2
save next=3; 2.next=1;    prev=2; cur=3
save next=None; 3.next=2  → new head=3
```

## 8. Implementation

```python
class Node:
    def __init__(self, value: int, next: "Node | None" = None):
        self.value = value
        self.next = next


def reverse(head: Node | None) -> Node | None:
    prev = None
    current = head
    while current:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev
```

## 9. Complexity

Reversal touches every node once: `O(N)` time and `O(1)` auxiliary space. Recursive reversal also
touches each node once but uses `O(N)` call-stack space.

## 10. Common mistakes

- overwriting `current.next` before saving it;
- comparing node values when node identity matters;
- forgetting even/odd length behavior in slow/fast pointer logic;
- dereferencing `fast.next` without checking `fast`;
- creating accidental cycles while reconnecting sublists.

## 11. When NOT to use it

- Frequent index access strongly favors arrays.
- Membership lookup is not a linked-list strength.
- If copying to an array is permitted and clarity matters more than in-place constraints, the array
  solution may be entirely reasonable.

## 12. Neighboring patterns

- **Linked list + two pointers:** slow/fast cycle and middle detection.
- **Linked list + recursion:** recursive reverse/merge mirrors chain structure.
- **Linked list vs array:** pointer-local updates versus random access/cache locality.

## 13. Mutation ladder

```text
reverse whole list       → three-pointer iteration
find middle              → slow/fast pointers
cycle exists?            → Floyd slow/fast
reverse subrange         → sentinel + local rewiring
random access required   → array becomes better structure
```

## 14. Practice ladder

- **Understand:** reverse list, merge two sorted lists.
- **Recognize:** middle, kth from end, cycle detection.
- **Apply:** reorder list, reverse subrange/groups.
- **Mixed:** decide whether an auxiliary array is allowed and simpler.
