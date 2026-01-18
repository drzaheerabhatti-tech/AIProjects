# rag_eval.py
import os
import time
import json
import numpy as np
import cohere
from common import timed, summarize_bucket
from data_ai import AI_DOCS, QUERY

# Models (based on what your key supports)
MODEL_EMBED = "embed-english-v3.0"
MODEL_RERANK = "rerank-v4.0-fast"
MODEL_CHAT = "command-r-08-2024"

# RAG knobs
TOP_K_RETRIEVE = 5     # how many docs to take from embedding similarity
TOP_N_RERANK = 3       # how many docs to keep after rerank
N_RUNS = 5             # keep small to avoid trial limits
SLEEP_SEC = 1.6        # trial-safe pacing

# Latency buckets
lat_embed_docs_ms = []
lat_embed_query_ms = []
lat_rerank_ms = []
lat_chat_ms = []

# Question

OOS_QUERY = "Who invented the transformer architecture?"


# Cohere client
co = cohere.ClientV2(os.environ["COHERE_API_KEY"])

if "COHERE_API_KEY" not in os.environ:
    raise RuntimeError("COHERE_API_KEY not set")


# Cache doc embeddings (embed docs once)
doc_embs_cache = None

def cosine(a, b):
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def build_doc_cache():
    global doc_embs_cache
    if doc_embs_cache is not None:
        return

    resp = timed(
        "Embed docs (cache build)",
        lambda: co.embed(
            model=MODEL_EMBED,
            input_type="search_document",
            texts=AI_DOCS
        ),
        bucket=lat_embed_docs_ms
    )
    doc_embs_cache = resp.embeddings.float

def retrieve_by_embedding(query: str, top_k: int):
    """Return top_k candidate docs using embedding similarity (local retrieval)."""
    build_doc_cache()

    q_resp = timed(
        "Embed query",
        lambda: co.embed(
            model=MODEL_EMBED,
            input_type="search_query",
            texts=[query]
        ),
        bucket=lat_embed_query_ms
    )
    q_emb = q_resp.embeddings.float[0]

    scored = []
    for i, d_emb in enumerate(doc_embs_cache):
        scored.append((cosine(q_emb, d_emb), i, AI_DOCS[i]))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [t for _, _, t in scored[:top_k]]

def rerank(query: str, candidates, top_n: int):
    """Reorder candidates by relevance using Cohere rerank."""
    rr = timed(
        "Rerank",
        lambda: co.rerank(
            model=MODEL_RERANK,
            query=query,
            documents=candidates,
            top_n=min(top_n, len(candidates))
        ),
        bucket=lat_rerank_ms
    )
    ranked = [candidates[r.index] for r in rr.results]
    return ranked

def generate_answer(query: str, context_docs):
    """Generate answer using Command, constrained to provided context."""
    context = "\n".join([f"- {d}" for d in context_docs])

    resp = timed(
        "Command chat (grounded)",
        lambda: co.chat(
            model=MODEL_CHAT,
            messages=[
                {"role": "system", "content": (
                    "You are a helpful assistant.\n"
                    "You MUST follow these rules:\n"
                    "1) Answer ONLY using the provided context.\n"
                    "2) If the answer is not explicitly supported by the context, reply EXACTLY with:\n"
                    "I don't know based on the provided context.\n"
                    "3) Do not add any extra words."
                )},

                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
            ],
        ),
        bucket=lat_chat_ms
    )
    return resp.message.content[0].text

def rag_once(query: str, show_debug: bool = False):
    # 1) retrieve (via embedding similarity)
    candidates = retrieve_by_embedding(query, TOP_K_RETRIEVE)

    # 2) rerank candidates
    top_docs = rerank(query, candidates, TOP_N_RERANK)

    # 3) generate grounded answer
    answer = generate_answer(query, top_docs)

    if show_debug:
        print("\n--- RAG Debug ---")
        print("Query:", query)
        print("\nCandidates (post-embed retrieval):")
        for c in candidates:
            print("-", c)
        print("\nTop docs (post-rerank):")
        for d in top_docs:
            print("-", d)
        print("\nAnswer:")
        print(answer)

    return answer

def grounding_test():
    print("\n========================")
    print("Grounding Test (Out-of-scope)")
    print("========================")

    answer = rag_once(OOS_QUERY, show_debug=True).strip()

    expected = "I don't know based on the provided context."
    if answer == expected:
        print("\n✅ PASS: Model refused correctly.")
    else:
        print("\n❌ FAIL: Model did not refuse correctly.")
        print("Expected exactly:")
        print(expected)
        print("\nGot:")
        print(answer)

def print_summary():
    print("\n--- Latency Summary (RAG stages) ---")
    summarize_bucket("Embed docs (cache build)", lat_embed_docs_ms)
    summarize_bucket("Embed query", lat_embed_query_ms)
    summarize_bucket("Rerank", lat_rerank_ms)
    summarize_bucket("Command chat (grounded)", lat_chat_ms)

def main():
    # First run: show debug so you can see the pipeline
    rag_once(QUERY, show_debug=True)

    # Out-of-scope grounding check
    grounding_test()

    # Remaining runs: just gather latency samples
    for _ in range(N_RUNS - 1):
        if SLEEP_SEC > 0:
            time.sleep(SLEEP_SEC)
        rag_once(QUERY, show_debug=False)

    print_summary()

if __name__ == "__main__":
    main()
