from langgraph.graph import StateGraph, END
from typing import TypedDict

# --------------------
# STATE
# --------------------
class State(TypedDict):
    number: int
    next_step: str  # State has two fields: 'number' and 'next_step'


# --------------------
# ORCHESTRATOR NODE
# --------------------
def orchestrator(state: State):
    if state["number"] < 5:
        return {"next_step": "add"}
    else:
        return {"next_step": "multiply"}


# --------------------
# WORKER NODES
# --------------------
def add_one(state: State):
    return {"number": state["number"] + 1}

def multiply_by_two(state: State):
    return {"number": state["number"] * 2}


# --------------------
# GRAPH
# --------------------
graph = StateGraph(State)

graph.add_node("orchestrator", orchestrator)
graph.add_node("add", add_one)
graph.add_node("multiply", multiply_by_two)

# Orchestrator is the entry point
graph.set_entry_point("orchestrator")

# Conditional routing based on orchestrator decision
def route(state: State):
    return state["next_step"]

graph.add_conditional_edges(
    "orchestrator",
    route,
    {
        "add": "add",
        "multiply": "multiply",
    },
)

# After worker nodes, stop
graph.add_edge("add", END)
graph.add_edge("multiply", END)

# Compile
app = graph.compile()

# --------------------
# RUN
# --------------------
result = app.invoke({"number": 7, "next_step": ""})
print(result)
