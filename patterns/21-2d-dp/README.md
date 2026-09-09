# 21 — 2D DP

## 1. What problem shape does this solve?

2D DP is natural when a subproblem needs two independent coordinates to describe what remains or has
been processed: two string indices, grid row/column, day/state, or position plus another bounded
dimension.

## 2. Signals to notice

```text
compare two sequences
grid path/count/cost
state depends on row and column
prefix of A + prefix of B
```

## 3. Naive idea

Recursively branch on choices from both coordinates without remembering pairs already solved.

## 4. Why the naive idea breaks

Different branches repeatedly reach the same `(i, j)` question. The number of recursive paths can be
exponential even though there are only `rows × cols` distinct coordinate states.

## 5. Core intuition

Ask what `(i, j)` means. For longest common subsequence:

> `dp[i][j]` = LCS length using the first `i` characters of A and first `j` characters of B.

That sentence determines both base cases and transition direction.

## 6. Invariant

At cell `(i, j)`, every dependency cell represents a smaller prefix/subproblem under the same
definition and has already been computed.

## 7. Step-by-step walkthrough

For strings `ab` and `ac`:

```text
      '' a c
''     0 0 0
a      0 1 1
b      0 1 1
```

Matching `a/a` extends the diagonal. At `b/c`, characters differ, so inherit the best of dropping one
side: `max(up, left)`.

## 8. Implementation

```python
def lcs_length(a: str, b: str) -> int:
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]
```

## 9. Complexity

There are `(len(a)+1) × (len(b)+1)` states and constant transition work, so time and table space are
`O(MN)`. Some problems allow rolling-row compression to `O(min(M,N))` space.

## 10. Common mistakes

- unclear meaning of row/column indices;
- forgetting the extra zero row/column;
- mixing character indices `i` with DP prefix length `i+1`;
- iterating in an order before dependencies exist;
- compressing rows while still needing overwritten diagonal/previous-row values.

## 11. When NOT to use it

- If one coordinate is redundant, a 1D state is simpler.
- If `MN` is too large, look for sparsity, greedy structure, binary-search optimization, or a
  different formulation.

## 12. Neighboring patterns

- **2D DP vs BFS grid:** optimal/count state over coordinates vs shortest equal-cost movement.
- **2D DP vs backtracking:** aggregate repeated coordinate states vs enumerate concrete paths.
- **2D DP vs edit/LCS variants:** same grid-of-prefixes model, different transitions.

## 13. Mutation ladder

```text
grid count paths             → 2D DP
grid shortest equal steps    → BFS instead
compare two strings          → prefix-pair DP
only previous row needed     → rolling-space optimization
state adds another dimension → complexity may become O(N³) or worse
```

## 14. Practice ladder

- **Understand:** unique paths, minimum path sum.
- **Recognize:** LCS/edit-distance state grids.
- **Apply:** obstacles, reconstruction, rolling rows.
- **Mixed:** decide whether the grid is a graph-distance problem or a DP-state problem.
