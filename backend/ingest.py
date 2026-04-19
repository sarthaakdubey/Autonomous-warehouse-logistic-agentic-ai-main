import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from sentence_transformers import SentenceTransformer
from rag.db import reset_collection
import fitz  # PyMuPDF

# Initialize DB
collection = reset_collection()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# 🔹 TEXT CHUNKING FUNCTION
# -----------------------------
def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


# -----------------------------
# 🔹 PDF PROCESSING
# -----------------------------
def process_pdf(file_path):
    doc = fitz.open(file_path)
    full_text = ""

    for page_num, page in enumerate(doc):
        full_text += page.get_text()

    chunks = chunk_text(full_text)

    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"{file_path}_chunk_{i}"],
            metadatas=[{
                "source": file_path,
                "type": "pdf"
            }]
        )

    print(f"✅ Processed PDF: {file_path}")


# -----------------------------
# 🔹 CSV PROCESSING (EXISTING)
# -----------------------------
def process_csv(file_path):
    df = pd.read_csv(file_path)

    for i, row in df.iterrows():
        text = ", ".join([f"{col}:{row[col]}" for col in df.columns])
        embedding = model.encode(text).tolist()

        collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[f"{file_path}_{i}"],
            metadatas=[{
                "source": file_path,
                "type": "csv"
            }]
        )

    print(f"✅ Processed CSV: {file_path}")


# -----------------------------
# 🔹 MAIN INGEST FUNCTION
# -----------------------------
def ingest_file(file_path):
    if file_path.endswith(".pdf"):
        process_pdf(file_path)

    elif file_path.endswith(".csv"):
        process_csv(file_path)

    else:
        print("❌ Unsupported file type")


# -----------------------------
# 🔹 RUN (for testing)
# -----------------------------
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Example files
    pdf_path = os.path.join(BASE_DIR, "data", "sample.pdf")
    csv_path = os.path.join(BASE_DIR, "data", "warehouse.csv.csv")

    if os.path.exists(pdf_path):
        ingest_file(pdf_path)

    if os.path.exists(csv_path):
        ingest_file(csv_path)

    print("🚀 Ingestion complete")