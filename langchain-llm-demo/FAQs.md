# FAQ

## 📘 What is LangChain?
- LangChain is an open‑source framework for building applications powered by large language models (LLMs).
- It provides abstractions like **chains**, **agents**, and **memory** to make LLM integration easier.

## 📘 What is LangChain used for?
- Building chatbots, assistants, and tools that need reasoning over text.
- Connecting LLMs to external data sources, APIs, or custom workflows.
- Managing prompts, outputs, and multi‑step reasoning pipelines.

---

## 📘 What is LangSmith?
- LangSmith is LangChain’s tracing and evaluation platform.
- It lets you log, visualize, and debug LLM calls and agent workflows.

## 📘 What is LangSmith used for?
- Tracking latency, costs, and outputs of LLM runs.
- Evaluating quality with custom metrics (e.g. clarity, chunk counts).
- Sharing reproducible traces with teammates or interviewers.

---

## 📘 What is a graph?
- In LangGraph, a **graph** is a workflow made of connected nodes.
- Each node represents a step (e.g. draft explanation, chunk explanation).
- Edges define the order of execution.

## 📘 What is a node?
- A node is a single function or operation in the graph.
- Example: `draft_explanation` is a node that generates the first explanation.
- Nodes can pass state forward to other nodes.

---

## 📘 What is ChunkBuddy?
- ChunkBuddy is a demo agent that explains a concept, splits it into chunks, generates check questions, and summarizes with meta notes.
- It’s designed to showcase LangGraph workflows and evaluation with LangSmith.

## 📘 What does `evaluate_chunkbuddy.py` do?
- Loads a dataset of topics and levels.
- Runs the graph in batch mode.
- Applies evaluators (chunk count, question count, clarity).
- Logs results to LangSmith.

## 📘 What does `chunkbuddy_ui.py` do?
- Provides a Streamlit interface.
- Lets a user enter a topic interactively.
- Calls the graph once and displays explanation, chunks, questions, and summary.

---

## 📘 What is a dataset in this project?

A JSON file (`chunkbuddy-topics`) containing topics and difficulty levels for evaluation.  

---
## 📘 Why use evaluators?**  

To enforce quality checks (e.g. 3–7 chunks, 3–5 questions, clarity).  

---
## 📘 Why refactor?**  
To improve maintainability: centralized prompts, parsing helpers, logging, and modular UI.  

---
## 🔑 How do I get an OpenAI API key?
- Go to [OpenAI’s API keys page](https://platform.openai.com/account/api-keys).
- Sign in with your OpenAI account (create one if you don’t have it).
- Click **Create new secret key**.
- Copy the key and store it securely (e.g. in `.env` or environment variables).
- Never commit your API key to GitHub.

---

## 🔑 How do I get a LangSmith API key?
- If you want to use **LangSmith** (LangChain’s tracing and evaluation platform):
  - Go to [LangSmith](https://smith.langchain.com/).
  - Sign in with your GitHub or Google account.
  - Navigate to **Settings → API Keys**.
  - Generate a new key and add it to your environment (`LANGCHAIN_API_KEY`).
- This key enables logging, tracing, and evaluation features.

---

## 📘 Where should I put my API keys?
- Store them in a `.env` file or export them as environment variables:
```
  export OPENAI_API_KEY="your-openai-key"
  export LANGCHAIN_API_KEY="your-langsmith-key"
```
Use a library like python-dotenv to load .env automatically in development.
Never hard‑code keys in your scripts.
---
## 📘 How do I run ChunkBuddy locally?
Run the graph directly:
```
python chunkbuddy.py
```

## 📘 How do I launch the Streamlit UI?
```
streamlit run chunkbuddy_ui.py
```

## 📘 How do measure the performance of ChunkBuddy?
```
python evaluate_chunkbuddy.py
```
## 📘 What does evaluate_chunkbuddy.py check?
Chunk count: 3–7 chunks per explanation.
Question count: 3–5 check questions.
Clarity & difficulty: Summary meta notes parsed for readability and level.
Results are logged in LangSmith for inspection.
