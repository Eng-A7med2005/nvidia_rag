# 📜 Smart Contract Assistant v2

RAG-based Smart Contract Analysis System powered by **LangChain**, **OpenAI**, **FAISS**, and **Gradio**.

## Features

- **📥 Ingestion Pipeline** — Load PDF/TXT/DOCX files, chunk, embed, and store in FAISS
- **🔍 RAG with Citations** — Answer questions citing specific source documents and pages
- **🖥️ LangServe API** — REST API microservice via FastAPI + LangServe
- **🎨 Gradio UI** — Web interface for uploading files and chatting
- **📊 Evaluation** — Basic keyword-based answer quality testing

## Project Structure

```
smart_contract_assistant/
├── main.py              # 🚀 CLI entry point
├── config.py            # ⚙️ Configuration (.env, constants, logging)
├── ingestion.py         # 📥 Document loading, chunking, FAISS indexing
├── rag_chain.py         # 🔍 RAG pipeline with citations
├── evaluation.py        # 📊 Evaluation pipeline with test cases
├── server.py            # 🖥️ FastAPI + LangServe API server
├── app.py               # 🎨 Gradio UI frontend
├── requirements.txt     # 📋 Python dependencies
├── .env.example         # 🔑 Environment variable template
└── .gitignore           # Git ignore rules
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Ingest documents

```bash
python main.py ingest --files path/to/contract.pdf path/to/terms.txt
```

### 4. Launch the UI

```bash
python main.py ui
```

### 5. Or start the API server

```bash
python main.py serve
# API docs at:   http://localhost:8000/docs
# Playground at: http://localhost:8000/contract-assistant/playground
```

### 6. Run evaluation

```bash
python main.py evaluate
```

## Tech Stack

| Component | Technology |
|---|---|
| LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector Store | FAISS (CPU) |
| Framework | LangChain + LangChain Core |
| API Server | FastAPI + LangServe + Uvicorn |
| Frontend | Gradio |
| Config | python-dotenv |
