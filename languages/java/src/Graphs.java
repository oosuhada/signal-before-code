import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Deque;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Queue;

public final class Graphs {
    private Graphs() {}

    public static List<List<Integer>> adjacencyList(int n, int[][] edges) {
        List<List<Integer>> graph = new ArrayList<>();
        for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
        for (int[] edge : edges) {
            graph.get(edge[0]).add(edge[1]);
            graph.get(edge[1]).add(edge[0]);
        }
        return graph;
    }

    public static int[] bfsDistances(List<List<Integer>> graph, int start) {
        int[] distance = new int[graph.size()];
        Arrays.fill(distance, -1);
        Queue<Integer> queue = new ArrayDeque<>();
        distance[start] = 0;
        queue.add(start);
        while (!queue.isEmpty()) {
            int node = queue.remove();
            for (int next : graph.get(node)) {
                if (distance[next] != -1) continue;
                distance[next] = distance[node] + 1;
                queue.add(next);
            }
        }
        return distance;
    }

    public static List<Integer> dfsOrder(List<List<Integer>> graph, int start) {
        boolean[] visited = new boolean[graph.size()];
        Deque<Integer> stack = new ArrayDeque<>();
        List<Integer> order = new ArrayList<>();
        stack.push(start);
        while (!stack.isEmpty()) {
            int node = stack.pop();
            if (visited[node]) continue;
            visited[node] = true;
            order.add(node);
            List<Integer> neighbors = graph.get(node);
            for (int i = neighbors.size() - 1; i >= 0; i--) stack.push(neighbors.get(i));
        }
        return order;
    }

    public static final class UnionFind {
        private final int[] parent;
        private final int[] size;

        public UnionFind(int n) {
            parent = new int[n];
            size = new int[n];
            for (int i = 0; i < n; i++) {
                parent[i] = i;
                size[i] = 1;
            }
        }

        public int find(int x) {
            if (parent[x] != x) parent[x] = find(parent[x]);
            return parent[x];
        }

        public boolean union(int a, int b) {
            int rootA = find(a);
            int rootB = find(b);
            if (rootA == rootB) return false;
            if (size[rootA] < size[rootB]) {
                int temporary = rootA;
                rootA = rootB;
                rootB = temporary;
            }
            parent[rootB] = rootA;
            size[rootA] += size[rootB];
            return true;
        }
    }

    public static List<Integer> topologicalOrder(int n, int[][] edges) {
        List<List<Integer>> graph = new ArrayList<>();
        for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
        int[] indegree = new int[n];
        for (int[] edge : edges) {
            graph.get(edge[0]).add(edge[1]);
            indegree[edge[1]]++;
        }
        Queue<Integer> ready = new ArrayDeque<>();
        for (int node = 0; node < n; node++) if (indegree[node] == 0) ready.add(node);
        List<Integer> order = new ArrayList<>();
        while (!ready.isEmpty()) {
            int node = ready.remove();
            order.add(node);
            for (int next : graph.get(node)) if (--indegree[next] == 0) ready.add(next);
        }
        return order.size() == n ? order : List.of();
    }

    public static long[] dijkstra(List<List<int[]>> graph, int start) {
        long[] distance = new long[graph.size()];
        Arrays.fill(distance, Long.MAX_VALUE);
        PriorityQueue<long[]> heap = new PriorityQueue<>(Comparator.comparingLong(item -> item[0]));
        distance[start] = 0L;
        heap.add(new long[] {0L, start});
        while (!heap.isEmpty()) {
            long[] current = heap.remove();
            long dist = current[0];
            int node = (int) current[1];
            if (dist != distance[node]) continue;
            for (int[] edge : graph.get(node)) {
                int next = edge[0];
                long candidate = dist + edge[1];
                if (candidate >= distance[next]) continue;
                distance[next] = candidate;
                heap.add(new long[] {candidate, next});
            }
        }
        return distance;
    }
}
