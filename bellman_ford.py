# Representation : Edge List  →  [(u, v, weight), ...]
# Time complexity : O(V * E)
# Space complexity: O(V + E)

def bellman_ford(edge_list, num_nodes, source):
    distances = {i: float('inf') for i in range(num_nodes)}
    distances[source] = 0

    # Relax all edges (V-1) times
    for _ in range(num_nodes - 1):
        updated = False
        for u, v, weight in edge_list:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                updated = True
        if not updated:
            break  # early exit — nothing changed

    # Negative cycle check
    for u, v, weight in edge_list:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            return None  # negative cycle detected

    return distances