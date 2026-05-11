def dag_shortest_path(graph, source):
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

    topo_order.reverse()
    distances = {node: float('inf') for node in graph}
    distances[source] = 0

    for u in topo_order:
        if distances[u] == float('inf'):
            continue
        for v, weight in graph[u]:
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight

    return distances