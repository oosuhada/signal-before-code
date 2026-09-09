"""Reference implementation for the Two Pointers seed chapter."""

from collections.abc import Sequence


def find_pair_with_sum(values: Sequence[int], target: int) -> tuple[int, int] | None:
    """Return one value pair summing to target from non-decreasing input.

    The explicit precondition check makes the signal visible during learning: this version relies on
    sorted input for safe boundary elimination.
    """

    if any(values[index] > values[index + 1] for index in range(len(values) - 1)):
        raise ValueError("two-pointer pair search requires non-decreasing input")

    left = 0
    right = len(values) - 1

    while left < right:
        current = values[left] + values[right]
        if current == target:
            return values[left], values[right]
        if current < target:
            left += 1
        else:
            right -= 1

    return None
