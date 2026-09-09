# Case Study — Dependency Graphs: Traversal vs Topological Order

## Verified remote-main artifact

`dev-flow-dashboard/frontend/src/graphModel.ts`, blob
`f44bf41727de15d8816b1df666b6a7c3118a7f37`, builds dependency/downstream adjacency and performs a
queue + visited traversal to collect downstream pull requests.

That is a graph-traversal problem: **which nodes are reachable downstream?** It is not a topological
sort.

## Local-only observation

The local `agentic-ontology-dashboard` snapshot at commit
`35dc61aa625301cef1daa5b6cdb9b7783cc5927d` contains
`api/ontology_dashboard/analysis_service.py::_topological_order`. It constructs indegrees, starts a
`deque` with zero-indegree nodes, releases outgoing dependencies, and rejects a graph when the number
of emitted nodes is smaller than the number of nodes.

The local branch is `main...origin/main [ahead 81, behind 908]`, and that file currently returns 404
from GitHub default-branch contents API. Therefore this repository records the observation but does
**not** present a GitHub `main` source link as verified evidence.

## Same-looking data, different question

```text
dependency graph
├─ “what can this PR affect downstream?” → traversal
└─ “in what order can these analysis nodes run?” → topological sort
```

## Why not DFS for everything?

DFS can answer reachability and can implement a topological order with postorder/cycle coloring. But
Kahn's indegree version makes “ready because no prerequisites remain” explicit, which maps naturally
to schedulable work queues.

## Why not Union-Find?

Union-Find forgets direction and ordering. It can answer whether undirected components have merged;
it cannot preserve “A must precede B.”
