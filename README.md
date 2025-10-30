🏛️ US Legislative Policy RAG System

A Retrieval-Augmented Generation (RAG) system designed to search, filter, and summarize US legislative policies using vector similarity search, BM25 keyword filtering, and JinaAI reranking.
The project combines semantic retrieval, lexical filtering, and LLM-based reranking to deliver high-quality, context-aware answers for complex legal queries.


📘 Table of Contents

-   Overview
-   System Architecture
-   Tech Stack
-   Project Structure
-   Setup & Installation
-   Running the App
-   API Endpoints
-   Future Enhancements



🧠 Overview

This project implements a RAG pipeline tailored for searching and summarizing US legislative bills.
It retrieves the most relevant policy documents by combining vector embeddings, BM25 scoring, and reranking via JinaAI, before generating a structured and factual answer using an LLM.




⚙️ System Architecture

                ┌────────────────────┐
                │      User Query     │
                └─────────┬───────────┘
                          │
                          ▼
           ┌──────────────────────────────┐
           │  BM25 Filter (Lexical Search)│
           └─────────┬────────────────────┘
                     │ Filtered Docs
                     ▼
           ┌──────────────────────────────┐
           │ Vector Similarity Search (Qdrant)│
           └─────────┬────────────────────┘
                     │ Top-k Candidates
                     ▼
           ┌──────────────────────────────┐
           │   JinaAI Reranker (Semantic) │
           └─────────┬────────────────────┘
                     │ Best Ranked Docs
                     ▼
           ┌──────────────────────────────┐
           │    LLM (Answer Generation)   │
           └──────────────────────────────┘



🚀 Features

✅ Hybrid Retrieval: Combines BM25 (keyword-based) and vector similarity search (semantic-based).
✅ Reranking: Uses JinaAI API for relevance reranking.
✅ Fast Search: Powered by Qdrant Vector DB for efficient similarity lookups.
✅ LLM Integration: Uses OpenAI or Groq models for contextual answer generation.
✅ Logging & Monitoring: Integrated logging (app.log, /logs) for debugging and insights.
✅ Extensible Design: Modular service-based architecture for easy extension or model swap.




🧩 Tech Stack
| Component        | Technology                   |
| ---------------- | ---------------------------- |
| Language         | Python 3.12+                 |
| Framework        | FastAPI                      |
| Vector Database  | Qdrant                       |
| Reranking API    | JinaAI                       |
| Embedding Models | OpenAI / Groq                |
| Retrieval        | BM25 + Vector Search         |
| Logging          | Python `logging`, `colorlog` |
| Configuration    | YAML & TOML                  |





📂 Project Structure

```
.
├── main.py                 # FastAPI app entry point
├── data/                   # Raw JSON legislative data
│   └── AL_2026rs_bills.json
├── src/
│   ├── router/             # API routing and data models
│   ├── services/           # Core business logic
│   │   ├── retrievers.py   # BM25 + Vector search logic
│   │   ├── reranker.py     # JinaAI reranking integration
│   │   ├── documents_handler.py
│   │   └── llms/           # LLM factory, embeddings, and tools
│   ├── utilities/          # Helper utilities and configs
│   │   ├── qdrant_vectordb.py
│   │   ├── logger.py
│   │   └── helper.py
│   └── resources/          # Configs and constants
│       └── constants.yaml
├── test.ipynb              # Interactive notebook for testing
├── pyproject.toml          # Dependencies and build configuration
├── uv.lock                 # Version-locked dependencies
├── logs/                   # Runtime logs
└── README.md
```



⚙️ Setup & Installation
1. Clone the repository

```
git clone https://github.com/yourusername/us-legislative-rag.git
cd us-legislative-rag
```


2. Create a virtual environment

```
uv venv
source .venv/bin/activate   # (Linux/macOS)
.venv\Scripts\activate      # (Windows)
```


3. Install dependencies
```
uv pip install -r pyproject.toml
```


4. Configure API Keys

Set your credentials in .env or export them:
```
export OPENAI_API_KEY="your_openai_key"
export JINA_API_KEY="your_jina_key"
```

▶️ Running the App

```
python main.py
```


The FastAPI app will start on:

```
http://127.0.0.1:8000/docs
```

You can test API endpoints directly in the Swagger UI.



🧮 **How It Works**

**User Query Input**

-   A text query is received via FastAPI.

**Document Filtering (BM25)**

-   Filters legislative bills based on lexical relevance.

**Vector Retrieval**

-   Fetches semantically similar documents using Qdrant vector search.

**Reranking**

-   Top candidates are reranked using JinaAI Reranker API.

**Answer Generation**

-   The best context is passed to an LLM (e.g., OpenAI GPT or Groq) to generate the final answer.



🔮 Future Enhancements

- Add support for multi-state bill datasets
- Implement streaming LLM responses
- Improve chunking and retrieval precision
- Add caching for frequent queries
- Integrate LangChain or LlamaIndex pipelines