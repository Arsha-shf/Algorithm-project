from graph_data import (
    graph_A_small, graph_B_small, graph_C_small, graph_D_small,
    generate_graph_A, generate_graph_B, generate_graph_C, generate_graph_D
)
from experiments import (
    run_fair_comparison, run_capability_test,
    run_scalability_test, fmt
)

ALGOS = ["dijkstra", "bellman_ford", "dag_shp"]
SIZES = [10, 50, 100, 200, 500]

# PRINT HELPERS

def print_fair(res):
    print(f"\n  {res['label']} — n={res['nodes']}, edges={res['edges']}")
    print(f"  {'Algorithm':<16} {'Time'}")
    print(f"  {'─'*32}")
    for a in ALGOS:
        print(f"  {a:<16} {fmt(res[a]['time'])}")


def print_capability(res):
    scenario_labels = {
        "A": "Scenario A — acyclic, non-negative",
        "B": "Scenario B — cyclic, non-negative",
        "C": "Scenario C — acyclic, negative edges",
        "D": "Scenario D — cyclic, negative edges",
    }
    print(f"\n  {scenario_labels[res['scenario']]}")
    for a in ALGOS:
        e = res[a]
        t = fmt(e["time"]) if e["time"] is not None else "—"
        print(f"  {a:<16} {t:<18}  [{e['note']}]")

    # Correctness line — show which algorithms agree and on what distance
    valid = [(a, res[a]["distances"]) for a in ALGOS if res[a]["distances"] is not None]
    if valid:
        target = max(valid[0][1].keys())
        distances = {a: d[target] for a, d in valid}
        names = " & ".join(a for a, _ in valid)
        dist_val = list(distances.values())[0]
        all_agree = len(set(distances.values())) == 1
        if all_agree:
            print(f"  {'─'*50}")
            if len(valid) == 1:
                print(f"  Only {names} runs → distance {dist_val} to node {target}")
            else:
                print(f"  {names} return distance {dist_val} to node {target}")


def print_scalability(records, label):
    print(f"\n  {label}")
    print(f"  {'n':<8} {'Edges':<8} {'Dijkstra':<18} {'Bellman-Ford':<18} {'DAG-ShP':<18}")
    print(f"  {'─'*66}")
    for r in records:
        d  = fmt(r["dijkstra_time"])
        bf = fmt(r["bellman_ford_time"])
        dg = fmt(r["dag_shp_time"])
        print(f"  {r['n']:<8} {r['edges']:<8} {d:<18} {bf:<18} {dg}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():

    print("""
════════════════════════════════════════════════════════
  COMPLEXITY REFERENCE
════════════════════════════════════════════════════════
  Algorithm       Time               Space       Representation
  ──────────────────────────────────────────────────────────
  Dijkstra        O((V+E) log V)     O(V + E)    Adjacency List
  Bellman-Ford    O(V · E)           O(V + E)    Edge List
  DAG-ShP         O(V + E)           O(V + E)    Adjacency List""")

    print("""
════════════════════════════════════════════════════════
  STEP 1 — FAIR COMPARISON (Graph A)
═══════════════════════════════════════════════════════════""")

    print_fair(run_fair_comparison(graph_A_small, "graph_A_small"))
    print_fair(run_fair_comparison(generate_graph_A(100), "graph_A_large"))

    print("""
════════════════════════════════════════════════════════
  STEP 2 — CAPABILITY COMPARISON
════════════════════════════════════════════════════════""")

    print_capability(run_capability_test(graph_A_small, "A"))
    print_capability(run_capability_test(graph_B_small, "B"))
    print_capability(run_capability_test(graph_C_small, "C"))
    print_capability(run_capability_test(graph_D_small, "D"))

    print("""
════════════════════════════════════════════════════════
  STEP 3 — SCALABILITY
════════════════════════════════════════════════════════""")

    print_scalability(run_scalability_test(generate_graph_A, SIZES, "A"), "Graph A — acyclic, non-negative")
    print_scalability(run_scalability_test(generate_graph_B, SIZES, "B"), "Graph B — cyclic (DAG-ShP: N/A)")
    print_scalability(run_scalability_test(generate_graph_C, SIZES, "C"), "Graph C — negative edges (Dijkstra: N/A)")
    print_scalability(run_scalability_test(generate_graph_D, SIZES, "D"), "Graph D — cyclic + negative (Dijkstra: N/A | DAG-ShP: N/A)")


if __name__ == "__main__":
    main()