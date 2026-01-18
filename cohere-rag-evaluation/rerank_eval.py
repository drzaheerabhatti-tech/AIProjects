# rerank_eval.py
import os
import time
import cohere
from common import timed, summarize_bucket
from data_ai import AI_DOCS, QUERY

MODEL_RERANK = "rerank-v4.0-fast"
N_RUNS = 10
SLEEP_SEC = 1.6  # trial-safe pacing (optional)

lat_rerank_ms = []

co = cohere.ClientV2(os.environ["COHERE_API_KEY"])
if "COHERE_API_KEY" not in os.environ:
    raise RuntimeError("COHERE_API_KEY not set")


def rerank_once(q: str, candidates):
    rr = timed("Rerank", lambda: co.rerank(
        model=MODEL_RERANK,
        query=q,
        documents=candidates,
        top_n=3
    ), bucket=lat_rerank_ms)

    ranked = [(r.relevance_score, candidates[r.index]) for r in rr.results]
    print("\nTop 3 after rerank:")
    for score, text in ranked:
        print(f"{score:.3f}  {text}")

def main():
    rerank_once(QUERY, AI_DOCS)
    for _ in range(N_RUNS - 1):
        if SLEEP_SEC > 0:
            time.sleep(SLEEP_SEC)
        # run silently after the first print
        timed("Rerank", lambda: co.rerank(
            model=MODEL_RERANK,
            query=QUERY,
            documents=AI_DOCS,
            top_n=3
        ), bucket=lat_rerank_ms)

    print("\n--- Latency Summary ---")
    summarize_bucket("Rerank", lat_rerank_ms)

if __name__ == "__main__":
    main()
