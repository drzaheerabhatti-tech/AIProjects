# Cohere API Evaluation – Practical Learning & RAG Foundations

This repository documents a **hands-on evaluation of Cohere’s APIs**, with a focus on:

- understanding how different model families are used
- measuring **latency distributions** (avg / p50 / p95)
- observing **tail latency and variability**
- assembling a minimal but realistic **RAG pipeline**

The goal is **learning and evaluation**, not building a production system.

---

## Models Covered

This project evaluates the following Cohere model families:

### 1. Command (Command-R)
**Purpose:**  
Text generation, reasoning, and explanation.

**Used for:**  
- answering questions
- synthesizing responses
- grounded generation in RAG

---

### 2. Embed
**Purpose:**  
Convert text into vectors for semantic similarity.

**Used for:**  
- document embedding
- query embedding
- retrieval based on cosine similarity

---

### 3. Rerank
**Purpose:**  
Reorder candidate documents by relevance to a query.

**Used for:**  
- improving retrieval quality after embedding
- selecting the most relevant context for generation

---

### 4. Classify
**Purpose:**  
Assign labels to text using a command-based classification flow.

**Used for:**  
- text categorization experiments
- latency comparison with other model families

---

### 5. RAG (Combined Pipeline)
**Purpose:**  
Bring everything together into a grounded question-answering flow.

**Pipeline:**
1. Embed documents
2. Embed query
3. Retrieve top candidates
4. Rerank candidates
5. Generate an answer grounded in retrieved context

---

## Repository Structure

```text
cohere-rag-evaluation/
├── README.md
├── list_models.py
├── command_eval.py
├── embed_eval.py
├── rerank_eval.py
├── classify_eval.py
├── rag_eval.py
├── common.py
└── data_ai.py
````

Each script evaluates **one model family** to keep responsibilities clear.

---

## Evaluation Philosophy

This project treats AI APIs as **distributed systems**, not black boxes.

For every model call we observe:

* variability between runs
* long-tail latency
* effects of caching
* realistic infrastructure constraints (rate limits)

**Key idea:**
Correctness alone is not enough — **performance distributions matter**.

---

## What Each Script Does

### `command_eval.py`

* Sends repeated chat requests to Command-R
* Measures end-to-end latency
* Reports avg / p50 / p95 / max
* Demonstrates long-tail behavior in generation models

---

### `embed_eval.py`

* Embeds a fixed document set (cached)
* Embeds queries repeatedly
* Computes cosine similarity
* Measures latency separately for:

  * document embedding (one-time)
  * query embedding (steady-state)

**Mental model:**
*Read the book once; answer questions many times.*

---

### `rerank_eval.py`

* Reranks a list of candidate documents for a query
* Measures rerank latency distribution
* Shows improved ordering compared to embedding alone

---

### `classify_eval.py`

* Classifies short texts into predefined labels
* Demonstrates command-based classification
* Highlights latency variability across runs

---

### `rag_eval.py`

Implements a minimal **RAG pipeline**:

1. Embed documents (cached)
2. Embed query
3. Retrieve candidates
4. Rerank candidates
5. Generate a grounded answer

Also includes **grounding tests**, where the model correctly refuses to answer when the context does not support the question.

---

## Key Learnings

### Latency Is Variable

Even identical prompts show variability due to:

* shared inference infrastructure
* queueing effects
* internal scheduling

---

### Averages Are Misleading

A single slow request can skew averages dramatically.

---

### p95 Reflects Real Experience

p95 captures the **worst latency most users will experience**, making it far more useful than averages.

---

### Embeddings Are Fast and Stable

* much lower latency than generation
* tighter distributions
* smaller tail effects

---

### Caching Changes the System

Caching document embeddings:

* reduces cost
* improves latency
* produces clearer performance signals

---

### Rate Limits Are Real

Trial keys enforce request limits, shaping:

* pacing
* batching
* caching strategies

---

## Python Virtual Environment Setup

Using a virtual environment ensures isolation and reproducibility.

### Create Environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
```

**Linux / macOS:**

```bash
python3 -m venv .venv
```

---

### Activate Environment

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

If blocked:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

You should see `(.venv)` in your prompt.

---

### Install Dependencies

```bash
pip install cohere python-dotenv numpy
```

---

## API Key Management

This project uses the `COHERE_API_KEY` environment variable.
Keys are **never hard-coded**.

---

### Temporary (Current Session Only)

**Windows (PowerShell):**

```powershell
$env:COHERE_API_KEY="your_api_key_here"
```

**Linux / macOS:**

```bash
export COHERE_API_KEY="your_api_key_here"
```

---

### Persistent (Recommended)

**Windows:**

```powershell
setx COHERE_API_KEY "your_api_key_here"
```

Restart your terminal afterward.

**Linux / macOS:**
Add to `~/.bashrc`, `~/.bash_profile`, or `~/.zshrc`:

```bash
export COHERE_API_KEY="your_api_key_here"
```

Reload:

```bash
source ~/.bashrc
```

---

### Using a `.env` File (Local Development)

Create `.env` in the project root:

```env
COHERE_API_KEY=your_api_key_here
```

Ensure `.env` is in `.gitignore`.

Install helper:

```bash
pip install python-dotenv
```

Load in Python:

```python
from dotenv import load_dotenv
load_dotenv()
```

Access key via:

```python
os.environ["COHERE_API_KEY"]
```

---

## Getting an API Key

1. Visit: [https://dashboard.cohere.com/api-keys](https://dashboard.cohere.com/api-keys)
2. Create a free trial key
3. Store it securely using one of the methods above

---

## Quick Start

```bash
python list_models.py
python command_eval.py
python embed_eval.py
python rerank_eval.py
python classify_eval.py
python rag_eval.py
```

Observe:

* latency variability
* p95 vs average
* effects of caching
* grounded vs ungrounded answers

---

## Final Takeaway

This project demonstrates **practical, measurable use of Cohere APIs**:

* correct API usage
* performance evaluation
* distribution-based thinking
* realistic RAG construction

These are the same concerns that appear in **production AI systems**, explored here in a controlled, transparent way.

