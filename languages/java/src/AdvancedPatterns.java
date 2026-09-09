import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class AdvancedPatterns {
    private AdvancedPatterns() {}

    public static int[] nextGreaterValues(int[] values) {
        int[] answer = new int[values.length];
        java.util.Arrays.fill(answer, -1);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < values.length; i++) {
            while (!stack.isEmpty() && values[stack.peek()] < values[i]) {
                answer[stack.pop()] = values[i];
            }
            stack.push(i);
        }
        return answer;
    }

    public static int[] slidingMaximum(int[] values, int k) {
        int[] result = new int[values.length - k + 1];
        Deque<Integer> deque = new ArrayDeque<>();
        for (int i = 0; i < values.length; i++) {
            while (!deque.isEmpty() && deque.peekFirst() <= i - k) deque.removeFirst();
            while (!deque.isEmpty() && values[deque.peekLast()] <= values[i]) deque.removeLast();
            deque.addLast(i);
            if (i >= k - 1) result[i - k + 1] = values[deque.peekFirst()];
        }
        return result;
    }

    public static final class Trie {
        private static final class Node {
            Map<Character, Node> children = new HashMap<>();
            boolean terminal;
        }

        private final Node root = new Node();

        public void insert(String word) {
            Node node = root;
            for (char ch : word.toCharArray()) {
                node = node.children.computeIfAbsent(ch, ignored -> new Node());
            }
            node.terminal = true;
        }

        public boolean contains(String word) {
            Node node = root;
            for (char ch : word.toCharArray()) {
                node = node.children.get(ch);
                if (node == null) return false;
            }
            return node.terminal;
        }
    }

    public static int countSetBits(int value) {
        int count = 0;
        while (value != 0) {
            value &= value - 1;
            count++;
        }
        return count;
    }

    public static List<List<Integer>> subsetsByMask(int[] values) {
        List<List<Integer>> result = new ArrayList<>();
        for (int mask = 0; mask < (1 << values.length); mask++) {
            List<Integer> subset = new ArrayList<>();
            for (int i = 0; i < values.length; i++) {
                if ((mask & (1 << i)) != 0) subset.add(values[i]);
            }
            result.add(subset);
        }
        return result;
    }
}
