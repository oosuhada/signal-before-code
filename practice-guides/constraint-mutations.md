# Constraint Mutation Drill

Keep the problem statement fixed and change only scale. The point is to **remove approaches**, not to
guess a pattern from `N` alone.

| Mutation | First question |
| --- | --- |
| `N <= 20` | can exponential subset/backtracking state fit? |
| `N <= 200` | is `O(N^3)` plausible for the actual language/time limit? |
| `N <= 2,000` | does `O(N^2)` fit memory and constants? |
| `N <= 200,000` | which quadratic candidates must disappear? |
| `N <= 1,000,000` | can the solution stay close to linear and memory-conscious? |

## Drill

Take “find the best pair under a relation.” At `N=20`, brute force is useful as a correctness
baseline. At `N=200,000`, pair enumeration is a warning sign; now look for sorting, hashing,
monotonicity, or another structure. The constraints changed the **budget**, not the semantic proof.
