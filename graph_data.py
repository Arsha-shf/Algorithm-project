import random

# SMALL GRAPHS (manual)

# Graph A — clean DAG, non-negative weights
graph_A_small = {
    0:  [(1, 5), (2, 3), (3, 8)],
    1:  [(4, 2), (5, 6)],
    2:  [(4, 4), (5, 2), (6, 7)],
    3:  [(5, 3), (6, 4)],
    4:  [(7, 6), (8, 3)],
    5:  [(7, 2), (8, 5), (9, 4)],
    6:  [(8, 2), (9, 6)],
    7:  [(10, 3), (11, 7)],
    8:  [(10, 4), (11, 2), (12, 5)],
    9:  [(11, 3), (12, 4)],
    10: [(13, 6), (14, 3)],
    11: [(13, 2), (14, 5)],
    12: [(14, 4), (15, 7)],
    13: [(16, 3)],
    14: [(16, 2), (17, 6)],
    15: [(17, 3)],
    16: [(18, 4)],
    17: [(18, 2), (19, 5)],
    18: [(19, 1)],
    19: []
}

# Graph B — has cycles (back edges), non-negative weights
graph_B_small = {
    0:  [(1, 5), (2, 3), (3, 8)],
    1:  [(4, 2), (5, 6)],
    2:  [(4, 4), (5, 2), (6, 7)],
    3:  [(5, 3), (6, 4)],
    4:  [(7, 6), (8, 3)],
    5:  [(7, 2), (8, 5), (9, 4)],
    6:  [(8, 2), (9, 6)],
    7:  [(10, 3), (11, 7)],
    8:  [(10, 4), (11, 2), (12, 5)],
    9:  [(11, 3), (12, 4)],
    10: [(13, 6), (14, 3)],
    11: [(13, 2), (14, 5)],
    12: [(14, 4), (15, 7)],
    13: [(16, 3)],
    14: [(16, 2), (17, 6)],
    15: [(17, 3)],
    16: [(18, 4)],
    17: [(18, 2), (19, 5)],
    18: [(19, 1), (5, 3)],   # back edge → cycle
    19: [(0, 2)]             # back edge → cycle
}

# Graph C — has negative edges, no negative cycles
graph_C_small = {
    0:  [(1, 5), (2, 3), (3, 8)],
    1:  [(4, 2), (5, 6)],
    2:  [(4, 4), (5, 2), (6, 7)],
    3:  [(5, 3), (6, 4)],
    4:  [(7, 6), (8, 3)],
    5:  [(7, -2), (8, 5), (9, 4)],  # negative edge
    6:  [(8, 2), (9, 6)],
    7:  [(10, 3), (11, 7)],
    8:  [(10, 4), (11, 2), (12, 5)],
    9:  [(11, 3), (12, 4)],
    10: [(13, 6), (14, 3)],
    11: [(13, 2), (14, 5)],
    12: [(14, 4), (15, 7)],
    13: [(16, 3)],
    14: [(16, 2), (17, 6)],
    15: [(17, 3)],
    16: [(18, 4)],
    17: [(18, 2), (19, 5)],
    18: [(19, 1)],
    19: []
}


# Graph D — cycles + negative edges, NO negative cycle
graph_D_small = {
    0:  [(1, 5), (2, 3), (3, 8)],
    1:  [(4, 2), (5, 6)],
    2:  [(4, 4), (5, 2), (6, 7)],
    3:  [(5, 3), (6, 4)],
    4:  [(7, 6), (8, 3)],
    5:  [(7, -2), (8, 5), (9, 4)],  # negative edge
    6:  [(8, 2), (9, 6)],
    7:  [(10, 3), (11, 7)],
    8:  [(10, 4), (11, 2), (12, 5)],
    9:  [(11, 3), (12, 4)],
    10: [(13, 6), (14, 3)],
    11: [(13, 2), (14, 5)],
    12: [(14, 4), (15, 7)],
    13: [(16, 3)],
    14: [(16, 2), (17, 6)],
    15: [(17, 3)],
    16: [(18, 4)],
    17: [(18, 2), (19, 5)],
    18: [(19, 1), (5, 3)],   # back edge → cycle
    19: [(3, 2)]             # back edge → cycle
}

# EDGE LIST CONVERTER
# Used by Bellman-Ford
def to_edge_list(graph):
    edges = []
    for u in graph:
        for v, w in graph[u]:
            edges.append((u, v, w))
    return edges

# LARGE GRAPH GENERATORS

def generate_graph_A(n):
    """Clean DAG, non-negative weights — adjacency list."""
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, min(i + 6, n)):
            graph[i].append((j, random.randint(1, 10)))
    return graph

def generate_graph_B(n):
    """Has cycles (back edges) — adjacency list."""
    graph = generate_graph_A(n)
    for i in range(5, n, 10):
        back = random.randint(0, i - 1)
        graph[i].append((back, random.randint(1, 10)))
    return graph

def generate_graph_C(n):
    """Has negative edges, no negative cycles — adjacency list."""
    graph = generate_graph_A(n)
    for i in range(0, n - 5, 10):
        graph[i].append((i + 3, -random.randint(1, 5)))
    return graph

def generate_graph_D(n):
    """Cycles + negative edges, no negative cycle — adjacency list."""
    graph = generate_graph_C(n)  
    for i in range(5, n, 10):   
        back = random.randint(0, i - 1)
        graph[i].append((back, random.randint(1, 10)))  
    return graph