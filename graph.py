from langgraph.graph import StateGraph, START, END
from state import InitialState
from rich import print

from nodes import analyse_input,analyse_requirements

def build_graph():
    graph = StateGraph(InitialState)
    graph.add_node("analyse_input", analyse_input)
    graph.add_node("analyse_requirements", analyse_requirements)

    graph.add_edge(START, "analyse_input")
    graph.add_edge("analyse_input", "analyse_requirements")
    graph.add_edge("analyse_requirements", END)
    return graph.compile()


if __name__ == "__main__":
    app_graph = build_graph()
    user_input = "I want to create a website for my new cafe that serves organic coffee and pastries using reactJs and nodeJs with a modern and minimalist design. The website should have an online menu, reservation system, and a blog section for sharing news and updates about the cafe."
    # user_input = input("Enter your Idea you want to create: ")
    result = app_graph.invoke({
        "user_input": user_input,
    })


    print(result['requirements'])