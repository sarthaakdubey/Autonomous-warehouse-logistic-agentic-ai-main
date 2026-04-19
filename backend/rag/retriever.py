import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.db import get_collection
from sentence_transformers import SentenceTransformer

collection = get_collection()

# Load SAME embedding model (VERY IMPORTANT)
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_context(question: str, top_k=5):
    """
    Retrieves relevant context using semantic search
    """

    # 🔹 Convert query → embedding
    query_embedding = model.encode(question).tolist()

    # 🔹 Query vector DB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]
    metadatas = results.get("metadatas", [[]])[0]

    # 🔹 Combine context + metadata
    context = []
    for doc, meta in zip(documents, metadatas):
        source = meta.get("source", "unknown")
        context.append(f"[Source: {source}]\n{doc}")

    return "\n\n".join(context)


# test
if __name__ == "__main__":
    print("\n🔎 Searching warehouse memory...\n")
    print(retrieve_context("Which warehouse has delays?"))