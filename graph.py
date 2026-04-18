from langchain_core.globals import set_verbose, set_debug
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
from nodes import *
import sqlite3

set_debug(True)
set_verbose(True)

# Create SQLite connection
conn = sqlite3.connect("agent_state.db", check_same_thread=False)

# Initialize checkpointer
checkpointer = SqliteSaver(conn)

graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")

graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)

graph.set_entry_point("planner")

agent = graph.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    user_prompt = input("Enter your Idea: ")
    result = agent.invoke(
        {"user_prompt": user_prompt},
        {
            "recursion_limit": 100,
            "configurable": {"thread_id": "todo-app-1"}  # important for persistence
        }
    )
    print("Final State:", result)
