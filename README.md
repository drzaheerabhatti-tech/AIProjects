# AIProjects

A research-oriented repository exploring applied AI system design using modern large language models (LLMs).  
This repository is organized around **research areas**, with each area containing focused, hands-on experiments and demos.

The goal is not to provide polished products, but to demonstrate understanding of **core concepts, trade-offs, and implementation patterns** in contemporary AI systems.

---

## Research Areas

### 🔹 Agentic AI Systems
Exploratory research into agent-based AI systems, focusing on multi-step reasoning, orchestration, and evaluation-driven development.

📁 `agents/`  
➡️ See `agents/README.md` for detailed implementation notes and experiments.

---

### 🔹 Cohere Platform Experiments
Hands-on exploration of Cohere’s LLM platform, starting from foundational usage and progressing toward applied patterns such as structured outputs, retrieval, and evaluation.

📁 `cohere-demos/`  
➡️ Includes step-by-step demos using the Cohere Chat API, along with notes on API evolution and response parsing.

---

### 🔹 Retrieval-Augmented Generation (RAG)
Research into retrieval-based architectures for grounding large language models with external knowledge sources.

*(Projects forthcoming)*

---

### 🔹 Evaluation & Observability
Investigation of evaluation techniques, feedback loops, and observability patterns for LLM-based systems.

*(Projects forthcoming)*

---

## Repository Philosophy

- **Concept-first, tool-second**  
  Folder structure reflects *what is being studied* (agents, RAG, evaluation), not just which library is used.

- **Small, focused demos**  
  Each example is intentionally scoped to highlight a specific capability or concept.

- **Learning transparency**  
  Where useful, friction encountered during development is documented to capture lessons learned and prevent repeat mistakes.

---

## Notes on Secrets and Configuration

- API keys and secrets are **never committed**
- `.env` files are gitignored
- `.env.example` files are used where configuration needs to be documented

---

## Status

This repository is actively evolving as new experiments are added and existing ones are refined.


## Cohere RAG Evaluation

**Hands-on evaluation of Cohere’s core APIs** (Command, Embed, Rerank, Classify) and how they compose into a minimal **Retrieval-Augmented Generation (RAG)** pipeline.

This project focuses on **real-world behavior**, not toy examples.

### What’s Covered
- **Command** – text generation and reasoning
- **Embed** – semantic similarity and retrieval
- **Rerank** – relevance ordering of candidate documents
- **Classify** – zero-shot text classification
- **RAG pipeline** – Embed → Rerank → Command (grounded generation)

### What Was Measured
- End-to-end latency per API call
- Latency distributions (avg / p50 / p95 / max)
- Tail latency behavior under repeated runs
- Impact of **embedding cache vs. no cache**
- Trial API rate-limit effects

### Key Learnings
- Latency in AI systems is **inherently variable**
- Averages can be misleading; **p95 is more meaningful**
- Embeddings are fast and stable compared to generation
- Caching dramatically improves performance and cost
- RAG improves grounding and refusal behavior for out-of-scope queries

### Why This Matters
This mirrors **production concerns**:
- performance predictability
- tail latency
- cost-aware design
- safe, grounded generation

📁 **Code:** `cohere-rag-evaluation/`  
🐍 **Tech:** Python, Cohere ClientV2, vector similarity, RAG patterns

