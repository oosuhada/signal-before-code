# Mixed Set 01 — review

Open this only after attempting [`../set-01.md`](../set-01.md).

| Problem | Main signal | Candidate family to defend | Common tempting alternative |
| --- | --- | --- | --- |
| Two Sum II | sorted pair relation; moving an extreme changes sum monotonically | two pointers | hash complement lookup |
| Number of Islands | implicit grid graph; consume one connected component at a time | BFS or DFS | repeated local checks without visited state |
| 완주하지 못한 선수 | repeated name multiplicity / unmatched key | frequency hash map or sorting | membership-only set that loses duplicate counts |
| Container With Most Water | objective limited by shorter boundary; width only decreases | two pointers with a proof for boundary elimination | enumerate all pairs |
| Rotting Oranges | equal-time spread from many starting sources | multi-source BFS | one BFS per source / DFS timing |
| Group Anagrams | canonical representation can become a grouping key | hash map from signature → group | pairwise string comparison |

The review label is secondary. The main question is whether the signal was recognized **before** the
implementation was known.
