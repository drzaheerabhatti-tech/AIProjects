# chunkbuddy_graph.py
# ---------------------------------------------------------------------------
# Core LangGraph workflow for ChunkBuddy.
# ---------------------------------------------------------------------------

from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
import re

from agent_demo.load_env import load_env
load_env()  # Load environment variables once


# ---------------------------------------------------------------------------
# Shared State Definition
# ---------------------------------------------------------------------------
class LearningState(TypedDict, total=False):
    topic: str
    level: str
    raw_explanation: str
    chunks: List[str]
    check_questions: List[str]
    summary: str
    meta: dict


# ---------------------------------------------------------------------------
# Node 1: draft_explanation
# ---------------------------------------------------------------------------
def draft_explanation(state: LearningState, llm):
    topic = state.get("topic", "a technical topic")
    level = state.get("level", "beginner")

    prompt = f"""
You are a friendly technical learning assistant.

Explain the topic below to a {level} learner.

Topic: {topic}

Requirements:
- Use simple, clear language.
- Ensure that the total number of words in the explanation does not exceed 30 words.
- Avoid unnecessary jargon, or explain it when you must use it.
- Define technical terms the first time you use them.
- Use a real-world metaphor.
- Focus on core ideas first.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"raw_explanation": response.content}


# ---------------------------------------------------------------------------
# Node 2: chunk_explanation
# ---------------------------------------------------------------------------
def chunk_explanation(state: LearningState, llm):
    raw = state.get("raw_explanation", "")
    if not raw:
        return {"chunks": []}

    prompt = f"""
Break the explanation into 4 short learning chunks.

Rules:
- One idea per chunk.
- 2–4 sentences each.
- Start each chunk with a title like: "Chunk 1: What a partition is"

Explanation:
{raw}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    chunks = [c.strip() for c in response.content.split("\n\n") if c.strip()]
    return {"chunks": chunks}


# ---------------------------------------------------------------------------
# Node 3: generate_check_questions
# ---------------------------------------------------------------------------
def generate_check_questions(state: LearningState, llm):
    chunks = state.get("chunks", [])
    if not chunks:
        return {"check_questions": []}

    chunks_text = "\n\n".join(chunks)
    prompt = f"""
Create 5 short retrieval-practice questions based on these learning chunks:

{chunks_text}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    text = response.content

    questions = []
    num_pat = re.compile(r'^\s*\d+[\.\)\-]\s*(.+)$')
    bullet_pat = re.compile(r'^\s*[\-\*]\s+(.+)$')

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = num_pat.match(line)
        if m:
            questions.append(m.group(1).strip())
            continue
        m = bullet_pat.match(line)
        if m:
            questions.append(m.group(1).strip())
            continue
        if line.endswith("?"):
            questions.append(line)

    if not questions:
        for c in chunks[:5]:
            title = c.split("\n", 1)[0].strip()
            title = title.removeprefix("Chunk ").split(":", 1)[-1].strip()
            questions.append(f"What is {title.lower()}?")

    return {"check_questions": questions}


# ---------------------------------------------------------------------------
# Node 4: summarize_and_meta
# ---------------------------------------------------------------------------
def summarize_and_meta(state: LearningState, llm):
    topic = state.get("topic", "this topic")
    raw = state.get("raw_explanation", "")
    chunks = state.get("chunks", [])
    questions = state.get("check_questions", [])

    chunks_text = "\n".join(f"- {c.splitlines()[0]}" for c in chunks[:6])
    questions_text = "\n".join(f"- {q}" for q in questions[:5])

    prompt = f"""
You are a learning scientist.

Topic: {topic}

Raw explanation:
{raw}

Chunk titles:
{chunks_text or "- (none)"}

Check questions:
{questions_text or "- (none)"}

Tasks:
1) Write a ONE-SENTENCE TL;DR summary beginning with "Summary:".
2) Write 2–3 bullets explaining how the structure supports learning.
"""
    response = llm.invoke([HumanMessage(content=prompt)])

    summary_line = ""
    bullets = []

    for line in response.content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("Summary:") and not summary_line:
            summary_line = line[len("Summary:"):].strip()
        elif line.startswith("- "):
            bullets.append(line[2:].strip())

    return {
        "summary": summary_line or f"A short overview of {topic}.",
        "meta": {
            "learning_design_notes": bullets,
            "num_chunks": len(chunks),
            "num_questions": len(questions),
        },
    }


# ---------------------------------------------------------------------------
# Graph Construction
# ---------------------------------------------------------------------------
def build_app():
    from langchain_openai import ChatOpenAI
    from agent_demo.state import ChunkBuddyState

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    # Wrap nodes so they capture llm via closure
    def draft_node(state):
        return draft_explanation(state, llm)

    def chunk_node(state):
        return chunk_explanation(state, llm)

    def questions_node(state):
        return generate_check_questions(state, llm)

    def summary_node(state):
        return summarize_and_meta(state, llm)

    graph = StateGraph(ChunkBuddyState)

    graph.add_node("draft_explanation", draft_node)
    graph.add_node("chunk_explanation", chunk_node)
    graph.add_node("generate_check_questions", questions_node)
    graph.add_node("summarize_and_meta", summary_node)

    graph.add_edge(START, "draft_explanation")
    graph.add_edge("draft_explanation", "chunk_explanation")
    graph.add_edge("chunk_explanation", "generate_check_questions")
    graph.add_edge("generate_check_questions", "summarize_and_meta")
    graph.add_edge("summarize_and_meta", END)

    return graph.compile()