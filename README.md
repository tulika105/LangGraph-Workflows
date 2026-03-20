# LangGraph Basics

> A beginner-friendly, hands-on introduction to building **graph-based AI workflows** with LangGraph. 

LangGraph is a library built on top of LangChain that lets you model complex, multi-step workflows as **graphs** — where each step is a *node* and the connections between steps are *edges*. This repo walks you through the two most fundamental patterns: sequential execution and conditional (orchestrator-driven) routing.

---

## 📁 Project Structure

```
LangGraph Basics/
├── sequential_graph.py    # Linear graph: nodes run one after another
├── conditional_graph.py   # Orchestrator graph: routes to nodes based on state
├── requirements.txt       # Python dependencies
└── README.md
```

| File | What it teaches |
|---|---|
| `sequential_graph.py` | How to build a fixed, linear pipeline of nodes |
| `conditional_graph.py` | How to use an orchestrator node + conditional edges for dynamic routing |
| `requirements.txt` | Minimal dependencies to get LangGraph running |

---

## ⚙️ Setup

### Prerequisites
- Python 3.9 or higher

### Installation

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Dependencies (`requirements.txt`)
| Package | Purpose |
|---|---|
| `langgraph` | Core graph execution engine |
| `langchain` | Base utilities used by LangGraph |
| `typing-extensions` | Backports for TypedDict & type hints |

---

## ▶️ Running the Examples

```bash
# Run the sequential graph
python sequential_graph.py

# Run the conditional graph
python conditional_graph.py
```

---

## 🧠 Core Concepts

Before diving into the examples, here are the four building blocks of every LangGraph program:

| Concept | Description |
|---|---|
| **State** | A shared `TypedDict` dictionary that flows through the entire graph. Every node reads from and writes to this state. |
| **Nodes** | Plain Python functions. Each node receives the current state and returns a dictionary of updates to merge back into the state. |
| **Edges** | Static connections between nodes — they define a fixed execution order. |
| **Conditional Edges** | Dynamic connections — a routing function inspects the state and decides which node to go to next. |

---

## 📖 Example Walkthroughs

### 1. `sequential_graph.py` — Linear Pipeline

This graph runs two nodes in a **fixed sequence**, regardless of the input.

**Graph structure:**
```
[START] → add_one → multiply_by_two → [END]
```

**Nodes:**
- `add_one` — reads `state["number"]` and returns `number + 1`
- `multiply_by_two` — reads `state["number"]` and returns `number * 2`

**State shape:**
```python
class State(TypedDict):
    number: int
```

**Execution trace with input `3`:**
```
Initial state : { "number": 3 }
After add_one : { "number": 4 }   # 3 + 1
After multiply: { "number": 8 }   # 4 × 2
Final output  : { "number": 8 }
```

**Key code pattern:**
```python
graph = StateGraph(State)
graph.add_node("add", add_one)
graph.add_node("multiply", multiply_by_two)

graph.set_entry_point("add")
graph.add_edge("add", "multiply")
graph.add_edge("multiply", END)

app = graph.compile()
result = app.invoke({"number": 3})
```

---

### 2. `conditional_graph.py` — Orchestrator + Conditional Routing

This graph uses an **orchestrator node** to inspect the input and dynamically decide which worker node to call next.

**Graph structure:**
```
[START] → orchestrator ──(number < 5)──→ add_one     → [END]
                       └──(number ≥ 5)──→ multiply_by_two → [END]
```

**Nodes:**
- `orchestrator` — decides routing by setting `state["next_step"]` to `"add"` or `"multiply"`
- `add_one` — adds 1 to the number
- `multiply_by_two` — multiplies the number by 2

**State shape:**
```python
class State(TypedDict):
    number: int
    next_step: str   # Set by the orchestrator to control routing
```

**Execution traces:**

| Input | Orchestrator decision | Worker called | Output |
|---|---|---|---|
| `number = 3` | 3 < 5 → `"add"` | `add_one` | `4` |
| `number = 7` | 7 ≥ 5 → `"multiply"` | `multiply_by_two` | `14` |

**Key code pattern (conditional edges):**
```python
def route(state: State):
    return state["next_step"]   # Returns the name of the next node

graph.add_conditional_edges(
    "orchestrator",   # Source node
    route,            # Routing function
    {
        "add": "add",           # if route() returns "add" → go to "add" node
        "multiply": "multiply", # if route() returns "multiply" → go to "multiply" node
    }
)
```

---

## 🔄 LangGraph Execution Flow

Every LangGraph program follows this lifecycle:

```
1. Define State  →  2. Write Node functions  →  3. Build Graph
       ↓                                              ↓
4. Set Entry Point  →  5. Add Edges / Conditional Edges
       ↓
6. Compile (graph.compile())  →  7. Invoke (app.invoke({...}))
       ↓
8. Receive Final State
```

- **`graph.compile()`** — validates the graph structure and returns a runnable `app`
- **`app.invoke({...})`** — runs the graph synchronously and returns the final state

---
