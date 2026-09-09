# 02 — Two Pointers

## 1. What problem shape does this solve?

Two pointers fit problems where two positions can move through an ordered structure and each move can
**safely eliminate** a set of impossible candidates. Common shapes include pair sums in sorted data,
palindrome checks, partition-like scans, merging ordered sequences, and opposing-boundary geometry.

## 2. Signals to notice

```text
sorted / ordered
pair satisfying a relation
left/right boundary
palindrome
merge two ordered sequences
```

The strongest signal is not “array.” It is monotonic movement: after a comparison, one pointer never
needs to move backward.

## 3. Naive idea

For a pair problem, test every `(i, j)` pair: `O(N²)`.

## 4. Why the naive idea breaks

It ignores ordering. If a sorted sequence tells you that every value to one side is even larger or
smaller, checking those candidates individually is repeated proof.

## 5. Core intuition

Use a comparison to discard an entire boundary. In sorted two-sum, if `a[left] + a[right]` is too
small, pairing `a[left]` with any smaller right value cannot help. So `left` is the disposable side.

## 6. Invariant

Every valid pair outside the current `[left, right]` search region has already been ruled out. Each
pointer move must preserve that claim.

## 7. Step-by-step walkthrough

Sorted array `[1, 2, 4, 7, 9]`, target `10`:

```text
L=1, R=9  sum=10 → found

target 11 instead:
L=1, R=9  10 < 11 → left++
L=2, R=9  11      → found
```

Why not move `right` after `10 < 11`? That would only make the sum smaller.

## 8. Implementation

```python
def pair_sum_sorted(nums: list[int], target: int) -> tuple[int, int] | None:
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None
```

## 9. Complexity

Each pointer moves in only one direction and can move at most `N` positions total. The loop is
therefore `O(N)`, not `O(N²)`, even though two positions are involved. Extra space is `O(1)`.

## 10. Common mistakes

- using the pattern without sorted/monotonic structure;
- moving the wrong boundary because the elimination argument is unstated;
- using `left <= right` when two distinct indices are required;
- mishandling duplicates when all unique pairs are requested;
- sorting input without considering whether original indices/output order must be preserved.

## 11. When NOT to use it

- Unordered membership questions may be cleaner with hashing.
- One monotonic answer boundary is binary-search territory.
- Contiguous variable-length constraints usually suggest sliding window.

## 12. Neighboring patterns

- **Two pointers vs binary search:** coordinate two positions vs locate one boundary.
- **Two pointers vs sliding window:** both move boundaries; sliding window maintains a contiguous
  range condition, while classic two pointers often reason about endpoint combinations.
- **Two pointers vs hash:** exploit order versus remember complements.

## 13. Mutation ladder

```text
sorted two-sum           → opposing pointers
unsorted two-sum         → hash or sort first
three-sum                → sort + fix one + two pointers
longest valid substring  → sliding-window form of two moving boundaries
minimum feasible value   → binary search on answer
```

## Visual Trace / Try Predicting

See the boundary-elimination state in [`../../visuals/two-pointers.md`](../../visuals/two-pointers.md),
then run `python3 scripts/trace.py two-pointers --predict` from the repository root.

## 14. Practice ladder

- **Understand:** sorted pair sum, palindrome.
- **Recognize:** container/water-style boundary elimination.
- **Apply:** three-sum, duplicate skipping, merge/sweep hybrids.
- **Mixed:** distinguish pointer elimination from a true sliding-window invariant.

See [`../../comparisons/binary-search-vs-two-pointers.md`](../../comparisons/binary-search-vs-two-pointers.md).
