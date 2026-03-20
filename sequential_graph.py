# Import StateGraph to build the workflow (graph)
# Import END to tell LangGraph where execution should stop
from langgraph.graph import StateGraph, END

# TypedDict is used to define the structure of the shared state
from typing import TypedDict

# -------------------------------------------------
# STATE: Shared memory that flows through the graph
# -------------------------------------------------

# State defines the shape of the data that all nodes will share
# It behaves like a dictionary passed between nodes
class State(TypedDict):
    number: int   # This key holds the number being processed. State has one field called 'number'.

# -------------------------------------------------
# NODE 1: A simple function (adds 1 to the number)
# -------------------------------------------------

# A LangGraph node is just a normal Python function
# It receives the current state and returns updates to the state
def add_one(state: State):
    # Read the value from the state
    current_number = state["number"]
    
    # Return an updated value (LangGraph merges this into the state)
    return {"number": current_number + 1}

# -------------------------------------------------
# NODE 2: Another function (multiplies number by 2)
# -------------------------------------------------

def multiply_by_two(state: State):
    # Read the value from the state
    current_number = state["number"]
    
    # Return the updated value
    return {"number": current_number * 2}

# -------------------------------------------------
# GRAPH: Defines execution order of nodes
# -------------------------------------------------

# Create a graph and tell it what state structure it will use
graph = StateGraph(State)

# Register the nodes inside the graph
# "add" and "multiply" are node names used in edges
graph.add_node("add", add_one)
graph.add_node("multiply", multiply_by_two)

# -------------------------------------------------
# EDGES: Control the flow of execution
# -------------------------------------------------

# Set the entry point (first node to run)
graph.set_entry_point("add") # graph.add_edge(START, "add") is also valid

# After 'add' finishes, go to 'multiply'
graph.add_edge("add", "multiply")

# After 'multiply' finishes, stop execution
graph.add_edge("multiply", END)

# -------------------------------------------------
# COMPILE: Convert graph definition into a runnable app
# -------------------------------------------------

# Compilation validates and freezes the graph structure
app = graph.compile()

# -------------------------------------------------
# EXECUTION: Run the graph with initial state
# -------------------------------------------------

# Invoke the graph with an initial state
# This state is passed to the entry node
result = app.invoke({"number": 3})

# Print the final state after the graph finishes
print(result)

