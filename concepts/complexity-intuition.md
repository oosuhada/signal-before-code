# Complexity Intuition: What Work Must Disappear?

Big-O is most useful here as an elimination tool. Instead of reciting definitions, ask what kind of
work each growth rate permits as input grows.

## `O(1)` — work independent of collection size

Examples: array indexing, a hash lookup on average, checking the heap root.

The important nuance is that “constant” does not mean “free.” A large constant, allocation, hashing
a long string, or a cache miss still costs time. Complexity describes scaling behavior.

## `O(log N)` — repeatedly throw away a fraction

Binary search and balanced-tree operations feel fast because one decision removes a large part of
the remaining search space.

```text
1,000,000 candidates
→ 500,000
→ 250,000
→ ...
→ about 20 decisions
```

The signal is not merely “sorted.” It is **safe elimination**.

## `O(N)` — touch each relevant item a bounded number of times

Many excellent interview solutions are linear because every element enters and leaves a structure
once: sliding window, monotonic stack, BFS/DFS over adjacency lists.

When an algorithm looks nested, ask for amortized reasoning. A `while` loop inside a `for` loop can
still be `O(N)` if an element can be removed only once.

## `O(N log N)` — linear work plus ordering/divide-and-conquer

Sorting often dominates here. It is a strong candidate when ordering unlocks a much simpler scan,
two-pointer sweep, greedy proof, or interval merge.

Do not reject sorting just because `O(N)` sounds theoretically better. A clean `O(N log N)` solution
is often the right engineering/interview choice at `N = 100,000`.

## `O(N²)` — every item interacts with many others

Pair enumeration, 2D state over two sequence positions, and simple DP transitions often land here.

At `N = 1,000`, this may be fine. At `N = 100,000`, it is usually a clue that you are recomputing or
comparing far too much.

## `O(2^N)` — every subset

Each item contributes a binary decision: include/exclude. This is natural for subset enumeration,
some backtracking, and bitmask DP.

At `N = 20`, about one million subsets is plausible. At `N = 50`, it is not without a stronger idea
such as meet-in-the-middle.

## `O(N!)` — every ordering

Permutations explode faster than subsets. Backtracking survives only for small N or when constraints
prune most branches early.

## Complexity questions to ask before implementation

```text
What work repeats?
Can I remember it?
Can I maintain it incrementally?
Can I sort once instead of scanning repeatedly?
Can I eliminate half the search space each decision?
Can each element enter/leave a data structure at most once?
Can I define a state so I solve each subproblem once?
```

Those questions map directly to hash tables, windows, sorting/two pointers, binary search,
monotonic structures, and dynamic programming.

## Space is part of the trade-off

Speedups frequently buy memory:

- hash table: remember seen values;
- prefix sum: store cumulative results;
- BFS: store frontier + visited;
- DP: store solved states;
- trie: store shared prefixes explicitly.

The best solution is not “lowest time complexity at any cost.” It is the simplest approach that fits
both the time and memory constraints and whose correctness you can defend.
