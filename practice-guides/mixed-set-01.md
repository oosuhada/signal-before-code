# Mixed Recognition Set 01

This is textbook practice, not personal evidence. Categories are intentionally hidden.

For each item, write two candidate patterns and the deciding signal before opening the answer.

1. [`leetcode-560`](https://leetcode.com/problems/subarray-sum-equals-k/) — negative values are
   allowed; count contiguous ranges whose sum equals a target.
2. [`leetcode-875`](https://leetcode.com/problems/koko-eating-bananas/) — find the minimum rate that
   completes all work before a deadline.
3. [`leetcode-994`](https://leetcode.com/problems/rotting-oranges/) — multiple starting cells spread
   to neighbors one minute per step.
4. [`leetcode-435`](https://leetcode.com/problems/non-overlapping-intervals/) — remove as few ranges
   as possible to leave no overlaps.
5. [`leetcode-739`](https://leetcode.com/problems/daily-temperatures/) — find the next warmer position
   for each day.
6. [`leetcode-416`](https://leetcode.com/problems/partition-equal-subset-sum/) — determine whether a
   subset reaches exactly half of a total.

<details>
<summary>Review only after classification</summary>

1. Prefix sum + hash: negative values make ordinary positive-sum shrinking-window logic unsafe.
2. Binary search on answer: feasibility is monotonic in the processing rate.
3. Multi-source BFS: equal-time layers spread from all initial sources simultaneously.
4. Interval greedy: sorting by finish time exposes the choice that preserves future room.
5. Monotonic stack: unresolved earlier temperatures are finalized by the first greater value.
6. Knapsack-style DP: subset sum uses bounded target capacity as the state dimension.

</details>
