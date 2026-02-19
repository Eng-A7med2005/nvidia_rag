# Smart Contract Assistant v2

A powerful AI-driven tool for analyzing and querying smart contracts and legal documents. This project leverages Retrieval-Augmented Generation (RAG) to provide accurate answers with citations from your documents.

## 🚀 Key Features

*   **Document Ingestion**: Supports PDF, TXT, and other formats using robust loaders.
*   **RAG with Citations**: Answers questions based on document content, citing the specific source file and page number.
*   **Interactive UI**: User-friendly interface built with Gradio for easy document uploading and chatting.
*   **Microservice API**: Automatically generates a FastAPI server (`server.py`) to expose the RAG functionality as a REST API.
*   **Evaluation**: Built-in basic evaluation to check answer quality against keywords.

## 🛠️ Prerequisites

*   Python 3.10+
*   OpenAI API Key (Set as `OPENAI_API_KEY` environment variable or in `.env`)

## 📦 Installation

1.  **Clone the repository** (if applicable) or download the project files.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You might need to install `poppler-utils` or other system dependencies for `unstructured` if processing complex PDFs.*

## ⚙️ Configuration

Set your OpenAI API key in a `.env` file or export it in your terminal:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 📖 Usage

### Running the Notebook
The core logic resides in `smart_contract_assistant_v2.ipynb`. Open it in Jupyter Notebook or JupyterLab to execute the cells step-by-step.

### Using the Gradio UI
Run the notebook cells to launch the Gradio interface. It provides three tabs:
1.  **Ingestion**: Upload your contract files (PDF, TXT, etc.) and click "Ingest & Save Index".
2.  **Chat**: Ask questions about the uploaded contracts.
3.  **Local API**: Instructions for running the backend server.

### Running the API Server
The notebook generates a `server.py` file. To run the standalone API server:

1.  Open a terminal in the project directory.
2.  Run the server:
    ```bash
    python server.py
    ```
3.  Access the API documentation at `http://localhost:8000/docs`.
4.  Access the playground at `http://localhost:8000/contract-assistant/playground`.

## 📁 Project Structure

*   `smart_contract_assistant_v2.ipynb`: Main project notebook containing all logic.
*   `server.py`: Auto-generated FastAPI server script.
*   `requirements.txt`: List of Python dependencies.
*   `faiss_index/`: Directory where the vector store is saved (created after ingestion).

## 🧩 Architecture

The system uses **LangChain** for orchestration, **FAISS** for vector storage, **OpenAI** for embeddings and LLM, and **FastAPI/LangServe** for the API layer.

1.  **Ingestion**: Documents -> Chunking -> Embeddings -> Vector Store.
2.  **Retrieval**: Query -> Embeddings -> Vector Search -> Top-k Context.
3.  **Generation**: Context + Query -> LLM -> Answer with Sources.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📄 License

[MIT License](LICENSE)
