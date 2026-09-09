# BFS vs Dijkstra

## Same-looking problem

Both answer shortest-path questions.

## What changes?

The edge costs.

```text
A --1--> B --10--> D
 \------5--------> D
```

BFS counts edges and prefers `A → D` because it is one edge. If edge weight matters, that path costs
5 while `A → B → D` costs 11. In a different graph the fewer-edge path can be *more* expensive.

## Deciding signal

- all edges equal cost → BFS layers are distance layers;
- non-negative arbitrary weights → Dijkstra orders the frontier by best known distance;
- weights only 0 or 1 → 0-1 BFS is a specialized candidate;
- negative edges → ordinary Dijkstra's settled-node assumption is unsafe.

The key distinction is what “closest frontier item” means: hop count or accumulated weight.
