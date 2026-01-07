# 🧠 LangChain Python Projects

This workspace contains hands-on demos and experiments using **LangChain**, **LangGraph**, and **LangSmith**, focused on building interpretable, multi-step agents with strong evaluation workflows.

Each subfolder is a self-contained agent or demo with its own code and environment.

---

## 📦 Featured Project — `agent_demo/` (ChunkBuddy)

A complete learning assistant called **ChunkBuddy**, built with **LangGraph** and evaluated using **LangSmith**.

### Highlights

- ✅ Multi-step DAG: explanation → chunking → questions → summary  
- ✅ LangSmith evaluation: rule-based checks + LLM-as-judge  
- ✅ Streamlit UI for interactive exploration  
- ✅ Cognitive-science-aligned design (chunking, retrieval practice, clarity)  
- ✅ Supports both **standalone Python execution** and **LangGraph Studio**

👉 See the full walkthrough and instructions in  
[`agent_demo/README.md`](agent_demo/README.md)

---

## 🧪 Goals of This Workspace

- Showcase real-world **LangGraph** agents  
- Demonstrate **LangSmith** evaluation workflows  
- Build reusable components for agent development  

---

## 📁 Repository Structure

```text
LANGCHAIN-PYTHON/
│
├── agent_demo/                       # ChunkBuddy agent
│   ├── chunkbuddy_studio_graph.py    # Graph for LangGraph Studio
│   ├── chunkbuddy_standalone_graph.py# Standalone Python runner
│   ├── chunkbuddy.py                 # Node logic
│   ├── state.py                      # ChunkBuddyState schema
│   ├── evaluate_chunkbuddy.py        # LangSmith evaluation suite
│   ├── chunkbuddy_ui.py              # Optional Streamlit UI
│   ├── load_env.py                   # Loads agent_demo/.env
│   ├── .env.example                  # Safe template for environment variables
│   └── README.md                     # Detailed ChunkBuddy documentation
│
├── .gitignore
├── README.md                         # Workspace overview (this file)
├── requirements.txt                  # Optional shared dependencies
└── pyproject.toml                    # Project metadata
```

---

## 🛠 Setup

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
pip install -r agent_demo/requirements.txt
```

### 2️⃣ Configure environment variables

Copy the example environment file:

```bash
cp agent_demo/.env.example agent_demo/.env
```

Fill in your API keys before running any demos (for example):
- `OPENAI_API_KEY`
- `LANGSMITH_API_KEY`

---

## 📬 Contact

Created by **Zaheer Bhatti**

🔗 GitHub: https://github.com/drzaheerabhatti-tech  

Feel free to fork, adapt, or reach out with questions or feedback.
