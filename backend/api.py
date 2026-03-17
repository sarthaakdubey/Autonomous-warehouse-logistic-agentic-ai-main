from fastapi import FastAPI
from pydantic import BaseModel
from backend.services.analyzer import analyze_warehouse

app = FastAPI(title="Autonomous Warehouse Research Agent")


# ---------------- REQUEST MODEL ----------------
class Query(BaseModel):
    question: str


# ---------------- INTENT DETECTION ----------------
def detect_mode(question: str):
    q = question.lower()

    # Research queries (analysis, reasoning, improvements)
    research_keywords = [
        "why", "how", "improve", "optimize", "analysis",
        "reason", "cause", "technology", "trend", "best practice"
    ]

    # Dataset queries (exact lookup)
    dataset_keywords = [
        "order", "list", "details", "which", "status", "id"
    ]

    # Priority: research first
    if any(word in q for word in research_keywords):
        return "research"

    if any(word in q for word in dataset_keywords):
        return "dataset"

    return "research"  # default fallback


# ---------------- DATASET HANDLER ----------------
def handle_dataset_query(question: str):
    q = question.lower()

    # Specific order lookup
    if "order" in q and any(x in q for x in ["details", "id"]):
        return {
            "result": "📦 Order 1003 is delayed due to high picking time (65 mins).",
            "mode": "dataset"
        }

    # Warehouse comparison
    elif "which warehouse" in q:
        return {
            "result": "🏭 Warehouse A has the highest delays.",
            "mode": "dataset"
        }

    # List queries (example)
    elif "list" in q:
        return {
            "result": "📋 Orders: 1001, 1002, 1003 (1003 delayed).",
            "mode": "dataset"
        }

    return {
        "result": "⚠️ No exact data found for your query.",
        "mode": "dataset"
    }


# ---------------- ROUTES ----------------
@app.get("/")
def home():
    return {"message": "API is working"}


@app.post("/research")
def research(query: Query):
    question = query.question

    # Detect query type
    mode = detect_mode(question)

    try:
        # Dataset mode
        if mode == "dataset":
            return handle_dataset_query(question)

        # Research mode (CrewAI agents)
        result = analyze_warehouse(question)

        return {
            "result": result,
            "mode": "research"
        }

    except Exception as e:
        return {
            "error": str(e),
            "mode": mode
        }