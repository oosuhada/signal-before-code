# Wrong Turn — Forcing a topological order through a cycle

## Tempting idea
Dependencies imply topological sort, so keep removing “some” node until an order appears.

## Why it looks reasonable
Most course-schedule examples are DAGs, making acyclicity feel implicit.

## Smallest counterexample
`A→B`, `B→A`.

## Step-by-step failure
Both nodes have indegree 1. The ready queue is empty from the start. Picking either anyway violates a
prerequisite; no linear order can satisfy both edges.

## Correct signal
Topological ordering requires a DAG. Processed-count `< node-count` is evidence of a cycle.

## Better candidates
Cycle detection, SCC decomposition, or domain-specific conflict reporting.

## General lesson
When an algorithm stalls, ask whether the problem violated its existence condition.
