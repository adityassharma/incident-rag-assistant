# 🛠️ Smart Incident Knowledge Assistant (RAG)

A lightweight AI-powered troubleshooting assistant that uses **Retrieval-Augmented Generation (RAG)** to help engineers quickly diagnose and resolve incidents using historical alert data.

Built using:
- Semantic search (embeddings)
- Vector database retrieval
- LLM reasoning (Claude)
- Streamlit chat interface

---

## 🚀 Overview

Modern observability platforms like Netcool and BigPanda generate thousands of alerts. Engineers often need to answer:

- Have we seen this issue before?
- What was the root cause?
- How was it resolved?

This project simulates that workflow using a full RAG pipeline.

---

## 🧠 Architecture

```mermaid
flowchart TD
    A[User Query (Streamlit UI)] --> B[Embedding Model]
    B --> C[ChromaDB Vector Store]
    C --> D[Top-K Similar Incidents]
    D --> E[Context Builder]
    E --> F[Claude LLM]
    F --> G[Final Answer]
    D --> H[Similar Incidents Display]

📂 Project Structure
incident-rag-assistant/
│
├── data/
│   └── incidents.json
│
├── src/
│   ├── ingest.py
│   ├── retrieve.py
│   ├── rag.py
│   └── app.py
│
├── chroma_db/              # persisted vector store
├── requirements.txt
├── .env
└── README.md

▶️ How to Run the Project

1. Clone repository
git clone https://github.com/yourusername/incident-rag-assistant.git
cd incident-rag-assistant

2. Create virtual environment
python -m venv .venv

Activate:

Windows
.venv\Scripts\activate

Mac/Linux
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Add API key

Create .env file:
ANTHROPIC_API_KEY=your_api_key_here

5. Ingest incident data
python src/ingest.py

This:
Generates embeddings
Stores them in ChromaDB
Persists vector database locally

6. Run Streamlit app
streamlit run src/app.py

💡 Example Queries
"High CPU and latency on API service"
"Database connection timeouts"
"Kubernetes pod crash looping"
"Redis cache miss spike"

✨ Features
Semantic incident search
RAG-based reasoning
Chat-style UI
Incident similarity scoring
Persistent vector database

🧾 Quick Command Summary
# Setup environment
python -m venv .venv
.venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Load data into vector DB
python src/ingest.py

# Run app
streamlit run src/app.py

📌 Notes on Persistence
ChromaDB stores embeddings locally in ./chroma_db
No need to re-run ingestion unless:
dataset changes
embedding logic changes
database is deleted