# Code-less Reasoning Drills

These drills stop **before implementation**. Speak or write only constraints, candidate approaches,
complexity, invariant, and rejection reasons.

## Drill format

For each prompt, answer in this order:

1. What fact in the constraints changes the candidate set?
2. What brute-force approach gives a correctness baseline?
3. Which two patterns remain plausible?
4. What invariant would make each one correct?
5. Which candidate do you reject, and why?
6. What mutation would reverse that decision?

## Prompts

### 1 — Delivery network

An undirected network has 100,000 vertices. Every edge costs exactly one unit. Return minimum hop
count from one source to all reachable vertices.

### 2 — Same network, new cost model

The topology is unchanged, but every edge now has a nonnegative travel time from 1 to 10,000.

### 3 — Capacity planning

You can test whether a capacity `C` finishes all work before a deadline in O(n). If `C` works, every
larger capacity works. Find the smallest valid capacity.

### 4 — Dynamic teams

There are 200,000 users and 300,000 online operations. Operations either merge two teams or ask
whether two users are currently in the same team.

### 5 — Static analytics

An immutable array receives 500,000 range-sum queries.

### 6 — Analytics becomes mutable

The same array now receives point updates between range queries.

### 7 — Streaming top K

Events arrive one at a time. At any moment, report the 20 largest scores seen so far; full sorted
history is never requested.

### 8 — Full report

The same scores are all known upfront and the final requirement is to output every score in sorted
order once.

### 9 — Workflow dependencies

Tasks form a directed prerequisite graph. Return a legal execution order or report that the
dependencies contain a cycle.

### 10 — Sequence with negative values

Find a shortest contiguous subarray satisfying a sum threshold, but values may be negative.

The goal is not to name an algorithm quickly. The goal is to state exactly which assumption makes
one candidate valid and a neighbor invalid.
