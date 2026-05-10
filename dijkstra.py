import heapq

def dijkstra(graph, source):
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    heap = [(0, source)]

    while heap:
        current_dist, u = heapq.heappop(heap)

        if current_dist > distances[u]:
            continue

        for v, weight in graph[u]:
            new_dist = distances[u] + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                heapq.heappush(heap, (new_dist, v))

    return distances