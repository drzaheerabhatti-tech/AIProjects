# 📚 ChunkBuddy — A LangGraph Learning Assistant

ChunkBuddy is a multi‑step learning assistant built with **LangGraph**, evaluated using **LangSmith**, and optionally served through a **Streamlit UI**.  
It demonstrates how to build interpretable, state‑driven agents that follow a clear DAG:

> **explanation → chunking → question generation → summary**

This project is designed for clarity, reproducibility, and cognitive‑science‑aligned learning.

---

# 🚀 Quick Start

## ✅ 1. Install dependencies

From the project root:

```bash
pip install -r requirements.txt
pip install -r agent_demo/requirements.txt
```

---

## ✅ 2. Set up environment variables

Copy the example file:

```bash
cp agent_demo/.env.example agent_demo/.env
```

Fill in your API keys:

```
LANGCHAIN_API_KEY=your-key
LANGSMITH_API_KEY=your-key
LANGSMITH_PROJECT=chunkbuddy
MODEL_NAME=gpt-4
```

ChunkBuddy loads this file automatically via:

```
agent_demo/load_env.py
```

---

# 🧠 How ChunkBuddy Works

ChunkBuddy is implemented as a **LangGraph StateGraph** with the following nodes:

| Node | Purpose |
|------|---------|
| `explain_node` | Generates a clear explanation of the topic |
| `chunk_node` | Breaks the explanation into digestible chunks |
| `question_node` | Produces retrieval‑practice questions |
| `summary_node` | Produces a final summary |

The state is defined in:

```
agent_demo/state.py
```

The node logic lives in:

```
agent_demo/chunkbuddy.py
```

---

# ✅ How to Run ChunkBuddy

You can run ChunkBuddy in **three different ways**, depending on your workflow.

---

# ✅ 1. Run the Standalone Graph (Python only)

This uses:

```
agent_demo/chunkbuddy_standalone_graph.py
```

Run it:

```bash
cd agent_demo
python chunkbuddy_standalone_graph.py
```

This executes the graph end‑to‑end using:

- `ChunkBuddyState`
- Node functions in `chunkbuddy.py`
- `app.invoke()` for synchronous execution

Use this when you want a **pure Python workflow**.

---

# ✅ 2. Run the Graph in LangGraph Studio

This uses:

```
agent_demo/chunkbuddy_studio_graph.py
```

This version exposes:

```python
return graph.compile()
```

### Run Studio:

```bash
langgraph dev
```

Then open the Studio UI (usually http://localhost:2024).

Inside Studio you can:

- Inspect state transitions  
- Click through nodes  
- View LLM calls  
- Trigger runs interactively  
- Send custom inputs  
- Export traces to LangSmith  

Use this when you want **visual debugging** or **demo‑friendly interaction**.

---

# ✅ 3. Run the Evaluation Suite (LangSmith)

This uses:

```
agent_demo/evaluate_chunkbuddy.py
```

Run it:

```bash
cd agent_demo
python evaluate_chunkbuddy.py
```

This script:

- Loads your `.env`
- Runs rule‑based checks
- Runs LLM‑as‑judge evaluations
- Logs results to LangSmith
- Produces a structured evaluation report

Use this when you want **quantitative and qualitative evaluation**.

---

# 🗂 Folder Structure

```
agent_demo/
│
├── chunkbuddy_studio_graph.py      # Graph for LangGraph Studio
├── chunkbuddy_standalone_graph.py  # Standalone Python runner
├── chunkbuddy.py                   # Node logic
├── state.py                        # ChunkBuddyState schema
├── evaluate_chunkbuddy.py          # LangSmith evaluation suite
├── chunkbuddy_ui.py                # Optional Streamlit UI
├── load_env.py                     # Loads agent_demo/.env
├── .env.example                    # Safe template for environment variables
├── images/                         # Screenshots and diagrams
└── README.md                       # This file
```

---

# 🧪 Design Principles

ChunkBuddy is built around:

- **Interpretability** — every node is explicit  
- **Deterministic structure** — DAG ensures predictable flow  
- **Cognitive alignment** — chunking + retrieval practice  
- **Observability** — LangSmith traces for every run  
- **Reproducibility** — standalone + Studio + evaluation suite  

---

# 📬 Contact

Created by **Zaheer Bhatti**  
https://github.com/drzaheerabhatti-tech