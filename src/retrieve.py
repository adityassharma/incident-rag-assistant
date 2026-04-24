import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

# Same embedding model as ingest.py
model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(name="incidents")

def embed(text: str) -> List[float]:
    embedding = model.encode(text)
    try:
        return embedding.tolist()
    except AttributeError:
        return list(embedding)


def retrieve(query: str, k: int = 3) -> List[Dict[str, Any]]:
    query_embedding = embed(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    # Handle None values
    metadatas = results.get("metadatas") or [[]]
    documents = results.get("documents") or [[]]
    distances = results.get("distances") or [[]]

    metadatas = metadatas[0] if metadatas else []
    documents = documents[0] if documents else []
    distances = distances[0] if distances else []

    combined_results = []

    for i in range(min(len(metadatas), len(documents), len(distances))):
        combined_results.append({
            "metadata": metadatas[i],
            "document": documents[i],
            "distance": distances[i],
            "confidence": round(max(0, (1 - distances[i]) * 100), 1)
        })

    return combined_results