# 28 — Bitmask / Subset Enumeration

## 1. What problem shape does this solve?

Bitmasking represents a subset of a small fixed universe as an integer. It is useful when `N` is
small enough to enumerate `2^N` states or when a subset itself is a compact DP/memoization key.

## 2. Signals to notice

```text
all subsets / choose any combination
N around 15-22
visited subset of nodes/items
state is which items are used
```

## 3. Naive idea

Store each subset as a Python set/list and recursively copy it at every branch.

## 4. Why the naive idea breaks

The exponential number of states is already expensive. Heavy per-state allocation/comparison adds
avoidable overhead and makes subset identity harder to hash or index.

## 5. Core intuition

Bit `i` answers whether item `i` is included. One integer therefore provides membership tests,
insertion/removal, equality, and array/dict keys for a whole subset.

## 6. Invariant

Mask bit `i` has one stable meaning throughout the algorithm. A mask in `[0, 2^N)` uniquely
represents one subset of N indexed items.

## 7. Step-by-step walkthrough

For items `A,B,C`, mask `5 = 0b101`:

```text
bit 0 = 1 → A included
bit 1 = 0 → B absent
bit 2 = 1 → C included
subset = {A, C}
```

Enumerating masks `0..7` visits all eight subsets exactly once.

## 8. Implementation

```python
def all_subsets(nums: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    for mask in range(1 << len(nums)):
        subset = [nums[i] for i in range(len(nums)) if mask & (1 << i)]
        result.append(subset)
    return result
```

## 9. Complexity

There are `2^N` masks. Materializing every subset inspects up to N bits, so output construction is
`O(N 2^N)`. If each state transition can be updated more cleverly, some algorithms achieve closer to
`O(2^N)` state work.

## 10. Common mistakes

- forgetting exponential growth because bit operations look constant-time;
- using wrong bit index/item mapping;
- precedence errors in `mask & (1 << i)`;
- accidentally mutating a shared subset while also using masks;
- choosing bitmask DP with too many state dimensions.

## 11. When NOT to use it

- N around 50 makes full subset enumeration infeasible.
- Strong pruning and construction constraints may favor backtracking.
- Large sparse universes may be clearer with sets/frozensets.

## 12. Neighboring patterns

- **Bitmask vs backtracking:** direct state iteration vs recursive choose/undo/prune.
- **Bitmask vs DP:** mask can become one DP state dimension when only best/count per subset matters.
- **Bitmask vs bit manipulation:** subset representation is an application of bit operations.

## 13. Mutation ladder

```text
N <= 20, enumerate all subsets → bitmask
strong partial invalidity       → backtracking may prune better
need best value per subset      → bitmask DP
N around 40                     → meet-in-the-middle candidate
N huge                          → subset enumeration impossible
```

## 14. Practice ladder

- **Understand:** enumerate subsets and test membership.
- **Recognize:** used-node subset state, small-N exhaustive choices.
- **Apply:** traveling-state/assignment-style bitmask DP.
- **Mixed:** use N to reject exponential approaches early.
