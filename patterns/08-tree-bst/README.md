# 08 — Tree / BST

## 1. What problem shape does this solve?

Trees model hierarchical parent/child relationships. BST problems add an ordering invariant that can
eliminate subtrees during search or validate local bounds globally.

## 2. Signals to notice

```text
root / child / leaf / depth / height
ancestor / subtree / path
inorder / preorder / postorder
binary search tree / ordered tree
```

## 3. Naive idea

Treat the structure as an arbitrary collection and scan all nodes for every query.

## 4. Why the naive idea breaks

It discards hierarchy and, for BSTs, ordering. Repeated queries can retraverse subtrees that a bound
comparison could exclude immediately.

## 5. Core intuition

A recursive tree call should have a clear contract: “solve this question for the subtree rooted at
`node`.” Parent logic then combines child answers. In a BST, values also carry range information:
left descendants are smaller, right descendants larger under the chosen duplicate policy.

## 6. Invariant

For BST validation, every node must lie inside a range inherited from **all** ancestors, not merely
compare correctly with its parent.

## 7. Step-by-step walkthrough

Validate:

```text
      8
     / \
    3  10
       /
      9
```

`8` allows `(-∞,∞)`. Left child inherits `(-∞,8)`, right child `(8,∞)`. Node `9` inherits `(8,10)`,
so it is valid. This range propagation catches deeper violations that parent-only checks miss.

## 8. Implementation

```python
def is_valid_bst(node, low=float("-inf"), high=float("inf")) -> bool:
    if node is None:
        return True
    if not low < node.val < high:
        return False
    return is_valid_bst(node.left, low, node.val) and is_valid_bst(node.right, node.val, high)
```

## 9. Complexity

Validation visits each node once: `O(N)` time. Recursion uses `O(H)` stack space where `H` is tree
height—`O(log N)` for a balanced tree but `O(N)` for a chain-shaped tree.

## 10. Common mistakes

- checking only parent-child ordering in a BST;
- confusing depth (root-to-node) with height (node-to-deepest-leaf);
- forgetting null/base cases;
- assuming a BST is balanced;
- mixing traversal order when construction/serialization depends on it.

## 11. When NOT to use it

The input being called a “tree” does not mean BST search applies. Without the ordering invariant,
arbitrary lookup may still require traversal.

## 12. Neighboring patterns

- **Tree DFS vs graph DFS:** trees have no cycles if parent edges are handled correctly.
- **BST vs binary search:** pointer hierarchy versus indexed sorted sequence.
- **Tree + DP:** subtree answers often become tree-DP states.

## 13. Mutation ladder

```text
plain binary tree        → traversal only
BST ordering guaranteed  → eliminate one subtree during search
tree becomes unbalanced  → search worst case degrades
need level order         → BFS queue
need subtree optimum     → tree DP candidate
```

## 14. Practice ladder

- **Understand:** max depth, inorder traversal, invert tree.
- **Recognize:** validate BST, lowest common ancestor.
- **Apply:** serialize/deserialize, subtree aggregate/path problems.
- **Mixed:** identify whether BST ordering is actually guaranteed.
