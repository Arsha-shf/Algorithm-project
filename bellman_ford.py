def bellman_ford(edge_list, num_nodes, source):
    distances = {i: float('inf') for i in range(num_nodes)}
    distances[source] = 0

    for _ in range(num_nodes - 1):
        updated = False
        for u, v, weight in edge_list:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                updated = True
        if not updated:
            break  

    for u, v, weight in edge_list:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            return None 

    return distances