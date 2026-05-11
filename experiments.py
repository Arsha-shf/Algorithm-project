import time
from dijkstra import dijkstra
from bellman_ford import bellman_ford
from dag_shp import dag_shortest_path
from graph_data import to_edge_list


def _time_it(func, *args):
    start = time.perf_counter()
    result = func(*args)
    return result, time.perf_counter() - start

def graph_stats(graph):
    nodes = len(graph)
    edges = sum(len(v) for v in graph.values())
    return nodes, edges

def fmt(t):
    """Format time in scientific notation: 4.2 × 10⁻⁵ s"""
    if t is None:
        return "N/A"
    exp = 0
    val = t
    if val > 0:
        import math
        exp = int(math.floor(math.log10(val)))
        val = t / (10 ** exp)
    superscripts = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    exp_str = str(exp).translate(superscripts)
    return f"{val:.1f} × 10{exp_str} s"

def run_fair_comparison(graph, label):
    source = 0
    nodes, edges = graph_stats(graph)
    edge_list = to_edge_list(graph)

    d_result,  d_time  = _time_it(dijkstra,         graph,     source)
    bf_result, bf_time = _time_it(bellman_ford,      edge_list, nodes, source)
    dg_result, dg_time = _time_it(dag_shortest_path, graph,     source)

    return {
        "label": label, "nodes": nodes, "edges": edges,
        "dijkstra":     {"time": d_time,  "distances": d_result},
        "bellman_ford": {"time": bf_time, "distances": bf_result},
        "dag_shp":          {"time": dg_time, "distances": dg_result},
    }

def run_capability_test(graph, scenario_name):
    source = 0
    nodes, edges = graph_stats(graph)
    edge_list = to_edge_list(graph)
    res = {"scenario": scenario_name, "nodes": nodes, "edges": edges}


    if scenario_name in ("C", "D"):
        res["dijkstra"] = {"time": None, "distances": None,
                        "note": "✗ failed — negative edges present"}
    else:
        r, t = _time_it(dijkstra, graph, source)
        res["dijkstra"] = {"time": t, "distances": r, "note": "✓ valid"}


    r, t = _time_it(bellman_ford, edge_list, nodes, source)
    if r is None:
        res["bellman_ford"] = {"time": t, "distances": None,
                            "note": "✗ failed — negative cycle detected"}
    elif scenario_name == "D":
        res["bellman_ford"] = {"time": t, "distances": r,
                            "note": "✓ only valid algorithm"}
    else:
        res["bellman_ford"] = {"time": t, "distances": r, "note": "✓ valid"}

    if scenario_name in ("B", "D"):
        res["dag_shp"] = {"time": None, "distances": None,
                    "note": "✗ failed — cycles present"}
    else:
        r, t = _time_it(dag_shortest_path, graph, source)
        res["dag_shp"] = {"time": t, "distances": r, "note": "✓ valid"}

    return res


def run_scalability_test(generate_func, sizes, scenario_name):
    records = []
    for n in sizes:
        graph = generate_func(n)
        edge_list = to_edge_list(graph)
        source = 0
        nodes, edges = graph_stats(graph)
        row = {"n": n, "nodes": nodes, "edges": edges}

        row["dijkstra_time"]     = _time_it(dijkstra,         graph,     source)[1] if scenario_name not in ("C", "D") else None
        row["bellman_ford_time"] = _time_it(bellman_ford,      edge_list, nodes, source)[1]
        row["dag_shp_time"]          = _time_it(dag_shortest_path, graph,     source)[1] if scenario_name not in ("B", "D") else None

        records.append(row)
    return records