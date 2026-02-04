from support_agent import build_support_graph

def visualize_graph():
    """Generate and display the LangGraph workflow visualization"""
    
    print("Generating Customer Support Agent Graph Visualization...")
    
    graph = build_support_graph()
    
    try:
        # Use LangGraph's built-in Mermaid visualization
        graph_image = graph.get_graph().draw_mermaid_png()
        
        with open("support_agent_graph.png", "wb") as f:
            f.write(graph_image)
        
        print("Graph visualization saved as: support_agent_graph.png")
        print("\nGraph Structure:")
        print(graph.get_graph())
        
    except Exception as e:
        print(f"Error generating graph visualization: {e}")
        print("\nTo generate graph visualization, install:")
        print("pip install pygraphviz")
        print("or")
        print("pip install grandalf")

def main():
    visualize_graph()

if __name__ == "__main__":
    main()
