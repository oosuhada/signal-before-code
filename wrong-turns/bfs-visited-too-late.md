# Wrong Turn: Marking BFS Visited on Dequeue

If a node is marked visited only after it leaves the queue, several parents can enqueue the same
node before that happens.

```text
A → C
B → C
```

When both A and B are processed, C may be inserted twice. In dense graphs that duplication can grow
dramatically.

For ordinary BFS, mark a node visited when it is **enqueued**. That makes “in the queue” part of the
already-discovered state and preserves the one-enqueue invariant.
