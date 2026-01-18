# Cohere API Evaluation – Practical Learning & Performance Analysis

This repository documents a **hands-on evaluation of Cohere’s AI APIs**, with a focus on **latency behavior, performance distributions, grounding, and real-world usage patterns** — not just producing correct answers.

The goal of this work was **learning and evaluation**, rather than building a production application.

---

## Models & Capabilities Evaluated

### 1. Command (Command-R)
Used for **text generation and reasoning**, such as explaining technical concepts.

Key focus:
- end-to-end latency
- tail behavior (p95, max)
- refusal and grounding behavior when constrained by context

---

### 2. Embed
Used for **semantic representation** of text.

Capabilities evaluated:
- document embedding
- query embedding
- semantic similarity via cosine distance
- latency distribution (avg / p50 / p95 / max)
- impact of caching document embeddings

This forms the **retrieval foundation** for RAG systems.

---

### 3. Rerank
Used to **re-score and reorder candidate documents** for a given query.

Capabilities evaluated:
- ranking quality improvements over raw embedding similarity
- latency characteristics under repeated runs

Rerank was evaluated both standalone and as part of a RAG pipeline.

---

### 4. Classify
Used for **zero-shot text classification** via a command-based classifier.

Capabilities evaluated:
- label assignment without task-specific training
- latency distribution
- cold-start vs steady-state behavior
- tail latency effects

---

### 5. RAG (Retrieval-Augmented Generation)
A complete **Embed → Rerank → Command** pipeline was implemented and evaluated.

Key properties:
- document retrieval via embeddings
- candidate refinement via reranking
- grounded answer generation using retrieved context only
- explicit refusal when context is insufficient

---

## Environment & Setup

- Python virtual environment
- Cohere Python SDK (`ClientV2`)
- API key supplied via environment variable (`COHERE_API_KEY`)
- Modular evaluation scripts:
  - `command_eval.py`
  - `embed_eval.py`
  - `rerank_eval.py`
  - `classify_eval.py`
  - `rag_eval.py`
  - shared utilities in `common.py` and `data_ai.py`

Scripts were intentionally kept **small, explicit, and readable** to support learning and inspection.

---

## What the Evaluation Scripts Do

### Command Evaluation
- Sends structured prompts to a versioned Command-R model
- Measures end-to-end latency across repeated runs
- Reports average, p50, p95, and max latency
- Exposes long-tail behavior in generation models

---

### Embed Evaluation
- Embeds a fixed set of documents
- Embeds a query independently
- Computes cosine similarity to rank documents
- Separately measures:
  - document embedding latency (cold start)
  - query embedding latency (steady state)
- Demonstrates the impact of **caching document embeddings**

---

### Rerank Evaluation
- Takes a query and candidate documents
- Produces relevance-scored rankings
- Measures rerank latency distributions
- Compares embedding-only retrieval vs reranked results

---

### Classify Evaluation
- Classifies multiple texts into predefined labels
- Demonstrates zero-shot classification
- Highlights cold-start effects and tail latency
- Reinforces the need for percentile-based analysis

---

### RAG Evaluation
- Combines Embed → Rerank → Command
- Enforces **strict grounding rules**
- Explicitly tests:
  - in-scope questions
  - out-of-scope questions
- Validates correct refusal behavior when context is insufficient
- Measures latency per pipeline stage

---

## Key Learnings

### 1. Model Versioning Matters
- Older model names were deprecated
- Explicit, versioned model identifiers provide stability

**Takeaway:** Always verify available models programmatically.

---

### 2. Latency Is Inherently Variable
Even with identical inputs, latency varied due to:
- shared inference infrastructure
- queueing and scheduling
- network variability

**Takeaway:** Variability is normal — measure distributions, not single values.

---

### 3. Averages Are Misleading
Rare slow requests significantly skewed averages.

**Takeaway:** Averages hide real user experience.

---

### 4. Percentiles Matter (p95 > Average)
- p95 latency consistently reflected realistic worst-case behavior
- Tail events were visible but bounded

**Takeaway:** Percentiles are essential for system evaluation.

---

### 5. Long-Tail Behavior Is Real
- Very slow responses occurred
- Requests completed successfully
- Systems recovered normally

**Takeaway:** Tail latency must be expected in distributed AI systems.

---

### 6. Embeddings Are Fast and Stable
Compared to generation:
- lower latency
- tighter distributions
- smaller tails

Typical steady-state query embedding:
- p50 ≈ 160 ms
- p95 ≈ 170 ms

---

### 7. Caching Fundamentally Changes the System
Without caching:
- documents re-embedded every query
- higher latency and cost

With caching:
- documents embedded once
- clean separation of retrieval vs query cost

**Mental model:**  
_Read the book once; answer questions many times._

---

### 8. Grounded RAG Prevents Hallucinations
- The model correctly refused when answers were not supported by context
- Out-of-scope questions were handled safely

**Takeaway:** Retrieval alone is not enough — grounding rules matter.

---

### 9. Rate Limits Shape Design
Using a trial API key exposed:
- request-per-minute limits
- the need for pacing, caching, and batching

**Takeaway:** Infrastructure constraints influence system architecture, even in experiments.

---

## Summary

This evaluation demonstrated that working with modern AI systems requires understanding:

- latency distributions, not just outputs
- tail behavior and cold starts
- caching and retrieval strategies
- grounding and refusal behavior
- realistic infrastructure constraints

The same principles apply to **small experiments and large production systems**.

---

## Next Steps
- Evaluate retrieval quality metrics beyond latency
- Add citation-style answers to RAG output
- Explore batching and concurrency effects
- Compare alternative embedding and rerank models

---

## Appendix

### Obtaining a Cohere API Key

To run the examples in this repository, you need a **Cohere API key**.

1. Go to the Cohere dashboard:
   https://dashboard.cohere.com/

2. Create a free account (or sign in).

3. Navigate to:
   **Dashboard → API Keys**

4. Create a new API key.
   - A **trial key** is sufficient for learning and evaluation.
   - Trial keys have rate limits (e.g. requests per minute), which this project intentionally surfaces and measures.

5. Copy the key and set it using one of the methods above (environment variable or `.env` file).

---

### Notes on Trial Keys

- Trial keys are rate-limited (e.g. ~40 requests/minute).
- Rate limits influenced:
  - pacing logic
  - caching decisions
  - latency distribution analysis
- This was treated as a **realistic constraint**, not a limitation to hide.

Production keys can be created later if higher throughput is required.

---

## Appendix – API Key Management

This project uses the **COHERE_API_KEY** environment variable.  
API keys are **never hard-coded** in source files.

---

### Obtaining a Cohere API Key

1. Go to the Cohere dashboard:  
   https://dashboard.cohere.com/

2. Create a free account (or sign in).

3. Navigate to **Dashboard → API Keys**.

4. Create a new API key.
   - A **trial key** is sufficient for learning and evaluation.
   - Trial keys are rate-limited (this project intentionally surfaces those limits).

5. Copy the key and set it using one of the methods below.

---

### Temporary (Current Session Only)

Use this when experimenting or testing.

#### Windows (PowerShell)
```
$env:COHERE_API_KEY="your_api_key_here"
```

### Linux / macOS (bash, zsh)
```
export COHERE_API_KEY="your_api_key_here"
```
---

### Using a `.env` File (Local Development)

For local development, API keys can be stored in a `.env` file instead of being set manually in the shell.

1. Create a file named `.env` in the project root:
   ```env
   COHERE_API_KEY=your_api_key_here
   ```
Add .env to .gitignore to prevent committing secrets:

gitignore
```
.env
```

2. Install the helper library:

```
pip install python-dotenv
```

3. Load the variables in Python:
Near the top of your Python script (before accessing os.environ):

```
import os
from dotenv import load_dotenv
load_dotenv()
```

This reads the .env file and injects variables into the environment.

4. Access the API key in code
Once loaded, the API key is available via:

```
api_key = os.environ["COHERE_API_KEY"]
```

This approach keeps credentials out of source control while supporting repeatable local runs.