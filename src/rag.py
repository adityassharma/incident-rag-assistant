import anthropic
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def build_context(results: List[Dict[str, Any]]) -> str:
    blocks = []
    for r in results:
        m = r["metadata"]
        blocks.append(f"""
Title: {m.get('title')}
Service: {m.get('service')}
Severity: {m.get('severity')}

Symptoms:
{m.get('symptoms')}

Root Cause:
{m.get('root_cause')}

Resolution:
{m.get('resolution')}
""".strip())

    return "\n\n---\n\n".join(blocks)

def generate_answer(query: str, retrieved_results: List[Dict[str, Any]]) -> str:
    context = build_context(retrieved_results)
    messages = [
        anthropic.types.MessageParam(
            role="user",
            content=f"""
You are a senior Site Reliability Engineer (SRE).

Use ONLY the incident context below.

Context:
{context}

---

User Question:
{query}

---

Provide:
1. Root cause
2. Fix recommendation
3. Similar incident reference
"""
        )
    ]

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        temperature=0.2,
        messages=messages
    )
    text_output = []
    for block in response.content:
        if hasattr(block, "text"):
            text_output.append(block.text)

    return "\n".join(text_output)