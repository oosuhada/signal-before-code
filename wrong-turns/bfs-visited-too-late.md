# Wrong Turn — marking BFS visited only when dequeued

## Tempting idea

Mark a node visited when it is removed from the queue because that is when it is “actually visited.”

## Why it looks reasonable

DFS examples often blur discovery and processing. In BFS, however, multiple frontier nodes may
discover the same neighbor before that neighbor reaches the front of the queue.

## Smallest counterexample

```text
A → B → D
└→ C → D
```

## Step-by-step failure

`A` enqueues `B,C`. `B` enqueues `D`, but `D` is still unmarked. `C` also enqueues `D`. The queue
contains two copies, growing redundant work and possibly duplicating parent/state effects.

## Correct signal

When one discovery is sufficient, mark visited **when enqueuing** so discovered state enters the
frontier at most once.

## Better candidates

Standard BFS with discovery-time marking. Some specialized algorithms intentionally revisit state,
but they need an explicit reason rather than accidental duplicates.

## General lesson

Ask when ownership of a state is established: discovery, enqueue, dequeue, or finalization are not
interchangeable events.
