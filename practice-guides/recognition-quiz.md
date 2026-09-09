# Pattern Recognition Quiz

Do not open the answer section until you have written at least two candidates and one rejection.

## Questions

### Q1

`N = 200,000`. A sorted array contains positive integers. Determine whether any pair sums to a
target.

- What signals matter?
- What candidates survive the constraint?
- What property lets you discard candidates safely?

### Q2

A service receives jobs over time. Repeatedly execute the waiting job with the smallest deadline;
new jobs can arrive between executions.

- Why is sorting once not enough?
- What structure should be a candidate?

### Q3

Given course prerequisites, return an order that satisfies every prerequisite or report that no such
order exists.

- What graph property is central?
- Which algorithm both produces an order and detects impossibility?

### Q4

Find the minimum truck capacity that can ship all packages within D days. If capacity X works, every
larger capacity also works.

- What is the actual search space?
- What one predicate would you write first?

### Q5

Find the longest substring containing at most K distinct characters.

- What is the changing state?
- Why can one boundary move only forward?

### Q6

An undirected network receives `union(a, b)` operations and thousands of `connected(a, b)` queries.
No path itself is required.

- Why might repeated BFS be wasteful?
- What information can be remembered permanently?

### Q7

You may choose or skip each of 18 features. Find the best valid subset under a compatibility rule.

- Which constraint gives permission for exponential work?
- Backtracking or bitmask: what detail would decide?

### Q8

Each cell in a grid has a non-negative movement cost. Find the least total cost from the start to the
target.

- Why is ordinary BFS not automatically correct?
- Which frontier ordering matters?

## Answers

1. Two pointers is the primary candidate: sorted order makes the sum monotonic when either endpoint
   moves. Hashing also works but gives up the existing order and uses extra memory.
2. Heap / priority queue: the candidate set changes between extractions, so dynamic repeated minimum
   selection matters.
3. Topological sort; Kahn's algorithm exposes a cycle when fewer than all nodes can be removed.
4. Binary search on answer. Predicate: “can ship within D days using capacity C?”
5. Variable sliding window with a frequency map; shrink while distinct-count exceeds K.
6. Union-Find stores component representatives across updates.
7. `N = 18` makes `2^N` plausible. Bitmask suits direct subset iteration; backtracking suits strong
   pruning or construction constraints.
8. Dijkstra; the frontier must be ordered by accumulated path cost, not edge count.
