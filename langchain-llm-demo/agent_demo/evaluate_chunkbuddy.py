"""
evaluate_chunkbuddy.py

Run LangSmith evaluations for the ChunkBuddy LangGraph app.

Prereqs:
- LANGCHAIN_TRACING_V2=true
- LANGCHAIN_API_KEY=<your-langsmith-api-key>
- LANGCHAIN_PROJECT=chunkbuddy   (or any project name you like)
- OPENAI_API_KEY=<your-openai-api-key>

- A LangSmith dataset named "chunkbuddy-topics" with at least:
    - topic (string)
    - level (string: beginner / intermediate / advanced)
"""

# --- Imports & environment bootstrap ----------------------------------------
# We load environment variables first so API keys and project settings
# are available to LangGraph and LangSmith.
from typing import Dict, Any, List
import json
from langsmith import Client
from langsmith.evaluation import evaluate
from langchain_openai import ChatOpenAI

from chunkbuddy_standalone_graph import build_app
from load_env import load_env
load_env()

# --- Build the LangGraph app ------------------------------------------------
# We compile the ChunkBuddy graph once and reuse it for all dataset rows.
app = build_app()

# LangSmith client (optional: useful if you want to inspect datasets,
# experiments, or metadata directly).
client = Client()

# ---------------------------------------------------------------------------
# Target function: how LangSmith calls your app
# ---------------------------------------------------------------------------

def chunkbuddy_target(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Target function for LangSmith evaluation.

    `inputs` will be one row from your dataset, e.g.:
        {"topic": "Kafka partitions", "level": "beginner"}

    We invoke the LangGraph app with this state and return a flat dict
    of outputs that evaluators can inspect.
    """
    topic = inputs["topic"]
    level = inputs.get("level", "beginner")

    # Run the graph on this dataset row
    state = app.invoke({"topic": topic, "level": level})

    # Return only the fields we want evaluators to check
    return {
        "raw_explanation": state.get("raw_explanation", ""),
        "chunks": state.get("chunks", []),
        "check_questions": state.get("check_questions", []),
        "summary": state.get("summary", ""),
    }

# ---------------------------------------------------------------------------
# Simple rule-based evaluators
# ---------------------------------------------------------------------------

def chunk_count_ok(inputs: dict, outputs: dict) -> dict:
    """
    Evaluator: check that the number of chunks is in a reasonable range (3–7).

    Returns a dict with:
      - score: 1.0 if ok, 0.0 otherwise
      - value: the actual chunk count
      - name: the name of this evaluator
    """
    chunks: List[str] = outputs.get("chunks", [])
    n = len(chunks)
    score = 1.0 if 3 <= n <= 7 else 0.0
    return {"score": score, "value": n, "name": "chunk_count_ok"}

def question_count_ok(inputs: dict, outputs: dict) -> dict:
    """
    Evaluator: check that the number of questions is in a reasonable range (3–7).
    """
    questions: List[str] = outputs.get("check_questions", [])
    n = len(questions)
    score = 1.0 if 3 <= n <= 7 else 0.0
    return {"score": score, "value": n, "name": "question_count_ok"}

# ---------------------------------------------------------------------------
# LLM-as-judge evaluator for clarity vs learner level
# ---------------------------------------------------------------------------
# Instead of a fixed rule, we ask a model to rate clarity on a 1–5 scale.
eval_llm = ChatOpenAI(model="gpt-4o-mini")

def clarity_for_level(inputs: dict, outputs: dict) -> dict:
    """
    Evaluator: use an LLM-as-judge to rate how clear the explanation is
    for the given learner level.

    We ask the model to return JSON like:
      {"score": 4, "reason": "..."}
    and parse it.
    """
    explanation = outputs.get("raw_explanation", "")
    topic = inputs.get("topic", "")
    level = inputs.get("level", "beginner")

    prompt = f"""
You are evaluating the clarity of an explanation for a learner.

Topic: {topic}
Level: {level}

Explanation:
\"\"\"{explanation}\"\"\"

Please rate how clear, accurate, and appropriate this explanation is for the given learner level.

Respond ONLY as a JSON object with the following structure:
{{
  "score": <number from 1 to 5>,
  "reason": "<short explanation of your rating>"
}}
"""
    response = eval_llm.invoke(prompt)
    text = response.content

    try:
        data = json.loads(text)
        score = float(data.get("score", 0.0))
        reason = data.get("reason", "")
    except Exception:
        # Fallback if the model doesn't follow JSON perfectly
        score = 0.0
        reason = f"Could not parse JSON from response: {text}"

    return {"score": score, "reason": reason, "name": "clarity_for_level"}

# ---------------------------------------------------------------------------
# Run the evaluation
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Name of the dataset you created in LangSmith UI
    DATASET_NAME = "chunkbuddy-topics"

    # Run evaluation: apply target function to dataset rows,
    # then score outputs with evaluators.
    experiment_results = evaluate(
        chunkbuddy_target,
        data=DATASET_NAME,
        evaluators=[
            chunk_count_ok,
            question_count_ok,
            clarity_for_level,  # LLM-as-judge evaluator
        ],
        experiment_prefix="chunkbuddy-eval",
        metadata={"app": "chunkbuddy", "version": "v1"},
    )

    print("✅ LangSmith experiment created:")
    print("  Name:", experiment_results.experiment_name)
