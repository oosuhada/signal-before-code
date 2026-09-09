# 09 — Recursion

## 1. What problem shape does this solve?

Recursion fits self-similar structure: a problem can be solved by solving smaller versions of the
same problem, especially trees, divide-and-conquer ranges, and decision trees.

## 2. Signals to notice

```text
subtree / nested structure
divide into smaller instances
choose then solve the remainder
natural base case
```

## 3. Naive idea

Write recursive calls because the code looks short, without defining what each call returns.

## 4. Why the naive idea breaks

Recursion without a contract produces unclear base cases, duplicated work, and accidental exponential
runtime. “It calls itself” is a mechanism, not a correctness argument.

## 5. Core intuition

State the function contract first:

> `solve(x)` returns ______ for the subproblem represented by `x`.

Then trust recursive calls to satisfy that contract for smaller inputs and focus on how to combine
their results.

## 6. Invariant

Every recursive call must make measurable progress toward a base case. If the state can repeat
without shrinking or changing, termination is not guaranteed.

## 7. Step-by-step walkthrough

Tree height:

```text
height(None) = 0
height(node) = 1 + max(height(left), height(right))
```

The parent does not need to know how child heights are computed; it only relies on their contract.

## 8. Implementation

```python
def tree_height(node) -> int:
    if node is None:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))
```

## 9. Complexity

For a tree height computation, each node is visited once: `O(N)` time and `O(H)` call-stack space.
Complexity must be derived from the recursion tree, not guessed from the number of recursive lines.

## 10. Common mistakes

- missing or unreachable base case;
- recursive state that does not shrink;
- exponential repeated subproblems mistaken for harmless recursion;
- mutating shared state without undoing it;
- hitting Python recursion depth on chain-like inputs.

## 11. When NOT to use it

- Very deep inputs may require iterative stacks/queues.
- Repeated overlapping subproblems may need memoization/DP.
- Straight linear scans are often clearer iteratively.

## 12. Neighboring patterns

- **Recursion vs stack:** explicit vs implicit stack.
- **Recursion vs backtracking:** backtracking adds choose/explore/undo over a decision tree.
- **Recursion vs DP:** memoization collapses repeated states.

## 13. Mutation ladder

```text
tree traversal             → plain recursion
need all choices           → backtracking
same state repeats         → memoized recursion / DP
depth may be 100,000       → iterative form
split array in halves      → divide and conquer
```

## 14. Practice ladder

- **Understand:** factorial only as mechanics; tree depth as meaningful structure.
- **Recognize:** recursive linked-list/tree transformations.
- **Apply:** divide-and-conquer and recursive state composition.
- **Mixed:** identify when recursion hides exponential repeated work.
