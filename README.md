# LangGraph Starter

A beginner-friendly introduction to building graph-based workflows with LangGraph.
---

## Files

| File | Description |
|---|---|
| `sequential_graph.py` | Linear graph — nodes run one after another |
| `conditional_graph.py` | Orchestrator graph — routes to different nodes based on state |
| `requirements.txt` | Python dependencies |

---

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python sequential_graph.py
python conditional_graph.py
```

---

## How It Works

### `sequential_graph.py`
Runs two nodes in a fixed order:
1. `add_one` — adds 1 to the number
2. `multiply_by_two` — multiplies by 2

**Example:** input `3` → `(3 + 1) × 2` = **`8`**

---

### `conditional_graph.py`
An orchestrator node decides which worker to call:
- If `number < 5` → runs `add_one`
- If `number >= 5` → runs `multiply_by_two`

**Example:** input `7` → routes to `multiply` → **`14`**

---

## Core Concepts

- **State** — a shared dictionary passed between nodes
- **Nodes** — plain Python functions that read/update state
- **Edges** — define execution order
- **Conditional edges** — route dynamically based on state values
