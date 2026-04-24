import chromadb
import json
from sentence_transformers import SentenceTransformer

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(name="incidents")

def embed(text):
    return model.encode(text).tolist()

def ingest():
    with open("data/incidents.json") as f:
        data = json.load(f)

    for i, incident in enumerate(data):
        text = f"{incident['title']} {incident['symptoms']} {incident['root_cause']}"
        collection.add(
            documents=[text],
            embeddings=[embed(text)],
            metadatas=[incident],
            ids=[str(i)]
        )

    print(f"Ingested {len(data)} incidents successfully!")

if __name__ == "__main__":
    ingest()