from agent_demo.chunkbuddy_standalone_graph import build_app

# LangGraph Studio will call build_app() itself.
# Do NOT call build_app() at import time.

# Optional: expose a function for manual use
def get_app():
    return build_app()

# Only run locally when executing `python app.py`
if __name__ == "__main__":
    app = build_app()
    print("Graph built successfully.")