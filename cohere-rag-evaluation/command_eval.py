# command_eval.py
import os
import time
import cohere
from common import timed, summarize_bucket

MODEL_CHAT = "command-r-08-2024"
N_RUNS = 5
SLEEP_SEC = 1.6  # trial-safe pacing (optional)

lat_chat_ms = []
co = cohere.ClientV2(os.environ["COHERE_API_KEY"])

if "COHERE_API_KEY" not in os.environ:
    raise RuntimeError("COHERE_API_KEY not set")


def chat_once():
    resp = timed("Command chat", lambda: co.chat(
        model=MODEL_CHAT,
        messages=[
            {"role":"system","content":"You are an AI tutor. Be concise, accurate, and avoid hype."},
            {"role":"user","content":"Explain transformers in exactly 5 bullet points."}
        ],
    ), bucket=lat_chat_ms)
    print(resp.message.content[0].text)

def main():
    chat_once()
    for _ in range(N_RUNS - 1):
        if SLEEP_SEC > 0:
            time.sleep(SLEEP_SEC)
        timed("Command chat", lambda: co.chat(
            model=MODEL_CHAT,
            messages=[
                {"role":"system","content":"You are an AI tutor. Be concise, accurate, and avoid hype."},
                {"role":"user","content":"Explain transformers in exactly 5 bullet points."}
            ],
        ), bucket=lat_chat_ms)

    print("\n--- Latency Summary ---")
    summarize_bucket("Command chat", lat_chat_ms)

if __name__ == "__main__":
    main()
