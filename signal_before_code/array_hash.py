"""Reference implementations for the Array & Hash seed chapter.

These functions intentionally stay small. The chapter README contains the reasoning that should come
before using them.
"""

from collections.abc import Hashable, Iterable


def first_duplicate[T: Hashable](values: Iterable[T]) -> T | None:
    """Return the first value whose occurrence proves it was seen earlier."""

    seen: set[T] = set()
    for value in values:
        if value in seen:
            return value
        seen.add(value)
    return None


def frequency_count[T: Hashable](values: Iterable[T]) -> dict[T, int]:
    """Count values with explicit key-to-count state."""

    counts: dict[T, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return counts
