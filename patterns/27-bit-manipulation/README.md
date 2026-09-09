# 27 — Bit Manipulation

## 1. What problem shape does this solve?

Bit manipulation is useful when integers encode binary flags, powers of two, parity, or XOR
cancellation. It is strongest when the bit-level property is part of the problem's mathematical
structure, not merely a trick to shorten code.

## 2. Signals to notice

```text
binary representation
power of two
toggle flags
unique number where others repeat
count/set/test bits
```

## 3. Naive idea

Convert numbers to binary strings or maintain a separate boolean array/set for every flag.

## 4. Why the naive idea breaks

String conversion can obscure constant-time integer operations and repeated flag structures waste
space when a machine word already represents those booleans naturally.

## 5. Core intuition

Think of an integer as a compact set of bit positions:

```text
set bit i:    mask |= 1 << i
clear bit i:  mask &= ~(1 << i)
test bit i:   mask & (1 << i)
toggle bit i: mask ^= 1 << i
```

XOR is especially useful because `x ^ x = 0` and `x ^ 0 = x`.

## 6. Invariant

When using a bitmask as flags, bit `i` must consistently represent one documented property. When
using XOR cancellation, the multiset assumptions (for example, every other value appears exactly
twice) are part of correctness.

## 7. Step-by-step walkthrough

Unique value in `[4, 1, 4, 2, 2]`:

```text
0 ^ 4 ^ 1 ^ 4 ^ 2 ^ 2
= (4^4) ^ (2^2) ^ 1
= 0 ^ 0 ^ 1
= 1
```

Order does not matter because XOR is associative/commutative.

## 8. Implementation

```python
def single_number(nums: list[int]) -> int:
    value = 0
    for number in nums:
        value ^= number
    return value


def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0
```

## 9. Complexity

The single-number scan is `O(N)` time and `O(1)` extra space. Individual fixed-width bit operations
are treated as constant time in interview complexity models, though Python integers are arbitrary
precision for very large values.

## 10. Common mistakes

- applying XOR cancellation when duplicate counts differ from the assumption;
- forgetting Python's behavior for negative arbitrary-precision integers;
- precedence mistakes around shifts and comparisons;
- using bit tricks that are harder to explain than direct arithmetic;
- confusing bit position with numeric value `1 << i`.

## 11. When NOT to use it

- If flags exceed a manageable bit width or readability suffers, sets/booleans may be better.
- Do not force bit tricks into ordinary arithmetic problems with no binary invariant.

## 12. Neighboring patterns

- **Bit manipulation vs bitmask enumeration:** operations on one encoded state vs iterate many subset
  states.
- **Bit flags vs set:** compact fixed universe vs general readable membership structure.

## 13. Mutation ladder

```text
every duplicate appears twice → XOR cancellation
duplicates appear three times → different bit-count reasoning
need subset identity          → bitmask state
need > word-sized universe    → set/other representation may be clearer
```

## 14. Practice ladder

- **Understand:** test/set bits, power of two, single number.
- **Recognize:** XOR parity/cancellation.
- **Apply:** bitwise counting and state encoding.
- **Mixed:** state the algebraic property before using the trick.
