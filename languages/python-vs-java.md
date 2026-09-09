# Python → Java Algorithm Transfer

The algorithm does not change when the language changes. The implementation hazards do.

## Translation table

| Reasoning role | Python | Java | Interview friction |
| --- | --- | --- | --- |
| key → value | `dict` | `HashMap<K,V>` | boxed generics; `getOrDefault` / `merge` |
| membership | `set` | `HashSet<T>` | boxed primitives |
| FIFO frontier | `collections.deque` | `ArrayDeque<T>` | use `addLast/removeFirst`; avoid `Stack` |
| LIFO worklist | `list`/`deque` | `ArrayDeque<T>` | `push/pop` or explicit ends |
| min priority | `heapq` | `PriorityQueue<T>` | comparator and custom record/class |
| dynamic list | `list` | `ArrayList<T>` | primitive values become boxed in generics |
| integer | arbitrary precision | `int` / `long` | overflow is part of correctness |

## Preserve the invariant first

When translating binary search, do not begin by converting syntax. Begin with:

> If the target exists, it remains inside the chosen search interval.

Then choose one interval convention in Java and keep it consistent. The same applies to BFS's
frontier, Dijkstra's finalized distances, or DP's state definition.

## Java hazards worth saying out loud

### `int` vs `long`

Python hides most integer overflow. Java does not. Pair sums, prefix sums, distances, and products
should use `long` whenever the maximum mathematical value can exceed roughly 2.1 billion. Casting
*after* an `int + int` overflow is too late; promote before the operation.

### Primitive vs boxed types

`HashMap<Integer, Integer>` and `PriorityQueue<Integer>` store objects, not primitive `int`s. This is
usually fine for interviews, but it explains extra allocation and why arrays are attractive for
small bounded integer domains.

### `PriorityQueue` comparator

Python tuples naturally compare lexicographically. Java custom state usually needs a comparator.
Prefer `Comparator.comparingLong(...)` over subtraction such as `a.cost - b.cost`, which can
overflow.

### `ArrayDeque`

Use it for both queue and stack behavior. For BFS, make the FIFO ends explicit. For DFS, `push/pop`
is readable. `ArrayDeque` does not allow `null`.

### Recursion depth

Python often hits its recursion limit early; Java has no language-level recursion limit but still
has a finite thread stack. A path-like graph with hundreds of thousands of nodes can overflow either
runtime. Iterative DFS is not merely a Python workaround.

### Arrays vs collections

When node IDs are dense `0..N-1`, primitive arrays (`int[]`, `boolean[]`, `long[]`) are simpler and
cheaper than maps. When IDs are sparse or semantic, maps may better reflect the problem.

## Canonical transfer set

[`java/catalog.json`](java/catalog.json) maps 29 canonical Java implementations to the 28 textbook
chapters. The examples live in [`java/src/`](java/src/) and are compiled by CI with Java 21.

Do not memorize both languages independently. Explain the invariant once, then notice which library
choice and numeric hazard changes during translation.
