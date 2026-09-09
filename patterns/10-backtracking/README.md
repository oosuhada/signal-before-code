# 10 — Backtracking

## 1. What problem shape does this solve?

Backtracking explores a decision tree when the task asks for combinations, permutations, valid
configurations, or existence under constraints and `N` is small enough for exponential search.

## 2. Signals to notice

```text
all combinations / permutations
construct any/all valid arrangement
N small (often <= 20, sometimes much smaller)
choose / skip / undo
constraints can prune partial choices
```

## 3. Naive idea

Generate every possible full candidate, then test validity only at the end.

## 4. Why the naive idea breaks

The search tree is already exponential; postponing validity checks expands branches that could have
been rejected much earlier.

## 5. Core intuition

Build one partial solution. After each choice, ask whether that prefix can still lead to a valid full
solution. If not, stop exploring that branch. Otherwise recurse, then undo the choice.

## 6. Invariant

At entry to `dfs(state)`, the current path represents exactly the choices made for that state and is
valid so far. After the recursive call returns, undo must restore the state exactly.

## 7. Step-by-step walkthrough

Generate length-2 permutations from `{A,B,C}`:

```text
[]
├─ A → [A,B], [A,C] → undo A
├─ B → [B,A], [B,C] → undo B
└─ C → [C,A], [C,B]
```

The undo step is what lets sibling branches see a clean state.

## 8. Implementation

```python
def permutations(nums: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    path: list[int] = []
    used = [False] * len(nums)

    def dfs() -> None:
        if len(path) == len(nums):
            result.append(path.copy())
            return
        for i, value in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(value)
            dfs()
            path.pop()
            used[i] = False

    dfs()
    return result
```

## 9. Complexity

Permutation generation has `N!` leaves and output itself is that large, so no polynomial algorithm
can list them all. For subset choices, the tree often has `2^N` states. Pruning changes practical
work but must be justified separately.

## 10. Common mistakes

- forgetting to undo mutable state;
- appending `path` instead of `path.copy()`;
- treating duplicate values as distinct when the output requires unique combinations;
- pruning without proving the branch cannot recover;
- ignoring exponential constraints because each recursive function body is short.

## 11. When NOT to use it

- If only an optimal/count answer is needed and states repeat, DP may collapse work.
- If N is large, exhaustive search is usually impossible without strong structure.
- If subsets can be iterated directly and no pruning is needed, bitmasking may be simpler.

## 12. Neighboring patterns

- **Backtracking vs DP:** enumerate paths vs cache repeated states.
- **Backtracking vs bitmask:** recursive construction/pruning vs compact subset identity.
- **Backtracking vs DFS:** backtracking is DFS over an implicit decision tree with state restoration.

## 13. Mutation ladder

```text
all permutations       → backtracking
duplicates added       → sort + duplicate-skip rule
only count/best needed → memoization/DP candidate
N around 20 subsets    → bitmask may simplify
strong prefix rules    → pruning becomes central
```

## 14. Practice ladder

- **Understand:** subsets, permutations, combinations.
- **Recognize:** phone-letter combinations, constrained construction.
- **Apply:** N-Queens/word search-style pruning.
- **Mixed:** decide whether repeated state suggests DP instead.

See [`../../comparisons/backtracking-vs-dp.md`](../../comparisons/backtracking-vs-dp.md).
