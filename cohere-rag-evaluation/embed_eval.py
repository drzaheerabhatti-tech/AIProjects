# embed_eval.py
import os
import numpy as np
import cohere
from common import timed, summarize_bucket
from data_ai import AI_DOCS, QUERY

MODEL_EMBED = "embed-english-v3.0"
N_QUERY_RUNS = 10
SLEEP_SEC = 1.6  # trial-safe pacing (optional)

lat_docs_ms = []
lat_query_ms = []
doc_embs_cache = None

co = cohere.ClientV2(os.environ["COHERE_API_KEY"])

if "COHERE_API_KEY" not in os.environ:
    raise RuntimeError("COHERE_API_KEY not set")


def cosine(a, b):
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def build_doc_cache():
    global doc_embs_cache
    if doc_embs_cache is not None:
        return
    resp = timed("Embed docs (cache build)", lambda: co.embed(
        model=MODEL_EMBED,
        input_type="search_document",
        texts=AI_DOCS
    ), bucket=lat_docs_ms)
    doc_embs_cache = resp.embeddings.float

def embed_query(q: str):
    return timed("Embed query", lambda: co.embed(
        model=MODEL_EMBED,
        input_type="search_query",
        texts=[q]
    ), bucket=lat_query_ms).embeddings.float[0]

def rank_docs(q: str, show_top=False):
    build_doc_cache()
    qv = embed_query(q)

    scored = []
    for i, dv in enumerate(doc_embs_cache):
        scored.append((cosine(qv, dv), i, AI_DOCS[i]))
    scored.sort(reverse=True, key=lambda x: x[0])

    if show_top:
        print("\nTop 3 by embedding similarity:")
        for s, i, t in scored[:3]:
            print(f"{s:.3f}  (doc {i})  {t}")

def main():
    import time
    rank_docs(QUERY, show_top=True)
    for _ in range(N_QUERY_RUNS - 1):
        if SLEEP_SEC > 0:
            time.sleep(SLEEP_SEC)
        rank_docs(QUERY, show_top=False)

    print("\n--- Latency Summary ---")
    summarize_bucket("Embed docs (cache build)", lat_docs_ms)
    summarize_bucket("Embed query (steady state)", lat_query_ms)

if __name__ == "__main__":
    main()
