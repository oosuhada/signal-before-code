# Wrong Turn: BFS on a Weighted Graph

## Temptation

“This is a shortest-path problem, and BFS finds shortest paths.”

## The missing assumption

BFS layers certify shortest distance only when every move has the same cost. With arbitrary edge
weights, “one more edge” is not “one more unit of distance.”

## Counterexample

```text
S --100--> A
 \--1--> B --1--> A
```

BFS can discover A directly in one edge, but cost 100 is worse than the two-edge path of cost 2.

## Repair

- equal weights → BFS;
- weights 0/1 → consider 0-1 BFS;
- non-negative weights → Dijkstra;
- negative weights → choose an algorithm whose correctness permits them.
