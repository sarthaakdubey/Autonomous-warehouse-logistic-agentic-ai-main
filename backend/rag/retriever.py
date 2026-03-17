import sys
import os

# allow imports when FastAPI runs from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.db import get_collection

collection = get_collection()


def retrieve_context(question: str):
    """
    Retrieves relevant warehouse data from vector DB
    """
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    documents = results["documents"][0]
    return "\n".join(documents)


# direct testing
if __name__ == "__main__":
    print("\n🔎 Searching warehouse memory...\n")
    print(retrieve_context("Which warehouse has delays?"))