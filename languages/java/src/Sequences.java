import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;

public final class Sequences {
    private Sequences() {}

    public static boolean containsDuplicate(int[] values) {
        Set<Integer> seen = new HashSet<>();
        for (int value : values) {
            if (!seen.add(value)) return true;
        }
        return false;
    }

    public static int[] twoSumSorted(int[] values, int target) {
        int left = 0;
        int right = values.length - 1;
        while (left < right) {
            long sum = (long) values[left] + values[right];
            if (sum == target) return new int[] {left, right};
            if (sum < target) left++;
            else right--;
        }
        return new int[] {-1, -1};
    }

    public static int longestAtMostKDistinct(String text, int k) {
        Map<Character, Integer> count = new HashMap<>();
        int left = 0;
        int best = 0;
        for (int right = 0; right < text.length(); right++) {
            char added = text.charAt(right);
            count.merge(added, 1, Integer::sum);
            while (count.size() > k) {
                char removed = text.charAt(left++);
                int remaining = count.get(removed) - 1;
                if (remaining == 0) count.remove(removed);
                else count.put(removed, remaining);
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static boolean balancedBrackets(String text) {
        Map<Character, Character> pair = Map.of(')', '(', ']', '[', '}', '{');
        Deque<Character> stack = new ArrayDeque<>();
        for (char ch : text.toCharArray()) {
            if (ch == '(' || ch == '[' || ch == '{') stack.push(ch);
            else if (pair.containsKey(ch)) {
                if (stack.isEmpty() || stack.pop() != pair.get(ch)) return false;
            }
        }
        return stack.isEmpty();
    }

    public static int binarySearch(int[] values, int target) {
        int left = 0;
        int right = values.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (values[mid] == target) return mid;
            if (values[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }

    public static List<Integer> kSmallest(int[] values, int k) {
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        for (int value : values) heap.add(value);
        List<Integer> result = new ArrayList<>();
        for (int i = 0; i < k && !heap.isEmpty(); i++) result.add(heap.remove());
        return result;
    }
}
