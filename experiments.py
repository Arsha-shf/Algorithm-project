import time
from dijkstra import dijkstra
from bellman_ford import bellman_ford
from dag import dag_shortest_path
from graph_data import to_edge_list


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _time_it(func, *args):
    start = time.perf_counter()
    result = func(*args)
    return result, time.perf_counter() - start

def graph_stats(graph):
    nodes = len(graph)
    edges = sum(len(v) for v in graph.values())
    return nodes, edges


# ─────────────────────────────────────────────
# FAIR COMPARISON — same graph, all three
# Only valid on Graph A (DAG, non-negative)
# ─────────────────────────────────────────────

def run_fair_comparison(graph, label="graph"):
    source = 0
    nodes, edges = graph_stats(graph)
    edge_list = to_edge_list(graph)

    d_result,   d_time  = _time_it(dijkstra,          graph,     source)
    bf_result,  bf_time = _time_it(bellman_ford,       edge_list, nodes, source)
    dag_result, dag_time= _time_it(dag_shortest_path,  graph,     source)

    return {
        "label": label, "nodes": nodes, "edges": edges,
        "dijkstra":     {"time": d_time,   "distances": d_result},
        "bellman_ford": {"time": bf_time,  "distances": bf_result},
        "dag":          {"time": dag_time, "distances": dag_result},
    }


# ─────────────────────────────────────────────
# CAPABILITY TEST — different graph types
# Shows which algorithms fail and why
# ─────────────────────────────────────────────

def run_capability_test(graph, scenario_name):
    source = 0
    nodes, edges = graph_stats(graph)
    edge_list = to_edge_list(graph)
    results = {"scenario": scenario_name, "nodes": nodes, "edges": edges}

    # Dijkstra — fails on negative edges
    if scenario_name == "C":
        results["dijkstra"] = {
            "time": None, "distances": None,
            "note": "not applicable — negative edges break greedy assumption"
        }
    else:
        r, t = _time_it(dijkstra, graph, source)
        results["dijkstra"] = {"time": t, "distances": r, "note": "ok"}

    # Bellman-Ford — always valid
    r, t = _time_it(bellman_ford, edge_list, nodes, source)
    if r is None:
        results["bellman_ford"] = {
            "time": t, "distances": None,
            "note": "negative cycle detected — no valid solution"
        }
    else:
        results["bellman_ford"] = {"time": t, "distances": r, "note": "ok"}

    # DAG — fails on cyclic graphs
    if scenario_name == "B":
        results["dag"] = {
            "time": None, "distances": None,
            "note": "not applicable — topological sort undefined on cyclic graphs"
        }
    else:
        r, t = _time_it(dag_shortest_path, graph, source)
        results["dag"] = {"time": t, "distances": r, "note": "ok"}

    return results


# ─────────────────────────────────────────────
# SCALABILITY TEST — growing input size
# ─────────────────────────────────────────────

def run_scalability_test(generate_func, sizes, scenario_name="A"):
    records = []
    for n in sizes:
        graph = generate_func(n)
        edge_list = to_edge_list(graph)
        source = 0
        nodes, edges = graph_stats(graph)
        row = {"n": n, "nodes": nodes, "edges": edges}

        row["dijkstra_time"]    = _time_it(dijkstra, graph, source)[1]          if scenario_name != "C" else None
        row["bellman_ford_time"]= _time_it(bellman_ford, edge_list, nodes, source)[1]
        row["dag_time"]         = _time_it(dag_shortest_path, graph, source)[1] if scenario_name != "B" else None

        records.append(row)
    return records