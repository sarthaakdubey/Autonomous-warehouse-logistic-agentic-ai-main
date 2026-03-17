import os
from chromadb import PersistentClient
from chromadb.config import Settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "vector_db")

client = PersistentClient(
    path=DB_PATH,
    settings=Settings(anonymized_telemetry=False, allow_reset=True)
)

COLLECTION_NAME = "warehouse"

def get_collection():
    return client.get_or_create_collection(name=COLLECTION_NAME)

def reset_collection():
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except:
        pass
    return client.get_or_create_collection(name=COLLECTION_NAME)