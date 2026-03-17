import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORT_DIR = os.path.join(BASE_DIR, "knowledge_base")

os.makedirs(REPORT_DIR, exist_ok=True)

def save_report(question: str, answer: str):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"report_{timestamp}.txt"

    filepath = os.path.join(REPORT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("AUTONOMOUS LOGISTICS RESEARCH REPORT\n")
        f.write("="*50 + "\n\n")
        f.write(f"Query:\n{question}\n\n")
        f.write("Analysis:\n")
        f.write(answer)

    return filepath
