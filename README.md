# Comparative Shortest Path Algorithm Analysis

A comparative implementation and analysis of three shortest-path algorithms on four types of weighted directed graphs.

**Algorithms:** Dijkstra | Bellman-Ford | DAG Shortest Path  
**Course:** CSE202 — Algorithms II | Acibadem University

---

## Project Structure

```
├── graph_data.py       # Graph definitions and generators
├── dijkstra.py         # Dijkstra's algorithm (Adjacency List)
├── bellman_ford.py     # Bellman-Ford algorithm (Edge List)
├── dag_shp.py          # DAG Shortest Path (Topological Sort)
├── experiments.py      # Comparison logic (fair, capability, scalability)
└── main.py             # Entry point — runs and prints all results
```

---

## Graph Types

| Graph | Properties |
|-------|-----------|
| A | Acyclic (DAG), non-negative weights |
| B | Cyclic, non-negative weights |
| C | Acyclic, negative edges |
| D | Cyclic + negative edges |

---

## Requirements

Python 3.x — no external libraries needed.

---

## How to Run

```bash
python main.py
```

That's it. The output covers three steps:

1. **Fair Comparison** — all three algorithms on Graph A (small and large)
2. **Capability Comparison** — which algorithms work or fail on each graph type
3. **Scalability Test** — runtime across n = 10, 50, 100, 200, 500 for all four graphs

---

## Algorithm — Representation Mapping

| Algorithm | Representation | Time Complexity |
|-----------|---------------|-----------------|
| Dijkstra | Adjacency List | O((V+E) log V) |
| Bellman-Ford | Edge List | O(V · E) |
| DAG Shortest Path | Adjacency List | O(V + E) |

All three use **O(V+E) space**.

---

## Notes

- Source node is always **node 0**, target is always the **last node**
- Graph weights are randomly generated — rerunning produces different numbers
- Bellman-Ford detects negative cycles and returns `None` if found
- DAG algorithm is skipped on cyclic graphs (B, D)
- Dijkstra is skipped on graphs with negative edges (C, D)
