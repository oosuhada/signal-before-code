# Visual Trace — Dynamic Programming

Start with the **meaning of a cell**, not the recurrence.

```text
dp[i] = Fibonacci(i)

dp[0] = 0
dp[1] = 1
dp[2] = dp[1] + dp[0] = 1
dp[3] = dp[2] + dp[1] = 2
```

The 2D demo uses:

```text
dp[r][c] = number of right/down paths from the start to (r,c)

 1  1  1
 1  2  3
 1  3  6
```

Each cell may be filled only after the states it references already have a fixed meaning.

```bash
python3 scripts/trace.py dp --predict
python3 scripts/trace.py dp-grid --step
```
