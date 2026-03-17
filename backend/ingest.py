import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from sentence_transformers import SentenceTransformer
from rag.db import reset_collection

collection = reset_collection()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "warehouse.csv.csv")

df = pd.read_csv(DATA_PATH)

model = SentenceTransformer("all-MiniLM-L6-v2")

for i, row in df.iterrows():
    text = ", ".join([f"{col}:{row[col]}" for col in df.columns])
    embedding = model.encode(text).tolist()

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(i)]
    )

print("✅ Data stored in vector DB")