# Applied Algorithm Defense

These case studies connect textbook selection questions to verified engineering artifacts. They are
not claims that production systems should literally use interview implementations.

| Case | Engineering question | Main lesson |
| --- | --- | --- |
| [Priority selection](priority-selection.md) | heap or scan? | repeated extrema are not enough; candidate count and rescoring matter |
| [Dependency graphs](dependency-graphs.md) | traversal or topo order? | the query asked of the graph chooses the algorithm |
| [Reliable queue](reliable-queue.md) | what does FIFO omit? | production queues add ownership, capacity, durability, recovery |
| [Cache keys](cache-keys.md) | hash map or database? | the lookup idea transfers; the storage mechanism may not |
| [Ranked search](ranked-search.md) | sort all or maintain top-K? | output requirement changes the selection structure |

Remote-main file SHAs were checked with authenticated `gh api` on 2026-09-09. The one
`agentic-ontology-dashboard` observation is explicitly local-only because its working `main` snapshot
is heavily diverged from `origin/main` and the relevant file is not currently on GitHub default
branch.
