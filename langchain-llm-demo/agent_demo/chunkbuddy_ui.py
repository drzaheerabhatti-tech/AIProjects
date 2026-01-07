# chunkbuddy_ui.py
# ---------------------------------------------------------------------------
# Streamlit front-end for ChunkBuddy.
# This provides an interactive UI where a learner can type in any topic
# and level, then see the LangGraph outputs (explanation, chunks, questions,
# summary, and meta notes).
# ---------------------------------------------------------------------------

import streamlit as st
from typing import TypedDict, List

# Reuse the existing LangGraph app and state definition
from chunkbuddy_standalone_graph import build_app, LearningState
from load_env import load_env
load_env()

# --- Build the LangGraph app once at startup -------------------------------
# We compile the graph once and keep it in memory. Each user interaction
# simply invokes this app with a new initial state.
app = build_app()

# --- Streamlit page setup --------------------------------------------------
st.set_page_config(page_title="ChunkBuddy", page_icon="🧠", layout="wide")

st.title("🧠 ChunkBuddy – LangGraph Learning Assistant")
st.write(
    "Turn any technical topic into a structured learning experience with "
    "explanations, chunks, questions, and a summary."
)

# --- Sidebar controls ------------------------------------------------------
# Sidebar lets the user configure topic and learner level.
st.sidebar.header("Settings")
default_topic = "Kafka partitions"
topic = st.sidebar.text_input("Topic you want to learn", value=default_topic)

level = st.sidebar.selectbox(
    "Your level",
    options=["beginner", "intermediate", "advanced"],
    index=0,
)

# Button to trigger graph execution
run_button = st.sidebar.button("Teach me 🚀")

st.markdown("---")

# --- Main interaction flow -------------------------------------------------
if run_button:
    if not topic.strip():
        # Guard clause: require a non-empty topic
        st.error("Please enter a topic.")
    else:
        # Show spinner while the graph runs
        with st.spinner("ChunkBuddy is thinking..."):
            # Prepare initial state for the graph
            initial_state: LearningState = {
                "topic": topic.strip(),
                "level": level,
            }
            # Invoke the graph and collect results
            result = app.invoke(initial_state)

        # --- Layout: 2 columns (explanation + summary) ----------------------
        col1, col2 = st.columns([2, 1])

        # 1. Full explanation
        with col1:
            st.subheader("1. Explanation")
            st.write(result.get("raw_explanation", "_No explanation generated._"))

        # 2. TL;DR summary
        with col2:
            st.subheader("4. Quick Summary")
            st.write(result.get("summary", "_No summary generated._"))

        st.markdown("---")

        # 3. Chunks (expandable sections)
        st.subheader("2. Learning chunks")
        chunks = result.get("chunks", [])
        if not chunks:
            st.write("_No chunks generated._")
        else:
            for i, chunk in enumerate(chunks, start=1):
                with st.expander(f"Chunk {i}"):
                    st.write(chunk)

        st.markdown("---")

        # 4. Check-your-understanding questions
        st.subheader("3. Check your understanding")
        questions = result.get("check_questions", [])
        if not questions:
            st.write("_No questions generated._")
        else:
            for q in questions:
                st.markdown(f"- {q}")

        st.markdown("---")

        # 5. Meta learning notes (optional)
        meta = result.get("meta", {})
        notes = meta.get("learning_design_notes", [])
        if notes:
            st.subheader("🧩 How this structure helps you learn")
            for note in notes:
                st.markdown(f"- {note}")

        # 6. Developer view: raw state (for debugging)
        with st.expander("Developer view: raw state"):
            st.json(result)

else:
    # Initial info message before user clicks the button
    st.info("Enter a topic and click **Teach me 🚀** in the sidebar to get started.")
