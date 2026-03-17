from backend.rag.db import client  # reuse existing Chroma client
from crewai import LLM
import uuid

MEMORY_COLLECTION = "warehouse_memory"


# ----------------------------------
# Small LLM for Compression (Low TPM)
# ----------------------------------
memory_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    temperature=0.1,
    max_tokens=180  # small limit
)


# ----------------------------------
# Get Collection
# ----------------------------------
def get_memory_collection():
    return client.get_or_create_collection(name=MEMORY_COLLECTION)


# ----------------------------------
# Structured Memory Compression
# ----------------------------------
def compress_memory(answer: str) -> str:
    prompt = f"""
Compress the following warehouse report.

Keep EXACT headings:
Root Cause:
Insights:
Industry Best Practices:
Recommendations:

Rules:
- Maximum 2 short bullet points per section
- No explanations
- Keep total under 150 words
- Maintain clean bullet format

Report:
{answer}
"""

    summary = memory_llm.call(prompt)
    return summary.strip()


# ----------------------------------
# Save Memory (Compressed)
# ----------------------------------
def save_memory(question: str, answer: str):
    collection = get_memory_collection()

    compressed_answer = compress_memory(answer)

    memory_text = f"""
Question:
{question}

{compressed_answer}
"""

    collection.add(
        documents=[memory_text],
        ids=[str(uuid.uuid4())]
    )


# ----------------------------------
# Retrieve Memory
# ----------------------------------
def get_memory(query: str = "", limit: int = 3):
    collection = get_memory_collection()

    if not query.strip():
        results = collection.get(limit=limit)
        return "\n\n".join(results["documents"]) if results["documents"] else ""

    results = collection.query(
        query_texts=[query],
        n_results=limit
    )

    if not results["documents"]:
        return ""

    return "\n\n".join(results["documents"][0])