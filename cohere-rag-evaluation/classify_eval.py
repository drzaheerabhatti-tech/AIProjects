# classify_eval.py
import os
import time
import json
import cohere
from common import timed, summarize_bucket

MODEL_CLASSIFY = "command-r-08-2024"
N_RUNS = 10
SLEEP_SEC = 1.6  # trial-safe pacing

lat_classify_ms = []

co = cohere.ClientV2(os.environ["COHERE_API_KEY"])
if "COHERE_API_KEY" not in os.environ:
    raise RuntimeError("COHERE_API_KEY not set")

LABELS = [
    "AI Concepts",
    "Business",
    "Entertainment"
]

TEXTS = [
    "Transformers use self-attention to model relationships between words.",
    "This quarter we should focus on reducing operational costs.",
    "Batman is a superhero who protects Gotham City."
]

def classify_once():
    prompt = f"""
You are a text classification system.

Valid labels:
{json.dumps(LABELS)}

Classify each input text into exactly ONE label.
Return the result as JSON in the form:
[
  {{ "text": "...", "label": "...", "confidence": 0.0 }}
]

Texts:
{json.dumps(TEXTS)}
"""

    resp = timed(
        "Classify",
        lambda: co.chat(
            model=MODEL_CLASSIFY,
            messages=[
                {"role": "system", "content": "You are a precise classifier. Do not explain."},
                {"role": "user", "content": prompt}
            ],
        ),
        bucket=lat_classify_ms
    )

    output = resp.message.content[0].text
    print("\nRaw model output:")
    print(output)

def main():
    # First run: show classification output
    classify_once()

    # Remaining runs: latency only
    for _ in range(N_RUNS - 1):
        if SLEEP_SEC > 0:
            time.sleep(SLEEP_SEC)
        timed(
            "Classify",
            lambda: co.chat(
                model=MODEL_CLASSIFY,
                messages=[
                    {"role": "system", "content": "You are a precise classifier. Do not explain."},
                    {"role": "user", "content": f"Classify the following texts into {LABELS}: {TEXTS}"}
                ],
            ),
            bucket=lat_classify_ms
        )

    print("\n--- Latency Summary ---")
    summarize_bucket("Classify (Command-based)", lat_classify_ms)

if __name__ == "__main__":
    main()
