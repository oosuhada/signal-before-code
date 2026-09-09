# Binary Search vs Two Pointers

## Same-looking problem

Both exploit order to eliminate candidates faster than a full scan of combinations.

## What changes?

- Search for one boundary/target in a monotonic space → binary search.
- Coordinate two positions whose movement can be justified from a combined condition → two
  pointers.

For sorted two-sum, comparing `a[left] + a[right]` tells you which endpoint can be discarded. That
relationship is more direct than running a binary search for every left endpoint.

For “minimum capacity that can ship within D days,” there are not two sequence endpoints to move;
the monotonic object is the **answer value**, so binary search on answer is natural.
