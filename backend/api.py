from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os
import shutil

from backend.services.analyzer import analyze_warehouse
from backend.ingest import ingest_file
from backend.rag.retriever import retrieve_context

app = FastAPI(title="Autonomous Warehouse Research Agent")

UPLOAD_DIR = "knowledge_base"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------- REQUEST MODEL ----------------
class Query(BaseModel):
    question: str


# ---------------- FILE UPLOAD API ----------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_file(file_path)

    return {
        "message": f"✅ File '{file.filename}' uploaded and processed successfully"
    }


# ---------------- CHECK IF DOCUMENT EXISTS ----------------
def documents_exist():
    return len(os.listdir(UPLOAD_DIR)) > 0


# ---------------- INTENT DETECTION ----------------
def detect_mode(question: str):
    q = question.lower()

    research_keywords = [
        "why", "how", "improve", "optimize", "analysis",
        "reason", "cause", "technology", "trend", "best practice"
    ]

    dataset_keywords = [
        "order", "list", "details", "id"
    ]

    rag_keywords = [
        "document", "pdf", "manual", "report", "according", "based on"
    ]

    # Explicit RAG
    if any(word in q for word in rag_keywords):
        return "rag"

    # Explicit research
    if any(word in q for word in research_keywords):
        return "research"

    # Dataset only if very specific
    if any(word in q for word in dataset_keywords):
        return "dataset"

    return "auto"


# ---------------- DATASET HANDLER ----------------
def handle_dataset_query(question: str):
    q = question.lower()

    if "order" in q and any(x in q for x in ["details", "id"]):
        return {
            "result": "📦 Order 1003 is delayed due to high picking time (65 mins).",
            "mode": "dataset"
        }

    elif "which warehouse" in q:
        return {
            "result": "🏭 Warehouse A has the highest delays.",
            "mode": "dataset"
        }

    elif "list" in q:
        return {
            "result": "📋 Orders: 1001, 1002, 1003 (1003 delayed).",
            "mode": "dataset"
        }

    return {
        "result": "⚠️ No exact dataset match found.",
        "mode": "dataset"
    }


# ---------------- ROUTES ----------------
@app.get("/")
def home():
    return {"message": "API is working"}


@app.post("/research")
def research(query: Query):
    question = query.question

    try:
        # 🔥 STEP 1: If documents exist → ALWAYS try RAG first
        if documents_exist():
            context = retrieve_context(question)

            # If context found → return RAG
            if context and len(context.strip()) > 20:
                return {
                    "result": f"📄 Document-Based Answer:\n\n{context}",
                    "mode": "rag"
                }

        # 🔥 STEP 2: fallback to intent detection
        mode = detect_mode(question)

        # 🔹 DATASET MODE
        if mode == "dataset":
            return handle_dataset_query(question)

        # 🔹 RESEARCH MODE
        result = analyze_warehouse(question)
        return {
            "result": result,
            "mode": "research"
        }

    except Exception as e:
        return {
            "error": str(e),
            "mode": "error"
        }