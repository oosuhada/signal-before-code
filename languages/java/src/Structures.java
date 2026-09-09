import java.util.ArrayList;
import java.util.List;

public final class Structures {
    private Structures() {}

    public static final class ListNode {
        int value;
        ListNode next;

        ListNode(int value) {
            this.value = value;
        }
    }

    public static final class TreeNode {
        int value;
        TreeNode left;
        TreeNode right;

        TreeNode(int value) {
            this.value = value;
        }
    }

    public static ListNode reverseList(ListNode head) {
        ListNode previous = null;
        ListNode current = head;
        while (current != null) {
            ListNode next = current.next;
            current.next = previous;
            previous = current;
            current = next;
        }
        return previous;
    }

    public static boolean isValidBst(TreeNode root) {
        return valid(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    private static boolean valid(TreeNode node, long low, long high) {
        if (node == null) return true;
        if (node.value <= low || node.value >= high) return false;
        return valid(node.left, low, node.value) && valid(node.right, node.value, high);
    }

    public static long factorial(int n) {
        if (n < 0) throw new IllegalArgumentException("n must be nonnegative");
        if (n <= 1) return 1L;
        return n * factorial(n - 1);
    }

    public static List<List<Integer>> subsets(int[] values) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(values, 0, new ArrayList<>(), result);
        return result;
    }

    private static void backtrack(
            int[] values, int index, List<Integer> path, List<List<Integer>> result) {
        if (index == values.length) {
            result.add(new ArrayList<>(path));
            return;
        }
        path.add(values[index]);
        backtrack(values, index + 1, path, result);
        path.remove(path.size() - 1);
        backtrack(values, index + 1, path, result);
    }
}
