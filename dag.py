# Representation : Adjacency List
# Time complexity : O(V + E)
# Space complexity: O(V + E)

def dag_shortest_path(graph, source):
    # Step 1: Topological sort via DFS
    visited = set()
    topo_order = []

    def dfs(u):
        visited.add(u)
        for v, _ in graph[u]:
            if v not in visited:
                dfs(v)
        topo_order.append(u)

    for node in graph:
        if node not in visited:
            dfs(node)

    topo_order.reverse()  # reverse post-order = topological order

    # Step 2: Relax edges in topological order
    distances = {node: float('inf') for node in graph}
    distances[source] = 0

    for u in topo_order:
        if distances[u] == float('inf'):
            continue
        for v, weight in graph[u]:
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight

    return distances