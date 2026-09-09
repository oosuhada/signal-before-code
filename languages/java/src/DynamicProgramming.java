import java.util.Arrays;

public final class DynamicProgramming {
    private DynamicProgramming() {}

    public static long fibonacciMemoized(int n) {
        long[] memo = new long[n + 1];
        Arrays.fill(memo, -1L);
        return fibonacci(n, memo);
    }

    private static long fibonacci(int n, long[] memo) {
        if (n <= 1) return n;
        if (memo[n] != -1L) return memo[n];
        memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo);
        return memo[n];
    }

    public static long climbStairs(int n) {
        if (n <= 1) return 1L;
        long previousTwo = 1L;
        long previousOne = 1L;
        for (int step = 2; step <= n; step++) {
            long current = previousOne + previousTwo;
            previousTwo = previousOne;
            previousOne = current;
        }
        return previousOne;
    }

    public static int uniquePaths(int rows, int cols) {
        int[][] dp = new int[rows][cols];
        for (int row = 0; row < rows; row++) dp[row][0] = 1;
        for (int col = 0; col < cols; col++) dp[0][col] = 1;
        for (int row = 1; row < rows; row++) {
            for (int col = 1; col < cols; col++) {
                dp[row][col] = dp[row - 1][col] + dp[row][col - 1];
            }
        }
        return dp[rows - 1][cols - 1];
    }

    public static int zeroOneKnapsack(int[] weights, int[] values, int capacity) {
        int[] dp = new int[capacity + 1];
        for (int item = 0; item < weights.length; item++) {
            for (int remaining = capacity; remaining >= weights[item]; remaining--) {
                dp[remaining] = Math.max(
                        dp[remaining], dp[remaining - weights[item]] + values[item]);
            }
        }
        return dp[capacity];
    }

    public static int lisLength(int[] values) {
        int[] tails = new int[values.length];
        int size = 0;
        for (int value : values) {
            int left = 0;
            int right = size;
            while (left < right) {
                int mid = left + (right - left) / 2;
                if (tails[mid] < value) left = mid + 1;
                else right = mid;
            }
            tails[left] = value;
            if (left == size) size++;
        }
        return size;
    }
}
