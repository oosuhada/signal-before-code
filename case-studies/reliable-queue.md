# Case Study — A Production Queue Is More Than FIFO

## Verified artifact

`browser-reliability-runtime/src/local-llm/queue.ts`, remote-main blob
`4cabba6324b5c67d936a119d72e8958f782951d4`.

The source has `pending/running/blocked/completed/failed` states, an optional pending limit, atomic
temporary-file publication, `rename`-based claim ownership, and stale-running recovery.

## Textbook bridge

A coding-test queue usually asks only:

```text
who arrived first?
```

The production system must also ask:

```text
who owns this job?
can another worker claim it?
what if a worker dies?
can producers overload the pending set?
can readers observe a partial write?
```

The FIFO intuition transfers, but correctness now includes concurrency and durability invariants.

## Why not an in-memory `deque`?

An in-memory deque cannot survive process restart or coordinate claim ownership through filesystem
state. It would solve ordering while ignoring persistence/recovery requirements.

## Why not a heap?

No evidence here says priority order is the primary requirement. Replacing queue semantics with a
heap would change fairness/order and still would not solve atomic ownership or recovery.
