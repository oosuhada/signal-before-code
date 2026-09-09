# 03 — Sliding Window

## 1. What problem shape does this solve?

Sliding window searches contiguous subarrays/substrings while reusing state from the previous range.
It is especially strong for longest/shortest ranges satisfying a condition and fixed-size rolling
aggregates.

## 2. Signals to notice

```text
contiguous subarray / substring
longest / shortest window
at most / no more than / without repeating
fixed length K
condition maintained while boundaries move
```

## 3. Naive idea

Enumerate every start/end pair and recompute the contents of each range.

## 4. Why the naive idea breaks

Neighboring ranges overlap heavily. Recounting the same characters or values makes `O(N²)` ranges
and sometimes `O(N³)` total work.

## 5. Core intuition

Keep one live interval. When `right` adds an element, update just the state that changed. If the
window becomes invalid, advance `left` until the invariant returns.

## 6. Invariant

For the classic longest-valid-window form: **after the shrink loop, `[left, right]` is valid**. If
`left` only moves forward, each element enters and leaves the window at most once.

## 7. Step-by-step walkthrough

Longest substring without repeated characters in `abca`:

```text
r=0: [a]       valid
r=1: [ab]      valid
r=2: [abc]     valid, best=3
r=3: [abca]    duplicate a
      remove a at left → [bca] valid again
```

The value of the window is reused; we do not restart at every index.

## 8. Implementation

```python
def longest_unique(text: str) -> int:
    counts: dict[str, int] = {}
    left = 0
    best = 0
    for right, char in enumerate(text):
        counts[char] = counts.get(char, 0) + 1
        while counts[char] > 1:
            old = text[left]
            counts[old] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

## 9. Complexity

`right` advances `N` times. `left` also advances at most `N` times across the whole run. The nested
`while` is therefore amortized `O(N)`, with space proportional to the tracked window state.

## 10. Common mistakes

- assuming every contiguous problem supports sliding window;
- shrinking with `if` when multiple removals may be needed;
- updating the answer before restoring validity;
- forgetting to remove/decrement state as `left` moves;
- using sum-based shrink logic when negative numbers destroy monotonicity.

## 11. When NOT to use it

- Many known range-sum queries → prefix sum.
- Negative values can invalidate monotonic sum-window logic.
- Non-contiguous subsequence problems are not window problems.
- Window max/min needs a stronger structure at scale: monotonic queue.

## 12. Neighboring patterns

- **Sliding window vs prefix sum:** discover a range vs query a known range.
- **Sliding window vs two pointers:** both move endpoints, but window state/invariant is central here.
- **Sliding window vs monotonic queue:** ordinary counts/sums vs maintaining window extrema.

## 13. Mutation ladder

```text
fixed K rolling sum             → fixed window
longest at most K distinct      → variable window + counts
minimum sum >= target, positive → variable sum window
allow negative numbers          → ordinary sum window may fail
window maximum                  → monotonic queue
```

## 14. Practice ladder

- **Understand:** fixed-size averages, longest unique substring.
- **Recognize:** at-most-K distinct, minimum valid window.
- **Apply:** frequency constraints and multi-condition windows.
- **Mixed:** decide whether prefix sums or a monotonic deque better matches the mutation.

See [`../../wrong-turns/sliding-window-with-negative-values.md`](../../wrong-turns/sliding-window-with-negative-values.md).
