from graph_data import (
    graph_A_small, graph_B_small, graph_C_small,
    generate_graph_A, generate_graph_B, generate_graph_C
)
from experiments import run_fair_comparison, run_capability_test, run_scalability_test


# ─────────────────────────────────────────────
# PRINT HELPERS
# ─────────────────────────────────────────────

def print_fair(res):
    print(f"\n{'='*55}")
    print(f"  FAIR COMPARISON — {res['label']}")
    print(f"  Nodes: {res['nodes']}  |  Edges: {res['edges']}")
    print(f"{'='*55}")
    print(f"  {'Algorithm':<16} {'Time (s)'}")
    print(f"  {'-'*35}")
    for algo in ["dijkstra", "bellman_ford", "dag"]:
        t = res[algo]["time"]
        print(f"  {algo:<16} {t:.6f}s")


def print_capability(res):
    print(f"\n{'='*55}")
    print(f"  CAPABILITY TEST — Scenario {res['scenario']}")
    print(f"  Nodes: {res['nodes']}  |  Edges: {res['edges']}")
    print(f"{'='*55}")
    for algo in ["dijkstra", "bellman_ford", "dag"]:
        entry = res[algo]
        t_str = f"{entry['time']:.6f}s" if entry["time"] is not None else "—"
        print(f"  {algo:<16} {t_str:<14}  [{entry['note']}]")

    bf_dist = res["bellman_ford"]["distances"]
    if bf_dist:
        target = max(bf_dist.keys())
        print(f"\n  Distance source → node {target}:")
        for algo in ["dijkstra", "bellman_ford", "dag"]:
            d = res[algo]["distances"]
            val = d.get(target, "unreachable") if d else "N/A"
            print(f"    {algo:<16} → {val}")


def print_scalability(records, title=""):
    print(f"\n{'='*65}")
    print(f"  SCALABILITY TEST — {title}")
    print(f"{'='*65}")
    print(f"  {'n':<8} {'Edges':<8} {'Dijkstra':<16} {'Bellman-Ford':<18} {'DAG'}")
    print(f"  {'-'*60}")
    for r in records:
        d  = f"{r['dijkstra_time']:.6f}s"     if r['dijkstra_time']     is not None else "N/A"
        bf = f"{r['bellman_ford_time']:.6f}s"  if r['bellman_ford_time'] is not None else "N/A"
        dg = f"{r['dag_time']:.6f}s"           if r['dag_time']          is not None else "N/A"
        print(f"  {r['n']:<8} {r['edges']:<8} {d:<16} {bf:<18} {dg}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    graph_A_large = generate_graph_A(100)

    # ── STEP 1: Fair Comparison ──────────────────
    print("\n" + "█"*55)
    print("  STEP 1 — FAIR COMPARISON")
    print("  Same graph (A), all three algorithms")
    print("  Graph A: DAG, non-negative weights, adjacency list")
    print("  Bellman-Ford uses edge list representation")
    print("█"*55)

    print_fair(run_fair_comparison(graph_A_small, "graph_A_small (n=20)"))
    print_fair(run_fair_comparison(graph_A_large, "graph_A_large (n=100)"))

    # ── STEP 2: Capability Comparison ───────────
    print("\n" + "█"*55)
    print("  STEP 2 — CAPABILITY COMPARISON")
    print("  A = clean DAG | B = cycles | C = negative edges")
    print("█"*55)

    print_capability(run_capability_test(graph_A_small, "A"))
    print_capability(run_capability_test(graph_B_small, "B"))
    print_capability(run_capability_test(graph_C_small, "C"))

    # ── STEP 3: Scalability ──────────────────────
    print("\n" + "█"*55)
    print("  STEP 3 — SCALABILITY TEST")
    print("  Graph A, increasing input size")
    print("█"*55)

    sizes = [10, 50, 100, 200, 500]
    print_scalability(
        run_scalability_test(generate_graph_A, sizes, "A"),
        title="Graph A (DAG, non-negative)"
    )


if __name__ == "__main__":
    main()